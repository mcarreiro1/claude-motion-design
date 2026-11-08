"""Soundtrack for FREERANGE: PIX & YOLK, 100 % synthesized (no downloaded media).
120 BPM, so every cut (5, 9, 13, 19, 24 s) lands on a beat. Music bed: plucked ukulele-ish chords,
marimba melody, soft bass and shaker; shot 3 drops to a tiptoe pizzicato for the suspicious look.
SFX are placed on the animation's own times (hops, skid, wave, squint, laugh, fist pump, claps, head turns).
Output: out/audio.wav normalized to -14 LUFS (two-pass loudnorm), true peak -1.5 dB.
    python3 audio.py
"""
import json, subprocess, wave
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
SR, T, BPM = 48000, 30.0, 120
BEAT = 60 / BPM
N = int(SR * T)
mix = np.zeros((N, 2))
rng = np.random.default_rng(7)


def add(sig, t, gain=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= N: return
    sig = sig[: N - i] * gain
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    mix[i:i + len(sig), 0] += sig * l * 1.414
    mix[i:i + len(sig), 1] += sig * r * 1.414


def tt(d): return np.arange(int(d * SR)) / SR
def hz(n): return 440 * 2 ** ((n - 69) / 12)  # midi -> Hz
def env(d, a=0.005, rel=0.05):
    x = tt(d); e = np.minimum(1, x / a); e *= np.clip((d - x) / rel, 0, 1); return e


def pluck(n, d=1.2, bright=1.0):
    f, x = hz(n), tt(d)
    s = sum((1 / k ** 1.3) * np.sin(2 * np.pi * f * k * x) * np.exp(-x * (3 + 2.2 * k * bright)) for k in range(1, 9))
    return s * env(d, 0.002, 0.08)


def marimba(n, d=0.7):
    f, x = hz(n), tt(d)
    s = np.sin(2 * np.pi * f * x) * np.exp(-x * 6) + 0.35 * np.sin(2 * np.pi * f * 4 * x) * np.exp(-x * 22)
    return s * env(d, 0.002, 0.05)


def bass(n, d=0.45):
    f, x = hz(n), tt(d)
    return (np.sin(2 * np.pi * f * x) + 0.25 * np.sin(4 * np.pi * f * x)) * np.exp(-x * 4) * env(d, 0.004, 0.06)


def noise(d): return rng.standard_normal(int(d * SR))


def hp(s, a=0.9):  # one-pole high-pass
    y = np.empty_like(s); prev_x = prev_y = 0.0
    for i, v in enumerate(s): prev_y = a * (prev_y + v - prev_x); prev_x = v; y[i] = prev_y
    return y


def lp(s, k=8):  # moving-average low-pass
    return np.convolve(s, np.ones(k) / k, mode='same')


def chirp(f0, f1, d, shape='sin'):
    x = tt(d); f = f0 * (f1 / f0) ** (x / d); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) if shape == 'sin' else 2 * ((ph / (2 * np.pi)) % 1) - 1


SHAKER = hp(noise(0.06), 0.97) * np.exp(-tt(0.06) * 60)
KICK = chirp(150, 50, 0.18) * np.exp(-tt(0.18) * 18)
BLOCK = (np.sin(2 * np.pi * 1600 * tt(0.05)) + 0.5 * np.sin(2 * np.pi * 2400 * tt(0.05))) * np.exp(-tt(0.05) * 90)

# ---------------- music ----------------
C, Am, F_, G, Em, E7 = [48, 52, 55, 60], [45, 52, 57, 60], [41, 53, 57, 60], [43, 50, 55, 59], [40, 52, 55, 59], [40, 50, 56, 59]
PROG = [C, Am, F_, G]
MEL = [[72, None, 76, 79, 76, None, 74, 72], [69, None, 72, 76, 74, None, 72, 69],
       [65, None, 69, 72, 74, 72, 69, None], [67, None, 71, 74, 79, None, 77, 74]]
