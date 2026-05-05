---
name: ios-icp-filing
description: |
  Extract Bundle ID, distribution-cert SHA-1 / MD5 fingerprints, and RSA public-key modulus
  from a signed iOS IPA, formatted for Chinese cloud ICP/APP filing forms (Tencent Cloud /
  Aliyun / Huawei Cloud — space-separated hex / continuous hex / PEM).
  Triggers in Chinese: "ICP 备案", "APP 备案", "腾讯云备案", "阿里云备案", "华为云备案",
  "苹果平台 App 包信息", "包名签名", "公共密钥", "应用签名 MD5", "应用签名 SHA-1",
  "iOS app 用的是哪个证书", "如何获取 iOS app 的公钥 / SHA1", "备案表里的公钥怎么填".
  In English: "iOS ICP filing", "ICP record submission", "China App Store filing",
  "Bundle ID + signing cert + public key for ICP filing".
  Even on vague mentions like "preparing iOS for China App Store" or "info needed for filing",
  invoke this skill.
tools: Bash, Read, Write
---

# iOS App ICP/APP Filing Info Extraction

China-mainland App Store distribution requires ICP/APP filing. The "Add Apple-platform App Bundle Info" form on Tencent Cloud / Aliyun / Huawei Cloud all want the same three things: **Bundle ID + cert SHA-1 + RSA public-key modulus**.

## Core principle

**Always reverse-look up the cert from the actual IPA. Never eyeball-pick from the developer.apple.com cert page.**

Xcode Cloud / fastlane and friends auto-rotate distribution certs. A team often holds 2–3 unexpired "Apple Distribution" certs at the same time. **Only the cert referenced by the IPA's `embedded.mobileprovision` is the one currently signing the App Store build** — the others are rotation residue. Mis-fill the form and the filing gets rejected.

## Workflow

### Step 1: Get the IPA of the currently-shipping version

By availability:

| Source | How |
|---|---|
| Xcode Cloud archive's `app-store.zip` artifact | `asc xcode-cloud artifacts list --run-id <id>`, find the entry whose fileName contains `app-store`, then `asc xcode-cloud artifacts download --id <id> --path /tmp/x.zip` |
| Local `xcodebuild -exportArchive` output (method=app-store-connect) | the `*.ipa` in the export dir |
| TestFlight build | Download via App Store Connect Web (annoying — last resort) |

> **Important**: use the `app-store`-signed IPA. **Don't use `ad-hoc` or `development`** — those use a different cert from Apple Distribution, and the filing info won't match the shipping build.

### Step 2: Run the extraction script

```bash
#!/bin/bash
set -e
IPA="/path/to/YourApp.ipa"   # ← edit this
OUT=/tmp/icp-extract
rm -rf "$OUT" && mkdir -p "$OUT"

# Unpack IPA → mobileprovision → DER cert
unzip -q "$IPA" -d "$OUT"
APP=$(echo "$OUT"/Payload/*.app)
security cms -D -i "$APP/embedded.mobileprovision" > "$OUT/profile.plist"
plutil -extract DeveloperCertificates.0 raw -o - "$OUT/profile.plist" \
  | base64 -D > "$OUT/cert.cer"

# Bundle ID (the entitlement value carries a team prefix; strip the leading TeamID.)
BUNDLE_ID=$(plutil -extract Entitlements.application-identifier raw -o - "$OUT/profile.plist" \
  | sed 's/^[A-Z0-9]*\.//')

echo "Bundle ID:  $BUNDLE_ID"
openssl x509 -inform DER -in "$OUT/cert.cer" -subject -dates -noout

echo ""
echo "=== SHA-1 (3 formats) ==="
SHA1=$(openssl x509 -inform DER -in "$OUT/cert.cer" -fingerprint -sha1 -noout | sed 's/sha1 Fingerprint=//')
echo "colon-separated:  $SHA1"
echo "continuous hex:   $(echo "$SHA1" | tr -d ':')"
echo "space-separated:  $(echo "$SHA1" | tr ':' ' ')"

echo ""
echo "=== Public-key modulus (RSA-2048 = 256 bytes = 512 hex chars) ==="
MOD=$(openssl x509 -inform DER -in "$OUT/cert.cer" -modulus -noout | sed 's/Modulus=//')
echo "continuous hex:"
echo "$MOD"
echo ""
echo "space-separated (macOS Keychain Access style — Tencent Cloud / Aliyun expect this):"
echo "$MOD" | fold -w 2 | paste -sd ' ' -

echo ""
echo "=== Public-key PEM (a few platforms ask for this) ==="
openssl x509 -inform DER -in "$OUT/cert.cer" -pubkey -noout

echo ""
echo "=== MD5 fingerprint (rarely asked) ==="
openssl x509 -inform DER -in "$OUT/cert.cer" -fingerprint -md5 -noout
```

### Step 3: Fill the form per platform

The "Apple-platform App Bundle Info" form across the three big Chinese cloud vendors:

| Field | Tencent Cloud | Aliyun | Huawei Cloud |
|---|---|---|---|
| Bundle ID | as-is | same | same |
| Public key / "公共密钥" | **space-separated hex modulus** (512 hex chars + spaces) | same | same |
| Signing SHA-1 | **space-separated hex** (40 hex chars + spaces) | same | same |

**Common label trap**: Tencent Cloud's field is labeled "**签名 MD5 值**" (signing MD5 value), but the red placeholder says "请输入 40 位长度的 SHA-1 值（以 16 进制形式填写）" (enter a 40-char SHA-1 value in hex). **Fill SHA-1, not MD5.** This is a Tencent Cloud legacy-naming bug — go by the red placeholder, not the label.

## Common mistakes

| Pitfall | Fix |
|---|---|
| Picking the cert with the latest expiry from the Apple Developer site | Always reverse-look up from the IPA — latest-expiry isn't necessarily the one in use |
| Pasting the full PEM (with `-----BEGIN/END-----`) into the public-key field | Fill hex modulus, not PEM |
| Pasting the full SubjectPublicKeyInfo DER (588 hex chars) | Fill the modulus (512 chars) — the form's "256 bytes" hint means modulus |
| Field labeled "签名 MD5 值" → filling actual MD5 fingerprint | Fill SHA-1 — read the red placeholder |
| Using an `ad-hoc` or `development`-signed IPA for reverse lookup | Must be `app-store`-signed |
| Cert expires 1 year after filing and isn't refreshed | Apple Distribution certs are 1-year and auto-rotate; calendar a re-filing reminder 30 days ahead |

## Which "public-key format" to pick?

| Form hint | What to fill |
|---|---|
| "256 bytes" / "公共密钥" label | **space-separated modulus hex** (most common — copy what macOS Keychain Access shows) |
| "string of digits or hex" | prefer space-separated modulus hex; fall back to continuous hex if not accepted |
| Explicit "PEM format" | PEM (with `-----BEGIN PUBLIC KEY-----`) |
| Explicit "DER base64" | PEM stripped of headers, single-line base64 |

## Bundle ID fallback

If extracting Bundle ID from entitlements fails (profile field mismatch), grab it from the .app's Info.plist:

```bash
plutil -extract CFBundleIdentifier raw -o - "$APP/Info.plist"
```

## Verification

Sanity-check before filling:

- SHA-1 should be 40 hex chars (after stripping spaces)
- modulus for RSA-2048 should be 512 hex chars (after stripping spaces) = 256 bytes
- cert subject should contain `Apple Distribution: <Team Name> (<TeamID>)`, **not** `Apple Development:` or `Apple Distribution: ... (Developer ID)`
- cert validity: `notAfter` within 1 year is reasonable (Apple's standard window)
