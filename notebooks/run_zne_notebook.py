"""Headless execution helper for the ZNE demo notebook.

This script runs the bundled ZNE notebook from the command line, updating
all code cell outputs and regenerating the ``zne_results.svg`` chart. It is
compatible with Python 3.7+ and assumes execution from the repository root:
``python notebooks/run_zne_notebook.py``.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
from typing import Iterator


@contextlib.contextmanager
def chdir(path: Path) -> Iterator[None]:
    """Temporarily change the working directory (Python 3.7 compatible)."""
    original = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original)

import contextlib
import io
import json
from pathlib import Path


"""Utility to execute and refresh the ZNE demo notebook without Jupyter."""

def run_notebook(notebook_path: Path) -> None:
    notebook_path = notebook_path.resolve()
    notebook_dir = notebook_path.parent
    nb = json.loads(notebook_path.read_text())

    globals_ns = {}
    exec_count = 1

    with contextlib.ExitStack() as stack:
        stack.enter_context(chdir(notebook_dir))
        stack.enter_context(contextlib.chdir(notebook_dir))
        # Allow the notebook to import local helpers from the repository root.
        globals_ns.setdefault("__path__", [])
        globals_ns.setdefault("__file__", notebook_path.name)
        globals_ns.setdefault("__package__", None)
        globals_ns.setdefault("__spec__", None)
        globals_ns.setdefault("__name__", "__main__")
        globals_ns.setdefault("__builtins__", __builtins__)
        parent = notebook_dir.parent
        if str(parent) not in globals_ns.setdefault("sys", __import__("sys")).path:
            globals_ns["sys"].path.insert(0, str(parent))
        for cell in nb.get("cells", []):
            if cell.get("cell_type") != "code":
                continue

            source = "".join(cell.get("source", []))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                exec(compile(source, notebook_path.name, "exec"), globals_ns)

            output_text = buf.getvalue()
            cell["execution_count"] = exec_count
            exec_count += 1
            cell_outputs = []
            if output_text:
                cell_outputs.append(
                    {
                        "output_type": "stream",
                        "name": "stdout",
                        "text": output_text.splitlines(keepends=True),
                    }
                )
            cell["outputs"] = cell_outputs

    notebook_path.write_text(json.dumps(nb, indent=1))
    svg_path = notebook_dir / "zne_results.svg"
    print(f"Executed {exec_count - 1} code cells.")
    print(f"Result SVG present: {svg_path.exists()} ({svg_path})")


def main() -> None:
    default_path = Path(__file__).with_name("Zero_Noise_Extrapolation_(ZNE)_Task.ipynb")
    run_notebook(default_path)


if __name__ == "__main__":
    main()
