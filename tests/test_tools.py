import pytest
from unittest.mock import patch, AsyncMock

from smolagents_capsule.tools import CapsulePythonTool, CapsuleJSTool


# ── Fixtures ─────────────────────────────────────────────────────────

FAKE_PY_WASM = "/fake/path/sandbox_py.wasm"
FAKE_JS_WASM = "/fake/path/sandbox_js.wasm"


@pytest.fixture
def run_mock():
    with patch("smolagents_capsule.tools.run", new_callable=AsyncMock) as mock:
        yield mock


# ── CapsulePythonTool ─────────────────────────────────────────────────

@patch("smolagents_capsule.tools.resources.path")
def test_python_forward_success(mock_path, run_mock):
    """A successful run returns the result from the sandbox as a string."""
    run_mock.return_value = {"success": True, "result": "2", "error": None}
    mock_path.return_value.__enter__.return_value = FAKE_PY_WASM

    result = CapsulePythonTool().forward("1 + 1")

    assert result == "2"
    run_mock.assert_called_once_with(file=FAKE_PY_WASM, args=["1 + 1"])


@patch("smolagents_capsule.tools.resources.path")
def test_python_forward_result_is_always_string(mock_path, run_mock):
    """forward() coerces the sandbox result to str, regardless of the raw value."""
    run_mock.return_value = {"success": True, "result": 42, "error": None}
    mock_path.return_value.__enter__.return_value = FAKE_PY_WASM

    result = CapsulePythonTool().forward("42")

    assert result == "42"
    assert isinstance(result, str)


@patch("smolagents_capsule.tools.resources.path")
def test_python_forward_error_raises(mock_path, run_mock):
    """A failed run raises an Exception whose message comes from the error payload."""
    run_mock.return_value = {
        "success": False,
        "result": None,
        "error": {"error_type": "SyntaxError", "message": "invalid syntax"},
    }
    mock_path.return_value.__enter__.return_value = FAKE_PY_WASM

    with pytest.raises(Exception, match="invalid syntax"):
        CapsulePythonTool().forward("def broken(")

    run_mock.assert_called_once_with(file=FAKE_PY_WASM, args=["def broken("])


@patch("smolagents_capsule.tools.resources.path")
def test_python_forward_error_fallback_to_error_type(mock_path, run_mock):
    """When the error dict has no 'message', the error_type is used as the message."""
    run_mock.return_value = {
        "success": False,
        "result": None,
        "error": {"error_type": "RuntimeError"},
    }
    mock_path.return_value.__enter__.return_value = FAKE_PY_WASM

    with pytest.raises(Exception, match="RuntimeError"):
        CapsulePythonTool().forward("raise RuntimeError()")


# ── CapsuleJSTool ─────────────────────────────────────────────────────

@patch("smolagents_capsule.tools.resources.path")
def test_js_forward_success(mock_path, run_mock):
    """A successful JS run returns the result from the sandbox as a string."""
    run_mock.return_value = {"success": True, "result": "2", "error": None}
    mock_path.return_value.__enter__.return_value = FAKE_JS_WASM

    result = CapsuleJSTool().forward("1 + 1")

    assert result == "2"
    run_mock.assert_called_once_with(file=FAKE_JS_WASM, args=["1 + 1"])


@patch("smolagents_capsule.tools.resources.path")
def test_js_forward_error_raises(mock_path, run_mock):
    """A failed JS run raises an Exception with the sandbox error message."""
    run_mock.return_value = {
        "success": False,
        "result": None,
        "error": {"error_type": "SyntaxError", "message": "missing formal parameter"},
    }
    mock_path.return_value.__enter__.return_value = FAKE_JS_WASM

    with pytest.raises(Exception, match="missing formal parameter"):
        CapsuleJSTool().forward("function broken(")

    run_mock.assert_called_once_with(file=FAKE_JS_WASM, args=["function broken("])


# ── Tool metadata ─────────────────────────────────────────────────────

def test_python_tool_metadata():
    tool = CapsulePythonTool()
    assert tool.name == "python_repl"
    assert "Python" in tool.description
    assert "code" in tool.inputs
    assert tool.inputs["code"]["type"] == "string"
    assert tool.output_type == "string"


def test_js_tool_metadata():
    tool = CapsuleJSTool()
    assert tool.name == "javascript_repl"
    assert "JavaScript" in tool.description
    assert "code" in tool.inputs
    assert tool.inputs["code"]["type"] == "string"
    assert tool.output_type == "string"
