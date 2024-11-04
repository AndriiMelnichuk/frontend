#!/bin/bash
CONDA_ENV="microservice"
export FLASK_APP=app.py
export FLASK_DEBUG="1"
export FLASK_ENV=deployment

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate $CONDA_ENV
flask run --reload 
