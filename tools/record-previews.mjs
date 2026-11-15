// Видео-превью каждого дизайна для галереи: презентация листается сама, и мы записываем экран (видны переходы и анимации).
//   cd tools && npm install && node record-previews.mjs            # все, у которых ещё нет видео
//   node record-previews.mjs 8 17 40                               # только эти номера (перезаписать)
// Свои PDF превращаются в слайд-шоу из страниц. Нужны Google Chrome, ffmpeg, pdftoppm (poppler), Python 3.
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const MEDIA = path.join(ROOT, 'gallery', 'media');
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = Number(process.env.PORT || 4790);
const STEP = 1700;      // мс на шаг (слайд или появление элемента)
const SECONDS = 13;     // длина превью

const designs = JSON.parse(fs.readFileSync(path.join(ROOT, 'catalog', 'designs.json'), 'utf8'));
const only = process.argv.slice(2).filter((a) => /^\d+$/.test(a)).map(Number);
fs.mkdirSync(MEDIA, { recursive: true });

const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.gif': 'image/gif' };
const server = http.createServer((req, res) => {
  let f = path.join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!f.startsWith(ROOT)) { res.writeHead(403).end(); return; }
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
  if (!fs.existsSync(f)) { res.writeHead(404).end(); return; }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f).toLowerCase()] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
}).listen(PORT);

function finish(raw, n, ss = 2.4) { // любое видео → 960×540 mp4 + обложка
  const mp4 = path.join(MEDIA, `${n}.mp4`);
  execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', raw, '-t', String(SECONDS), '-vf', 'scale=960:540:force_original_aspect_ratio=decrease,pad=960:540:(ow-iw)/2:(oh-ih)/2:color=0x0b0b0c,fps=30',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '30', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', mp4]);
  execFileSync('ffmpeg', ['-y', '-v', 'error', '-ss', String(ss), '-i', mp4, '-frames:v', '1', '-vf', 'scale=640:360', '-q:v', '4', path.join(MEDIA, `${n}.jpg`)]);
}

function pdfShow(d) { // свои PDF: страницы → слайд-шоу с плавной сменой
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'pdf-'));
  execFileSync('pdftoppm', ['-r', '60', '-l', '7', '-png', path.join(ROOT, d.path), path.join(tmp, 'p')]);
  const pages = fs.readdirSync(tmp).filter((f) => f.endsWith('.png')).sort().slice(0, 7);
  const per = 1.9, fade = 0.5;
  const args = ['-y', '-v', 'error'];
  pages.forEach((p) => args.push('-loop', '1', '-t', String(per + fade), '-i', path.join(tmp, p)));
  let fc = pages.map((_, i) => `[${i}]scale=960:540:force_original_aspect_ratio=decrease,pad=960:540:(ow-iw)/2:(oh-ih)/2:color=0x0b0b0c,setsar=1,fps=30[v${i}]`).join(';');
  let last = 'v0';
  for (let i = 1; i < pages.length; i++) { fc += `;[${last}][v${i}]xfade=transition=${['smoothleft', 'fade', 'circleopen', 'slideup'][i % 4]}:duration=${fade}:offset=${(per * i).toFixed(2)}[x${i}]`; last = `x${i}`; }
  const raw = path.join(tmp, 'raw.mp4');
  execFileSync('ffmpeg', [...args, '-filter_complex', fc, '-map', `[${last}]`, '-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', raw]);
  finish(raw, d.n, 0.8);
}

function target(d) {
  if (d.kind === 'tokens') {
    execFileSync('python3', [path.join(ROOT, 'scripts', 'build_deck.py'), '--demo', String(d.n)]);
    return `http://localhost:${PORT}/gallery/live/${d.n}/index.html`;
  }
  if (d.engine === 'reveal') return `http://localhost:${PORT}/${d.path}`;
  return `http://localhost:${PORT}/${d.path}`;
}

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, protocolTimeout: 120000, args: ['--hide-scrollbars', '--mute-audio'] });
let done = 0; const failed = [];
for (const d of designs) {
  if (only.length ? !only.includes(d.n) : fs.existsSync(path.join(MEDIA, `${d.n}.mp4`))) continue;
  try {
    if (d.path && d.path.endsWith('.pdf')) { pdfShow(d); done++; console.log(`✓ ${d.n} ${d.name}`); continue; }
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 720 });
    await page.goto(target(d), { waitUntil: 'networkidle2', timeout: 45000 }).catch(() => {});
    await new Promise((r) => setTimeout(r, 1500));
    const raw = path.join(os.tmpdir(), `deck-${d.n}.webm`);
    const rec = await page.screencast({ path: raw });
    await new Promise((r) => setTimeout(r, 300));
    // листание запускаем только после старта записи, чтобы видео начиналось с обложки
    await page.evaluate((ms) => {
      if (window.deckAuto) window.deckAuto(ms);
      else if (window.Reveal) Reveal.configure({ autoSlide: ms, controls: false, progress: false, fragments: false });
      else if (window.impress) setInterval(() => impress().next(), ms + 300);
    }, STEP);
    await new Promise((r) => setTimeout(r, SECONDS * 1000 + 500));
    await rec.stop();
    await new Promise((r) => setTimeout(r, 1500)); // дать ffmpeg дописать файл
    await page.close();
    finish(raw, d.n);
    done++; console.log(`✓ ${d.n} ${d.name}`);
  } catch (e) { failed.push(`${d.n} ${d.name}: ${e.message.split('\n')[0]}`); }
}
await browser.close(); server.close();
console.log('готово:', done);
if (failed.length) console.log('не получилось:\n  ' + failed.join('\n  '));
console.log('дальше: python3 scripts/build_gallery.py');
