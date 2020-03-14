FROM python:3.7.6

# install requirements
RUN pip install --no-cache-dir vaderSentiment
RUN pip install --no-cache-dir python-dotenv
RUN pip install --no-cache-dir git+https://github.com/tweepy/tweepy@premium-search
RUN pip install --no-cache-dir pandas-datareader
RUN pip install --no-cache-dir pandas
RUN pip install --no-cache-dir pycountry
RUN pip install --no-cache-dir pycountry_convert
RUN pip install --no-cache-dir textblob
RUN pip install --no-cache-dir gensim
RUN pip install --no-cache-dir nltk
RUN pip install --no-cache-dir pyLDAvis
RUN pip install --no-cache-dir spacy
RUN python -m spacy download en
RUN pip install --no-cache-dir pyenchant
RUN apt update && apt-get install -y libenchant-dev 

# copy files
COPY data-analysis /data-analysis
COPY web-app /web-app
WORKDIR /data-analysis

ARG DATA_ANALYSIS
RUN if [ "$DATA_ANALYSIS" = "true" ] ; then ./run_app.sh ; else echo "Bypassing data analysis"; fi
