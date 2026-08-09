# Qualification Runtime Monorepo, Jujutsu, Gerrit, and Zuul

## Summary

- Create public `fatb4f/ctrl` from `kernel-spec`, `ppf`, `runtime`, `tdd-seed`, and `sdk-feedback`, preserving all reachable Git history.
- Keep CUEstrap external to the qualification product boundary. Import neither its code nor its history; any use remains a design or implementation dependency, never a normative authority source.
- Make Gerrit 3.14.2 the canonical review repository, GitHub the submitted-code mirror and canonical issue tracker, and jj 0.43.x the primary local interface over colocated Git.
- Gate submission through Zuul 14.2.0, one non-uploader `Code-Review +2`, and automated `Verified +1`.
- Use MIT for all first-party monorepo content, retaining third-party notices and migration attribution.

## 1. Repository migration and target structure

1. Create the empty Gerrit project `ctrl` and GitHub repository `fatb4f/ctrl` from the local `~/src/uvt` template. Do not accept development changes until the historical import is complete.
2. Freeze all five source repositories atomically:
   - Land the untracked PPF documentation before freezing.
   - Fast-forward the local `tdd-seed` checkout to its remote.
   - Resolve `fatb4f/runtime` as the canonical remote despite the local checkout lacking one.
   - Require clean worktrees, no open PRs, and passing native validation.
   - Tag each source tip `monorepo-freeze/<cutover-date>`.
3. Record a machine-readable migration manifest containing source URLs, terminal commits, tree IDs, all branch and tag tips, licenses, validation results, and destination paths.
4. Import each bare mirror with pinned `git-filter-repo`, rewriting paths as follows:

   ```text
   fatb4f/kernel-spec  → spec/
   fatb4f/ppf          → packages/ppf/
   fatb4f/runtime      → packages/runtime/
   fatb4f/tdd-seed     → agents/tdd/
   fatb4f/sdk-feedback → integrations/openai/
   ```

5. Preserve authors, timestamps, messages, tags, and every reachable branch. Namespace source tags and non-main branch tips under `migration/<source>/...`; record original-to-rewritten commit maps because path prefixing necessarily changes commit hashes.
6. Merge the five rewritten default branches into one import branch using explicit unrelated-history merge commits. These migration merges are the only exception to the future linear-history rule.
7. Refactor the imported tree into:

   ```text
   ctrl/
   ├── spec/
   ├── packages/
   │   ├── ppf/
   │   └── runtime/
   ├── agents/tdd/
   ├── integrations/openai/
   ├── evals/
   ├── fixtures/
   ├── docs/
   ├── ops/{gerrit,zuul}/
   ├── tools/
   ├── zuul.d/
   ├── cue.mod/
   ├── pyproject.toml
   ├── uv.lock
   ├── justfile
   ├── AGENTS.md
   └── LICENSE
   ```

8. Redistribute `sdk-feedback` by function:
   - Move its accepted ADR into `docs/adr/`.
   - Move App Server boundary material into integration documentation.
   - Keep accepted landscape surveys under `docs/research/` and retain exploratory integration material under `integrations/openai/research/`.
   - Retire its empty Python distribution and duplicated packaging scaffolding.
9. Move reusable TDD evaluation assets to root `evals/tdd/` and shared fixtures to `fixtures/tdd/`; retain specialization-private test fixtures within `agents/tdd/`.
10. Add a root MIT license. Preserve existing MIT notices, dependency licenses, and source-repository attribution in the migration manifest.

## 2. Workspace and interface consolidation

- Create one non-package root uv workspace for the three publishable Python projects. Retain separate build metadata and independent versions but replace separate lockfiles with one committed root `uv.lock`.
- Standardize on Python `>=3.14,<3.15` and root commands: `just sync`, `just check`, `just qualify`, `just build`, and package-specific variants.
- Preserve import roots `ppf`, `runtime_promptgen`, and `tdd_agent_skills`.
- Preserve `ppf-validate`, `ppf-assess`, `ppf-qualify`, `python-ppf`, and `promptgen`.
- Assign `python-ppf` exclusively to `packages/ppf`; remove the duplicate TDD entry point.
- Preserve PPF’s existing `python-ppf workflow plan` behavior. Expose TDD’s Markdown compiler as:

  ```text
  python-ppf workflow compile PLAN \
    --fixtures FIXTURES \
    --probes PROBES \
    --realizations REALIZATIONS \
    [--output OUTPUT | --check SNAPSHOT]
  ```

- Have PPF compose the TDD library directly; TDD exposes services and models but does not own a second control-plane executable.
- Establish one root CUE module: `github.com/fatb4f/ctrl`, language version CUE v0.18.0. Rewrite kernel and TDD imports to the new module paths.
- Upgrade TDD contracts from CUE v0.14 to v0.18 and qualify all positive and negative fixtures.
- Replace kernel-spec’s CUEstrap authority references with pinned upstream CUE semantics and local monorepo contracts. CI obtains the official CUE v0.18.0 binary by verified checksum.
- Use independent post-cutover versions and path-scoped tags:
  - `kernel-spec/v0.2.0`
  - `ppf/v0.4.0`
  - `runtime-promptgen/v0.1.1`
  - `tdd-agent-skills/v0.2.0`

## 3. Jujutsu and Gerrit contributor workflow