for i in range(60):  # one pass per beat (2 s bars, 15 bars)
    t, bar, b = i * BEAT, i // 4, i % 4
    if 9 <= t < 13:  # shot 3, suspicious: tiptoe pizzicato in A minor, shaker only
        seq = [45, 52, 48, 52] if bar % 2 == 0 else [44, 52, 47, 52]
        add(pluck(seq[b], 0.25, 2.5), t, 0.22, -0.2)
        add(pluck(seq[b] + 12, 0.18, 3), t + BEAT / 2, 0.08, 0.3)
        add(SHAKER, t, 0.025, 0.4); add(SHAKER, t + BEAT / 2, 0.05, 0.4)
        continue
    ch = PROG[bar % 4]
    end = bar == 14
    if end and b > 0: continue
    lift = 1.35 if 19 <= t < 24 else 1.0  # brighter during the fist pump
    for j, n in enumerate(ch): add(pluck(n + 12, 2.0 if end else 0.9, 1.3), t + j * 0.012, 0.07, -0.35 + j * 0.05)
    if not end:
        for j, n in enumerate(ch[1:]): add(pluck(n + 12, 0.35, 2), t + BEAT / 2 + j * 0.01, 0.035, -0.3)
        add(SHAKER, t, 0.035 * lift, 0.4); add(SHAKER, t + BEAT / 2, 0.06 * lift, 0.4)
    if b == 0: add(bass(ch[0] - 12, 1.6 if end else 0.45), t, 0.32); add(KICK, t, 0.22 if not end else 0.15)
    if b == 2: add(bass(ch[0] - 12 + 7, 0.45), t, 0.26); add(KICK, t, 0.18)
    if b in (1, 3): add(BLOCK, t, 0.05, -0.5)
    if t >= 5 and not end:  # melody enters with Yolk's wave
        for e in range(2):
            n = MEL[bar % 4][b * 2 + e]
            if n is not None: add(marimba(n + (12 if lift > 1 else 0)), t + e * BEAT / 2, 0.13, 0.25)
    if end: add(marimba(84, 2.0), t, 0.12, 0.25); add(marimba(79, 2.0), t + 0.06, 0.1, 0.25)

# ---------------- SFX ----------------
def boing(f0=320, f1=140, d=0.16):
    return chirp(f0, f1, d) * np.exp(-tt(d) * 14) * env(d, 0.002, 0.03)
def squish(): return lp(noise(0.09), 30) * np.exp(-tt(0.09) * 35) * 3 + chirp(160, 70, 0.09) * np.exp(-tt(0.09) * 25)
def squawk(f=950):
    d = 0.13; x = tt(d); f_ = f * (1 + 0.35 * np.sin(np.pi * x / d)) * (1 + 0.04 * np.sin(2 * np.pi * 38 * x))
    ph = 2 * np.pi * np.cumsum(f_) / SR
    return (np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sin(3 * ph)) * np.sin(np.pi * x / d) ** 0.6
def flap(): return hp(noise(0.05), 0.85) * np.exp(-tt(0.05) * 70)
def chime(notes, step=0.07):
    s = np.zeros(int(SR * (len(notes) * step + 1.0)))
    for i, n in enumerate(notes):
        b = np.sin(2 * np.pi * hz(n) * tt(1.0)) * np.exp(-tt(1.0) * 5) + 0.3 * np.sin(2 * np.pi * hz(n) * 2.76 * tt(1.0)) * np.exp(-tt(1.0) * 12)
        k = int(i * step * SR); s[k:k + len(b)] += b
    return s
def hmm():
    d = 0.75; x = tt(d); f = 165 * (1 - 0.12 * x / d)
    ph = 2 * np.pi * np.cumsum(f) / SR; s = sum(np.sin(k * ph) / k for k in range(1, 7))
    return lp(s, 6) * np.sin(np.pi * x / d) ** 0.5 * (1 + 0.1 * np.sin(2 * np.pi * 5 * x))
def giggle(f):
    d = 0.11; x = tt(d); ph = 2 * np.pi * np.cumsum(f * (1 - 0.15 * x / d)) / SR
    return (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)) * np.sin(np.pi * x / d) ** 1.5
