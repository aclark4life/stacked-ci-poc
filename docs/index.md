# stacked-ci-poc

Proof of concept: GitHub native **stacked pull requests** plus a CI workflow
that runs correctly for every PR in a stack.

```{toctree}
:maxdepth: 2
stack
ci
choices
```

The repo holds a 3-PR stack (`s1 -> main`, `s2 -> s1`, `s3 -> s2`) and one
tiered workflow that validates each PR independently.
