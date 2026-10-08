# GitHub Repository Analyzer

A Python CLI tool for analyzing GitHub repositories.

The project is being built as a learning project to practice Python, REST APIs,
testing, and software architecture.

## Current Features

- Fetch GitHub repository information
- Display repository statistics
- Display the repository's primary language
- Analyze language composition
- Fetch the repository file tree
- Count files and directories

## Requirements

- Python 3.14+
- GitHub repository URL

## Installation

Clone the repository and create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project and development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Usage

```bash
python src/github_analyzer/analyzer.py https://github.com/psf/requests
```

## Running Tests

```bash
pytest
```

## Project Structure

```
GitHubRepositoryAnalyzer/
├── src/
│   └── github_analyzer/
│       ├── __init__.py
│       └── analyzer.py
├── tests/
│   └── test_analyzer.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## Future Plans

* Analyze file types and source-code structure
* Identify test files
* Find the largest files
* Analyze repository activity
* Add GitHub API authentication
* Build a REST API with FastAPI
* Add a web frontend
* Store analysis results in PostgreSQL