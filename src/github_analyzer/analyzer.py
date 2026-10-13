import sys

from github_analyzer.github import (
    parse_repository_url,
    get_repository,
    get_languages,
    get_repository_tree,
)

from github_analyzer.analysis import (
    calculate_language_percentages,
    analyze_files,
    analyze_tree,
    generate_health_warnings,
)

from github_analyzer.output import (
    print_repository_info,
    print_languages,
    print_file_analysis,
    print_health_warnings,
)

import requests

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage:")
        print("    python analyzer.py <github_repository_url>")
        return

    url = sys.argv[1]

    try:
        owner, repo = parse_repository_url(url)

        repository = get_repository(url)
        branch = repository["default_branch"]

        languages = get_languages(owner, repo)
        percentages = calculate_language_percentages(languages)

        tree = get_repository_tree(owner, repo, branch)
        
        file_analysis = analyze_files(tree)

        test_files = file_analysis["test_file_percentage"]
        largest_files = file_analysis["largest_files"]
        warnings = generate_health_warnings(test_files, largest_files)

        print_repository_info(repository)
        print_languages(percentages)
        print_file_analysis(file_analysis)
        print_health_warnings(warnings)

    except requests.RequestException as error:
        print(f"Network error: {error}")

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
