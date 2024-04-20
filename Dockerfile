#docker tag herecomesanewchallenger herecomesanewchallenger
#docker push herecomesanewchallenger

FROM python:3.10.2-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

EXPOSE 8000

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "main:app"]
#CMD [ "gunicorn", "main:app" ]
