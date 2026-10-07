import sys
import requests


def get_repository(url: str) -> dict:
    parts = url.rstrip("/").split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL")

    owner = parts[-2]
    repo = parts[-1]

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


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage:")
        print("    python analyzer.py <github_repository_url>")
        return

    url = sys.argv[1]

    try:
        repository = get_repository(url)
        print_repository_info(repository)

    except requests.RequestException as error:
        print(f"Network error: {error}")

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()