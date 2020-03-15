#!/bin/bash

if [ "$DATA_ANALYSIS" = "true" ]; then 
    # remove old html pages
    rm /web-app/event*.html
    rm /web-app/results/sentiment/*.json
    rm /web-app/results/world/*.json

    # python data_retrieval.py
    # python clean_and_sentiment.py
    # python topic_analysis.py
    python prepare_app.py
else 
    echo "Bypassing data analysis";
fi