"""Common filesystem paths for the What Movie dataset."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataPaths:
    """Container holding canonical project and dataset locations."""

    root: Path
    data_dir: Path
    movies: Path
    ratings: Path
    cache: Path


def _compute_paths() -> DataPaths:
    """Return the resolved directory layout for the repository."""
    root = Path(__file__).resolve().parents[2]
    data_dir = root / 'data'
    return DataPaths(
        root=root,
        data_dir=data_dir,
        movies=data_dir / 'movies.csv',
        ratings=data_dir / 'ratings.csv',
        cache=data_dir / 'processed_data.pkl',
    )


DATA_PATHS = _compute_paths()

# Backwards-compatible exports for modules that import the legacy names.
ROOT: Path = DATA_PATHS.root
DATA_PATH: Path = DATA_PATHS.data_dir
MOVIES_PATH: Path = DATA_PATHS.movies
RATINGS_PATH: Path = DATA_PATHS.ratings
IMDB_DATA_OBJ_PATH: Path = DATA_PATHS.cache


def get_data_paths() -> DataPaths:
    """Expose a copy of the resolved filesystem paths."""
    return DATA_PATHS
