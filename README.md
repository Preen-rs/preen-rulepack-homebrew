# preen-rulepack-homebrew

Official Homebrew cleanup rulepack for Preen.

## Included rules

- `brew-cache`: clean Homebrew cache directories
- `brew-orphans`: remove orphaned formulas via `brew autoremove`

## Validate

```bash
python3 scripts/validate_pack.py
```

## Bump Version

```bash
python3 scripts/bump_version.py 1.0.3
```

Optional (auto-commit manifest version bump):

```bash
python3 scripts/bump_version.py 1.0.3 --commit
```

## Publish Checklist

Recommended (one-click):
1. Run `Release Rulepack (Manual)` workflow and pass `version` (example: `1.0.6`).
2. Wait for workflow success (it bumps manifest version, signs, commits, tags, and creates release).
3. Verify from Preen CLI:
   - `preen plugin preflight <git-url>@<tag>`
   - `preen plugin test <git-url>@<tag>`
   - `preen plugin install <git-url>@<tag>`

Fallback (manual steps):
1. Bump version (manual or with `scripts/bump_version.py`).
2. Run the `sign-manifest` workflow to generate and commit `manifest.sig` and `manifest.cert`.
3. Commit and tag (`vX.Y.Z`), then push tag.

Note:
- `manifest.sig` and `manifest.cert` must exist in the repo/tag for git-install verification.
- `signing.identity` must match the `sign-manifest` workflow identity.
- The release workflow also publishes additional CI signature artifacts (`manifest.ci.sig`, `manifest.ci.pem`).
- Release fails if tag version does not match `manifest.toml` version.
