// Render an animation spec (from animate.py) to transparent PNG frames.
// Usage: node animate.js out/anim/spec_1080x1920.json  -> out/anim/frames_1080x1920/f0000.png ...
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const specPath = process.argv[2];
  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  const dir = path.join(path.dirname(specPath), `frames_${spec.width}x${spec.height}`);
  fs.rmSync(dir, { recursive: true, force: true });
  fs.mkdirSync(dir, { recursive: true });

  const paths = spec.items.map((it, i) =>
    `<path id="p${i}" d="${it.d}" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" ` +
    `fill="none" stroke="${spec.color}" stroke-width="${it.width.toFixed(1)}" ` +
    `stroke-linejoin="round" stroke-linecap="round" opacity="0"/>`).join('');
  const html = `<html><body style="margin:0;background:transparent">
    <svg xmlns="http://www.w3.org/2000/svg" width="${spec.width}" height="${spec.height}">${paths}</svg></body></html>`;

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: spec.width, height: spec.height } });
  await page.setContent(html);
  const n = Math.ceil(spec.duration * spec.fps);
  for (let f = 0; f < n; f++) {
    const t = f / spec.fps;
    await page.evaluate(({ items, t, draw }) => {
      items.forEach((it, i) => {
        const p = Math.min(1, Math.max(0, (t - it.start) / draw));
        const e = 1 - Math.pow(1 - p, 3); // ease-out
        const el = document.getElementById('p' + i);
        el.setAttribute('opacity', p > 0 ? 1 : 0);
        el.setAttribute('stroke-dashoffset', (1 - e).toFixed(4));
      });
    }, { items: spec.items, t, draw: spec.draw });
    await page.screenshot({ path: path.join(dir, `f${String(f).padStart(4, '0')}.png`), omitBackground: true });
  }
  await browser.close();
  console.log(`${n} frames -> ${dir}`);
})();
