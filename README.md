# What Movie

Command-line helper that surfaces highly-rated IMDb titles that match the genres, languages and release window you care about. The project combines the public IMDb movie metadata and ratings datasets into a single pandas dataframe, applies filters, and then samples from the highest-rated results. The latest refactor wraps the workflow in reusable classes so the same engine can power scripts, notebooks, or the bundled CLI.

## Features
- Filters the bundled IMDb movie dataset by language, genre, and release year.
- Applies vote-count thresholds before ranking to avoid obscure titles with few votes.
- Randomly samples from the top-rated slice to keep recommendations varied.
- Caches a preprocessed dataframe (`data/processed_data.pkl`) so subsequent runs return almost instantly and automatically rebuilds the cache if it becomes incompatible.
- Exposes an object-oriented API (`ImdbDataset`, `RecommendationSettings`, `MovieRecommender`) for programmatic use.

## Project Layout
```
.
├── data/                   # IMDb CSV exports + cached pickle
├── main.py                 # CLI entry point
├── requirements.txt        # Runtime dependencies (numpy, pandas)
└── what_movie/
    ├── model/
    │   └── imdb.py         # Dataset wrapper + recommender classes
    └── utils/
        ├── constants.py    # Default settings and column metadata
        └── paths.py        # Filesystem helpers
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

## Usage (CLI)

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
| `-f`, `--year_from` | Earliest release year to include. | `1894` |
| `-t`, `--year_to` | Latest release year to include. | `2020` |

Use `python main.py --help` to see the full argument list.

### Adjusting default filters
The recommender ships with sensible defaults defined in `what_movie/utils/constants.py` (see the `DEFAULT_SETTINGS` dataclass):
- `DEFAULT_LANGUAGES = ('english', 'hindi')  # case insensitive`
- `DEFAULT_GENRES = ('comedy', 'thriller', 'horror', 'sci-fi')  # case insensitive`
- `MIN_NUM_VOTES = 1000`
- `CONSIDER_TOP_N = 100`

Update those constants or instantiate your own `RecommendationSettings` to narrow the candidate pool or tweak how aggressively the app filters low-vote titles. Legacy aliases (`LANGUAGE_FILTER`, `GENRE_FILTER`, etc.) remain available for backwards compatibility.

Here is a list of all the movie languages and genres. Note that the values in the `DEFAULT_LANGUAGES` and `DEFAULT_GENRES` are case insensitive. The values can also be found in `data/unique_genres_languages.json`.

