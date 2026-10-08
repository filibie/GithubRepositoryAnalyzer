from pathlib import Path

def calculate_language_percentages(languages: dict[str, int]) -> dict[str, float]:
    total = sum(languages.values())

    percentages = {}

    for language, bytes_count in languages.items():
        percentage = (bytes_count / total) * 100
        percentages[language] = percentage

    return percentages


def analyze_tree(tree: list) -> dict:
    files = [item for item in tree if item["type"] == "blob"]
    directories = [item for item in tree if item["type"] == "tree"]

    return {
        "files": len(files),
        "directories": len(directories)
    }


def analyze_files(tree: list) -> dict:
    files = [item for item in tree if item["type"] == "blob"]

    result = {
        "total_files": len(files),
        "extensions": {},
        "test_files": 0,
        "largest_files": []
    }

    for file in files:
        extension = Path(file["path"]).suffix
        if extension in result["extensions"]:
            result["extensions"][extension] += 1
        else:
            result["extensions"][extension] = 1

        filename = Path(file["path"]).stem
        if filename.startswith("test_") or filename.endswith("_test"):
            result["test_files"] += 1

    for file in sorted(
        files,
        key=lambda file: file["size"],
        reverse=True
    )[:5]:
        result["largest_files"].append({
            "path": file["path"],
            "size": file["size"]
        })

    return result
