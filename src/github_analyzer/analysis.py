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
        "test_file_percentage": 0.0,
        "files_by_category": {},
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

    result["test_file_percentage"] = calculate_test_files_percentage(result["test_files"], result["total_files"])
    result["files_by_category"] = count_files_by_category(result["extensions"], classify_extensions(result["extensions"]))

    return result

def classify_extensions(extensions: dict) -> dict:
    defined_extensions = {
        "source_code": { ".py", ".java", ".js", ".css" },
        "documentation":  { ".md", ".rst" },
        "assets": { ".png" },
        "configuration": { ".json", ".yaml" , ".yml"},
    }

    result = {
        "source_code": [],
        "documentation": [],
        "assets": [],
        "configuration": [],
        "other": [],
    }

    for extension in extensions:
        matched = False
        for category, known_extensions in defined_extensions.items():
            if extension in known_extensions:
                result[category].append(extension)
                matched = True
        if not matched:
            result["other"].append(extension)

    return result


def count_files_by_category(
        extensions: dict,
        classified_extensions: dict,
) -> dict:
    result = {
        "source_code": 0,
        "documentation": 0,
        "assets": 0,
        "configuration": 0,
        "other": 0,
    }

    for category, classified_ext in classified_extensions.items():
            total = 0
            print(category)
            print(classified_ext)
            for extension in classified_ext:
                # print(f"{category} {classified_ext}")
                total += extensions[extension]
            result[category] = total

    return result


def calculate_test_files_percentage(total_files: int, test_files: int) -> float:
    if test_files == 0 or total_files == 0:
        return 0.0

    return test_files / total_files * 100.0


def generate_health_warnings(
        test_file_percentage: float,
        largest_files: list,
) -> list:
    warnings = []
    if test_file_percentage == 0.0:
        warnings.append({"type": "WARNING", "message": "Repository has no test files!"})
    elif test_file_percentage < 5.0:
        warnings.append({"type": "WARNING", "message": f"Repository has low proportion of test files: {test_file_percentage}%"})
    if len(largest_files) > 0 and largest_files[0]["size"] > 1_000_000:
        warnings.append({"type": "WARNING", "message": "Repository contains a very large file"})

    return warnings