#### Languages:
```
Abkhazian, Aboriginal, Acholi, Afrikaans, Akan, Albanian, Algonquin, American Sign Language, Amharic, Ancient (to 1453), Apache languages, Arabic, Aragonese, Aramaic, Arapaho, Armenian, Aromanian, Assamese, Assyrian Neo-Aramaic, Athapascan languages, Australian Sign Language, Awadhi, Aymara, Azerbaijani, Bable, Balinese, Bambara, Basque, Belarusian, Bemba, Bengali, Berber languages, Bhojpuri, Bicolano, Bosnian, Brazilian Sign Language, Breton, British Sign Language, Bulgarian, Burmese, Cantonese, Catalan, Central American Indian languages, Chechen, Cheyenne, Chinese, Cornish, Corsican, Cree, Creek, Crimean Tatar, Croatian, Crow, Czech, Danish, Dari, Dinka, Dutch, Dyula, Dzongkha, Eastern Frisian, Egyptian (Ancient), English, Esperanto, Estonian, Ewe, Faroese, Filipino, Finnish, Flemish, French, French Sign Language, Frisian, Fulah, Gallegan, Georgian, German, German Sign Language, Greek, Greenlandic, Guarani, Gujarati, Gumatj, Haida, Haitian, Hakka, Haryanvi, Hassanya, Hausa, Hawaiian, Hebrew, Himachali, Hindi, Hmong, Hokkien, Hopi, Hungarian, Ibo, Icelandic, Indian Sign Language, Indonesian, Inuktitut, Irish, Italian, Japanese, Japanese Sign Language, Kabuverdianu, Kabyle, Kalmyk-Oirat, Kannada, Kashmiri, Kazakh, Khanty, Khmer, Kikuyu, Kinyarwanda, Kirghiz, Kirundi, Klingon, Konkani, Korean, Korean Sign Language, Kriolu, Kru, Kuna, Kurdish, Ladakhi, Ladino, Lao, Latin, Latvian, Lingala, Lithuanian, Low German, Luxembourgish, Macedonian, Maithili, Malay, Malayalam, Malinka, Maltese, Mandarin, Mandingo, Manipuri, Maori, Mapudungun, Marathi, Mari, Maya, Mende, Micmac, Middle English, Min Nan, Minangkabau, Mirandese, Mixtec, Mohawk, Mongolian, Montagnais, More, Nahuatl, Nama, Navajo, Neapolitan, Nenets, Nepali, Norse, North American Indian, Norwegian, Nyanja, Occitan, Ojibwa, Old, Old English, Oriya, Papiamento, Parsee, Pawnee, Persian, Peul, Polish, Polynesian, Portuguese, Pular, Punjabi, Purepecha, Pushto, Quechua, Quenya, Raeto-Romance, Rajasthani, Rhaetian, Romanian, Romany, Rotuman, Russian, Russian Sign Language, Ryukyuan, Saami, Samoan, Sanskrit, Sardinian, Scanian, Scots, Scottish Gaelic, Serbian, Serbo-Croatian, Shanghainese, Shanxi, Shona, Shoshoni, Sicilian, Sign Languages, Sindarin, Sindhi, Sinhalese, Sioux, Slovak, Slovenian, Somali, Songhay, Soninke, Southern Sotho, Spanish, Spanish Sign Language, Sranan, Swahili, Swedish, Swiss German, Syriac, Tagalog, Tajik, Tamashek, Tamil, Tarahumara, Tatar, Telugu, Teochew, Thai, Tibetan, Tigrigna, Tok Pisin, Tonga, Tswana, Tulu, Tupi, Turkish, Turkmen, Tzotzil, Uighur, Ukrainian, Ukrainian Sign Language, Ungwatsi, Urdu, Uzbek, Vietnamese, Visayan, Washoe, Wayuu, Welsh, Wolof, Xhosa, Yakut, Yiddish, Yoruba, Zulu
```

#### Genres:
```
Action, Adult, Adventure, Animation, Biography, Comedy, Crime, Documentary, Drama, Family, Fantasy, Film-Noir, History, Horror, Music, Musical, Mystery, News, Reality-TV, Romance, Sci-Fi, Sport, Thriller, War, Western
```

## Usage (Python API)

You can import the recommender from your own scripts:

```python
from what_movie.model import MovieRecommender, RecommendationSettings

settings = RecommendationSettings(
    languages=["english"],
    genres=["sci-fi", "thriller"],
    year_from=2000,
    year_to=2023,
    min_votes=5000,
)
recommender = MovieRecommender(settings=settings)
for movie in recommender.recommend(count=5):
    print(movie.title, movie.year, movie.rating)
```

## Regenerating the cached dataframe

To speed up subsequent runs, the first execution writes a processed pandas dataframe to `data/processed_data.pkl`. If you:
- upgrade pandas and encounter a pickle compatibility error (for example `AttributeError: Can't get attribute 'new_block'`), or
- want to rebuild the cache with modified filtering constants,

delete the pickle and run the CLI again (or call `ImdbDataset().invalidate_cache()`):

```bash
rm data/processed_data.pkl
python main.py
```

The dataframe will be reconstructed from the CSV sources using your current pandas version and constants. If the pickle cannot be read the project now refreshes it automatically.

## Development notes
- The core logic lives in `what_movie/model/imdb.py` and is covered by docstrings. Light inline comments call out the trickier parts of the pandas pipeline.
- `pylint` is listed in `requirements.txt` for linting; run `pylint what_movie` after making changes.
- There are no automated tests yet—consider adding unit tests around the filtering and sampling logic if you extend the project.

## License

This project is released under the [MIT License](LICENSE).
