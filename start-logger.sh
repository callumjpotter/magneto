#!/bin/bash
sleep 10
cd /home/pi/magneto/www
nohup /usr/bin/python3 ./app.py > app.out &
cd /home/pi/magneto/logger
nohup /usr/bin/python3 ./m-logger.py > m-logger.out &
nohup /usr/bin/python3 ./t-logger.py > t-logger.out &


