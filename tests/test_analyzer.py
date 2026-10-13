import pytest

from github_analyzer.github import parse_repository_url

from github_analyzer.analysis import (
    calculate_language_percentages,
    analyze_files,
    analyze_tree,
    classify_extensions,
    count_files_by_category,
    calculate_test_files_percentage,
    generate_health_warnings,
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


def test_classify_extensions():
    empty = classify_extensions({})

    assert empty == {
        "source_code": [],
        "documentation": [],
        "assets": [],
        "configuration": [],
        "other": [],
    }

    extensions = {
        ".py": 37,
        ".md": 13,
        ".png": 5,
        ".json": 4,
        ".yml": 10,
        ".rst": 16,
        ".css": 1,
        "Dockerfile": 1,
    }

    result = classify_extensions(extensions)

    assert ".py" in result["source_code"]
    assert ".css" in result["source_code"]
    assert ".json" in result["configuration"]
    assert ".yml" in result["configuration"]
    assert ".md" in result["documentation"]
    assert ".rst" in result["documentation"]
    assert ".png" in result["assets"]
    assert "Dockerfile" in result["other"]

    assert all(
        ".xzy" not in extensions
        for extensions in result.values()
    )


def test_count_files_by_category():
    extensions = {
        ".py": 37,
        ".md": 13,
        ".png": 5,
        ".json": 4,
        ".yml": 10,
        ".rst": 16,
        ".css": 1,
        "Dockerfile": 2,
    }

    result = count_files_by_category(extensions, classify_extensions(extensions))
    print(result)
    assert result["source_code"] == 38
    assert result["documentation"] == 29
    assert result["assets"] == 5
    assert result["configuration"] == 14
    assert result["other"] == 2


def test_calculate_test_files_percentage():
    assert calculate_test_files_percentage(100, 12) == 12.0
    assert calculate_test_files_percentage(50, 0) == 0.0
    assert calculate_test_files_percentage(0, 0) == 0.0


def test_generate_health_warnings():
    res = generate_health_warnings(3.0, [
        {"path": "assets/logo.png", "size": 1200000},
        {"path": "src/main.py", "size": 1500},
    ])

    assert {"type": "WARNING", "message": "Repository has low proportion of test files: 3.0%"} in res
    assert {"type": "WARNING", "message": 'Very large file: assets/logo.png (1.20 MB)'} in res


def test_generate_health_warnings_file_size_threshold():
    res = generate_health_warnings(3.0, [
        {"path": "assets/logo.png", "size": 1000000},
        {"path": "src/main.py", "size": 1500},
    ])

    assert {"type": "WARNING", "message": "Repository has low proportion of test files: 3.0%"} in res

    
def test_generate_health_warnings_for_healthy_repository():
    res = generate_health_warnings(20.0, [
        {"path": "assets/logo.png", "size": 50000},
        {"path": "src/main.py", "size": 1500},
    ])

    assert res == []


def test_generate_health_warnings_for_no_test_files():
    res = generate_health_warnings(0.0, [
        {"path": "assets/logo.png", "size": 50000},
        {"path": "src/main.py", "size": 1500},
    ])

    assert {"type": "WARNING", "message": "Repository has no test files!"} in res


def test_generate_health_warnings_for_no_files():
    res = generate_health_warnings(0.0, [])

    assert {"type": "WARNING", "message": "Repository has no test files!"} in res
