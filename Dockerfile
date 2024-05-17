#docker tag herecomesanewchallenger herecomesanewchallenger
#docker push herecomesanewchallenger

FROM python:3.10.12-slim

WORKDIR /app

COPY requirements.txt .

# Ensure the system is up-to-date with the latest security updates
#RUN apt-get update && \
#    apt-get upgrade --assume-yes  

# Install the runtime dependencies using pip and additionally cache the dependencies to optimise build times
#RUN python -m pip install pip~=23.0 --upgrade --no-cache-dir
RUN pip install --requirement requirements.txt 

COPY ./app .


#CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "main:app"]
#CMD [ "gunicorn", "main:app" ]

# Perform a healthcheck to ensure the service is up and running
HEALTHCHECK --interval=5s --timeout=5s --retries=5 CMD healthcheck.sh

