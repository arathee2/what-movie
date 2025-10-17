"""Tools for loading IMDb data and generating movie recommendations."""

from __future__ import annotations

import pickle
from dataclasses import dataclass, field
from typing import FrozenSet, List, Sequence, Set, Tuple

import pandas as pd

from what_movie.utils.constants import (
    COLUMN_LABELS,
    DEFAULT_SETTINGS,
    GENRE_COL,
    LANGUAGE_COL,
    MOVIE_COLS,
    NUM_VOTES,
    PRIMARY_KEY,
    RATING_COLS,
    SCORE_COL,
    TITLE_COL,
    YEAR_COL,
)
from what_movie.utils.paths import DataPaths, get_data_paths

__all__ = [
    "MovieRecommendation",
    "RecommendationSettings",
    "MovieRecommender",
    "ImdbDataset",
]


@dataclass(frozen=True)  # pylint: disable=too-few-public-methods
class RecommendationSettings:
    """User-configurable knobs for recommendation generation."""

    languages: Sequence[str] = DEFAULT_SETTINGS.languages
    genres: Sequence[str] = DEFAULT_SETTINGS.genres
    min_votes: int = DEFAULT_SETTINGS.min_votes
    year_from: int = DEFAULT_SETTINGS.oldest_year
    year_to: int = DEFAULT_SETTINGS.newest_year
    consider_top_n: int = DEFAULT_SETTINGS.consider_top_n

    @property
    def normalized_languages(self) -> Set[str]:
        """Return the desired languages as lowercase values."""
        return {language.lower() for language in self.languages if language}

    @property
    def normalized_genres(self) -> Set[str]:
        """Return the desired genres as lowercase values."""
        return {genre.lower() for genre in self.genres if genre}


@dataclass(frozen=True)  # pylint: disable=too-few-public-methods
class MovieRecommendation:
    """Structured representation of a recommended movie."""

    title: str
    rating: float
    year: int
    genres: Sequence[str]
    languages: Sequence[str]

    def as_display_rows(self) -> List[Tuple[str, str]]:
        """Return label/value pairs ready for CLI presentation."""
        return [
            (COLUMN_LABELS[TITLE_COL], self.title),
            (COLUMN_LABELS[SCORE_COL], f"{self.rating:.1f}"),
            (COLUMN_LABELS[YEAR_COL], str(self.year)),
            (COLUMN_LABELS[GENRE_COL], ", ".join(self.genres)),
            (COLUMN_LABELS[LANGUAGE_COL], ", ".join(self.languages)),
        ]


@dataclass
class ImdbDataset:
    """Loads, preprocesses, and caches the IMDb dataset."""

    paths: DataPaths = field(default_factory=get_data_paths)
    _dataframe: pd.DataFrame | None = field(init=False, default=None)

    def dataframe(self) -> pd.DataFrame:
        """Return the processed dataset, loading or rebuilding it if needed."""
        if self._dataframe is None:
            self._dataframe = self._load_or_build()
        return self._dataframe.copy()

    def invalidate_cache(self) -> None:
        """Clear the cached dataframe and backing pickle."""
        self._dataframe = None
        if self.paths.cache.exists():
            self.paths.cache.unlink()

    def _load_or_build(self) -> pd.DataFrame:
        if self.paths.cache.exists():
            try:
                return pd.read_pickle(self.paths.cache)
            except (pickle.UnpicklingError, AttributeError, ValueError):
                # Cached pickle is no longer compatible with the current pandas version.
                self.paths.cache.unlink()

        dataset = self._build_dataframe()
        dataset.to_pickle(self.paths.cache)
        return dataset

    def _build_dataframe(self) -> pd.DataFrame:
        """Construct a cleaned dataframe directly from the raw CSV exports."""
        movies_df = pd.read_csv(
            self.paths.movies,
            usecols=MOVIE_COLS,
            dtype={
                TITLE_COL: "string",
                YEAR_COL: "string",
                GENRE_COL: "string",
                LANGUAGE_COL: "string",
            },
            low_memory=False,
        )
        ratings_df = pd.read_csv(
            self.paths.ratings,
            usecols=RATING_COLS,
            dtype={SCORE_COL: "float64", NUM_VOTES: "Int64"},
            low_memory=False,
        )
        merged_df = movies_df.merge(ratings_df, on=PRIMARY_KEY)
        return self._preprocess(merged_df)

    @staticmethod
    def _preprocess(dataframe: pd.DataFrame) -> pd.DataFrame:
        cleaned = dataframe.dropna(subset=[TITLE_COL, YEAR_COL, SCORE_COL, LANGUAGE_COL]).copy()
        cleaned.loc[:, YEAR_COL] = pd.to_numeric(cleaned[YEAR_COL], errors="coerce")
        cleaned = cleaned.dropna(subset=[YEAR_COL])
        cleaned.loc[:, YEAR_COL] = cleaned[YEAR_COL].astype(int)
        cleaned.loc[:, LANGUAGE_COL] = cleaned[LANGUAGE_COL].apply(_split_to_set)
        cleaned.loc[:, GENRE_COL] = cleaned[GENRE_COL].apply(_split_to_set)
        cleaned.loc[:, NUM_VOTES] = (
            pd.to_numeric(cleaned[NUM_VOTES], errors="coerce").fillna(0).astype(int)
        )
        cleaned.loc[:, SCORE_COL] = pd.to_numeric(cleaned[SCORE_COL], errors="coerce")
        cleaned = cleaned.dropna(subset=[SCORE_COL])
        return cleaned.reset_index(drop=True)


