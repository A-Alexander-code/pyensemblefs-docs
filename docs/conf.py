# -- Project info
project = "pyensemblefs"
author = "pyensemblefs contributors"
release = "0.4.1"
html_title = "pyensemblefs — Ensemble Feature Selection for Python"

# This documentation repository uses the distribution in requirements.txt.

# -- Extensions
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_design",
]

autodoc_default_options = {"members": True, "undoc-members": True, "show-inheritance": True}
autodoc_typehints = "description"
autosectionlabel_prefix_document = True
napoleon_google_docstring = True
napoleon_numpy_docstring = True

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_logo = "_static/pyensamblefs_logo_v2.png"  # optional
html_theme_options = {"logo_only": False, "collapse_navigation": False, "navigation_depth": 4}

intersphinx_mapping = {
    "python":  ("https://docs.python.org/3/", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
    "numpy":   ("https://numpy.org/doc/stable/", None),
    "pandas":  ("https://pandas.pydata.org/pandas-docs/stable/", None),
}

myst_enable_extensions = ["colon_fence", "deflist", "fieldlist"]

# Optional dependency; the installed package supplies its core dependencies.
autodoc_mock_imports = ["skrebate"]
