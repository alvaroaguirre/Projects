// Convert every SVG in out/ (poster + cards) to PNG with the pre-installed Playwright Chromium.
// Usage: node to_png.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const out = path.join(__dirname, 'out');
  const files = [path.join(out, 'poster.svg')].concat(
    fs.readdirSync(path.join(out, 'cards')).filter(f => f.endsWith('.svg')).map(f => path.join(out, 'cards', f))
  );
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const f of files) {
    const svg = fs.readFileSync(f, 'utf8');
    const [, w, h] = svg.match(/width="(\d+)" height="(\d+)"/);
    await page.setViewportSize({ width: +w, height: +h });
    await page.setContent(`<body style="margin:0">${svg}</body>`);
    await page.screenshot({ path: f.replace(/\.svg$/, '.png') });
  }
  await browser.close();
  console.log(`${files.length} PNGs written`);
})();
