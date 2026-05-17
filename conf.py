# Configuration file for Sphinx documentation builder

import os
import sys
import shutil
import subprocess

# -------------------------------------------------
# Add package root (AnalyticsTools) to sys.path
# -------------------------------------------------

DOCS_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(DOCS_DIR, ".."))

# Add repo root so "AnalyticsTools" can be imported
sys.path.insert(0, ROOT_DIR)

# -------------------------------------------------
# Mount examples folder (if still used)
# -------------------------------------------------

def _mount_examples():
    src = os.path.join(ROOT_DIR, "Examples")
    dst = os.path.join(DOCS_DIR, "examples-src")

    if not os.path.isdir(src):
        print(f"[conf.py] No Examples folder at {src}; skipping.")
        return

    try:
        if os.path.exists(dst):
            if os.path.islink(dst):
                os.unlink(dst)
            elif os.path.isdir(dst):
                shutil.rmtree(dst)
            else:
                os.remove(dst)

        try:
            os.symlink(src, dst, target_is_directory=True)
            print(f"[conf.py] Linked examples-src -> {src}")

        except (OSError, NotImplementedError):
            try:
                subprocess.run(
                    ["cmd", "/c", "mklink", "/J", dst, src],
                    check=True,
                    shell=True,
                )
                print(f"[conf.py] Junction examples-src -> {src}")

            except Exception:
                shutil.copytree(src, dst)
                print(f"[conf.py] Copied examples to {dst}")

    except Exception as e:
        print(f"[conf.py] Failed to mount examples: {e}")

_mount_examples()

# -------------------------------------------------
# Project information
# -------------------------------------------------

project = "AnalyticsTools"
author = "Martin Mihaylov"
release = "0.1.0"

# -------------------------------------------------
# Extensions
# -------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autodoc_typehints = "description"

# -------------------------------------------------
# Mock heavy imports
# -------------------------------------------------

autodoc_mock_imports = [
    "numpy",
    "pandas",
    "matplotlib",
]

# -------------------------------------------------
# HTML output
# -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
    "titles_only": False,
    "includehidden": True,
    "sticky_navigation": True,
}

html_static_path = []