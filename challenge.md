# Final challenge: debugging the broken pipeline

I put the broken pipeline on a separate branch (`debug-challenge`), read each run, fixed one problem at a time and pushed after each fix. My working pipeline on `main` was not touched.

## Problems and fixes

| # | Symptom / risk | Cause | Fix | Rule that was broken |
|---|---|---|---|---|
| 1 | `test` fails in setup-python: version `3.1` was not found | `python-version: 3.10` has no quotes. YAML reads it as the number 3.1 and the zero is lost | `python-version: "3.10"` | Write version numbers as strings |
| 2 | `test` fails: `No module named pytest` | The test step runs before the install step, so nothing is installed yet | Install dependencies first, then run the tests | Install, then test |
| 3 | `test` fails: `Could not open requirements file ... 'requirement.txt'` | Typo in the file name. The real file is `requirements.txt` | `pip install -r requirements.txt` | Check names and paths |
| 4 | `release` fails: `not a git repository` | The job has no checkout, so `gh` cannot find the repository | `GH_REPO: ${{ github.repository }}` in the step's `env` | Every job starts on an empty machine |
| 5 | `release` would have no package to attach | The job never downloads the artifact from `build` | Add `actions/download-artifact@v4` with the same name as the upload | Pass results between jobs with artifacts |
| 6 | Security risk: the secret is written into the log with `echo` | The secret is inserted directly into the command. Masking only hides the exact value | Pass it via `env:` and log only its length (`${#DEPLOY_TOKEN}`) | Use secrets, never print them |
| 7 | Deployment can run even when tests fail | `build` and `deploy` have no `needs`, and `release` only waits for `build` | Chain: `test` → `build` → `deploy` → `release` | Deploy only after green tests |
| 8 | `build` is green, but the package is empty | No checkout in `build`, so `src/` does not exist and `zipfile` silently packs nothing | Add `actions/checkout@v4` as the first step of `build` | Every job needs its own checkout |
| 9 | The cache is never renewed. Changed dependencies keep old packages | Static key `pip-cache`, and the cache step was in a job that never uses pip | Key `${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}`, in the `test` job before the install step | Use `hashFiles()` in cache keys |
| 10 | Deployment and release run on every push and pull request, with no approval | No `if` condition and no `environment` | `if: github.ref == 'refs/heads/main'` and `environment: production` | Deploy only from `main`, with approval |

## Grouping

The six main problems of the challenge are covered by these rows:

- Python version: row 1
- Order of steps: row 2
- File name: row 3
- Missing checkout and missing `needs`: rows 7 and 8
- Missing condition, environment and printed secret: rows 6 and 10
- Static cache key: row 9

Rows 4 and 5 are extra defects in the `release` job that I found while fixing it.

## Result

All jobs were green on the branch. `deploy` and `release` were skipped there, which is correct, because they only run on `main`. My working `pipeline.yml` on `main` already meets all ten minimum requirements.