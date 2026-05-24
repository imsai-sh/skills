---
name: submit-show-hn
description: Use when the user is preparing or troubleshooting a Hacker News Show HN submission. Covers the silent new-account throttle (showlim redirect), community karma thresholds, account-warming timeline, what to do if a post got shadowbanned, and how to write a Show HN that doesn't get flagged. Also covers when Show HN is the wrong format vs. a regular submission.
---

# Submit Show HN

## When this skill applies

The user is about to (or just did) post a Show HN to Hacker News, OR is
troubleshooting why their submission isn't visible.

Common triggers:
- "I want to post my project on Hacker News"
- "I submitted Show HN but it doesn't show up"
- "Why did HN redirect me to /showlim?"
- "How do I get my Show HN to the front page?"
- "Is my HN account ready to post Show HN?"

## The single most important thing to know

**HN silently throttles Show HN from new / low-karma accounts.** Submitting
without warming up your account first results in a `/showlim` redirect and
a silently shadowbanned post that other users can't see.

This is the #1 failure mode. Almost everyone hits it on first try.

→ Full explanation in `references/showlim-page.md`.

## Before posting checklist

Run through this before the user submits:

### 1. Is "Show HN" the right format at all?

Reference: `references/showhn.txt` (pg's official guidelines).

Show HN is **only** for:
- Something the user has personally built
- That other people can **try out** (run, install, click, hold)
- Non-trivial (not "I prompted an LLM to spit this out")
- The submitter is around to answer comments

Not Show HN (use regular submission):
- Blog posts, even good technical ones
- Newsletter signups, landing pages, fundraisers
- Lists (`awesome-X`)
- Version bump announcements ("Foo 1.3.1 is out")
- AI-generated one-offs

### 2. Is the account warm enough?

Check via the HN public API (no auth needed):

```bash
curl -s "https://hacker-news.firebaseio.com/v0/user/<HN_USERNAME>.json" | python3 -m json.tool
```

Look at:
- `created` (unix timestamp) → translate to age
- `karma` → community-observed safe floor: ~50–100 for low risk, 200+ for
  safe. Below 10 is very likely to throttle.
- `submitted` array length → recent activity

If karma < 50 or account age < 30 days, **expect a throttle**. Recommend the
user wait and warm the account first (see "Account warming plan" below).

### 3. Is the post itself well-formed?

- Title starts with literal `Show HN:` (case-sensitive, with colon)
- Title ≤ 80 chars, no hype words ("revolutionary", "powerful", "amazing")
- Submit with a URL filled in (link to GitHub repo, live demo, etc.) — HN
  auto-displays the domain and star count for GitHub URLs
- Body text: explain *why* you built it (personal motivation), not just
  *what* it does
- No emoji, no markdown formatting bold/headers (HN doesn't render them)
- Be upfront about limitations / caveats — HN respects honesty, punishes
  hype

→ Full rules in `references/showhn.txt` and `references/newsguidelines.txt`.

## If the post got throttled (`/showlim` redirect)

Action playbook:

1. **Verify it's actually throttled**: open
   `https://news.ycombinator.com/threads?id=<USERNAME>` → if your post is
   there but doesn't appear on `/show` or `/shownew` for an incognito
   browser, you're throttled.

2. **Do NOT**:
   - Resubmit the same project (HN dedup hurts you)
   - Create a new account (HN sockpuppet detection → permanent ban risk)
   - Ask friends to upvote (voting ring detection → both accounts
     shadowbanned)
   - Delete the post (won't lift the throttle, just wastes the URL)

3. **Do**:
   - Leave the throttled post as-is
   - Start the account warming plan (next section)
   - Push the project to other channels in the meantime (Reddit, Twitter,
     Bluesky, awesome-* PRs, language-specific subreddits)
   - Plan to resubmit in 2–4 weeks after karma builds, with a small visible
     change (new version, new feature) to avoid pure dedup

## Account warming plan (1–2 weeks)

Goal: 50+ karma, demonstrable substantive participation, not look like a
drive-by self-promoter.

Daily routine:
- Read HN front page (`/news`) and `/show` daily
- Find 2–3 stories you genuinely know something about (AI tooling, CLI,
  TypeScript, devops, whatever your domain is)
- Write **technical, substantive** comments:
  - Explain a non-obvious trade-off
  - Share concrete experience ("when I did X, Y happened")
  - Suggest alternatives (don't just complain)
  - Ask curious questions, not "gotcha" cross-examination
- Avoid: "+1" / "this" / "great post" / one-liners — those don't earn karma
  and look like padding
- Avoid: linking to your own project in comments early on (HN flags
  self-promo patterns; once you have karma it's tolerated within reason)

Avoid:
- Politics, ideology, tech religious wars — karma comes fast but downvotes
  come faster
- Contrarian / inflammatory takes for engagement bait

After ~2 weeks (or once karma > 50), the Show HN throttle usually clears.
There's no notification — just try submitting again.

## Backup channels while HN is on cooldown

The project doesn't have to wait. Post to other places now and let GitHub
stars accumulate — when you eventually resubmit Show HN, you can lead with
"X stars in Y days" which signals legitimacy.

| Channel | Notes |
|---|---|
| r/<topic-subreddit> | Best subreddit depends on the project niche |
| r/programming | Generic, large but burns fast |
| Twitter/X | Thread format: hook + screenshot + code + link |
| Bluesky | Same as X but more friendly |
| Mastodon (fosstodon.org) | OSS-friendly fediverse |
| Dev.to / Hashnode | Long-form "how I built X" |
| awesome-* GitHub lists | PR to add your project; long-tail traffic |
| Product Hunt | If the project is consumer-facing |
| V2EX / 即刻 / 掘金 | Chinese tech community equivalents |

## Tips for the actual Show HN body (when you do resubmit)

Reference: `references/showhn.txt`, `references/newsguidelines.txt`.

Structural template that fits HN culture:

```
Hi HN, I built this because <personal motivation, 1-2 sentences>.

<What it does and how it works, 1-2 paragraphs. Include enough technical
detail that HN readers see it's not a toy. Mention the language, key
dependencies, and any clever design choice.>

<Caveats you want to be upfront about, as a bullet list:>
- Known limitation 1
- Untested platform / scenario
- Trade-off you made

<Link to install / try / docs.>

<License>. Feedback welcome.
```

Key habits:
- Start with "Hi HN" — community-friendly
- Use plain text, no markdown formatting that won't render
- Lead with motivation (why), not features (what)
- Be honest about caveats — HN respects it, hides hype
- Stay in the comments for at least 2 hours after submitting; first 30
  minutes determines front-page surfacing

## In the comments after submission

Reference: bottom section of `references/showhn.txt`.

Be respectful:
- Anyone sharing work is making a contribution, however modest
- Ask questions out of curiosity, don't cross-examine
- Instead of "you're doing it wrong", suggest alternatives
- When something isn't good, don't pretend it is — but don't be
  gratuitously negative

## Files in this skill

- `references/showhn.txt` — pg's official Show HN guidelines
- `references/newsguidelines.txt` — HN community-wide guidelines
- `references/newswelcome.txt` — HN's onboarding page for new users
- `references/showlim-page.md` — the throttle page content + community
  knowledge about how the throttle works
