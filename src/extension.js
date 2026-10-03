const vscode = require('vscode');
const crypto = require('crypto');

const VIEW_ID = 'patriota.petView';

class PetViewProvider {
  constructor(context) {
    this.context = context;
    this.view = undefined;
  }

  resolveWebviewView(view) {
    this.view = view;
    const media = vscode.Uri.joinPath(this.context.extensionUri, 'media');
    view.webview.options = { enableScripts: true, localResourceRoots: [media] };
    view.webview.html = this.html(view.webview, media);
    view.onDidDispose(() => (this.view = undefined));
    view.webview.onDidReceiveMessage((msg) => {
      if (msg.type === 'ready') this.sendConfig();
    });
  }

  sendConfig() {
    const cfg = vscode.workspace.getConfiguration('patriota.pet');
    this.post({ type: 'config', size: cfg.get('size'), speed: cfg.get('speed') });
  }

  post(message) {
    if (this.view) this.view.webview.postMessage(message);
  }

  html(webview, media) {
    const uri = (file) => webview.asWebviewUri(vscode.Uri.joinPath(media, file));
    const nonce = crypto.randomBytes(16).toString('hex');
    const csp = [
      "default-src 'none'",
      `style-src ${webview.cspSource}`,
      `script-src 'nonce-${nonce}'`,
    ].join('; ');
    return `<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8">
<meta http-equiv="Content-Security-Policy" content="${csp}">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="${uri('pet.css')}">
</head><body>
<div id="sky"></div><div id="stage"></div><div id="ground"></div>
<script nonce="${nonce}" src="${uri('flag.js')}"></script>
<script nonce="${nonce}" src="${uri('pet.js')}"></script>
</body></html>`;
  }
}

function activate(context) {
  const provider = new PetViewProvider(context);
  const item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
  item.text = '🇧🇷 Patriota';
  item.tooltip = 'Chamar o pet bandeirinha';
  item.command = 'patriota.pet.show';
  item.show();

  context.subscriptions.push(
    item,
    vscode.window.registerWebviewViewProvider(VIEW_ID, provider, {
      webviewOptions: { retainContextWhenHidden: true },
    }),
    vscode.commands.registerCommand('patriota.pet.show', () =>
      vscode.commands.executeCommand(`${VIEW_ID}.focus`)
    ),
    vscode.commands.registerCommand('patriota.pet.cheer', async () => {
      await vscode.commands.executeCommand(`${VIEW_ID}.focus`);
      provider.post({ type: 'cheer' });
    }),
    vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration('patriota.pet')) provider.sendConfig();
    }),
    vscode.tasks.onDidEndTaskProcess((e) => {
      if (e.exitCode === 0) provider.post({ type: 'cheer' });
    })
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
