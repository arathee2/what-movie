"""Common filesystem paths for the What Movie dataset."""

import os

op = os.path
abspath = op.abspath
joinpath = op.join
dirpath = op.dirname

ROOT = abspath(joinpath(dirpath(__file__), '..', '..'))
DATA_PATH = joinpath(ROOT, 'data')
MOVIES_PATH = joinpath(DATA_PATH, 'movies.csv')
RATINGS_PATH = joinpath(DATA_PATH, 'ratings.csv')
IMDB_DATA_OBJ_PATH = joinpath(DATA_PATH, 'processed_data.pkl')
