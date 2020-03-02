#!/bin/bash

python data_retrieval.py
python clean_data.py
python sentiment_analysis.py
python generate_html.py