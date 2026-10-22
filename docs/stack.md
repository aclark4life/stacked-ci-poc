# How the stack is built

Nothing special creates a stacked PR. A stack is any chain of PRs where each
PR's base branch is the previous branch instead of `main`:

```bash
git checkout -b s1 && git push -u origin s1
git checkout -b s2 && git push -u origin s2   # branched off s1
git checkout -b s3 && git push -u origin s3

gh pr create --base main --head s1 ...
gh pr create --base s1   --head s2 ...        # --base is the previous branch, NOT main
gh pr create --base s2   --head s3 ...
```

Rules:

- Branch each level off the previous branch.
- Pass `--base <previous-branch>` explicitly; the default base is `main`,
  which breaks the chain.
- Create PRs bottom-up so GitHub links the chain cleanly.
- For deep stacks, the `gh stack` CLI extension submits a whole branch chain
  in one command.

GitHub infers the stack from the bases: the chain appears in the PR header
(Shift+J/K navigates), a **merge stack** action lands the chain bottom-up,
the stack can pass through the merge queue as one merge group, and GitHub
auto-retargets when a lower PR merges or a base branch is deleted.

## Keeping up with main

Like any PR, a stacked branch goes stale when `main` moves — the difference
is that it **cascades**: rebasing `s1` rewrites `s2`'s base, forcing another
rebase, and so on up the chain. A 14-PR stack means 14 sequential rebases
per `main` change. This cascade, not the rebase itself, is what automation
solves: GitHub's native rebase-stack action, or the bot workflow in
[`rebase-stack.yml`](https://github.com/aclark4life/stacked-ci-poc/blob/main/.github/workflows/rebase-stack.yml).

Conflicts stop the automation and need a human, by design.
