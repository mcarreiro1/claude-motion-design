// Render film.html frame by frame with Playwright (Node).
//   node render.js probe 1.5 3.2 6 10     -> probe/sheet.png (stills, 4 columns)
//   node render.js part 5 9               -> re-render seconds 5..9 only, then re-encode
//   node render.js full                   -> out/video.mp4 (360 stop-motion poses at 12/s, encoded 24 fps, 3 parallel pages)
// Stop-motion on twos: every pose is held for 2 frames, so no subframe blending (real stop-motion has no motion blur).
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path');

const HERE = __dirname, URL = 'file://' + path.join(HERE, 'film.html');
const T = 30, SFPS = 12, OUT_FPS = 24, W = 1080, H = 1920;

async function openPage(browser) {
  const pg = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  const errs = [];
  pg.on('pageerror', e => errs.push(String(e)));
  pg.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await pg.goto(URL);
  await pg.waitForFunction('window.ready === true', null, { timeout: 120000 });
  return { pg, errs };
}
async function shot(pg, t, file, type = 'png') {
  await pg.evaluate(t => window.seek(t), t);
  await pg.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
  const el = await pg.$('#stage');
  await el.screenshot({ path: file, type, ...(type === 'jpeg' ? { quality: 95 } : {}) });
}
function clean(dir) { fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true }); }

async function probe(times) {
  const dir = path.join(HERE, 'probe'); clean(dir);
  const b = await chromium.launch(); const { pg, errs } = await openPage(b);
  for (let i = 0; i < times.length; i++) await shot(pg, times[i], path.join(dir, `p_${String(i).padStart(2, '0')}.png`));
  await b.close();
  if (errs.length) console.log('PAGE ERRORS:', errs.slice(0, 8));
  const cols = Math.min(4, times.length), rows = Math.ceil(times.length / cols);
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', path.join(dir, 'p_%02d.png'), '-vf',
    `scale=360:-1,tile=${cols}x${rows}:padding=6:color=white`, '-frames:v', '1', path.join(dir, 'sheet.png')]);
  console.log('probe ->', path.join(dir, 'sheet.png'));
}

async function full(from = 0, to = T * SFPS) { // 'part a b' re-renders poses a..b-1 and keeps the rest
  const dir = path.join(HERE, 'sub'); if (from === 0 && to === T * SFPS) clean(dir);
  const n = to, P = 3;
  const b = await chromium.launch();
  await Promise.all([...Array(P)].map(async (_, k) => {
    const { pg, errs } = await openPage(b);
    for (let i = from + k; i < n; i += P) {
      await shot(pg, i / SFPS, path.join(dir, `f_${String(i).padStart(4, '0')}.jpg`), 'jpeg');
      if (i % 60 === k) console.log(`pose ${i}/${n}`);
    }
    if (errs.length) console.log('PAGE ERRORS:', errs.slice(0, 8));
  }));
  await b.close();
  fs.mkdirSync(path.join(HERE, 'out'), { recursive: true });
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(SFPS), '-i', path.join(dir, 'f_%04d.jpg'),
    '-vf', `fps=${OUT_FPS},scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p`,
    '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-color_range', 'tv', '-colorspace', 'bt709',
    '-color_primaries', 'bt709', '-color_trc', 'bt709', '-t', String(T), path.join(HERE, 'out/video.mp4')]);
  console.log('video ->', path.join(HERE, 'out/video.mp4'));
}

const [cmd, ...args] = process.argv.slice(2);
if (cmd === 'probe') probe(args.map(Number));
else if (cmd === 'full') full();
else if (cmd === 'part') full(Math.round(+args[0] * SFPS), Math.round(+args[1] * SFPS)); // seconds
else console.log('usage: node render.js probe t1 t2 ... | full');
