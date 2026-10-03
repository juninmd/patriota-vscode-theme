// Gera media/icon.png (128x128) a partir da bandeira. Uso: node scripts/make_icon.js
const { chromium } = require('playwright');
const path = require('path');

const html = `<body style="margin:0;background:#002776;width:256px;height:256px;display:grid;place-items:center">
<svg width="216" viewBox="0 0 720 504"><rect width="720" height="504" rx="36" fill="#009c3b"/>
<polygon points="61,252 360,61 659,252 360,443" fill="#ffdf00"/>
<clipPath id="c"><circle cx="360" cy="252" r="126"/></clipPath><circle cx="360" cy="252" r="126" fill="#002776"/>
<path d="M 236 292 Q 360 250 484 206" fill="none" stroke="#fff" stroke-width="30" clip-path="url(#c)"/></svg></body>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 256, height: 256 }, deviceScaleFactor: 1 });
  await page.setContent(html);
  await page.screenshot({ path: path.join(__dirname, '..', 'media', 'icon.png'), omitBackground: false });
  await browser.close();
})();
