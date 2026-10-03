# 🚀 Publicação automática (semantic-release)

Cada push na `master` roda `.github/workflows/release.yml`: valida, testa e executa o
**semantic-release**, que lê os commits ([Conventional Commits](https://www.conventionalcommits.org/pt-br/)),
decide a versão, atualiza `package.json` e `CHANGELOG.md`, cria a tag e a GitHub Release com o `.vsix`
e publica nas lojas.

| Commit | Efeito |
|---|---|
| `fix: ...` | patch (0.0.X) |
| `feat: ...` | minor (0.X.0) |
| `feat!: ...` ou `BREAKING CHANGE:` no corpo | major (X.0.0) |
| `docs:`, `chore:`, `test:`... | sem release |

> Com squash merge, o **título do PR** vira o commit — use o formato acima.
> A primeira release (sem tags anteriores) sai como `v1.0.0`.

## Configuração (uma vez só)
1. Crie o publisher **`juninmd`** em <https://marketplace.visualstudio.com/manage>.
2. Crie um **Personal Access Token** em <https://dev.azure.com> (_User settings → Personal access tokens_),
   escopo **Marketplace → Manage**, organização **All accessible organizations**.
3. No GitHub (_Settings → Secrets and variables → Actions_) crie:
   - `VSCE_PAT` — token da VS Code Marketplace;
   - `OVSX_PAT` _(opcional)_ — token do [Open VSX](https://open-vsx.org) (VSCodium, Cursor...).
4. Se a `master` tiver branch protection, permita que `github-actions[bot]` faça push (o commit `chore(release)`).

Sem os tokens a release no GitHub sai normalmente e a publicação nas lojas é pulada.

## Manual (emergência)
```bash
npm ci && npm run validate && npm test
npx vsce package          # teste com "Install from VSIX..."
npx vsce publish -p $VSCE_PAT
```
