import argparse

from what_movie.model.imdb import IMDbDF
from what_movie.utils.constants import OUTPUT_COLS, LANGUAGE_FILTER, \
    GENRE_FILTER, COLS_TO_NAMES


def main(n, year_from, year_to):
    data = IMDbDF()
    data.filter_data(LANGUAGE_FILTER,
                     GENRE_FILTER,
                     year_from=year_from,
                     year_to=year_to)
    movies = data.pick_top_movies(movie_count=n)
    for i in range(n):
        heading = f'Movie #{i + 1}'
        hyphens = '-' * len(heading)
        print(f'{hyphens}\n{heading}\n{hyphens}')
        for col in OUTPUT_COLS:
            print(f'{COLS_TO_NAMES[col]}: {movies[i][col]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_movies", type=int, default=3,
                        help="Number of of movies to recommend.")
    parser.add_argument("-f", "--year_from", type=int, default=1800,
                        help="Consider movies released this "
                             "or after this year.")
    parser.add_argument("-t", "--year_to", type=int, default=2020,
                        help="Consider movies released this "
                             "or before this year.")
    args = parser.parse_args()
    main(args.num_movies, args.year_from, args.year_to)
