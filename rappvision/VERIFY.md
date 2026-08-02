# How these channels were verified

Every live scene in `rappvision/*/channel.json` drives a real application. A scene
that fails to drive it does not look broken — it looks like a video of an app
sitting still — so none of these were written from reading source. They were
written from measurements taken outside the page, in real headless Chromium,
against the actual RAPP Vision player.

Reproduce it:

```bash
# from the parent directory that holds both repos, so paths match GitHub Pages
python3 -m http.server 8777
# then drive the real player and assert on every scene
node verify.mjs rooms-tour arcade-cold-boot workbench-three-tools ...
```

## What the harness asserts, per scene

| Check | Why it exists |
|---|---|
| an iframe is present and same-origin | cross-origin degrades to captions; live replay would be a lie |
| `elementFromPoint(centre)` is not inside the entry gate | an overlay faded to `opacity:0` still contributes its text, so `innerText` cannot answer "did the gate close" — hit-testing can |
| pixels changed between two samples | catches a frozen or crashed renderer |
| **or** the app's DOM changed since scene start | a spreadsheet does not animate; "no pixels moved" is not the same as "the cues did nothing" |
| no 404s, no page errors | a missing app is a black rectangle with confident captions over it |

## Defects this found

Nine of these were written, all nine "looked right" in a browser, and the harness
rejected four of them. The list is kept because the failures are more useful than
the passes.

**The lightcycles script killed both players in nine seconds.** The moves were
`W` then `S` — a 180° flip, which in that game is instant self-collision. Every
turn in the shipped schedule is 90°. Two `REMATCH` cues sit at 24 s and 36 s and
cost nothing while the game is alive, because the player only presses a control
once it is genuinely clickable.

**The vector editor was never drawn in.** Its tools bind `pointerdown`, and the
player's `drag` dispatched `MouseEvent` only, so all four drags were silent
no-ops. Worse, `onDown`'s first statement is
`overlay.setPointerCapture(e.pointerId)`, which throws `NotFoundError` for a
synthetic pointer id and aborts the handler before it reads a coordinate. Both
were fixed in the player: `drag` now speaks Pointer Events as well as Mouse
Events, and pointer capture is shimmed to swallow exactly that failure.

*Named measurement:* three scripted shape drags → three new rows in the editor's
own LAYERS panel (66 → 69). Before the fix: 66 → 66.

**Skybreak Dogfight played its briefing card for the whole scene.** `#title` is a
full-screen `CLICK TO LAUNCH` overlay and no cue clicked it. It animates, so
every liveness check passed. The thumbnail caught it — which is the argument for
generating thumbnails from the running scene rather than choosing them by hand.

**The 808's sequencer played out of frame.** The sixteen-step grid sits below the
fold in a 16:10 stage, so the scene showed a header reading *No Song Loaded* for
seventy seconds. A `scroll` action was added to the player; the scene now brings
`#drumSequencer` into view before it starts the transport.

## Deliberate exclusions

**Pointer-lock games cannot be scripted.** A synthetic click carries no transient
user activation, so `requestPointerLock()` always fails for a script, and an app
that gates on it — Voxel World, for one — shows *Click to play* forever. Measured
both ways: with `allow-pointer-lock` present in the iframe sandbox and without.
Voxel World was cut from the Arcade channel for this reason and replaced with
Sky Realms.

The sandbox still gained `allow-pointer-lock`, because a *human* who pauses and
takes over is a trusted gesture and deserves the mouse. Chromium names the
missing permission out loud — `Blocked pointer lock ... the 'allow-pointer-lock'
permission is not set` — which is how it was found. Note that headless Chromium
refuses pointer lock outright (`The root document of this element is not valid
for pointer lock`), so that half is reasoned, not measured, and is marked as such
rather than claimed as verified.

## Selectors are read, not guessed

Every `selector` in these channels came out of the live DOM of the running app.
Where a control has no stable id it is addressed by its label instead of by
position — CHIP-8's ROM shelf is a grid whose order is not guaranteed, and
`nth-child` would quietly load the wrong game.

Times are measured from the scene's `ready` anchor, not from scene start, so a
slow machine drifts without desyncing.
