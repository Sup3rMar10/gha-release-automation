# gha-release-automation

Push a tag like `v0.1.1` and the pipeline tests, builds an archive and checksums, signs a **build provenance attestation**, publishes a GitHub Release with a changelog, then **downloads what it published and verifies it**.

## Flow

```
git tag vX.Y.Z; git push --tags
   -> test
   -> release: validate tag, build tarball + SHA256SUMS, attest provenance,
               changelog from commits since the previous tag, gh release create
   -> verify:  gh release download, sha256sum -c, gh attestation verify
```

## What ran (2026-10-16)

- **`v0.1.0`:** all three jobs succeeded. The release has `hello-v0.1.0.tar.gz` and `SHA256SUMS`, the checksum check passed, and `gh attestation verify` passed. Its changelog was the first commit only (no previous tag).
- **`v0.1.1`:** also succeeded. Its changelog contained only the one commit made since `v0.1.0` (the README), which shows the previous-tag range works.

## Decisions

- **Tag is validated** against `vMAJOR.MINOR.PATCH` before anything is built; the tag name goes through `env:`, not into the script.
- **Permissions are per job.** Only `release` can write contents and sign; `verify` is read-only.
- **Provenance attestation** records which workflow and commit built the file, so a downloader can check it (`gh attestation verify`).
- **Checksums plus a verify job** that tests the published artifact, not the one in the runner's workspace.
- **`--verify-tag`** refuses to create a release for a tag that does not exist on the remote.
- **Changelog from git history** (`git log prev..tag`); `fetch-depth: 0` is needed so tags and history exist.

## Honest limits

- The "build" is `git archive`, a stand-in for a real build.
- The changelog is raw commit subjects: no conventional-commit grouping, no PR links.
- No signing with a key (cosign or GPG), no SBOM, no protected-tag rules, no manual approval before release.
- Attestations need a public repo or a plan that supports them for private ones.

MIT licensed.
