"""Configures the search server."""
import pathlib

# URL of the index server
INDEX_API_URL = "http://localhost:8001/api/v1/hits/"

SEARCH_ROOT = pathlib.Path(__file__).resolve().parent
DATABASE_FILENAME = SEARCH_ROOT/'var'/'wikipedia.sqlite3'
