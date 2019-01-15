#app_python_team_classify
FROM python:3.7

WORKDIR /usr/src/app

# Install any needed packages specified in requirements.txt
# COPY pyinstall.txt ./


# Copy the project source code from the local host to the filesystem of
COPY . .



## Install phantomjs
RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    tar -jxf phantomjs-2.1.1-linux-x86_64.tar.bz2 && cp phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs


RUN pip install --no-cache-dir selenium beautifulsoup4 pandas matplotlib lxml

# Expose port
# EXPOSE 5000

# Define environment variable
ENV NAME app  

CMD [ "python", "run.py" ]
# CMD [ "python", "app.py" ]