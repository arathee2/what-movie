"""Helpers for loading, caching, and sampling IMDb metadata."""

import os
import pickle
import random
from typing import List

import numpy as np
import pandas as pd

from what_movie.utils.constants import (CONSIDER_TOP_N, GENRE_COL,
                                        LANGUAGE_COL, MIN_NUM_VOTES, NEWEST_YEAR,
                                        NUM_VOTES, OLDEST_YEAR, OUTPUT_COLS,
                                        PRIMARY_KEY, SCORE_COL, TITLE_COL,
                                        YEAR_COL)
from what_movie.utils.paths import (IMDB_DATA_OBJ_PATH, MOVIES_PATH,
                                    RATINGS_PATH)


class IMDbDF():
    """Represents the IMDb dataset merged across metadata and ratings."""

    def __init__(self):
        if os.path.exists(IMDB_DATA_OBJ_PATH):
            print(f"Pickle object path: {IMDB_DATA_OBJ_PATH}")
            self._dataframe = self._from_pickle(IMDB_DATA_OBJ_PATH)
        else:
            self._dataframe = self._from_csvs()
            self._dataframe = self._preprocess_data(self._dataframe)
            self._to_pickle(self._dataframe, IMDB_DATA_OBJ_PATH)
        self._consider_top_n = CONSIDER_TOP_N

    @staticmethod
    def _from_pickle(path):
        """Read object from file."""
        with open(path, 'rb') as pickle_file:
            return pickle.load(pickle_file)

    @staticmethod
    def _to_pickle(obj, path):
        """Write object to file."""
        with open(path, 'wb') as pickle_file:
            pickle.dump(obj, pickle_file)

    @staticmethod
    def _from_csvs():
        """Return pandas.DataFrame by combining movies.csv and ratings.csv."""
        # read movies csv
        movie_cols = [PRIMARY_KEY, TITLE_COL, YEAR_COL, GENRE_COL, LANGUAGE_COL]
        movies_df = pd.read_csv(MOVIES_PATH, low_memory=False)
        movies_df = movies_df[movie_cols]

        # read ratings csv
        rating_cols = [PRIMARY_KEY, SCORE_COL, NUM_VOTES]
        rating_df = pd.read_csv(RATINGS_PATH, low_memory=False)
        rating_df = rating_df[rating_cols]

        # merge
        merged_df = movies_df.merge(rating_df,
                                    left_on=PRIMARY_KEY,
                                    right_on=PRIMARY_KEY)
        return merged_df

    def _preprocess_data(self, dataframe):
        """Clean and normalize the dataframe columns used by the recommender."""
        dataframe[YEAR_COL] = dataframe[YEAR_COL].apply(self.str_to_int)
        for col in [TITLE_COL, YEAR_COL, SCORE_COL, LANGUAGE_COL]:
            dataframe = dataframe[pd.notnull(dataframe[col])]
        dataframe[YEAR_COL] = dataframe[YEAR_COL].apply(np.int32)
        dataframe[LANGUAGE_COL] = dataframe[LANGUAGE_COL].apply(self.to_set)
        dataframe[GENRE_COL] = dataframe[GENRE_COL].apply(self.to_set)
        return dataframe

    def filter_data(self,
                    languages: List[str],
                    genres: List[str],
                    year_from: int = OLDEST_YEAR,
                    year_to: int = NEWEST_YEAR):
        """Filter data based on year, genre and language."""

        language_mask = self._dataframe[LANGUAGE_COL]. \
            apply(lambda x: self.contains(x, languages))
        self._dataframe = self._dataframe[language_mask]
        genre_mask = self._dataframe[GENRE_COL]. \
            apply(lambda x: self.contains(x, genres))
        self._dataframe = self._dataframe[genre_mask]
        year_mask = (self._dataframe[YEAR_COL] <= year_to) & \
                    (self._dataframe[YEAR_COL] >= year_from)
        self._dataframe = self._dataframe[year_mask]
        num_votes_mask = self._dataframe[NUM_VOTES] > MIN_NUM_VOTES
        self._dataframe = self._dataframe[num_votes_mask]

    def sort_data(self):
        """Sort data based on movie rating."""

        self._dataframe = self._dataframe.sort_values(by=SCORE_COL,
                                                      ascending=False). \
            reset_index()

    def pick_top_movies(self, movie_count):
        """Return random movies names from highly-rated movies."""
        self.sort_data()
        self._consider_top_n = min(self._consider_top_n, self._dataframe.shape[0])
        movies = []
        picked_so_far = []
        while len(movies) != movie_count:
            random_value = random.choice(range(self._consider_top_n))
            if random_value not in picked_so_far:
                picked_so_far.append(random_value)
            else:
                continue
            movie = {}
            for col in OUTPUT_COLS:
                movie[col] = self._dataframe.loc[random_value, col]
            movies.append(movie)
        return movies

    @staticmethod
    def to_set(items):
        """Convert a comma-separated string to a set of words."""
        items = items.split(',')
        items = [item.strip().lower() for item in items]
        items = set(items)
        return items

    @staticmethod
    def contains(haystack, needles):
        """Return True if ``haystack`` and ``needles`` share common elements."""
        lower_needles = {item.lower() for item in needles}
        return bool(haystack.intersection(lower_needles))

    @staticmethod
    def str_to_int(string):
        """Convert string to integer."""
        try:
            return int(string)
        except ValueError:
            return None
