import pytest
from smolagents_capsule import CapsulePythonTool, CapsuleJSTool


# ---- Python : Basic tests ----
def test_python_basic():
    result = CapsulePythonTool().forward("1 + 1")
    assert str(result).strip() == "2"


# ---- Python : Multi-line & variables test ----
def test_python_multiline():
    code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

factorial(6)
"""
    result = CapsulePythonTool().forward(code)
    assert str(result).strip() == "720"

def test_python_variables():
    code = """
x = 10
y = 32
x + y
"""
    result = CapsulePythonTool().forward(code)
    assert str(result).strip() == "42"

def test_python_list_comprehension():
    code = "[i ** 2 for i in range(5)]"
    result = CapsulePythonTool().forward(code)
    assert str(result).strip() == "[0, 1, 4, 9, 16]"

def test_python_stdlib():
    code = """
import json
data = {"hello": "world", "number": 42}
json.dumps(data)
"""
    result = CapsulePythonTool().forward(code)
    assert '"hello"' in result
    assert '"world"' in result


# ---- Python : Errors test ----
def test_python_syntax_error():
    with pytest.raises(Exception, match="was never closed"):
        CapsulePythonTool().forward("def broken(")

def test_python_runtime_error():
    with pytest.raises(Exception, match="division by zero"):
        CapsulePythonTool().forward("1 / 0")

def test_python_name_error():
    with pytest.raises(Exception, match="undefined_variable"):
        CapsulePythonTool().forward("undefined_variable")


# ---- JavaScript : Basic tests ----
def test_js_basic():
    result = CapsuleJSTool().forward("1 + 2")
    assert str(result).strip() == "3"


# ---- JavaScript : Multi-line & variables test ----
def test_js_multiline():
    code = """
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
factorial(6)
"""
    result = CapsuleJSTool().forward(code)
    assert str(result).strip() == "720"

def test_js_variables():
    code = """
const x = 10;
const y = 32;
x + y
"""
    result = CapsuleJSTool().forward(code)
    assert str(result).strip() == "42"

def test_js_array_operations():
    code = "[1, 2, 3, 4, 5].map(x => x ** 2)"
    result = CapsuleJSTool().forward(code)
    assert str(result).strip() == "[1, 4, 9, 16, 25]"

def test_js_object():
    code = """
const data = { hello: "world", number: 42 };
JSON.stringify(data)
"""
    result = CapsuleJSTool().forward(code)
    assert "hello" in result
    assert "world" in result


# ---- JavaScript : Errors test ----
def test_js_syntax_error():
    with pytest.raises(Exception, match="missing formal parameter"):
        CapsuleJSTool().forward("function broken(")

def test_js_runtime_error():
    with pytest.raises(Exception, match="null"):
        CapsuleJSTool().forward("null.property")

def test_js_reference_error():
    with pytest.raises(Exception, match="undefinedVariable"):
        CapsuleJSTool().forward("undefinedVariable")
