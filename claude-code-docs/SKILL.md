---
name: claude-code-docs
description: Local mirror of the full Claude Code documentation set (code.claude.com/docs), one reference file per page. Use for any question about Claude Code CLI, IDE integrations, plugins, skills, hooks, MCP, the Agent SDK, deployment, configuration, or reference material. Load only the reference files relevant to the user question. Methodology and re-scrape scripts live in references/_meta/.
---

# Claude Code Documentation

> Official documentation for Claude Code, Anthropic's agentic coding tool available in the terminal, IDE, desktop app, and browser. Covers installation, configuration, skills, subagents, hooks, MCP, the Agent SDK, and reference material.

## Build provenance

This skill mirrors code.claude.com/docs as one reference file per page. Each `references/<slug>.md` is the verbatim markdown source returned by Mintlify's `.md` URL endpoint (e.g. `cli-reference.md` is `https://code.claude.com/docs/en/cli-reference.md`). No reformatting, summarization, or re-scraping — refresh by re-running `references/_meta/scripts/refetch-md.py`. Full methodology and gotchas in `references/_meta/scraping-method.md`.

## When to Use This Skill

Whenever the user asks about Claude Code features, configuration, plugins, skills, hooks, MCP, the Agent SDK, deployment options, or reference material. Each documentation page is preserved as its own file under `references/` — load only what you need rather than dumping the whole skill into context.

## References (140 files, one per documentation page)

### Core docs

