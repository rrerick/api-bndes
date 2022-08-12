# Gunicorn configuration file
# https://docs.gunicorn.org/en/stable/configure.html#configuration-file
# https://docs.gunicorn.org/en/stable/settings.html
import multiprocessing

max_requests = 1000
max_requests_jitter = 50
bind = '0.0.0.0:8000'
log_file = "-"

workers = multiprocessing.cpu_count() * 2 + 1