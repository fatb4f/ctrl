# Gerrit project controls

Apply `project.config` to `refs/meta/config` only after the historical import
and staging restore drill. `Service Users` contains only Zuul's Gerrit account;
the uploader cannot satisfy the non-uploader `Code-Review +2` predicate.

`replication.config` belongs in Gerrit's site configuration. Substitute the
GitHub SSH URL from the external secret environment. Its positive refspecs are
an allowlist: patch sets, NoteDb, and other metadata refs are not mirrored.
GitHub branch protection must allow writes only from the replication identity.