- [Set up Claude Code for your organization](references/admin-setup.md): A decision map for administrators deploying Claude Code, covering API providers, managed settings, policy enforcement, usage monitoring, and data handling.
- [Orchestrate teams of Claude Code sessions](references/agent-teams.md): Coordinate multiple Claude Code instances working together as a team, with shared tasks, inter-agent messaging, and centralized management.
- [Manage multiple agents with agent view](references/agent-view.md): Dispatch and manage many Claude Code sessions from one screen. Agent view shows what every session is doing and which ones need your input.
- [Run agents in parallel](references/agents.md): Compare the ways Claude Code can take on multiple tasks at once: subagents, agent view, agent teams, and isolated worktree sessions.
- [Claude Code on Amazon Bedrock](references/amazon-bedrock.md): Learn about configuring Claude Code through Amazon Bedrock, including setup, IAM configuration, and troubleshooting.
- [Track team usage with analytics](references/analytics.md): View Claude Code usage metrics, track adoption, and measure engineering velocity in the analytics dashboard.
- [Authentication](references/authentication.md): Log in to Claude Code and configure authentication for individuals, teams, and organizations.
- [Configure auto mode](references/auto-mode-config.md): Tell the auto mode classifier which repos, buckets, and domains your organization trusts. Set environment context, override the default block and allow rules, and inspect your effective config with the auto-mode CLI subcommands.
- [Best practices for Claude Code](references/best-practices.md): Tips and patterns for getting the most out of Claude Code, from configuring your environment to scaling across parallel sessions.
- [Champion kit](references/champion-kit.md): A playbook for engineers advocating Claude Code internally: what to share, how to answer questions, and how to grow adoption on your team.
- [Changelog](references/changelog.md): Release notes for Claude Code, including new features, improvements, and bug fixes by version.
- [Push events into a running session with channels](references/channels.md): Use channels to push messages, alerts, and webhooks into your Claude Code session from an MCP server. Forward CI results, chat messages, and monitoring events so Claude can react while you're away.
- [Channels reference](references/channels-reference.md): Build an MCP server that pushes webhooks, alerts, and chat messages into a Claude Code session. Reference for the channel contract: capability declaration, notification events, reply tools, sender gating, and permission relay.
- [Checkpointing](references/checkpointing.md): Track, rewind, and summarize Claude's edits and conversation to manage session state.
- [Use Claude Code with Chrome (beta)](references/chrome.md): Connect Claude Code to your Chrome browser to test web apps, debug with console logs, automate form filling, and extract data from web pages.
- [Use Claude Code on the web](references/claude-code-on-the-web.md): Configure cloud environments, setup scripts, network access, and Docker in Anthropic's sandbox. Move sessions between web and terminal with `--remote` and `--teleport`.
- [Explore the .claude directory](references/claude-directory.md): Where Claude Code reads CLAUDE.md, settings.json, hooks, skills, commands, subagents, rules, and auto memory. Explore the .claude directory in your project and ~/.claude in your home directory.
- [Claude Code on Claude Platform on AWS](references/claude-platform-on-aws.md): Configure Claude Code to use the Anthropic-operated Claude API with AWS authentication, IAM access control, and AWS Marketplace billing.
- [CLI reference](references/cli-reference.md): Complete reference for Claude Code command-line interface, including commands and flags.
- [Code Review](references/code-review.md): Set up automated PR reviews that catch logic errors, security vulnerabilities, and regressions using multi-agent analysis of your full codebase
- [Commands](references/commands.md): Complete reference for commands available in Claude Code, including built-in commands and bundled skills.
- [Common workflows](references/common-workflows.md): Step-by-step guides for exploring codebases, fixing bugs, refactoring, testing, and other everyday tasks with Claude Code.
- [Communications kit](references/communications-kit.md): Launch announcements, drip-campaign messages, and FAQ responses for rolling Claude Code out to your engineering organization.
- [Let Claude use your computer from the CLI](references/computer-use.md): Enable computer use in the Claude Code CLI so Claude can open apps, click, type, and see your screen on macOS. Test native apps, debug visual issues, and automate GUI-only tools without leaving your terminal.
- [Explore the context window](references/context-window.md): An interactive simulation of how Claude Code's context window fills during a session. See what loads automatically, what each file read costs, and when rules and hooks fire.
- [Manage costs effectively](references/costs.md): Track token usage, set team spend limits, and reduce Claude Code costs with context management, model selection, extended thinking settings, and preprocessing hooks.
- [Data usage](references/data-usage.md): Learn about Anthropic's data usage policies for Claude
- [Debug your configuration](references/debug-your-config.md): Diagnose why CLAUDE.md, settings, hooks, MCP servers, or skills aren't taking effect. Use /context, /doctor, /hooks, and /mcp to see what actually loaded.
- [Launch sessions from links](references/deep-links.md): Open a Claude Code terminal session from a URL. Embed `claude-cli://` links in runbooks, alerts, and dashboards so a click opens Claude Code in the right repo with the right prompt.
- [Desktop application](references/desktop.md): Get more out of Claude Code Desktop: parallel sessions with Git isolation, drag-and-drop pane layout, integrated terminal and file editor, side chats, computer use, Dispatch sessions from your phone, visual diff review, app previews, PR monitoring, connectors, and enterprise configuration.
- [Desktop changelog](references/desktop-changelog.md): Release notes for Claude Code on Desktop, covering new features, improvements, and bug fixes by Desktop app version.
- [Get started with the desktop app](references/desktop-quickstart.md): Install Claude Code on desktop and start your first coding session
- [Schedule recurring tasks in Claude Code Desktop](references/desktop-scheduled-tasks.md): Set up scheduled tasks in Claude Code Desktop to run Claude automatically on a recurring basis for daily code reviews, dependency audits, or morning briefings.
- [Development containers](references/devcontainer.md): Run Claude Code inside a dev container for consistent, isolated environments across your team.
- [Discover and install prebuilt plugins through marketplaces](references/discover-plugins.md): Find and install plugins from marketplaces to extend Claude Code with new skills, agents, and capabilities.
- [Environment variables](references/env-vars.md): Reference for environment variables that control Claude Code behavior.
- [Error reference](references/errors.md): Look up Claude Code runtime error messages with what each one means and how to fix it.
- [Speed up responses with fast mode](references/fast-mode.md): Get faster Opus responses in Claude Code by toggling fast mode.
- [Extend Claude Code](references/features-overview.md): Understand when to use CLAUDE.md, Skills, subagents, hooks, MCP, and plugins.
- [Fullscreen rendering](references/fullscreen.md): Enable a smoother, flicker-free rendering mode with mouse support and stable memory usage in long conversations.
- [Claude Code GitHub Actions](references/github-actions.md): Learn about integrating Claude Code into your development workflow with Claude Code GitHub Actions
- [Claude Code with GitHub Enterprise Server](references/github-enterprise-server.md): Connect Claude Code to your self-hosted GitHub Enterprise Server instance for web sessions, code review, and plugin marketplaces.
- [Claude Code GitLab CI/CD](references/gitlab-ci-cd.md): Learn about integrating Claude Code into your development workflow with GitLab CI/CD
- [Glossary](references/glossary.md): Definitions for Claude Code terminology. Learn what agentic loop, compaction, CLAUDE.md, hooks, subagents, MCP, and other core concepts mean.
- [Keep Claude working toward a goal](references/goal.md): Set a completion condition with /goal and Claude keeps working across turns until the condition is met.
- [Claude Code on Google Vertex AI](references/google-vertex-ai.md): Learn about configuring Claude Code through Google Vertex AI, including setup, IAM configuration, and troubleshooting.
- [Run Claude Code programmatically](references/headless.md): Use the Agent SDK to run Claude Code programmatically from the CLI, Python, or TypeScript.
- [Hooks reference](references/hooks.md): Reference for Claude Code hook events, configuration schema, JSON input/output formats, exit codes, async hooks, HTTP hooks, prompt hooks, and MCP tool hooks.
- [Automate workflows with hooks](references/hooks-guide.md): Run shell commands automatically when Claude Code edits files, finishes tasks, or needs input. Format code, send notifications, validate commands, and enforce project rules.
- [How Claude Code works](references/how-claude-code-works.md): Understand the agentic loop, built-in tools, and how Claude Code interacts with your project.
- [Interactive mode](references/interactive-mode.md): Complete reference for keyboard shortcuts, input modes, and interactive features in Claude Code sessions.
- [JetBrains IDEs](references/jetbrains.md): Use Claude Code with JetBrains IDEs including IntelliJ, PyCharm, WebStorm, and more
- [Customize keyboard shortcuts](references/keybindings.md): Customize keyboard shortcuts in Claude Code with a keybindings configuration file.
- [Legal and compliance](references/legal-and-compliance.md): Legal agreements, compliance certifications, and security information for Claude Code.
- [LLM gateway configuration](references/llm-gateway.md): Learn how to configure Claude Code to work with LLM gateway solutions. Covers gateway requirements, authentication configuration, model selection, and provider-specific endpoint setup.
- [Control MCP server access for your organization](references/managed-mcp.md): Restrict which MCP servers users can add or connect to with managed configuration files, allowlists, and denylists.
- [Connect Claude Code to tools via MCP](references/mcp.md): Learn how to connect Claude Code to your tools with the Model Context Protocol.
- [How Claude remembers your project](references/memory.md): Give Claude persistent instructions with CLAUDE.md files, and let Claude accumulate learnings automatically with auto memory.
- [Claude Code on Microsoft Foundry](references/microsoft-foundry.md): Learn about configuring Claude Code through Microsoft Foundry, including setup, configuration, and troubleshooting.
- [Model configuration](references/model-config.md): Learn about the Claude Code model configuration, including model aliases like `opusplan`
- [Monitoring](references/monitoring-usage.md): Learn how to enable and configure OpenTelemetry for Claude Code.
- [Enterprise network configuration](references/network-config.md): Configure Claude Code for enterprise environments with proxy servers, custom Certificate Authorities (CA), and mutual Transport Layer Security (mTLS) authentication.
- [Output styles](references/output-styles.md): Adapt Claude Code for uses beyond software engineering
- [Overview](references/overview.md): Claude Code is an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools. Available in your terminal, IDE, desktop app, and browser.
- [Choose a permission mode](references/permission-modes.md): Control whether Claude asks before editing files or running commands. Cycle modes with Shift+Tab in the CLI or use the mode selector in VS Code, Desktop, and claude.ai.
- [Configure permissions](references/permissions.md): Control what Claude Code can access and do with fine-grained permission rules, modes, and managed policies.
- [Platforms and integrations](references/platforms.md): Choose where to run Claude Code and what to connect it to. Compare the CLI, Desktop, VS Code, JetBrains, web, mobile, and integrations like Chrome, Slack, and CI/CD.
- [Constrain plugin dependency versions](references/plugin-dependencies.md): Declare version constraints on plugin dependencies so your plugin keeps working when an upstream plugin ships a breaking change.
- [Recommend your plugin from your CLI](references/plugin-hints.md): Emit a one-line marker from your CLI so Claude Code prompts users to install your official plugin.
- [Create and distribute a plugin marketplace](references/plugin-marketplaces.md): Build and host plugin marketplaces to distribute Claude Code extensions across teams and communities.
- [Create plugins](references/plugins.md): Create custom plugins to extend Claude Code with skills, agents, hooks, and MCP servers.
- [Plugins reference](references/plugins-reference.md): Complete technical reference for Claude Code plugin system, including schemas, CLI commands, and component specifications.
- [How Claude Code uses prompt caching](references/prompt-caching.md): Claude Code manages prompt caching automatically. See why a model switch triggers a slow uncached turn, what `/compact` costs, why CLAUDE.md edits don't apply mid-session, and how to check your cache hit rate.
- [Prompt library](references/prompt-library.md): Copy-paste prompts for Claude Code, tagged by task and role.
- [Quickstart](references/quickstart.md): Welcome to Claude Code!
- [Continue local sessions from any device with Remote Control](references/remote-control.md): Continue a local Claude Code session from your phone, tablet, or any browser using Remote Control. Works with claude.ai/code and the Claude mobile app.
- [Automate work with routines](references/routines.md): Put Claude Code on autopilot. Define routines that run on a schedule, trigger on API calls, or react to GitHub events from Anthropic-managed cloud infrastructure.
- [Choose a sandbox environment](references/sandbox-environments.md): Compare Claude Code sandbox options: the built-in sandboxed Bash tool, sandbox runtime, dev containers, Docker, and VMs. Choose the right isolation for your threat model.
- [Configure the sandboxed Bash tool](references/sandboxing.md): Learn how Claude Code's sandboxed Bash tool provides filesystem and network isolation for safer, more autonomous agent execution.
- [Run prompts on a schedule](references/scheduled-tasks.md): Use /loop and the cron scheduling tools to run prompts repeatedly, poll for status, or set one-time reminders within a Claude Code session.
- [Security](references/security.md): Learn about Claude Code's security safeguards and best practices for safe usage.
- [Configure server-managed settings](references/server-managed-settings.md): Centrally configure Claude Code for your organization through server-delivered settings, without requiring device management infrastructure.
- [Manage sessions](references/sessions.md): Name, resume, branch, and switch between Claude Code conversations. Covers `--continue`, `--resume`, `--from-pr`, the `/resume` picker, session naming, and where transcripts are stored.
- [Claude Code settings](references/settings.md): Configure Claude Code with global and project-level settings, and environment variables.
- [Advanced setup](references/setup.md): System requirements, platform-specific installation, version management, and uninstallation for Claude Code.
- [Extend Claude with skills](references/skills.md): Create, manage, and share skills to extend Claude's capabilities in Claude Code. Includes custom commands and bundled skills.
- [Claude Code in Slack](references/slack.md): Delegate coding tasks directly from your Slack workspace
- [Customize your status line](references/statusline.md): Configure a custom status bar to monitor context window usage, costs, and git status in Claude Code
- [Create custom subagents](references/sub-agents.md): Create and use specialized AI subagents in Claude Code for task-specific workflows and improved context management.
- [Configure your terminal for Claude Code](references/terminal-config.md): Fix Shift+Enter for newlines, get a terminal bell when Claude finishes, configure tmux, match the color theme, and enable Vim mode in the Claude Code CLI.
- [Enterprise deployment overview](references/third-party-integrations.md): Learn how Claude Code can integrate with various third-party services and infrastructure to meet enterprise deployment requirements.
- [Tools reference](references/tools-reference.md): Complete reference for the tools Claude Code can use, including permission requirements and per-tool behavior.
- [Troubleshoot installation and login](references/troubleshoot-install.md): Fix command not found, PATH, permission, network, and authentication errors when installing or signing in to Claude Code.
- [Troubleshooting](references/troubleshooting.md): Fix high CPU or memory usage, hangs, auto-compact thrashing, and search problems in Claude Code, and find the right page for other issues.
- [Plan in the cloud with ultraplan](references/ultraplan.md): Start a plan from your CLI, draft it on Claude Code on the web, then execute it remotely or back in your terminal
- [Find bugs with ultrareview](references/ultrareview.md): Run a deep, multi-agent code review in the cloud with /ultrareview to find and verify bugs before you merge.
- [Voice dictation](references/voice-dictation.md): Speak your prompts in the Claude Code CLI with hold-to-record or tap-to-record voice dictation.
- [Use Claude Code in VS Code](references/vs-code.md): Install and configure the Claude Code extension for VS Code. Get AI coding assistance with inline diffs, @-mentions, plan review, and keyboard shortcuts.
- [Get started with Claude Code on the web](references/web-quickstart.md): Run Claude Code in the cloud from your browser or phone. Connect a GitHub repository, submit a task, and review the PR without local setup.
- [Run parallel sessions with worktrees](references/worktrees.md): Isolate parallel Claude Code sessions in separate git worktrees so changes don't collide. Covers the `--worktree` flag, subagent isolation, `.worktreeinclude`, cleanup, and non-git VCS hooks.
- [Zero data retention](references/zero-data-retention.md): Learn about Zero Data Retention (ZDR) for Claude Code on Claude for Enterprise, including scope, disabled features, and how to request enablement.

