# The `/showlim` page — what HN shows when your Show HN gets throttled

When a new / low-karma account submits a Show HN, HN silently redirects to
`https://news.ycombinator.com/showlim` after the submit click. The post may
still appear in your own `/threads` view but it does NOT surface on `/show`
or `/shownew` for other users.

## Verbatim page content (captured 2026-05-25)

```
We're temporarily restricting Show HNs because of a massive influx, mostly
by users who aren't yet familiar with the site or its culture.

You're welcome on HN! Take some time to get to know the community, become
a good contributor, and then it will be fine to post an occasional Show HN.

Here are some links to get you started:

  https://news.ycombinator.com/newsguidelines.html
  https://news.ycombinator.com/newswelcome.html
  https://news.ycombinator.com/showhn.html
```

## What this actually means (community knowledge, not official)

- **It's not a ban.** Account is fine. Just Show HN privilege is gated.
- **The throttle is silent.** No notification, no "rejected" status. Your
  post is technically submitted but invisible to others.
- **HN doesn't publish thresholds.** Community-observed heuristics:
  - account age: at least a few weeks, often months
  - karma: 50–100 minimum, 200+ for safety
  - substantive comment history (not "+1" / one-liners)
  - no self-promotion pattern in comments
- **It clears automatically once you build reputation.** No appeal process.

## Why HN does this (2024+)

Massive influx of AI-generated / "vibe-coded" projects flooded Show HN,
many from accounts created same-day. dang (HN moderator) added this
silent throttle to filter for accounts that have demonstrated they
understand the community before letting them broadcast.

## Don't do these things

- ❌ Resubmit same project right away — HN dedup detects, hurts you
- ❌ Create a new account and resubmit — sockpuppet detection is strict,
  can result in permanent ban
- ❌ Ask friends to upvote — voting ring detection, both accounts get
  shadowbanned
- ❌ Delete the throttled post — won't help; HN remembers the attempt
