# preen-rulepack-homebrew

Official Homebrew cleanup rulepack for Preen.

## Included rules

- `brew-cache`: clean Homebrew cache directories
- `brew-orphans`: remove orphaned formulas via `brew autoremove`

## Validate

```bash
python3 scripts/validate_pack.py
```

## Publish Checklist

1. bump `version` in `manifest.toml`
2. Run the `sign-manifest` workflow to generate and commit `manifest.sig` and `manifest.cert` with keyless Sigstore.
3. commit and tag (`vX.Y.Z`)
4. push tag
5. Verify from Preen CLI:
   - `preen plugin preflight <git-url>@<tag>`
   - `preen plugin test <git-url>@<tag>`
   - `preen plugin install <git-url>@<tag>`

Note:
- `manifest.sig` and `manifest.cert` must exist in the repo/tag for git-install verification.
- `signing.identity` must match the `sign-manifest` workflow identity.
- The release workflow also publishes additional CI signature artifacts (`manifest.ci.sig`, `manifest.ci.pem`).
