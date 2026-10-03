# 🚀 Como publicar na VS Code Marketplace

## Uma vez só
1. Crie o publisher **`juninmd`** em <https://marketplace.visualstudio.com/manage> (login Microsoft).
2. Crie um **Personal Access Token** em <https://dev.azure.com> → _User settings → Personal access tokens_
   com escopo **Marketplace → Manage** e organização **All accessible organizations**.
3. No GitHub: _Settings → Secrets → Actions_ → crie `VSCE_PAT` com o token
   (opcional: `OVSX_PAT` para o [Open VSX](https://open-vsx.org), usado por VSCodium/Cursor).

## Publicar
- **Automático:** crie uma tag/release `vX.Y.Z` no GitHub — o workflow `publish.yml` valida, empacota e publica.
- **Manual:**
  ```bash
  npm ci
  npm run validate && npm test
  npx vsce package          # gera patriota-X.Y.Z.vsix (teste com "Install from VSIX...")
  npx vsce publish -p $VSCE_PAT
  ```

## Checklist
- [ ] Versão atualizada em `package.json` e `CHANGELOG.md`
- [ ] `npm run validate` e `npm test` verdes
- [ ] Screenshots atualizados (`npm run screenshots`)