### Agent SDK

- [How the agent loop works](references/agent-sdk/agent-loop.md): Understand the message lifecycle, tool execution, context window, and architecture that power your SDK agents.
- [Use Claude Code features in the SDK](references/agent-sdk/claude-code-features.md): Load project instructions, skills, hooks, and other Claude Code features into your SDK agents.
- [Track cost and usage](references/agent-sdk/cost-tracking.md): Learn how to track token usage, estimate costs, and configure prompt caching with the Claude Agent SDK.
- [Give Claude custom tools](references/agent-sdk/custom-tools.md): Define custom tools with the Claude Agent SDK's in-process MCP server so Claude can call your functions, hit your APIs, and perform domain-specific operations.
- [Rewind file changes with checkpointing](references/agent-sdk/file-checkpointing.md): Track file changes during agent sessions and restore files to any previous state
- [Intercept and control agent behavior with hooks](references/agent-sdk/hooks.md): Intercept and customize agent behavior at key execution points with hooks
- [Hosting the Agent SDK](references/agent-sdk/hosting.md): Deploy and host Claude Agent SDK in production environments
- [Connect to external tools with MCP](references/agent-sdk/mcp.md): Configure MCP servers to extend your agent with external tools. Covers transport types, tool search for large tool sets, authentication, and error handling.
- [Migrate to Claude Agent SDK](references/agent-sdk/migration-guide.md): Guide for migrating the Claude Code TypeScript and Python SDKs to the Claude Agent SDK
- [Modifying system prompts](references/agent-sdk/modifying-system-prompts.md): Choose between the `claude_code` preset and a custom system prompt, and customize behavior with CLAUDE.md, output styles, append, or a fully custom prompt.
- [Observability with OpenTelemetry](references/agent-sdk/observability.md): Export traces, metrics, and events from the Agent SDK to your observability backend using OpenTelemetry.
- [Agent SDK overview](references/agent-sdk/overview.md): Build production AI agents with Claude Code as a library
- [Configure permissions](references/agent-sdk/permissions.md): Control how your agent uses tools with permission modes, hooks, and declarative allow/deny rules.
- [Plugins in the SDK](references/agent-sdk/plugins.md): Load custom plugins to extend Claude Code with commands, agents, skills, and hooks through the Agent SDK
- [Agent SDK reference - Python](references/agent-sdk/python.md): Complete API reference for the Python Agent SDK, including all functions, types, and classes.
- [Quickstart](references/agent-sdk/quickstart.md): Get started with the Python or TypeScript Agent SDK to build AI agents that work autonomously
- [Securely deploying AI agents](references/agent-sdk/secure-deployment.md): A guide to securing Claude Code and Agent SDK deployments with isolation, credential management, and network controls
- [Persist sessions to external storage](references/agent-sdk/session-storage.md): Mirror session transcripts to S3, Redis, or your own backend so any host can resume them.
- [Work with sessions](references/agent-sdk/sessions.md): How sessions persist agent conversation history, and when to use continue, resume, and fork to return to a prior run.
- [Agent Skills in the SDK](references/agent-sdk/skills.md): Extend Claude with specialized capabilities using Agent Skills in the Claude Agent SDK
- [Slash Commands in the SDK](references/agent-sdk/slash-commands.md): Learn how to use slash commands to control Claude Code sessions through the SDK
- [Stream responses in real-time](references/agent-sdk/streaming-output.md): Get real-time responses from the Agent SDK as text and tool calls stream in
- [Streaming Input](references/agent-sdk/streaming-vs-single-mode.md): Understanding the two input modes for Claude Agent SDK and when to use each
- [Get structured output from agents](references/agent-sdk/structured-outputs.md): Return validated JSON from agent workflows using JSON Schema, Zod, or Pydantic. Get type-safe, structured data after multi-turn tool use.
- [Subagents in the SDK](references/agent-sdk/subagents.md): Define and invoke subagents to isolate context, run tasks in parallel, and apply specialized instructions in your Claude Agent SDK applications.
- [Todo Lists](references/agent-sdk/todo-tracking.md): Track and display todos using the Claude Agent SDK for organized task management
- [Scale to many tools with tool search](references/agent-sdk/tool-search.md): Scale your agent to thousands of tools by discovering and loading only what's needed, on demand.
- [Agent SDK reference - TypeScript](references/agent-sdk/typescript.md): Complete API reference for the TypeScript Agent SDK, including all functions, types, and interfaces.
- [TypeScript SDK V2 session API (removed)](references/agent-sdk/typescript-v2-preview.md): Reference for the removed V2 TypeScript Agent SDK session API, with session-based send/stream patterns for multi-turn conversations.
- [Handle approvals and user input](references/agent-sdk/user-input.md): Surface Claude's approval requests and clarifying questions to users, then return their decisions to the SDK.

