#docker tag herecomesanewchallenger herecomesanewchallenger
#docker push herecomesanewchallenger

FROM python:3.10.2-slim

WORKDIR /app

COPY requirements.txt .

# Ensure the system is up-to-date with the latest security updates
RUN apt-get update && \
    apt-get upgrade --assume-yes && \
    # cURL is necessary to invoke the "healthcheck" function using Docker
    apt-get install curl --assume-yes && \
    rm --recursive --force /var/lib/apt/lists/*

# Install the runtime dependencies using pip and additionally cache the dependencies to optimise build times
RUN --mount=type=cache,target=/root/.cache \
    python -m pip install pip~=23.0 --upgrade --no-cache-dir \
    --disable-pip-version-check --no-compile && \
    python -m pip install --requirement "requirements.txt" \
    --require-hashes --no-cache-dir --disable-pip-version-check --no-compile && \
    rm --force "requirements.txt"

COPY ./app .

EXPOSE 8000

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "main:app"]
#CMD [ "gunicorn", "main:app" ]

# Perform a healthcheck to ensure the service is up and running
HEALTHCHECK --interval=5s --timeout=5s --retries=5 CMD curl --include --request GET http://localhost:8000/healthcheck || exit 1

