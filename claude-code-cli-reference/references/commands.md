# Claude Code CLI — Commands

Full subcommand table, mirrored from <https://code.claude.com/docs/en/cli-reference.md>.

## Starting / resuming a session

| Command | Description | Example |
| :-- | :-- | :-- |
| `claude` | Start an interactive session | `claude` |
| `claude "query"` | Start an interactive session with an initial prompt | `claude "explain this project"` |
| `claude -p "query"` | Run via the SDK in print mode, then exit | `claude -p "explain this function"` |
| `cat file \| claude -p "query"` | Pipe content in | `cat logs.txt \| claude -p "explain"` |
| `claude -c` | Continue the most recent conversation in the current directory | `claude -c` |
| `claude -c -p "query"` | Continue in SDK / print mode | `claude -c -p "Check for type errors"` |
| `claude -r "<session>" "query"` | Resume a session by ID or name | `claude -r "auth-refactor" "Finish this PR"` |

## Install / update / authentication

| Command | Description | Example |
| :-- | :-- | :-- |
| `claude update` | Upgrade to the latest version | `claude update` |
| `claude install [version]` | Install or reinstall the native binary. Accepts `2.1.118` / `stable` / `latest` | `claude install stable` |
| `claude auth login` | Sign in to an Anthropic account. `--email` pre-fills email, `--sso` forces SSO, `--console` signs in with Console for API-key billing instead of a subscription | `claude auth login --console` |
| `claude auth logout` | Sign out | `claude auth logout` |
| `claude auth status` | Print authentication status as JSON. `--text` for human-readable. Exits with code 0 if logged in, 1 if not | `claude auth status` |
| `claude setup-token` | Generate a long-lived OAuth token for CI and scripts. Printed to the terminal only — not stored. Requires a Claude subscription | `claude setup-token` |

## Background agents / session management

| Command | Description | Example |
| :-- | :-- | :-- |
| `claude agents` | Open the [agent view](https://code.claude.com/docs/en/agent-view) to monitor and dispatch parallel background sessions. `--cwd <path>` filters to that directory | `claude agents` |
| `claude attach <id>` | Attach a background session to the current terminal | `claude attach 7c5dcf5d` |
| `claude logs <id>` | Print recent output from a background session | `claude logs 7c5dcf5d` |
| `claude respawn <id>` | Restart a stopped background session, conversation intact. `--all` restarts every stopped session | `claude respawn 7c5dcf5d` |
| `claude stop <id>` | Stop a background session. Also accepts `claude kill` | `claude stop 7c5dcf5d` |
| `claude rm <id>` | Remove a background session from the list | `claude rm 7c5dcf5d` |

## Configuration / meta commands

| Command | Description | Example |
| :-- | :-- | :-- |
| `claude mcp` | Configure Model Context Protocol servers. See the [MCP docs](https://code.claude.com/docs/en/mcp) | `claude mcp` |
| `claude plugin` | Manage plugins (alias `claude plugins`). Subcommands: see the [plugin reference](https://code.claude.com/docs/en/plugins-reference#cli-commands-reference) | `claude plugin install code-review@claude-plugins-official` |
| `claude project purge [path]` | Delete all local Claude Code state for one project: transcripts, task lists, debug logs, file-edit history, prompt history, and the project's entry in `~/.claude.json`. Flags: `--dry-run` to preview, `-y`/`--yes` to skip confirmation, `-i`/`--interactive` for per-item confirmation, `--all` for every project | `claude project purge ~/work/repo --dry-run` |
| `claude auto-mode defaults` | Print the built-in [auto mode](https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode) classifier rules as JSON. `claude auto-mode config` shows the effective config after settings are applied | `claude auto-mode defaults > rules.json` |
| `claude remote-control` | Start a [Remote Control](https://code.claude.com/docs/en/remote-control) server (no local interactive session) so Claude.ai or the Claude app can drive it | `claude remote-control --name "My Project"` |
| `claude ultrareview [target]` | Run [ultrareview](https://code.claude.com/docs/en/ultrareview#run-ultrareview-non-interactively) non-interactively. Exits 0 on success, 1 on failure. `--json` for raw payload, `--timeout <minutes>` to override the 30-minute default | `claude ultrareview 1234 --json` |

## Error handling

A mistyped subcommand triggers a "Did you mean ...?" hint and the CLI exits without starting a session. Example: `claude udpate` → `Did you mean claude update?`.
