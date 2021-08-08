# What movie should you watch tonight?
A simple app that recommends top-rated movies from IMDb.

# Setup
1. Clone repo.
```buildoutcfg
export PROJECTPATH=${HOME}/what-movie
git clone https://github.com/arathee2/what-movie.git ${PROJECTPATH}
```

2. Install [pyenv](https://github.com/pyenv/pyenv#installation) and Python 3.9.6 or higher.
```buildoutcfg
pyenv install 3.9.6
pyenv global 3.9.6
```

3. Setup virtual environment.
```buildoutcfg
export PYTHONPATH=${PYTHONPATH}:${PROJECTPATH}/
export VENVPATH=${HOME}/.what-movie
python -m venv $VENVPATH
source ${VENVPATH}/bin/activate
cd $PROJECTPATH
pip install -r requirements.txt
```

# Installation
The following command shows 3 movies to watch between 2010 and 2020.
```buildoutcfg
python main.py -n 3 -f 2010 -t 2020
```

# Uninstall
```buildoutcfg
deactivate
rm -r ${PROJECTPATH}
```