import argparse

from what_movie.model.imdb import MovieRecommender, RecommendationSettings


def main(num_movies: int, year_from: int, year_to: int) -> None:
    """Execute the CLI workflow with the provided filters."""
    settings = RecommendationSettings(year_from=year_from, year_to=year_to)
    recommender = MovieRecommender(settings=settings)
    recommendations = recommender.recommend(count=num_movies)

    if not recommendations:
        print("No movies found for the supplied filters.")
        return

    for index, movie in enumerate(recommendations, start=1):
        heading = f"Movie #{index}"
        hyphens = "-" * len(heading)
        print(f"{hyphens}\n{heading}\n{hyphens}")
        for label, value in movie.as_display_rows():
            print(f"{label}: {value}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--num_movies",
        type=int,
        default=3,
        help="Number of movies to recommend.",
    )
    parser.add_argument(
        "-f",
        "--year_from",
        type=int,
        default=1800,
        help="Consider movies released this or after this year.",
    )
    parser.add_argument(
        "-t",
        "--year_to",
        type=int,
        default=2020,
        help="Consider movies released this or before this year.",
    )
    args = parser.parse_args()
    main(args.num_movies, args.year_from, args.year_to)
