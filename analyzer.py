import sys
from urllib.parse import urlparse

import requests

def parse_repository_url(url: str) -> tuple[str, str]:
    parsed_url = urlparse(url)

    if parsed_url.netloc != "github.com":
        raise ValueError("Invalid Github URL")
    
    parts = parsed_url.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError("URL must point to GitHub repository")

    owner, repo = parts

    return owner, repo

def get_repository(url: str) -> dict:
    owner, repo = parse_repository_url(url)

    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(api_url)

    if response.status_code == 404:
        raise ValueError("Repository not found")

    response.raise_for_status()

    return response.json()


def print_repository_info(repository: dict) -> None:
    print()
    print("=" * 50)
    print("       GitHub Repository Analyzer")
    print("=" * 50)

    print(f"\nName:        {repository['name']}")
    print(f"Owner:       {repository['owner']['login']}")
    print(f"Description: {repository['description'] or 'No description'}")

    print("\nStatistics")
    print("-" * 50)
    print(f"Stars:       {repository['stargazers_count']}")
    print(f"Forks:       {repository['forks_count']}")
    print(f"Open issues: {repository['open_issues_count']}")
    print(f"Watchers:    {repository['watchers_count']}")

    print("\nRepository")
    print("-" * 50)
    print(f"Language:    {repository['language'] or 'Unknown'}")
    print(f"License:     {repository['license']['name'] if repository['license'] else 'None'}")
    print(f"Created:     {repository['created_at'][:10]}")
    print(f"Updated:     {repository['updated_at'][:10]}")
    print()


def get_languages(owner: str, repo: str) -> dict:
    api_url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    response = requests.get(api_url)
    response.raise_for_status()

    return response.json()


def calculate_language_percentages(languages: dict) -> dict:
    total = sum(languages.values())

    percentages = {}

    for language, bytes_count in languages.items():
        percentage = (bytes_count / total) * 100
        percentages[language] = percentage

    return percentages


def print_languages(percentages: dict) -> None:
    print("\nLanguages")
    print("-" * 50)

    for language, percentage in sorted(
        percentages.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        print(f"{language:<15} {percentage:>6.2f}%")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage:")
        print("    python analyzer.py <github_repository_url>")
        return

    url = sys.argv[1]

    try:
        owner, repo = parse_repository_url(url)

        repository = get_repository(url)
        
        languages = get_languages(owner, repo)
        percentages = calculate_language_percentages(languages)
        
        print_repository_info(repository)
        print_languages(percentages)

    except requests.RequestException as error:
        print(f"Network error: {error}")

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()