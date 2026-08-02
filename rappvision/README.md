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
  VERIFY.md         how every live scene here was measured, and what that rejected
  rooms/            channel: nine ambient places, live-only
  arcade/           channel: games and emulators, live-only
  workbench/        channel: production tools, live-only
```

## Four channels in one folder

A repo is not limited to one channel — a channel is just a `channel.json`, so
this folder holds four. Each subfolder is registered separately in the player's
[`channels.json`](https://github.com/kody-w/rapp-vision/blob/main/channels.json)
and resolves its apps with `../../`, straight back into this repo.

| Channel | Entries | Video files |
|---|---|---|
| `channel.json` — Local First Tools | 3 | 2 |
| `rooms/` — 🕯️ Rooms | 3 | **0** |
| `arcade/` — 🕹️ Arcade | 3 | **0** |
| `workbench/` — 🛠️ The Workbench | 3 | **0** |

The three live-only channels publish 57 KB of JSON between them and drive 31
scenes across 26 of the apps in this repo. Rendering the same thing as video
would be north of a gigabyte, and would not let anyone take the wheel.

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

## Adding a *live* entry

Different pipeline, because there is no file to drop:

1. Open the app and read its DOM. Take the real ids of the controls you intend
   to press — do not guess them, and do not address anything by position.
2. Write the scene: `app`, a `ready` anchor, and a list of `actions`.
3. Drive it in the actual player, in headless Chromium, and assert from outside
   the page that the app is genuinely running.

Step 3 is not optional. A scene that fails to drive its app does not look
broken — it looks like a video of an app sitting still. Four of the nine live
entries here failed on the first pass, and two of those failures were bugs in
the player itself. [`VERIFY.md`](VERIFY.md) has the list.

## Start your own channel

Copy the [channel template](https://github.com/kody-w/rapp-vision/tree/main/template).
