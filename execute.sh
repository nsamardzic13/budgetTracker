#!/bin/bash 

set -eo pipefail

# fake cicd :)
git pull 

TODAY=$(date +%Y-%m-%d)
HTML_FILE="output.html"
IPYNB_FILE="main.ipynb"
SUBJECT="Budget Report for ${TODAY}"

source .venv/bin/activate 
jupyter nbconvert --output ${HTML_FILE}  --no-input --to=HTML --execute ${IPYNB_FILE}
python send_email.py --subject "${SUBJECT}" --filename "${HTML_FILE}"

rm -f ${HTML_FILE}