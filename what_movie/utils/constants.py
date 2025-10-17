"""Static configuration values shared across the What Movie project."""

from dataclasses import dataclass
from typing import Mapping, Sequence, Tuple

PRIMARY_KEY = 'imdb_title_id'
TITLE_COL = 'title'
SCORE_COL = 'weighted_average_vote'
YEAR_COL = 'year'
GENRE_COL = 'genre'
LANGUAGE_COL = 'language'
NUM_VOTES = 'total_votes'

MOVIE_COLS: Tuple[str, ...] = (
    PRIMARY_KEY,
    TITLE_COL,
    YEAR_COL,
    GENRE_COL,
    LANGUAGE_COL,
)
RATING_COLS: Tuple[str, ...] = (
    PRIMARY_KEY,
    SCORE_COL,
    NUM_VOTES,
)
OUTPUT_COLS: Tuple[str, ...] = (
    TITLE_COL,
    SCORE_COL,
    YEAR_COL,
    GENRE_COL,
    LANGUAGE_COL,
)

OLDEST_YEAR = 1894
NEWEST_YEAR = 2020
MIN_NUM_VOTES = 1000
CONSIDER_TOP_N = 100  # only consider top N movies (based on rating) while choosing recommendations
DEFAULT_LANGUAGES: Tuple[str, ...] = ('english', 'hindi')
DEFAULT_GENRES: Tuple[str, ...] = ('comedy', 'thriller', 'horror', 'sci-fi')

COLUMN_LABELS: Mapping[str, str] = {
    TITLE_COL: 'Title',
    SCORE_COL: 'Rating',
    YEAR_COL: 'Year',
    GENRE_COL: 'Genre(s)',
    LANGUAGE_COL: 'Language',
    NUM_VOTES: 'Total Votes',
}


@dataclass(frozen=True)
class RecommendationDefaults:
    """Default knob settings for the recommendation engine."""

    languages: Sequence[str] = DEFAULT_LANGUAGES
    genres: Sequence[str] = DEFAULT_GENRES
    min_votes: int = MIN_NUM_VOTES
    consider_top_n: int = CONSIDER_TOP_N
    oldest_year: int = OLDEST_YEAR
    newest_year: int = NEWEST_YEAR


DEFAULT_SETTINGS = RecommendationDefaults()

# Backwards-compatible aliases kept for external users of the original package.
LANGUAGE_FILTER = list(DEFAULT_LANGUAGES)
GENRE_FILTER = list(DEFAULT_GENRES)
COLS_TO_NAMES = COLUMN_LABELS
