# preen-rulepack-homebrew

Official Homebrew cleanup rulepack for Preen.

## Workflows

- `Validate Rulepack (PR/Main)`: validates rulepack files on PRs and `main`.
- `Release Rulepack`: one-click release flow (version bump + signing + tag + release).

## Included rules

- `brew-cache`: clean Homebrew cache directories
- `brew-orphans`: remove orphaned formulas via `brew autoremove`

## Validate

```bash
python3 scripts/validate_pack.py
```

## Release (Recommended)

1. Run `Release Rulepack` and set `version` to `x.x.x`.
2. Wait for a green run.
3. Verify from Preen CLI:
   - `preen plugin preflight <git-url>@<tag>`
   - `preen plugin test <git-url>@<tag>`
   - `preen plugin install <git-url>@<tag>`

Note:
- `manifest.sig` and `manifest.cert` must exist in the repo/tag for git-install verification.
- `signing.identity` must match `release-manual.yml` identity.
- The release workflow also publishes additional CI signature artifacts (`manifest.ci.sig`, `manifest.ci.pem`).
- Release fails if tag version does not match `manifest.toml` version.
