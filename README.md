# GitHub Repository Analyzer

A Python CLI tool for analyzing GitHub repositories.

This project is being developed as a hands-on learning project to practice Python, REST APIs, automated testing, and software architecture.

## Current Features

* Fetch GitHub repository information and statistics
* Analyze programming language composition and calculate percentages
* Fetch and analyze the repository file tree
* Count files and directories
* Count files by extension
* Categorize file types into source code, documentation, assets, configuration, and other
* Identify test files and calculate their percentage of the repository
* Find the five largest files
* Generate repository health warnings for missing or uncommon test files and very large files
* Display analysis results in the terminal

## Technologies

* Python 3.14+
* GitHub REST API
* Requests
* pytest

## Requirements

* Python 3.14 or newer
* Git
* Internet connection
* A public GitHub repository URL

## Installation

Clone the repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd GitHubRepositoryAnalyzer
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project and development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Usage

Run the analyzer with a GitHub repository URL:

```bash
python src/github_analyzer/analyzer.py https://github.com/psf/requests
```

The analyzer fetches repository data and displays repository statistics, language composition, file analysis, and health warnings.

## Running Tests

Run the test suite from the project root:

```bash
python -m pytest
```

## Project Structure

```text
GitHubRepositoryAnalyzer/
├── src/
│   └── github_analyzer/
│       ├── __init__.py
│       ├── analyzer.py
│       ├── github.py
│       ├── analysis.py
│       └── output.py
├── tests/
│   └── test_analyzer.py
├── .gitignore
├── pyproject.toml
├── LICENSE
└── README.md
```

* `analyzer.py` — coordinates the analysis workflow and handles command-line input.
* `github.py` — communicates with the GitHub API.
* `analysis.py` — calculates statistics and generates health warnings.
* `output.py` — formats and prints the results.
* `tests/` — contains automated tests.

## Limitations

* Designed for public GitHub repositories.
* File categories are based on predefined file extensions.
* Health warnings use simple heuristics and do not represent a complete code-quality assessment.
* GitHub API rate limits may apply.

## Future Plans

* Export analysis results to JSON
* Analyze repository activity and commit history
* Add GitHub API authentication
* Build a REST API with FastAPI
* Add a web frontend
* Store analysis results in PostgreSQL

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
