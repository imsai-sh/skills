---
name: ios-icp-filing
description: |
  从已签名的 iOS IPA 反查 Bundle ID、Distribution 证书 SHA-1 / MD5 指纹、RSA 公钥 modulus，
  按腾讯云 / 阿里云 / 华为云 ICP/APP 备案表单要求的格式（空格分隔 hex / 连续 hex / PEM）输出。
  触发场景：用户提到"ICP 备案"、"APP 备案"、"腾讯云备案"、"阿里云备案"、"华为云备案"、
  "苹果平台 App 包信息"、"包名签名"、"公共密钥"、"应用签名 MD5"、"应用签名 SHA-1"，或问
  "iOS app 用的是哪个证书"、"如何获取 iOS app 的公钥 / SHA1"、"备案表里的公钥怎么填"。
  即使用户只模糊提"准备 iOS 上架中国大陆"或"备案需要的信息"，也应使用此 skill。
tools: Bash, Read, Write
---

# iOS App ICP/APP 备案信息提取

中国大陆 App Store 上架前要做 ICP/APP 备案。腾讯云 / 阿里云 / 华为云的"新增苹果平台 App 包信息"
表单都要三样东西：**Bundle ID + 证书 SHA-1 + RSA 公钥 modulus**。

## 核心原则

**永远从实际 IPA 反查证书，不要从 developer.apple.com 证书页用肉眼挑。**

Xcode Cloud / fastlane 等会自动 rotate distribution 证书，团队可能同时有 2-3 张未过期的
"Apple Distribution" cert。**只有 IPA 里 `embedded.mobileprovision` 引用的那张才是当前
App Store 实际签名用的**——其余都是历史轮换残留，备案信息填错会被拒。

## 流程

### Step 1: 拿到当前上架版本的 IPA

按可获得性排序：

| 来源 | 取法 |
|---|---|
| Xcode Cloud archive 的 `app-store.zip` artifact | `asc xcode-cloud artifacts list --run-id <id>` 找 fileName 含 `app-store` 的，`asc xcode-cloud artifacts download --id <id> --path /tmp/x.zip` |
| 本地 `xcodebuild -exportArchive` 输出（method=app-store-connect） | export 目录下的 `*.ipa` |
| TestFlight build | App Store Connect Web 下载（流程繁琐，最后选项） |

> **重要**：选 `app-store` 签名的 IPA，**不要用 `ad-hoc` 或 `development`** — 后两者用的不是
> Apple Distribution 证书，备案信息会与上架版本不匹配。

### Step 2: 跑提取脚本

```bash
#!/bin/bash
set -e
IPA="/path/to/YourApp.ipa"   # ← 改这里
OUT=/tmp/icp-extract
rm -rf "$OUT" && mkdir -p "$OUT"

# 解 IPA → mobileprovision → DER 证书
unzip -q "$IPA" -d "$OUT"
APP=$(echo "$OUT"/Payload/*.app)
security cms -D -i "$APP/embedded.mobileprovision" > "$OUT/profile.plist"
plutil -extract DeveloperCertificates.0 raw -o - "$OUT/profile.plist" \
  | base64 -D > "$OUT/cert.cer"

# Bundle ID（profile entitlement 带 team prefix，去掉前面的 TeamID.）
BUNDLE_ID=$(plutil -extract Entitlements.application-identifier raw -o - "$OUT/profile.plist" \
  | sed 's/^[A-Z0-9]*\.//')

echo "Bundle ID:  $BUNDLE_ID"
openssl x509 -inform DER -in "$OUT/cert.cer" -subject -dates -noout

echo ""
echo "=== SHA-1 (3 种格式)==="
SHA1=$(openssl x509 -inform DER -in "$OUT/cert.cer" -fingerprint -sha1 -noout | sed 's/sha1 Fingerprint=//')
echo "冒号分隔: $SHA1"
echo "连续 hex: $(echo "$SHA1" | tr -d ':')"
echo "空格分隔: $(echo "$SHA1" | tr ':' ' ')"

echo ""
echo "=== 公钥 modulus（RSA-2048 = 256 字节 = 512 hex chars）==="
MOD=$(openssl x509 -inform DER -in "$OUT/cert.cer" -modulus -noout | sed 's/Modulus=//')
echo "连续 hex:"
echo "$MOD"
echo ""
echo "空格分隔（macOS Keychain Access 风格，腾讯云 / 阿里云常用）:"
echo "$MOD" | fold -w 2 | paste -sd ' ' -

echo ""
echo "=== 公钥 PEM（少数平台要）==="
openssl x509 -inform DER -in "$OUT/cert.cer" -pubkey -noout

echo ""
echo "=== MD5 fingerprint（极少要）==="
openssl x509 -inform DER -in "$OUT/cert.cer" -fingerprint -md5 -noout
```

### Step 3: 按平台格式填表

国内主流云厂商的"苹果平台 App 包信息"表单格式：

| 字段 | 腾讯云 | 阿里云 | 华为云 |
|---|---|---|---|
| Bundle ID | 直接填 | 同 | 同 |
| 公钥 / 公共密钥 | **空格分隔 hex modulus**（512 hex chars + 空格）| 同 | 同 |
| 签名 SHA-1 | **空格分隔 hex**（40 hex chars + 空格）| 同 | 同 |

**常见字段名陷阱**：腾讯云字段标"**签名 MD5 值**"，但红字 placeholder 写"请输入 40 位长度的 SHA-1
值（以 16 进制形式填写）"——**实际填 SHA-1，不是 MD5**。这是腾讯云历史命名 bug，按红字填。

## Common Mistakes

| 坑 | 修法 |
|---|---|
| 从 Apple Developer 网站凭"过期日期最晚"挑 cert | 必从 IPA 反查；过期最晚不一定就是当前在用的 |
| 公钥填 PEM 整段（带 `-----BEGIN/END-----`）| 填 hex modulus，不要 PEM |
| 公钥填整个 SubjectPublicKeyInfo DER（588 hex chars）| 填 modulus（512 chars），表单标"256 字节"暗示是 modulus |
| 字段名"签名 MD5 值" → 真填 MD5 fingerprint | 填 SHA-1，看红字 placeholder |
| `ad-hoc` 或 `development` 签名的 IPA 反查 | 必须用 `app-store` 签名的 IPA |
| 备案后 1 年证书过期没更新 | Apple Distribution cert 1 年期，自动 rotate；日历提前 30 天提醒重备 |

## 选哪份"公钥格式"？

| 表单提示 | 应填 |
|---|---|
| "256 字节" / "公共密钥" 标签 | **空格分隔 modulus hex**（最常见，照搬 macOS Keychain Access 显示）|
| "一串数字或十六进制字符串" | 优先空格分隔 modulus hex；不接受换连续 hex |
| 明确说"PEM 格式" | PEM（带 `-----BEGIN PUBLIC KEY-----`）|
| 明确说"DER base64" | PEM 去头尾的单行 base64 |

## Bundle ID 兜底

如果从 entitlements 取 Bundle ID 失败（profile 字段不一致），从 .app 的 Info.plist 取：

```bash
plutil -extract CFBundleIdentifier raw -o - "$APP/Info.plist"
```

## 验证

填表前 sanity check：

- SHA-1 应是 40 hex chars（去空格后）
- modulus 对 RSA-2048 应是 512 hex chars（去空格后），256 字节
- 证书 subject 应含 `Apple Distribution: <Team Name> (<TeamID>)`，**不应**是
  `Apple Development:` 或 `Apple Distribution: ... (Developer ID)`
- 证书有效期：`notAfter` 在 1 年内合理（Apple 标准期限）
