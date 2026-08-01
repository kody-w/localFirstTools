# RAPP Vision channel — Local First Tools

This folder is a **RAPP Vision channel**. It lives inside the
[`localFirstTools`](https://github.com/kody-w/localFirstTools) repo, not inside the player's
repo — which is the whole point of the format.

Watch it: **https://kody-w.github.io/rapp-vision/#/channel/localfirsttools**

## Why it lives here

RAPP Vision resolves every path in `channel.json` **relative to that file's own URL**. So a
channel is portable: put `channel.json` in any public repo, host the media next to it, and the
player streams it. No upload, no account, no platform in the middle.

```
rappvision/
  channel.json      the catalog — titles, chapters, sources, live scripts
  media/            the video files
  thumbs/           poster images
```

## Two forms of the same story

This channel deliberately publishes both:

| Entry | Form | Size |
|---|---|---|
| `lft-tumbler-live` | **Live replay** — a script, no video file | a few KB |
| `lft-tumbler-reel` | Static pre-rendered video | ~7 MB |

The live entry has no `sources` at all. Instead it carries a `live.scenes` array: for each scene,
an app URL and a timeline of interactions. The player loads the real application in an iframe and
replays those interactions against a clock. Play, pause and seek behave normally — but the app is
genuinely running, so you can pause at any point and take over.

That works here because these are self-contained, offline-first apps served from the same origin
as the player on GitHub Pages. When it can't work — cross-origin, or a browser that blocks it —
the static video is still published alongside, and the player falls back.

## Adding a video

1. Drop the file in `media/` and a poster in `thumbs/`.
2. Add an entry to `channel.json`.
3. Push.

That's the entire publishing pipeline.

## Start your own channel

Copy the [channel template](https://github.com/kody-w/rapp-vision/tree/main/template).