- Initialize every developer checkout as colocated Git/jj with `jj git init --colocate`.
- Never commit `.jj/`. Commit a reviewed jj configuration template under `tools/vcs/`; `just jj-init` validates and installs it into jj’s machine-local repository configuration.
- Support `jj >=0.43.0,<0.44.0` and use exactly 0.43.0 in CI initially.
- Configure the canonical remote as `gerrit`, the mirror remote as `github`, `trunk()` as `main@gerrit`, automatic Gerrit trailers using `format_gerrit_change_id_trailer(self)`, and immutable heads from Gerrit main, tags, and remote bookmarks.
- Require users to configure their own name and email; bootstrap fails on an empty identity.
- Add `just review TOPIC [REVSET]` to fetch Gerrit, validate a linear stack, run focused checks, export jj state, and push the stack tip to `refs/for/main%topic=TOPIC`.
- Use jj change IDs as stable Gerrit `Change-Id` trailers. Amending or rebasing a jj change creates a new Gerrit patchset, not a new review.
- Deny direct pushes to `refs/heads/main`; retain plain Git for transport, CI, release tooling, and external consumers.
- Configure Gerrit with `REBASE_ALWAYS`, one non-uploader `Code-Review +2`, Zuul `Verified +1`, no blocking negative vote, no unresolved review threads, and whole-topic submission only when every change in the topic passes.

## 4. Gerrit, Zuul, GitHub, and cutover operations

- Deploy a pinned single-host container topology containing Gerrit 3.14.2, Zuul 14.2.0, scheduler/executor/merger/web services, Nodepool with an isolated static worker, ZooKeeper, MariaDB, `oauth2-proxy` using GitHub OAuth, and a TLS reverse proxy.
- Pin every container and Gerrit plugin by immutable digest. Keep OAuth credentials, SSH keys, replication credentials, database passwords, and backup keys outside the repository.
- Run build jobs under an unprivileged worker identity with ephemeral workspaces, no container-engine socket, no production secrets, and explicit resource/time/network limits.
- Configure Zuul pipelines:
  - `check`: lint, formatting, CUE validation, and package tests on every patchset; vote `Verified`.
  - `gate`: speculatively test the approved change stack with the full locked qualification suite and submit only on success.
  - `periodic`: run full clean-room qualification and backup/restore probes against submitted `main`.
  - `release`: build independently versioned artifacts from submitted tags only.
- Initially run all package jobs in parallel for every change. Add path-based optimization only after dependency-direction tests prove it safe.
- Configure Gerrit replication to mirror only submitted `main` and release tags to GitHub. Exclude `refs/changes/*`, `refs/meta/*`, and unpublished patchsets.
- Protect GitHub `main` against direct writes except the replication identity. Keep GitHub Issues writable; direct contributors to Gerrit for code review and close GitHub PRs with a Gerrit redirect.
- Migrate the two open PPF issues and seven open runtime issues into the new GitHub tracker, preserving bodies, comments with attribution, hierarchy, and original links. Export closed issues into the migration archive.
- Move qualification-domain concepts out of CUEstrap:
  - Create monorepo successors for active issues #3, #7, #8, #12, and #22.
  - Split #4 so domain execution architecture moves while CUE-only harness experiments remain in CUEstrap.
  - Keep #5 and #9 in CUEstrap.
  - Archive and cross-link completed domain issues #10, #13, #18, and #19.
- After the release candidate passes: back up Gerrit and Zuul, seed Gerrit `main`, verify GitHub replication, enable ACLs and Zuul gates, switch contributor documentation/remotes, close source issues with successor links, and archive the five source repositories.
- Keep CUEstrap active as a laboratory.
- Before source archival, rollback consists of disabling Gerrit writes, restoring frozen source repositories as canonical, and leaving the monorepo candidate unpublished.
- Take encrypted nightly and pre-upgrade backups of Gerrit repositories, NoteDb, configuration, Zuul SQL state, and ZooKeeper state. Retain 30 daily and 12 monthly snapshots and perform quarterly restore drills.

## Validation and acceptance gates

- `git fsck --full` passes for every source mirror, rewritten history, and the final monorepo.
- `just migration-verify` proves source refs, commit maps, terminal subtree trees, tags, and issue mappings.
- `uv sync --locked --all-packages --all-groups` succeeds from a clean environment.
- `just check` passes root policy, formatting, lint, typing, package tests, and generated-artifact checks.
- `just qualify` passes clean locked builds, installed-wheel tests, CUE contracts, evaluations, and integration fixtures.
- `cue vet ./...` passes authoritative CUE packages; declared negative fixtures fail for expected reasons.
- Installed CLI smoke tests prove exactly one `python-ppf` entry point and working `workflow plan` and `workflow compile` commands.
- `just jj-smoke` proves stable Gerrit Change-Ids across amend/rebase and rejects invalid review stacks.
- Gerrit staging tests prove direct main pushes are denied, uploader self-approval is insufficient, Zuul voting is required, unresolved threads block, and accepted changes submit with rebase-always semantics.
- Gerrit stack tests prove dependent jj changes receive distinct stable reviews and gate speculatively in order.
- GitHub replication tests prove submitted commits and release tags match Gerrit while patchset and metadata refs remain absent.
- A backup restoration drill passes before production cutover.

## Assumptions

- Gerrit is the canonical source and review authority; GitHub is authoritative only for issues and the submitted-code mirror.
- The operator supplies the review hostname, TLS/DNS control, OAuth application, GitHub replication identity, and encrypted off-host backup target.
- Commit hashes may change during path rewriting; preserved history is demonstrated through complete commit maps and tree equivalence.
- No CUEstrap contract, issue, implementation, or package is a normative authority source; any adopted implementation dependency remains external to the qualification product boundary.
- Generated, cache, runtime, credential, and machine-local files are excluded from migration unless already intentional tracked artifacts.
