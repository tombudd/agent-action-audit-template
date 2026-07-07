import ast
import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCAN_DIRS = [ROOT / "src", ROOT / "tools"]
FORBIDDEN_IMPORT_ROOTS = {"requests", "httpx", "urllib"}
FORBIDDEN_REMOTE_PHRASES = (
    "git push",
    "gh repo create",
    "gh release create",
    "vercel deploy",
    "wrangler deploy",
    "npm publish",
    "twine upload",
    "docker push",
)
SECRET_ENV_NAMES = (
    "api_key",
    "apikey",
    "token",
    "secret",
    "credential",
    "password",
)


def python_files():
    for directory in SCAN_DIRS:
        yield from directory.rglob("*.py")


def test_no_network_libraries_imported():
    for path in python_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.split(".")[0] not in FORBIDDEN_IMPORT_ROOTS, path
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert node.module.split(".")[0] not in FORBIDDEN_IMPORT_ROOTS, path


def test_no_remote_write_or_deploy_commands_appear_in_code():
    for path in python_files():
        text = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_REMOTE_PHRASES:
            assert phrase not in text, f"{phrase} appears in {path}"


def test_no_secret_environment_variables_required():
    for path in python_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == "getenv":
                    first_arg = node.args[0] if node.args else None
                    if isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str):
                        lowered = first_arg.value.lower()
                        assert not any(name in lowered for name in SECRET_ENV_NAMES), path
