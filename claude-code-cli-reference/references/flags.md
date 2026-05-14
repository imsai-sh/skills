# Claude Code CLI — Flags

Full flag list, mirrored from <https://code.claude.com/docs/en/cli-reference.md>.

> ⚠️ `claude --help` **does not list every flag** — a flag's absence from `--help` does not mean it is unavailable.

## Session / context

| Flag | Description | Example |
| :-- | :-- | :-- |
| `--continue`, `-c` | Continue the most recent conversation in the current directory. Includes sessions that added this directory via `/add-dir` | `claude --continue` |
| `--resume`, `-r` | Resume a session by ID or name; no argument opens an interactive picker. Includes sessions that added this directory via `/add-dir` | `claude --resume auth-refactor` |
| `--fork-session` | When resuming, create a new session ID instead of reusing the original (use with `--resume` / `--continue`) | `claude --resume abc123 --fork-session` |
| `--from-pr` | Resume sessions linked to a specific pull request. Accepts a PR number, a GitHub or GitHub Enterprise PR URL, a GitLab merge request URL, or a Bitbucket pull request URL. Sessions are linked automatically when Claude creates the PR | `claude --from-pr 123` |
| `--session-id` | Use a specific session ID for the conversation (must be a valid UUID) | `claude --session-id "550e8400-e29b-41d4-a716-446655440000"` |
| `--name`, `-n` | Set a display name shown in `/resume` and the terminal title. Resume with `claude --resume <name>`. `/rename` changes it mid-session and shows it on the prompt bar | `claude -n "my-feature-work"` |
| `--add-dir` | Add extra working directories. Grants file access; most `.claude/` configuration is NOT auto-discovered from these. For persistence use `permissions.additionalDirectories` in settings | `claude --add-dir ../apps ../lib` |
| `--worktree`, `-w` | Start in an isolated [git worktree](https://code.claude.com/docs/en/worktrees) at `<repo>/.claude/worktrees/<name>`. No name → auto-generated. `#<number>` or a GitHub PR URL fetches that PR from `origin` and branches from it | `claude -w feature-auth` |
| `--tmux` | Create a tmux session for the worktree. Requires `--worktree`. Uses iTerm2 native panes when available; `--tmux=classic` for traditional tmux | `claude -w feature-auth --tmux` |

## Mode control

| Flag | Description | Example |
| :-- | :-- | :-- |
| `--print`, `-p` | Print response without interactive mode. See the [Agent SDK docs](https://code.claude.com/docs/en/agent-sdk/overview) for programmatic usage | `claude -p "query"` |
| `--bare` | Minimal mode: skip auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and CLAUDE.md so scripted calls start faster. Bash, file read, and file edit tools remain. Sets `CLAUDE_CODE_SIMPLE`. See [bare mode](https://code.claude.com/docs/en/headless#start-faster-with-bare-mode) | `claude --bare -p "query"` |
| `--bg` | Start the session as a [background agent](https://code.claude.com/docs/en/agent-view) and return immediately. Prints the session ID and management commands. Combine with `--agent` to run a specific subagent | `claude --bg "investigate the flaky test"` |
| `--remote` | Create a new [web session](https://code.claude.com/docs/en/claude-code-on-the-web) on claude.ai with the provided task description | `claude --remote "Fix the login bug"` |
| `--remote-control`, `--rc` | Start an interactive session with [Remote Control](https://code.claude.com/docs/en/remote-control#start-a-remote-control-session) enabled so you can also control it from claude.ai or the Claude app. Optionally pass a session name | `claude --remote-control "My Project"` |
| `--remote-control-session-name-prefix <prefix>` | Prefix for auto-generated Remote Control session names (default: hostname → names like `myhost-graceful-unicorn`). Env equivalent: `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX` | `claude remote-control --remote-control-session-name-prefix dev-box` |
| `--teleport` | Resume a [web session](https://code.claude.com/docs/en/claude-code-on-the-web) in your local terminal | `claude --teleport` |

## Model / budget / effort

| Flag | Description | Example |
| :-- | :-- | :-- |
| `--model` | Pick a model by alias (`sonnet` / `opus`) or full name. Overrides the `model` setting and the `ANTHROPIC_MODEL` env var | `claude --model claude-sonnet-4-6` |
| `--fallback-model` | Automatic fallback model when the default is overloaded (print mode only) | `claude -p --fallback-model sonnet "query"` |
| `--effort` | Set the [effort level](https://code.claude.com/docs/en/model-config#adjust-effort-level): `low` / `medium` / `high` / `xhigh` / `max`. Available levels depend on the model. Overrides the `effortLevel` setting for this session and does not persist | `claude --effort high` |
| `--max-budget-usd` | Maximum dollar amount to spend on API calls before stopping (print mode only) | `claude -p --max-budget-usd 5.00 "query"` |
| `--max-turns` | Limit the number of agentic turns (print mode only). Exits with an error when the limit is reached. No limit by default | `claude -p --max-turns 3 "query"` |
| `--betas` | Beta headers to include in API requests (API key users only) | `claude --betas interleaved-thinking` |

## Permissions and tools

| Flag | Description | Example |
| :-- | :-- | :-- |
| `--permission-mode` | Start mode: `default` / `acceptEdits` / `plan` / `auto` / `dontAsk` / `bypassPermissions`. Overrides `defaultMode` in settings | `claude --permission-mode plan` |
| `--dangerously-skip-permissions` | Equivalent to `--permission-mode bypassPermissions`. See [permission modes](https://code.claude.com/docs/en/permission-modes#skip-all-checks-with-bypasspermissions-mode) | `claude --dangerously-skip-permissions` |
| `--allow-dangerously-skip-permissions` | Add `bypassPermissions` to the `Shift+Tab` cycle without starting in it. Lets you start in e.g. `plan` and switch later | `claude --permission-mode plan --allow-dangerously-skip-permissions` |
| `--permission-prompt-tool` | Use an MCP tool to handle permission prompts in non-interactive mode | `claude -p --permission-prompt-tool mcp_auth_tool "query"` |
| `--allowedTools` | Tools that execute without a permission prompt. Pattern syntax: see [permission rule syntax](https://code.claude.com/docs/en/settings#permission-rule-syntax). To **restrict** which tools are available use `--tools` | `"Bash(git log *)" "Bash(git diff *)" "Read"` |
| `--disallowedTools` | Tools removed from the model's context, cannot be used | `"Bash(git log *)" "Bash(git diff *)" "Edit"` |
| `--tools` | Restrict the built-in tool set. `""` disables all, `"default"` enables all, or list names like `"Bash,Edit,Read"` | `claude --tools "Bash,Edit,Read"` |
| `--disable-slash-commands` | Disable all skills and slash commands for this session | `claude --disable-slash-commands` |

## System prompt flags

All four work in both interactive and non-interactive modes.

| Flag | Behavior | Example |
| :-- | :-- | :-- |
| `--system-prompt` | Replaces the entire default prompt | `claude --system-prompt "You are a Python expert"` |
| `--system-prompt-file` | Replaces with file contents | `claude --system-prompt-file ./prompts/review.txt` |
| `--append-system-prompt` | Appends to the default prompt | `claude --append-system-prompt "Always use TypeScript"` |
| `--append-system-prompt-file` | Appends file contents to the default prompt | `claude --append-system-prompt-file ./style-rules.txt` |

**Rules:**
- `--system-prompt` and `--system-prompt-file` are **mutually exclusive**.
- Either append flag can combine with either replace flag.
- **When to append**: Claude should remain a coding assistant that also follows your extra rules — per-invocation instructions, output formatting, domain context for a `-p` script. Append preserves the default tool guidance, safety instructions, and coding conventions.
- **When to replace**: the surface, identity, or permission model differs from Claude Code's (e.g. a non-coding agent in a pipeline that no human watches). Replace drops the default prompt entirely (including tool guidance and safety instructions); you take responsibility for whatever the task still needs.
- These flags apply only to the current invocation. For persistent personas use [output styles](https://code.claude.com/docs/en/output-styles); for project conventions use [CLAUDE.md](https://code.claude.com/docs/en/memory).

## Agents / subagents

| Flag | Description | Example |
| :-- | :-- | :-- |
| `--agent` | Specify an agent for the current session (overrides the `agent` setting) | `claude --agent my-custom-agent` |
| `--agents` | Define custom subagents dynamically via JSON. Same field names as subagent [frontmatter](https://code.claude.com/docs/en/sub-agents#supported-frontmatter-fields), plus a `prompt` field | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--teammate-mode` | How [agent team](https://code.claude.com/docs/en/agent-teams) teammates display: `auto` (default) / `in-process` / `tmux`. Overrides `teammateMode` for this session | `claude --teammate-mode in-process` |

## MCP / plugins

| Flag | Description | Example |
| :-- | :-- | :-- |
| `--mcp-config` | Load MCP servers from JSON files or strings (space-separated for multiple) | `claude --mcp-config ./mcp.json` |
| `--strict-mcp-config` | Only use MCP servers from `--mcp-config`, **ignoring** all other MCP configurations | `claude --strict-mcp-config --mcp-config ./mcp.json` |
| `--plugin-dir` | Load a plugin from a directory or `.zip` for this session only. Repeat the flag for multiple plugins: `--plugin-dir A --plugin-dir B.zip` | `claude --plugin-dir ./my-plugin` |
| `--plugin-url` | Fetch a plugin `.zip` from a URL for this session only. Repeat the flag, or pass space-separated URLs in one quoted value | `claude --plugin-url https://example.com/plugin.zip` |
| `--channels` | (Research preview) MCP servers whose [channel](https://code.claude.com/docs/en/channels) notifications Claude should listen for. Space-separated `plugin:<name>@<marketplace>` entries. Requires Claude.ai authentication | `claude --channels plugin:my-notifier@my-marketplace` |
| `--dangerously-load-development-channels` | Enable [channels](https://code.claude.com/docs/en/channels-reference#test-during-the-research-preview) that are not on the approved allowlist, for local development. Accepts `plugin:<name>@<marketplace>` and `server:<name>`. Prompts for confirmation | `claude --dangerously-load-development-channels server:webhook` |

## Print-mode-only

| Flag | Description | Example |
| :-- | :-- | :-- |
| `--output-format` | Output format for print mode: `text` / `json` / `stream-json` | `claude -p "query" --output-format json` |
| `--input-format` | Input format for print mode: `text` / `stream-json` | `claude -p --output-format json --input-format stream-json` |
| `--include-partial-messages` | Include partial streaming events in output. Requires `--print` and `--output-format stream-json` | `claude -p --output-format stream-json --include-partial-messages "query"` |
| `--include-hook-events` | Include all hook lifecycle events in the output stream. Requires `--output-format stream-json` | `claude -p --output-format stream-json --include-hook-events "query"` |
| `--json-schema` | Validated JSON output matching a JSON Schema after the agent completes (print mode only — see [structured outputs](https://code.claude.com/docs/en/agent-sdk/structured-outputs)) | `claude -p --json-schema '{"type":"object","properties":{...}}' "query"` |
| `--replay-user-messages` | Re-emit user messages from stdin back on stdout for acknowledgment. Requires `--input-format stream-json` and `--output-format stream-json` | `claude -p --input-format stream-json --output-format stream-json --replay-user-messages` |
| `--exclude-dynamic-system-prompt-sections` | Move per-machine sections (working directory, environment info, memory paths, git-repo flag) from the system prompt into the first user message. Improves prompt-cache reuse across users/machines running the same task. Only applies with the default system prompt; ignored when `--system-prompt`/`--system-prompt-file` is set. Use with `-p` for scripted, multi-user workloads | `claude -p --exclude-dynamic-system-prompt-sections "query"` |
| `--no-session-persistence` | Don't save the session to disk; cannot be resumed. The `CLAUDE_CODE_SKIP_PROMPT_HISTORY` env var does the same in any mode | `claude -p --no-session-persistence "query"` |
| `--init` | Run [Setup hooks](https://code.claude.com/docs/en/hooks#setup) with the `init` matcher before the session | `claude -p --init "query"` |
| `--maintenance` | Run Setup hooks with the `maintenance` matcher before the session | `claude -p --maintenance "query"` |

## Startup / debugging / misc

| Flag | Description | Example |
| :-- | :-- | :-- |
| `--init-only` | Run Setup and `SessionStart` hooks, then exit without starting a conversation | `claude --init-only` |
| `--ide` | Automatically connect to an IDE on startup if exactly one valid IDE is available | `claude --ide` |
| `--chrome` | Enable [Chrome browser integration](https://code.claude.com/docs/en/chrome) | `claude --chrome` |
| `--no-chrome` | Disable Chrome integration for this session | `claude --no-chrome` |
| `--debug` | Enable debug mode with optional category filtering (e.g. `"api,hooks"` or `"!statsig,!file"`) | `claude --debug "api,mcp"` |
| `--debug-file <path>` | Write debug logs to a specific file. Implicitly enables debug mode. Takes precedence over `CLAUDE_CODE_DEBUG_LOGS_DIR` | `claude --debug-file /tmp/claude-debug.log` |
| `--verbose` | Verbose logging — shows full turn-by-turn output. Overrides `viewMode` for this session | `claude --verbose` |
| `--version`, `-v` | Output the version number | `claude -v` |
| `--settings` | Path to a settings JSON file or an inline JSON string. Values override the same keys in `settings.json` for this session; omitted keys keep their file-based values. See [settings precedence](https://code.claude.com/docs/en/settings#settings-precedence) | `claude --settings ./settings.json` |
| `--setting-sources` | Comma-separated list of setting sources to load (`user` / `project` / `local`) | `claude --setting-sources user,project` |
| `--enable-auto-mode` | Removed in v2.1.111. Auto mode is now in the `Shift+Tab` cycle by default; use `--permission-mode auto` to start in it | `claude --permission-mode auto` |
