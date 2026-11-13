# The Lion of Mars

A majestic lion silhouette stands on a red Martian sand dune, its long
mane streaming in the wind like flames. Deep red-orange dunes and
swirling dust fill the landscape, while a small blue Earth hangs in the
dark sky above — the king of beasts, far from home, still unbowed.

The image reads at a glance: one dark hero against a burning red
world, with the tiny blue Earth as the quiet punchline.

## Files

- `entry.png` — the artwork (1024×683 JPEG, uncropped; the full scene
  is preserved, nothing cut off at the edges)
- `main.py` — copies `entry.png` to the output directory and verifies
  it (size, SHA-256, JPEG magic bytes, and dimensions) byte-for-byte
- `LICENSE` — MIT

## How it runs

```sh
python3 main.py
```

The output directory is `$MAKEFUN_OUTPUT_DIR` when set, otherwise
`/output` (the grader's Docker container does not set the variable,
so the `/output` fallback is what the grading run uses).
