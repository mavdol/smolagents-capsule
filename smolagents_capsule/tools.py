"""
Capsule integration for running untrusted code securely in isolated WebAssembly sandboxes.
"""

import asyncio
from importlib import resources
from typing import Any

from capsule import run
from smolagents import Tool


def _get_wasm(filename: str) -> str:
    """Resolve the path to a .wasm file bundled inside this package."""
    with resources.path("smolagents_capsule.sandboxes", filename) as path:
        return str(path)


def _parse_capsule_error(error: Any) -> str:
    """Extract a human-readable message from a Capsule error payload."""
    if isinstance(error, dict):
        return error.get("message") or error.get("error_type") or str(error)
    return str(error)


async def _invoke_sandbox(wasm_file: str, code: str) -> str:
    """Call the Capsule sandbox and return the result value only."""
    res = await run(file=wasm_file, args=[code])

    if res.get("success"):
        return str(res.get("result", ""))

    error_msg = _parse_capsule_error(res.get("error"))
    raise Exception(error_msg)


class CapsulePythonTool(Tool):
    """Execute Python code inside an isolated Capsule WebAssembly sandbox."""

    name = "python_repl"
    description = (
        "Execute any Python code in a secure isolated WebAssembly sandbox. "
        "The last evaluated expression is returned as the result. "
        "End your code with an expression or return a value."
    )
    inputs = {
        "code": {
            "type": "string",
            "description": "The Python code to execute in the sandbox.",
        }
    }
    output_type = "string"

    def forward(self, code: str) -> str:
        return asyncio.run(
            _invoke_sandbox(_get_wasm("sandbox_py.wasm"), code)
        )


class CapsuleJSTool(Tool):
    """Execute JavaScript code inside an isolated Capsule WebAssembly sandbox."""

    name = "javascript_repl"
    description = (
        "Execute any JavaScript or TypeScript code in a secure isolated WebAssembly sandbox. "
        "The last evaluated expression is returned as the result. "
        "End your code with an expression or return a value."
    )
    inputs = {
        "code": {
            "type": "string",
            "description": "The JavaScript or TypeScript code to execute in the sandbox.",
        }
    }
    output_type = "string"

    def forward(self, code: str) -> str:
        return asyncio.run(
            _invoke_sandbox(_get_wasm("sandbox_js.wasm"), code)
        )
