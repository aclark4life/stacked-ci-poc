# stacked-ci-poc

Proof of concept: GitHub native **stacked pull requests** plus a CI workflow
that runs correctly for every PR in a stack.

The repo holds a 3-PR stack (`s1 -> main`, `s2 -> s1`, `s3 -> s2`) and one
workflow, [`.github/workflows/ci.yml`](.github/workflows/ci.yml), that
validates each PR independently.

## How the stack is built

Nothing special creates a stacked PR. A stack is any chain of PRs where each
PR's base branch is the previous branch instead of `main`:

```bash
git checkout -b s1 && git push -u origin s1
git checkout -b s2 && git push -u origin s2   # branched off s1, so it contains s1's commits
git checkout -b s3 && git push -u origin s3

gh pr create --base main --head s1 ...
gh pr create --base s1   --head s2 ...        # --base is the previous branch, NOT main
gh pr create --base s2   --head s3 ...
```

- Branch each level off the previous branch.
- Pass `--base <previous-branch>` explicitly; the default base is `main`,
  which breaks the chain.
- Create PRs bottom-up so GitHub links the chain cleanly.
- For deep stacks, the `gh stack` CLI extension can submit a whole branch
  chain in one command.

GitHub infers the stack from the bases and shows the chain in the PR header
(Shift+J/K to navigate), offers a **merge stack** action, auto-retargets the
stack when a lower PR merges or a base branch is deleted, and can land the
whole stack through the merge queue as one merge group.

## What the workflow demonstrates

1. **Trigger with no branch filter.** `on: pull_request` has no `branches:`
   filter. Stacked PRs target non-default branches, so any filter would
   silently skip them.
2. **Test the PR head, not the merge ref.** Actions checks out a merge commit
   of head into base by default. For a stacked PR whose base is itself
   unmerged, that tree was never reviewed. The workflow checks out the PR
   head commit instead:

   ```yaml
   env:
     HEAD_SHA: ${{ github.event.pull_request.head.sha || github.sha }}
   steps:
     - uses: actions/checkout@v4
       with:
         ref: ${{ env.HEAD_SHA }}
   ```

   Note: the `||` fallback must live in a job-level `env` — GitHub rejects
   `ref: ${{ github.event.pull_request.head.sha || github.sha }}` directly in
   `with:` (the workflow fails to parse, with no logs).
3. **Per-PR isolation.** A push to one PR's branch runs only that PR's CI.
   Other PRs keep their previous results — which means they can go stale
   when a lower PR in the stack changes. Native stacking mitigates this by
   rebasing the downstream PRs (preserving approvals) and re-running their
   checks.
4. **Only one workflow file.** It lives on `main` (push trigger) and on each
   PR branch (pull_request trigger takes the workflow file from the PR).
## Results observed

- Each PR got its own CI run; all three green.
- Merging (e.g. the merge-stack button) lands the chain bottom-up, one merge
  commit per PR.
