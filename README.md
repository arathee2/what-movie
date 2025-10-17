# What Movie

Command-line helper that surfaces highly-rated IMDb titles that match the genres, languages and release window you care about. The project combines the public IMDb movie metadata and ratings datasets into a single pandas dataframe, applies filters, and then samples from the highest-rated results.

## Features
- Filters the bundled IMDb movie dataset by language, genre, and release year.
- Applies vote-count thresholds before ranking to avoid obscure titles with few votes.
- Randomly samples from the top-rated slice to keep recommendations varied.
- Caches a preprocessed dataframe (`data/processed_data.pkl`) so subsequent runs return almost instantly.

## Project Layout
```
.
├── data/                   # IMDb CSV exports + cached pickle
├── main.py                 # CLI entry point
├── requirements.txt        # Runtime dependencies (numpy, pandas)
└── what_movie/
    ├── model/imdb.py       # Data loading, filtering, ranking logic
    └── utils/              # Constants and common paths
```

## Getting Started

### Prerequisites
- Python 3.8 or newer.
- `pip` for installing Python dependencies.

### Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/arathee2/what-movie.git
   cd what-movie
   ```
2. **(Optional) Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

The repository includes `data/movies.csv` and `data/ratings.csv` so you can start exploring immediately. Both CSVs come from the IMDb datasets (as distributed via Kaggle’s “IMDb movies” collection) and are subject to IMDb’s original licensing terms.

## Usage

Run the recommender from the project root:

```bash
python main.py -n 3 -f 2010 -t 2020
```

Example output (results are random within the filtered top slice):

```
------
Movie #1
------
Title: Andhadhun
Rating: 8.2
Year: 2018
Genre(s): thriller, crime
Language: hindi, english

------
Movie #2
------
Title: Knives Out
Rating: 8.0
Year: 2019
Genre(s): mystery, thriller, comedy
Language: english
```

### Command-line options
| Flag | Description | Default |
| --- | --- | --- |
| `-n`, `--num_movies` | Number of recommendations to return. | `3` |
| `-f`, `--year_from` | Earliest release year to include. | `1800` |
| `-t`, `--year_to` | Latest release year to include. | `2020` |

Use `python main.py --help` to see the full argument list.

### Adjusting default filters
The recommender ships with sensible defaults defined in `what_movie/utils/constants.py`:
- `LANGUAGE_FILTER = ['english', 'hindi']`
- `GENRE_FILTER = ['comedy', 'thriller', 'horror']`
- `MIN_NUM_VOTES = 1000`
- `CONSIDER_TOP_N = 100`

Update those constants to narrow the pool of candidates or tweak how aggressively the app de-duplicates low-vote titles.

## Regenerating the cached dataframe

To speed up subsequent runs, the first execution writes a processed pandas dataframe to `data/processed_data.pkl`. If you:
- upgrade pandas and encounter a pickle compatibility error (for example `AttributeError: Can't get attribute 'new_block'`), or
- want to rebuild the cache with modified filtering constants,

delete the pickle and run the CLI again:

```bash
rm data/processed_data.pkl
python main.py
```

The dataframe will be reconstructed from the CSV sources using your current pandas version and constants.

## Development notes
- The core logic lives in `what_movie/model/imdb.py` and is covered by docstrings. Light inline comments call out the trickier parts of the pandas pipeline.
- `pylint` is listed in `requirements.txt` for linting; run `pylint what_movie` after making changes.
- There are no automated tests yet—consider adding unit tests around the filtering and sampling logic if you extend the project.

## License

This project is released under the [MIT License](LICENSE).
