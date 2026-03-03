# smolagents-capsule

[Capsule](https://github.com/mavdol/capsule) integration for [smolagents](https://github.com/huggingface/smolagents).

## What is this?

`smolagents-capsule` gives smolagents the ability to safely execute Python and JavaScript code in an isolated WebAssembly sandbox.

The WebAssembly sandbox files (.wasm) are already bundled inside this package; no configuration or network request is necessary to execute the sandboxes dynamically.

## Installation

```bash
pip install smolagents-capsule
```

## Usage

The package provides tools for executing code inside an isolated environment.

```python
from smolagents_capsule import CapsulePythonTool, CapsuleJSTool

# Python Example
python_tool = CapsulePythonTool()
result = python_tool.forward("1 + 1")
print(result)  # "2"

# JavaScript / TypeScript Example
js_tool = CapsuleJSTool()
result = js_tool.forward("1 + 2")
print(result)  # "3"
```

### With a smolagents agent

```python
from smolagents import CodeAgent, HfApiModel
from smolagents_capsule import CapsulePythonTool, CapsuleJSTool

agent = CodeAgent(
    tools=[CapsulePythonTool(), CapsuleJSTool()],
    model=HfApiModel(),
)

agent.run("Calculate the factorial of 10 using the python sandbox")
```

## Check our main repo

Visit [Capsule](https://github.com/mavdol/capsule) repository for more information.

## License

MIT License