class MovieRecommender:
    """High-level API that applies filters and samples recommended titles."""

    def __init__(
        self,
        dataset: ImdbDataset | None = None,
        settings: RecommendationSettings | None = None,
    ) -> None:
        self._dataset = dataset or ImdbDataset()
        self._settings = settings or RecommendationSettings()

    @property
    def settings(self) -> RecommendationSettings:
        """Expose the active recommendation settings."""
        return self._settings

    @property
    def dataset(self) -> ImdbDataset:
        """Expose the underlying dataset wrapper."""
        return self._dataset

    def recommend(self, count: int) -> List[MovieRecommendation]:
        """Return up to ``count`` random picks from the highest-rated movies."""
        if count <= 0:
            return []

        frame = self._dataset.dataframe()
        filtered = self._apply_filters(frame)
        if filtered.empty:
            return []

        top_candidates = filtered.nlargest(self._settings.consider_top_n, SCORE_COL)
        sample_size = min(count, len(top_candidates))
        sample = top_candidates.sample(n=sample_size, replace=False, random_state=None)

        recommendations: List[MovieRecommendation] = []
        for _, row in sample.iterrows():
            recommendations.append(
                MovieRecommendation(
                    title=str(row[TITLE_COL]),
                    rating=float(row[SCORE_COL]),
                    year=int(row[YEAR_COL]),
                    genres=sorted(row[GENRE_COL]),
                    languages=sorted(row[LANGUAGE_COL]),
                )
            )
        return recommendations

    def _apply_filters(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Apply the configured filters to the source dataframe."""
        languages = self._settings.normalized_languages
        genres = self._settings.normalized_genres
        filtered = dataframe.copy()

        if languages:
            filtered = filtered[
                filtered[LANGUAGE_COL].apply(lambda values: bool(values.intersection(languages)))
            ]
        if genres:
            filtered = filtered[
                filtered[GENRE_COL].apply(lambda values: bool(values.intersection(genres)))
            ]

        filtered = filtered[
            (filtered[YEAR_COL] >= self._settings.year_from)
            & (filtered[YEAR_COL] <= self._settings.year_to)
        ]
        filtered = filtered[filtered[NUM_VOTES] >= self._settings.min_votes]
        return filtered.reset_index(drop=True)


def _split_to_set(raw: str | float) -> FrozenSet[str]:
    """Convert a comma-separated string to a normalized set of values."""
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return frozenset()
    if not isinstance(raw, str):
        raw = str(raw)
    parts = (part.strip().lower() for part in raw.split(","))
    return frozenset(part for part in parts if part)
