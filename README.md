# QRCode Bundler

A Python bundler that consolidates the entire [python-qrcode](https://github.com/lincolnloop/python-qrcode) library into a single file.

---

Even Claude wrote this README, I hinted at some data structures and non-obvious solutions, but they managed to go through this for 90% of the work, tbh was quite enjoyable <3

---

## Why?

Sometimes you just want one file. No pip install, no dependencies to manage - just drop `qrcode.py` into your project and go.

## What it does

The bundler:
- Parses all python-qrcode modules into ASTs
- Builds a dependency graph (with proper DFS ordering)
- Removes TYPE_CHECKING blocks to avoid circular dependencies
- Creates namespace objects so `base.rs_blocks()` still works
- Consolidates everything into one ~2400 line file
- Preserves both library and CLI functionality

## Usage

### Generate the bundle

```bash
make generate
```

This creates `qrcode.py` - a standalone file with the full python-qrcode library.

### Test it

```bash
make test
```

Runs golden master tests for both library and CLI usage.

### Use it

As a library:
```python
import qrcode

qr = qrcode.QRCode()
qr.add_data('Hello World')
qr.make()
print(qr.modules)
```

As a CLI:
```bash
echo "Hello World" | python qrcode.py
# Or:
python qrcode.py "Hello World"
```

## How it was built

Vibe coded with Claude - started with "let's bundle this library" and iterated through:
- Import resolution and dependency ordering (the DFS took a few tries!)
- Namespace collision handling (turns out `base` is used in multiple modules)
- TYPE_CHECKING removal (circular deps were sneaky)
- Deterministic output (sets are not your friend for reproducibility)
- Proper licensing (BSD + MIT, all accounted for)

The whole conversation was basically: "hmm, this breaks" → "ah right, because..." → "fixed!" on repeat until everything clicked.

## License

- **Bundler tool** (bundler.py, test_qrcode.py, etc.): MIT License - Copyright (c) 2025 c4ffein
- **Generated qrcode.py**: BSD 3-Clause License (from python-qrcode)

See [LICENSE](LICENSE) for full details.

## Files

- `bundler.py` - The bundler itself
- `qrcode.py` - Generated single-file library (commit this!)
- `test_qrcode.py` - Golden master tests
- `golden_masters/` - Test fixtures for lib and CLI
- `.github/workflows/test.yml` - CI to ensure qrcode.py stays up-to-date

## CI

GitHub Actions runs:
1. Golden master tests (verify functionality)
2. Regeneration check (verify committed qrcode.py is current)

If you modify the bundler or update the python-qrcode submodule, remember to regenerate!

---

*Built with curiosity and a bit of AST wrangling* ✨
