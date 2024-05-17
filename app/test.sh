pip install -r requirements-dev.txt
docker compose -f docker-compose-dev.yml down -v
docker compose -f docker-compose-dev.yml up -d
sleep 5
python pytest -v tests/
docker compose -f docker-compose-dev.yml down -v