### What's new (weekly changelog)

- [Week 13 · March 23–27, 2026](references/whats-new/2026-w13.md): Auto mode for hands-off permissions, computer use built in, PR auto-fix in the cloud, transcript search, and a PowerShell tool for Windows.
- [Week 14 · March 30 – April 3, 2026](references/whats-new/2026-w14.md): Computer use in the CLI, interactive in-product lessons, flicker-free rendering, per-tool MCP result-size overrides, and plugin executables on PATH.
- [Week 15 · April 6–10, 2026](references/whats-new/2026-w15.md): Ultraplan cloud planning, the Monitor tool with self-pacing /loop, /team-onboarding for packaging your setup, and /autofix-pr from your terminal.
- [Week 16 · April 13–17, 2026](references/whats-new/2026-w16.md): Claude Opus 4.7 with the new xhigh effort level, Routines on Claude Code on the web, mobile push notifications that ping your phone when Claude needs you, a /usage breakdown that shows what's driving your limits, and native binaries replacing the bundled JavaScript.
- [Week 17 · April 20–24, 2026](references/whats-new/2026-w17.md): /ultrareview opens as a research preview, automatic session recaps when you return to a terminal, custom color themes you can build and ship in plugins, and a redesigned Claude Code on the web.
- [Week 18 · April 27 – May 1, 2026](references/whats-new/2026-w18.md): Claude Code on Windows runs without Git Bash, claude auth login accepts a pasted OAuth code when the browser callback can't reach localhost, claude project purge cleans up local state per project, and pasting a PR URL into /resume finds the session that created it.
- [Week 19 · May 4–8, 2026](references/whats-new/2026-w19.md): Load plugins from .zip archives and URLs, search command history across every project with Ctrl+R, branch new worktrees from local HEAD or the remote default, and block actions unconditionally with auto mode hard deny rules.
- [Week 20 · May 11–15, 2026](references/whats-new/2026-w20.md): Manage every Claude Code session from one screen with agent view, keep Claude working toward a goal until a condition holds, and run fast mode on Opus 4.7 by default.
- [What's new](references/whats-new/index.md): A weekly digest of notable Claude Code features, with code snippets, demos, and context on why they matter.

## Meta

- [How this skill was built](references/_meta/scraping-method.md): Source, tools, exact recipe, refresh procedure, and known gotchas.
- [Fetcher script](references/_meta/scripts/refetch-md.py): Curls the Mintlify `.md` endpoint for every page in llms.txt; run any time to refresh the snapshot.
- [SKILL.md generator](references/_meta/scripts/generate-skill-md.py): Regenerates this file from the references/ tree.
