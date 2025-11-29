#!/usr/bin/env python3
"""
Generate documentation for the Enana project using Sphinx.

This script handles:
- Generating Markdown API documentation from docstrings
- Incremental builds (only rebuild when source files change)
- Error and warning handling
- Logging and status reporting
- Integration with CI/CD workflows
"""

import os
import sys
import subprocess
import logging
import hashlib
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Constants
DOCS_DIR = Path("docs")
BUILD_DIR = DOCS_DIR / "_build"
MARKDOWN_DIR = BUILD_DIR / "markdown"
SOURCE_DIR = Path("enana")
CACHE_FILE = BUILD_DIR / ".doc_cache"


def get_file_hash(file_path: Path) -> str:
    """
    Calculate the SHA256 hash of a file.

    Args:
        file_path: Path to the file

    Returns:
        str: SHA256 hash of the file
    """
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_source_files() -> list[Path]:
    """
    Get all Python source files in the enana directory.

    Returns:
        list[Path]: List of Python source files
    """
    source_files = []
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(".py"):
                source_files.append(Path(root) / file)
    return source_files


def get_current_hash() -> dict[str, str]:
    """
    Calculate hashes for all source files.

    Returns:
        dict[str, str]: Dictionary mapping file paths to their hashes
    """
    hashes = {}
    for file_path in get_source_files():
        hashes[str(file_path)] = get_file_hash(file_path)
    return hashes


def load_cache() -> dict[str, str]:
    """
    Load the cached hashes from the cache file.

    Returns:
        dict[str, str]: Cached hashes or empty dict if cache doesn't exist
    """
    if not CACHE_FILE.exists():
        return {}
    try:
        import json

        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.warning(f"Failed to load cache: {e}")
        return {}


def save_cache(hashes: dict[str, str]) -> None:
    """
    Save the current hashes to the cache file.

    Args:
        hashes: Dictionary mapping file paths to their hashes
    """
    import json

    CACHE_FILE.parent.mkdir(exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(hashes, f, indent=2)


def needs_rebuild() -> bool:
    """
    Check if the documentation needs to be rebuilt.

    Returns:
        bool: True if documentation needs to be rebuilt, False otherwise
    """
    current_hashes = get_current_hash()
    cached_hashes = load_cache()

    # Check if any files have changed
    if current_hashes != cached_hashes:
        logger.info("Source files have changed, rebuilding documentation...")
        return True

    # Check if output directory doesn't exist
    if not MARKDOWN_DIR.exists():
        logger.info(
            "Output directory doesn't exist, rebuilding documentation..."
        )
        return True

    # Check if any documentation files are missing
    expected_files = [
        MARKDOWN_DIR / "index.md",
        MARKDOWN_DIR / "enana.md",
    ]
    for file in expected_files:
        if not file.exists():
            logger.info(f"Missing documentation file {file}, rebuilding...")
            return True

    logger.info("Documentation is up to date, skipping rebuild...")
    return False


def generate_docs() -> int:
    """
    Generate the documentation using Sphinx.

    Returns:
        int: Exit code of the Sphinx build process
    """
    # Create build directories if they don't exist
    MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)

    # Run Sphinx build
    cmd = [
        sys.executable,
        "-m",
        "sphinx",
        "-b",
        "markdown",
        str(DOCS_DIR),
        str(MARKDOWN_DIR),
        # Commented out -W flag to allow warnings during development
        # "-W",  # Treat warnings as errors
    ]

    logger.info(f"Running Sphinx build: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd, check=True, capture_output=True, text=True
        )
        logger.info("Sphinx build completed successfully!")
        logger.debug(f"Sphinx output: {result.stdout}")

        # Update cache
        save_cache(get_current_hash())

        return 0
    except subprocess.CalledProcessError as e:
        logger.error(f"Sphinx build failed with exit code {e.returncode}")
        logger.error(f"Sphinx stderr: {e.stderr}")
        logger.error(f"Sphinx stdout: {e.stdout}")
        return e.returncode
    except Exception as e:
        logger.error(f"Unexpected error during Sphinx build: {e}")
        return 1


def main() -> int:
    """
    Main function to generate documentation.

    Returns:
        int: Exit code
    """
    logger.info("Starting documentation generation...")

    # Check if we need to rebuild
    if not needs_rebuild():
        return 0

    # Generate documentation
    exit_code = generate_docs()

    if exit_code == 0:
        logger.info(f"Documentation generated successfully in {MARKDOWN_DIR}")
        # List generated files
        generated_files = list(MARKDOWN_DIR.glob("*.md"))
        logger.info(f"Generated {len(generated_files)} Markdown files:")
        for file in sorted(generated_files):
            logger.info(f"  - {file.name}")
    else:
        logger.error("Documentation generation failed")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
