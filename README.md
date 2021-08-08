# What movie should you watch tonight?
A simple app that recommends top-rated movies from IMDb.

# Setup
1. Clone repo.
```buildoutcfg
export PROJECTPATH=${HOME}/what-movie
git clone https://github.com/arathee2/what-movie.git ${PROJECTPATH}
```

2. [OPTIONAL] Install `pyenv` by following [these](https://github.com/pyenv/pyenv#installation) instructions and install Python 3.
```buildoutcfg
pyenv install 3.9.6
pyenv global 3.9.6
```

3. Setup virtual environment.
```buildoutcfg
export PYTHONPATH=${PYTHONPATH}:${PROJECTPATH}/
export VENVPATH=${HOME}/.what-movie
python3 -m venv $VENVPATH
source ${VENVPATH}/bin/activate
pip install -r ${PROJECTPATH}/requirements.txt
```

# Run
The following command shows 3 movies to watch between 2010 and 2020. Output is stochastic and always shows high-rated movies.
```buildoutcfg
python3 ${PROJECTPATH}/main.py -n 3 -f 2010 -t 2020
```

Running the command for the first time takes a few seconds (~10 seconds on a MacBook Pro 13") but subsequent runs display the output instantaneously.

# Usage
```buildoutcfg
python3 ${PROJECTPATH}/main.py --help
```

# Add Filters
Set `LANGUAGE_FILTER` and `GENRE_FILTER` [here](https://github.com/arathee2/what-movie/blob/main/what_movie/utils/constants.py) to show movies that meet these criteria.

# Uninstall
```buildoutcfg
deactivate
rm -r $PROJECTPATH
rm -r $VENVPATH
```

Shoot an email to arathee2@gmail.com for feedback.
