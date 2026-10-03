// Tira prints do tema num VS Code real (code-server). Uso: npm run screenshots
// Requer: code-server no PATH (ou CODE_SERVER_BIN) e playwright (NODE_PATH global ok).
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const PORT = 8899;
const THEMES = { dark: 'Patriota', light: 'Patriota Claro' };
const SAMPLE = {
  'src/app.ts': fs.readFileSync(path.join(__dirname, 'sample', 'app.ts'), 'utf-8'),
  'src/main.py': fs.readFileSync(path.join(__dirname, 'sample', 'main.py'), 'utf-8'),
};

function prepare(theme) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'patriota-'));
  const ext = path.join(tmp, 'ext', 'juninmd.patriota-dev');
  fs.mkdirSync(ext, { recursive: true });
  for (const f of ['package.json', 'themes', 'src', 'media']) {
    fs.cpSync(path.join(ROOT, f), path.join(ext, f), { recursive: true });
  }
  for (const [file, content] of Object.entries(SAMPLE)) {
    fs.mkdirSync(path.dirname(path.join(tmp, 'ws', file)), { recursive: true });
    fs.writeFileSync(path.join(tmp, 'ws', file), content);
  }
  fs.mkdirSync(path.join(tmp, 'ud', 'User'), { recursive: true });
  fs.writeFileSync(path.join(tmp, 'ud', 'User', 'settings.json'), JSON.stringify({
    'workbench.colorTheme': theme, 'workbench.startupEditor': 'none', 'update.mode': 'none',
    'telemetry.telemetryLevel': 'off', 'security.workspace.trust.enabled': false,
    'editor.fontSize': 14, 'editor.guides.bracketPairs': 'active', 'typescript.tsserver.enabled': false,
    'workbench.tips.enabled': false, 'window.commandCenter': true,
  }));
  return tmp;
}

async function shoot(theme, name) {
  const tmp = prepare(theme);
  const bin = process.env.CODE_SERVER_BIN || 'code-server';
  const server = spawn(bin, ['--auth', 'none', '--bind-addr', `127.0.0.1:${PORT}`,
    '--user-data-dir', path.join(tmp, 'ud'), '--extensions-dir', path.join(tmp, 'ext')], { stdio: 'ignore' });
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 860 } });
    for (let i = 0; ; i++) {
      try { await page.goto(`http://127.0.0.1:${PORT}/?folder=${encodeURIComponent(path.join(tmp, 'ws'))}`); break; }
      catch (e) { if (i > 30) throw e; await page.waitForTimeout(1000); }
    }
    await page.waitForSelector('.monaco-workbench', { timeout: 90000 });
    await page.waitForTimeout(5000);
    await page.click('text=src');
    await page.click('text=main.py');
    await page.waitForTimeout(1500);
    await page.click('text=app.ts');
    await page.waitForTimeout(2000);
    await page.keyboard.press('F1');
    await page.keyboard.type('Patriota: Chamar o pet');
    await page.waitForTimeout(700);
    await page.keyboard.press('Enter');
    await page.waitForTimeout(3500);
    await page.click('#stage', { force: true }).catch(() => {});
    await page.screenshot({ path: path.join(ROOT, 'images', `${name}.png`) });
  } finally {
    await browser.close();
    server.kill();
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

(async () => {
  fs.mkdirSync(path.join(ROOT, 'images'), { recursive: true });
  for (const [name, theme] of Object.entries(THEMES)) await shoot(theme, name);
  console.log('Prints salvos em images/');
})();
