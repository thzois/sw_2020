FROM python:3.7.6

# install requirements
RUN pip install --no-cache-dir vaderSentiment
RUN pip install --no-cache-dir python-dotenv
RUN pip install --no-cache-dir git+https://github.com/tweepy/tweepy@premium-search
RUN pip install --no-cache-dir pandas-datareader
RUN pip install --no-cache-dir pycountry

# copy files
COPY data-analysis /data-analysis
WORKDIR /data-analysis

ARG DATA_ANALYSIS
RUN if [ "$DATA_ANALYSIS" = "true" ] ; then ./run_app.sh ; else echo "Bypassing data analysis"; fi
