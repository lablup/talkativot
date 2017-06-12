#!/bin/bash
export TALKATIVOT_DEV_MODE=0
export TALKATIVOT_TELEGRAM_TOKEN = str(os.environ.get('TALKATIVOT_TELEGRAM_TOKEN', ''))
export TALKATIVOT_VENV=/TALKATIVOT/venv
eval "$(pyenv init -)"
pyenv shell 3.6.1
source $TALKATIVOT_VENV/bin/activate
python3 /TALKATIVOT/serve/nest.py
