# Contributing through Gerrit and Jujutsu

Use jj `>=0.43.0,<0.44.0` over a colocated Git repository. Configure your own
identity; the repository does not provide one.

```sh
git remote add gerrit ssh://USER@REVIEW_HOST:29418/ctrl
git remote add github https://github.com/fatb4f/ctrl.git
jj git init --colocate
jj config set --repo user.name "Your Name"
jj config set --repo user.email "you@example.com"
just jj-init
```

The installed repository configuration defines `trunk()` as `main@gerrit`,
adds Gerrit Change-Id trailers from stable jj change IDs, and treats Gerrit
heads, tags, and remote bookmarks as immutable. `.jj/` is machine-local and
must never be committed.

Create one jj change per reviewable concern. Amend or rebase that same change
to create a new Gerrit patchset; do not create a new jj change merely to answer
review feedback. Upload one linear topic stack with:

```sh
just review TOPIC 'trunk()..@'
```

The command fetches Gerrit, rejects merge/empty/immutable or non-linear stacks,
runs `just check`, exports jj state to Git, and pushes the stack tip to
`refs/for/main%topic=TOPIC`. Gerrit denies direct main pushes. Submission needs
one non-uploader `Code-Review +2`, Zuul `Verified +1`, resolved threads, and a
passing whole-topic speculative gate.
