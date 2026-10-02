## Pipeline Architecture

| Job | Purpose | Trigger / condition | needs | Environment | Artifact |
|---|---|---|---|---|---|
| `test` | Install dependencies and run `python -m pytest` | Every `push` and every `pull_request` | none | none | none |
| `build` | Zip `src/` into `build/app.zip` | Same events as `test`, runs only if `test` is green | `test` | none | uploads `build/` |
| `deploy` | Download the package, check the secret, create a GitHub release with the zip attached | Only on `push` to `main` (`if: github.ref == 'refs/heads/main'`), skipped on pull requests | `build` | `production` (required reviewer, deployment branch `main`) | downloads the package from `build` |

## Permissions, Secrets and Variables

| Item | Value |
|---|---|
| Global `permissions` | `contents: read` |
| Extra rights for `deploy` only | `contents: write` (create the release), `actions: read` (get the artifact) |
| Secret | `DEPLOY_TOKEN`, used in `deploy` via `env:`, only its length is logged |
| Variable | `DEPLOY_TARGET` (for example `staging`) |
| Built-in token | `GITHUB_TOKEN`, used by `gh release create` |