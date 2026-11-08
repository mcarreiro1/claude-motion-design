# FREERANGE: Pix & Yolk (30 s, 9:16)

The six-shot script rebuilt in code: claymation look (clay shading, thumbprint texture, per-pose outline "boil"), stop-motion on twos (12 poses/s in a 24 fps file), lime `#c6ff3d` backdrop, shallow depth of field. No lettering and no dialogue. Pix has the five-point comb and Yolk is mustard-yellow, as the script specifies.

| Shot | Time | What happens |
|---|---|---|
| 01 | 0-5 | Static medium. Pix hops in from the left, panicked, and skids to a stop by the pink notes. Yolk sits by the mug, smiling |
| 02 | 5-9 | Slow push-in on Yolk, who gives a big wave with rosy cheeks. Pix watches |
| 03 | 9-13 | Close-up. Pix leans in and squints, wing to chin, eyes darting. The music drops to a tiptoe |
| 04 | 13-19 | Yolk laughs, shaking with both arms up. Pix is at the left edge |
| 05 | 19-24 | Low angle. Pix fist-pumps and bounces, comb wobbling. Yolk claps |
| 06 | 24-30 | Side by side, both turn to camera, Yolk tilts. Slow push-in |

```bash
node render.js probe 2 6 10 15 21 27   # stills -> probe/sheet.png
node render.js full                    # 360 poses -> out/video.mp4
node render.js part 5 9                # re-render one shot only
python3 audio.py                       # synthesized music + SFX, -14 LUFS -> out/audio.wav
ffmpeg -i out/video.mp4 -i out/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart out/freerange-pix-yolk.mp4
```
Needs Node Playwright (`NODE_PATH=$(npm root -g)` if it is installed globally), ffmpeg and numpy. Open `film.html?preview` to scrub: Space plays or pauses, the arrow keys step one pose, R replays.
