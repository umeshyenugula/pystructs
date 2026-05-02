# Contributing to pystructs

Thank you for your interest in contributing! This document covers the essentials.

---

## Getting Started

```bash
git clone https://github.com/umeshyenugula/pystructs
cd pystructs
pip install -e ".[dev]"
```

---

## Running Tests

```bash
# No extra dependencies required (unittest only)
python -m unittest discover -s tests -p "test_*.py" -v

# With coverage
pytest tests/ --cov=pystructs --cov-report=term-missing
```

All tests must pass before a pull request is merged. New features must include tests.

---

## Code Standards

- **Python 3.10+** — use `from __future__ import annotations` in every module.
- **Type hints** — every public function and method must have complete type annotations.
- **Docstrings** — every public class and method needs a docstring (Google style).
- **`__slots__`** — add `__slots__` to every class that holds instance state.
- **No external dependencies** — keep the library dependency-free.
- **Line length** — 100 characters max (enforced by `ruff`).

Run the linter before submitting:

```bash
ruff check pystructs/
ruff format pystructs/
```

---

## Adding a New Data Structure

1. Create `pystructs/structures/your_structure.py`.
2. Implement the class with `__slots__`, type hints, and docstrings.
3. Export it from `pystructs/structures/__init__.py`.
4. Export it from `pystructs/__init__.py` (flat public API).
5. Add tests in `tests/test_structures.py`.
6. Document it in `README.md` with a code example.

## Adding a New Algorithm

1. Add the function to the appropriate module in `pystructs/algorithms/`.
2. Decorate it with `@complexity(...)` from `pystructs.core.complexity`.
3. Export it from `pystructs/algorithms/__init__.py` and `pystructs/__init__.py`.
4. Add tests in `tests/test_algorithms.py`.
5. Document it in `README.md`.

---

## Pull Request Checklist

- [ ] All existing tests pass
- [ ] New tests added for the change
- [ ] Type hints complete
- [ ] Docstring added/updated
- [ ] README updated if public API changed
- [ ] `ruff` linter passes

---

## Reporting Issues

Please include:
- Python version (`python --version`)
- pystructs version (`python -c "import pystructs; print(pystructs.__version__)"`)
- Minimal reproducible example
- Expected vs actual behaviour
