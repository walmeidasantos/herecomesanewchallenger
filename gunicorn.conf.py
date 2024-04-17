from dotenv import dotenv_values
config = dotenv_values(".env")

bind = config['GUNICORN_BIND']
workers = config['GUNICORN_WORKERS']
worker_class = 'uvicorn.workers.UvicornWorker'
keepalive = config['GUNICORN_KEEPALIVE']
forwarded_allow_ips = config['GUNICORN_FORWARDED_ALLOW_IPS']
