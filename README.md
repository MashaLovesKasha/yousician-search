# Yousician Song Search

## Overview

This is a command line program for searching for songs on the Yousician website https://yousician.com/songs/. The program extracts the search results (artist and song name), sorts them alphabetically by artist and song name, and prints a sorted list. The program can work with pagination.

## Prerequisites

- Python 3.x

## Setup

1. Clone the repository or download the files to your local machine
2. Create and activate a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script with the search string as the argument. You can also include the --headless flag to run the program in headless mode.

```bash
python yousician_search.py <search_string> [--headless]
```

### Some examples to run different scenarios:

- 1-page result, 1-word search

```bash
python yousician_search.py muse
```

- 1-page result, 2-word search

```bash
python yousician_search.py Harry Styles
```

- 4-page result, 1-word search

```bash
python yousician_search.py song
```

- 2-page result, 2-word search

```bash
python yousician_search.py Billie Eilish
```

- Multi-page page result (60 pages)

```bash
python yousician_search.py yousicians
```

- Empty result

```bash
python yousician_search.py prodigy
```

## Things to improve

- **Refactor functions:** Consider breaking down larger functions into smaller, more modular functions to improve readability and maintainability.
- **Modularize codebase:** Separate functions into different files based on their functionality. This will improve the organization of the codebase and make it easier to manage and scale.
- **Centralize CSS selectors:** Define all CSS selectors at the beginning of file. This practice improves maintainability by making it easier to update selectors in a single location, reducing the risk of errors when the website structure changes.