def clap():
    s = hp(noise(0.12), 0.8); e = np.exp(-tt(0.12) * 35)
    for k in (0.0, 0.008, 0.016):
        i = int(k * SR); e[i:] += 0.5 * np.exp(-np.arange(len(e) - i) / SR * 120)
    return s * e
def whoosh(d=0.35, up=True):
    x = tt(d); s = noise(d); a = np.sin(np.pi * x / d) ** 2
    return lp(hp(s, 0.6 if up else 0.8), 4) * a

# shot 1: panicked hop-in (hops land at 0.9, 1.55, 2.2, 2.85), squawks, wing flutter, skid, pant
for t in (0.9, 1.55, 2.2, 2.85): add(squish(), t, 0.5); add(boing(280, 120), t, 0.12)
for i, t in enumerate((0.35, 1.0, 1.65, 2.3)): add(squawk(900 + 90 * (i % 2)), t, 0.16, -0.3)
for k in range(28):
    t = 0.25 + k / 12
    if t < 2.85 and ((t - 0.25) % 0.65) / 0.65 > 0.1: add(flap(), t, 0.12, -0.2)
sk = lp(noise(0.7), 3) * np.linspace(1, 0, int(0.7 * SR)) ** 1.5; add(sk, 2.85, 0.18)
add(chirp(1400, 600, 0.5) * np.exp(-tt(0.5) * 6), 2.85, 0.03)
for k in range(5): add(lp(noise(0.12), 12) * np.sin(np.pi * tt(0.12) / 0.12), 3.55 + k * 0.42, 0.12, -0.2)
# shot 2: wave, rosy cheeks
add(chime([84, 88, 91, 96]), 5.32, 0.12, 0.4)
for k in range(6): add(flap(), 5.75 + k * 0.21, 0.04, 0.4)
# shot 3: suspicious squint, eye darts
add(whoosh(0.4), 9.2, 0.08)
add(hmm(), 9.55, 0.2, -0.1)
for t in (10.45, 11.45, 12.4): add(BLOCK, t, 0.12, -0.3)
add(chirp(500, 900, 0.18) * np.exp(-tt(0.18) * 8), 11.6, 0.06)
# shot 4: laughing giggles
r = np.random.default_rng(3)
t = 13.15
while t < 18.4:
    for k in range(4): add(giggle(780 + 120 * ((k + int(t * 3)) % 3) + r.uniform(-30, 30)), t + k * 0.14, 0.11, 0.2)
    t += 0.14 * 4 + 0.35
# shot 5: fist pump, comb boing, bounces, claps
add(whoosh(0.3), 19.3, 0.12)
add(chime([79, 84, 88, 91, 96], 0.05), 19.55, 0.14, -0.2)
add(boing(500, 200, 0.3), 19.55, 0.1)
for k in range(5): add(squish(), 19.5 + 0.42 * (k + 1), 0.3 * 0.75 ** k, -0.2)
for k in range(12): add(clap(), 19.6 + k / 3, 0.22, 0.45)
# shot 6: head turns to camera, soft sparkle, button at the end
add(boing(600, 420, 0.12), 24.9, 0.07, -0.25)
add(boing(700, 480, 0.12), 25.25, 0.07, 0.25)
add(chime([91, 96, 100], 0.09), 25.9, 0.08)
add(squish(), 26.3, 0.15, 0.2)

# ---------------- master ----------------
fade = np.ones(N); fade[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR)) ** 2
mix *= fade[:, None]
mix /= np.abs(mix).max() * 1.05
(HERE / 'out').mkdir(exist_ok=True)
raw = HERE / 'out/audio_raw.wav'
with wave.open(str(raw), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
ln = 'loudnorm=I=-14:TP=-1.5:LRA=11'
r1 = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(raw), '-af', ln + ':print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = json.loads(r1[r1.rindex('{'):r1.rindex('}') + 1])
ln2 = (f"{ln}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
       f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', ln2, '-ar', str(SR), str(HERE / 'out/audio.wav')], check=True)
print('audio ->', HERE / 'out/audio.wav', '(input', m['input_i'], 'LUFS)')
