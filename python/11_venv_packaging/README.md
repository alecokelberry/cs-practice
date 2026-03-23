# Lesson 11 — Virtual Environments & Packaging

## Overview

Python projects need isolated environments to avoid dependency conflicts between projects. A **virtual environment** is a self-contained directory with its own Python interpreter and installed packages — completely separate from your system Python.

---

## Virtual Environments with `venv`

### Create and Activate

```bash
# Create a venv in your project directory (convention: name it .venv)
python3 -m venv .venv

# Activate — macOS/Linux
source .venv/bin/activate

# Activate — Windows
.venv\Scripts\activate

# Deactivate (returns to system Python)
deactivate
```

Once activated, `python` and `pip` point to the venv's copies:

```bash
which python     # → .../your-project/.venv/bin/python
pip list         # shows only packages installed in this venv
```

### Always gitignore your venv

```
.venv/
__pycache__/
*.pyc
*.pyo
```

---

## Managing Packages with `pip`

```bash
pip install requests                   # latest version
pip install requests==2.31.0           # exact version
pip install "requests>=2.28,<3.0"      # version range
pip uninstall requests
pip list                               # all installed packages
pip show requests                      # info about one package
pip install --upgrade requests         # upgrade to latest
```

### `requirements.txt` — Traditional Dependency Pinning

```bash
# Save exact versions of everything installed in the current venv
pip freeze > requirements.txt

# Re-create the environment elsewhere
pip install -r requirements.txt
```

`requirements.txt` is flat and pinned — good for deployed apps where reproducibility matters.

---

## Modern Packaging with `pyproject.toml`

`pyproject.toml` is the modern standard (PEP 517/518) for Python projects. It replaces the old `setup.py` and `setup.cfg`.

### Minimal `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "my-package"
version = "0.1.0"
description = "A short description"
requires-python = ">=3.12"
dependencies = [
    "requests>=2.28",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "mypy>=1.8",
]
```

### Install in Editable Mode

```bash
pip install -e .          # install this project as a package (editable/dev mode)
pip install -e ".[dev]"   # also install dev extras
```

Editable mode means changes to your source files take effect immediately — no reinstall needed.

---

## Recommended Project Structure

```
my-project/
├── .venv/                   ← venv (gitignored)
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── module.py
├── tests/
│   └── test_module.py
├── pyproject.toml
├── requirements.txt         ← optional, for app deployment
└── README.md
```

The `src/` layout prevents accidentally importing your package from the project root instead of the installed copy.

---

## pip vs pipx

| Tool | Use case |
|------|----------|
| `pip` | Install libraries into a project's venv |
| `pipx` | Install CLI tools globally in isolated envs (e.g., `black`, `ruff`, `httpie`) |

```bash
pipx install ruff     # installs ruff globally, isolated from all projects
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Installing packages globally | Always activate a venv first |
| Committing `.venv/` | Add to `.gitignore` |
| Using `pip freeze` for a library | It pins transitive deps too — use `pyproject.toml` `dependencies` for libraries instead |
| `python` vs `python3` | In a venv, `python` always refers to the venv's Python. Outside, it may be Python 2 on some systems |
| Missing `__init__.py` | Without it, Python won't recognize the folder as a package |
| Re-running `pip install` without activating | Installs to system Python or the wrong env |

---

## Quick Reference Card

```bash
# Create and activate
python3 -m venv .venv
source .venv/bin/activate       # macOS/Linux
.venv\Scripts\activate          # Windows

# Install
pip install package
pip install -r requirements.txt
pip install -e ".[dev]"         # editable + dev extras

# Inspect
pip list
pip show package
pip freeze > requirements.txt

# Deactivate
deactivate
```

```toml
# pyproject.toml skeleton
[project]
name = "my-package"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["requests>=2.28"]

[project.optional-dependencies]
dev = ["pytest>=8.0", "mypy>=1.8"]
```
