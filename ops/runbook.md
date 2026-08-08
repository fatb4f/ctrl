# Review service runbook

## Preconditions

Do not deploy from mutable tags. Populate `images.lock.json` with registry
references of the form `image@sha256:<64 hex>`, add every Gerrit plugin with an
immutable digest, set `cutoverReady`, and run:

```sh
python tools/ops/validate_deploy.py --require-ready ops/images.lock.json
python tools/migration.py verify --require-cutover-ready ops/migration/manifest.json
```

The operator supplies DNS, TLS, GitHub OAuth, Gerrit/Zuul SSH keys, replication
credentials, database passwords, backup encryption keys, and the off-host
backup target. None belongs in Git. The static worker has no production secret,
outbound production route, privileged identity, or container-engine socket.

## Cutover

1. Disable source-repository writes and confirm every freeze tag and native
   validation recorded in the migration ledger.
2. Back up Gerrit repositories, NoteDb/configuration, Zuul SQL, and ZooKeeper.
3. Restore that backup into staging and run the staging test matrix.
4. Seed Gerrit `main`; compare the imported tree, refs, and commit maps.
5. Enable replication and prove that only submitted `main` and release tags
   appear on GitHub.
6. Enable ACLs and Zuul, then run uploader/non-uploader, thread, stack, and
   rebase-always submission tests.
7. Switch contributor remotes and documentation. Migrate and cross-link issues.
8. Archive source repositories only after the release candidate qualifies.

Before archival, rollback disables Gerrit writes, restores the frozen source
repositories as canonical, and leaves the candidate unpublished.

## Backups and restoration

Take encrypted backups nightly and immediately before upgrades. Include Gerrit
Git repositories, NoteDb and site configuration, Zuul SQL, and ZooKeeper state.
Retain 30 daily and 12 monthly snapshots off-host. Quarterly, restore a complete
snapshot to isolated staging, validate checksums, start every service, clone
Gerrit, replay one gated change, and verify GitHub replication exclusions.
Record the restoration timestamp, snapshot identifiers, operator, elapsed time,
and probe results in the external operations log.

## Required staging assertions

- direct pushes to `refs/heads/main` are denied;
- uploader self-approval cannot submit;
- `Verified +1` and resolved threads are mandatory;
- accepted changes use rebase-always and whole-topic submission;
- dependent jj changes keep distinct Change-Ids and gate in order;
- GitHub has submitted commits/tags and no patchset or metadata refs;
- backup restoration completes before production cutover.
