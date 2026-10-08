import pytest

from github_analyzer.analyzer import (
    parse_repository_url,
    calculate_language_percentages
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