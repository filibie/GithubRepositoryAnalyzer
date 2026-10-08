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


def get_languages(owner: str, repo: str) -> dict:
    api_url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    response = requests.get(api_url)
    response.raise_for_status()

    return response.json()


def get_repository_tree(owner: str, repo: str, branch: str) -> list:
    api_url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/git/trees/{branch}?recursive=1"
    )

    response = requests.get(api_url)
    response.raise_for_status()

    return response.json()["tree"]
