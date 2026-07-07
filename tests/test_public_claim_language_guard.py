import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[1]
PUBLIC_TEXT_FILES = [
    ROOT / "README.md",
    ROOT / "docs" / "LIMITATIONS.md",
    ROOT / "docs" / "EVAL_FACTSHEET.md",
    ROOT / "docs" / "PUBLIC_CLAIM_BOUNDARY.md",
    ROOT / "SECURITY.md",
    ROOT / "CITATION.cff",
]

FORBIDDEN_ASSERTIVE_CLAIMS = (
    "certified safe",
    "proves safety",
    "proves agentic ai is safe",
    "deployment-ready",
    "externally validated",
    "release approved",
    "guaranteed safe",
)


def test_public_text_avoids_assertive_overclaim_language():
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in PUBLIC_TEXT_FILES)
    for phrase in FORBIDDEN_ASSERTIVE_CLAIMS:
        assert phrase not in combined


def test_readme_describes_two_layers():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Two Layers" in readme
    assert "receipt schema and human review templates" in readme
    assert "local request classifier demo" in readme
