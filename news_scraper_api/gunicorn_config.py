loglevel = "info"
errorlog = "gunicorn-error.log"
accesslog = "gunicorn-access.log"
worker_tmp_dir = "/dev/shm"
graceful_timeout = 120
timeout = 120
keepalive = 5
threads = 3
