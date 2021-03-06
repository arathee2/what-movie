import os

op = os.path
abspath = op.abspath
joinpath = op.join
dirpath = op.dirname

import pickle
import random
from typing import List

import numpy as np
import pandas as pd

from what_movie.utils.paths import IMDB_DATA_OBJ_PATH, MOVIES_PATH, RATINGS_PATH
from what_movie.utils.constants import PRIMARY_KEY, TITLE_COL, SCORE_COL, \
    YEAR_COL, GENRE_COL, LANGUAGE_COL, OLDEST_YEAR, NEWEST_YEAR, NUM_VOTES, \
    MIN_NUM_VOTES, CONSIDER_TOP_N, OUTPUT_COLS


class IMDbDF():
    """Represents IMDb data."""

    def __init__(self):
        if os.path.exists(IMDB_DATA_OBJ_PATH):
            self._dataframe = self._from_pickle(IMDB_DATA_OBJ_PATH)
        else:
            self._dataframe = self._from_csvs()
            self._dataframe = self._preprocess_data(self._dataframe)
            self._to_pickle(self._dataframe, IMDB_DATA_OBJ_PATH)
        self._CONSIDER_TOP_N = CONSIDER_TOP_N

    def _from_pickle(self, path):
        """Read object from file."""
        with open(path, 'rb') as f:
            return pickle.load(f)

    def _to_pickle(self, obj, path):
        """Write object to file."""
        with open(path, 'wb') as f:
            pickle.dump(obj, f)

    def _from_csvs(self):
        """Return pandas.DataFrame by combining movies.csv and ratings.csv."""
        # read movies csv
        MOVIE_COLS = [PRIMARY_KEY, TITLE_COL, YEAR_COL, GENRE_COL, LANGUAGE_COL]
        movies_df = pd.read_csv(MOVIES_PATH, low_memory=False)
        movies_df = movies_df[MOVIE_COLS]

        # read ratings csv
        RATING_COLS = [PRIMARY_KEY, SCORE_COL, NUM_VOTES]
        rating_df = pd.read_csv(RATINGS_PATH,
                                low_memory=False)
        rating_df = rating_df[RATING_COLS]

        # merge
        df = movies_df.merge(rating_df,
                             left_on=PRIMARY_KEY,
                             right_on=PRIMARY_KEY)
        return df

    def _preprocess_data(self, df):
        """"""
        df[YEAR_COL] = df[YEAR_COL].apply(self.str_to_int)
        for col in [TITLE_COL, YEAR_COL, SCORE_COL, LANGUAGE_COL]:
            df = df[pd.notnull(df[col])]
        df[YEAR_COL] = df[YEAR_COL].apply(np.int32)
        df[LANGUAGE_COL] = df[LANGUAGE_COL].apply(self.to_set)
        df[GENRE_COL] = df[GENRE_COL].apply(self.to_set)
        return df

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

    def pick_top_movies(self, n):
        """Return random movies names from highly-rated movies."""

        self.sort_data()
        self._CONSIDER_TOP_N = min(self._CONSIDER_TOP_N, self._dataframe.shape[0])
        movies = list()
        picked_so_far = list()
        while len(movies) != n:
            random_value = random.choice(range(self._CONSIDER_TOP_N))
            if random_value not in picked_so_far:
                picked_so_far.append(random_value)
            else:
                continue
            movie = dict()
            for col in OUTPUT_COLS:
                movie[col] = self._dataframe.loc[random_value, col]
            movies.append(movie)
        return movies

    def to_set(self, items):
        """Convert a comma-separated string to a set of words."""
        items = items.split(',')
        items = [item.strip().lower() for item in items]
        items = set(items)
        return items

    def contains(self, A, B):
        """Return True if set A and B have common elements."""
        B = {item.lower() for item in B}
        if A.intersection(B):
            return True
        else:
            return False

    def str_to_int(self, string):
        """Convert string to integer."""
        try:
            return int(string)
        except ValueError:
            return None
