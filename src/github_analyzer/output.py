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


def print_languages(percentages: dict) -> None:
    print("\nLanguages")
    print("-" * 50)

    for language, percentage in sorted(
        percentages.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        print(f"{language:<15} {percentage:>6.2f}%")


def print_file_analysis(file_analysis: dict) -> None:
    print("\nFiles")
    print("-" * 50)

    print(f"Total files: {file_analysis['total_files']}")
    print(f"Test files:  {file_analysis["test_files"]}")

    print("\nFile types")
    for extension, count in sorted(
        file_analysis["extensions"].items(),
        key=lambda item: item[1],
        reverse=True
    ):
        print(f"{extension or '[no extension]':<15} {count}")

    print("\nLargest files")
    for file in file_analysis["largest_files"]:
        size_kb = file["size"] / 1024

        print(f"{file['path']:<40} {size_kb:>0.2f} KB")
