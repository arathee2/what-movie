PRIMARY_KEY = 'imdb_title_id'
TITLE_COL = 'title'
SCORE_COL = 'weighted_average_vote'
YEAR_COL = 'year'
GENRE_COL = 'genre'
LANGUAGE_COL = 'language'
NUM_VOTES = 'total_votes'
MOVIE_COLS = [PRIMARY_KEY, TITLE_COL, YEAR_COL, GENRE_COL, LANGUAGE_COL]
RATING_COLS = [PRIMARY_KEY, SCORE_COL, NUM_VOTES]
OUTPUT_COLS = [TITLE_COL, SCORE_COL, YEAR_COL, GENRE_COL, LANGUAGE_COL]

OLDEST_YEAR = 1894
NEWEST_YEAR = 2020
LANGUAGE_FILTER = ['english', 'hindi']
GENRE_FILTER = ['comedy', 'thriller', 'horror']
MIN_NUM_VOTES = 1000
CONSIDER_TOP_N = 100  # number of movies to look at while picking a movie

COLS_TO_NAMES = {TITLE_COL: 'Title',
                 SCORE_COL: 'Rating',
                 YEAR_COL: 'Year',
                 GENRE_COL: 'Genre(s)',
                 LANGUAGE_COL: 'Language',
                 NUM_VOTES: 'Total Votes'}
