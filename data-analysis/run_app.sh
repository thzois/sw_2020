#!/bin/bash

# remove old html pages
rm /web-app/event*.html

# python data_retrieval.py
# python clean_and_sentiment.py
python prepare_app.py