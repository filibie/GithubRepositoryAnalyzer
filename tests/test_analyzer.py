import pytest

from github_analyzer.analyzer import (
    parse_repository_url,
    calculate_language_percentages,
    analyze_tree,
    analyze_files
)

def test_parse_repository_url():
    owner, repo = parse_repository_url(
        "https://github.com/torvalds/linux"
    )

    assert owner == "torvalds"
    assert repo == "linux"


def test_parse_repository_url_with_trailing_slash():
    owner, repo = parse_repository_url(
        "https://github.com/torvalds/linux/"
    )

    assert owner == "torvalds"
    assert repo == "linux"


def test_parse_repository_url_rejects_non_github_url():
    with pytest.raises(ValueError):
        parse_repository_url(
            "https://example.com/torvalds/linux"
        )

def test_parse_repository_url_rejects_invalid_path():
    with pytest.raises(ValueError):
        parse_repository_url(
            "https://github.com/torvalds"
        )


def test_calculate_language_percentages():
    languages = {
        "Python": 75,
        "Java": 25,
    }

    result = calculate_language_percentages(languages)

    assert result["Python"] == 75
    assert result["Java"] == 25


def test_calculate_language_percentages_with_multiple_languages():
    languages = {
        "Python": 50,
        "Java": 30,
        "C": 20,
    }

    result = calculate_language_percentages(languages)

    assert result["Python"] == 50
    assert result["Java"] == 30
    assert result["C"] == 20


def test_analyze_tree():
    tree = [
        {"path": "README.md", "type": "blob"},
        {"path": "src", "type": "tree"},
        {"path": "src/main.py", "type": "blob"},
        {"path": "tests", "type": "tree"},
        {"path": "tests/test_main.py", "type": "blob"},
    ]

    result = analyze_tree(tree)

    assert result["files"] == 3
    assert result["directories"] == 2


def test_analyze_tree_with_empty_tree():
    result = analyze_tree([])

    assert result["files"] == 0
    assert result["directories"] == 0


def test_analyze_files():
    tree = [
        {"path": "src/main.py", "type": "blob", "size": 5000},
        {"path": "src/utils.py", "type": "blob", "size": 2000},
        {"path": "tests/test_main.py", "type": "blob", "size": 1500},
        {"path": "src/user_test.py", "type": "blob", "size": 1200},
        {"path": "README.md", "type": "blob", "size": 1000},
        {"path": "src/small.py", "type": "blob", "size": 500},
        {"path": "src", "type": "tree"},
    ]

    result = analyze_files(tree)

    assert result["total_files"] == 6
    assert result["extensions"][".py"] == 5
    assert result["extensions"][".md"] == 1
    assert result["test_files"] == 2

    assert len(result["largest_files"]) == 5
    assert all(
        file["path"] != "src/small.py"
        for file in result["largest_files"]
    )
    assert result["largest_files"][0]["path"] == "src/main.py"
    assert result["largest_files"][0]["size"] == 5000

    assert result["largest_files"][1]["path"] == "src/utils.py"
    assert result["largest_files"][1]["size"] == 2000