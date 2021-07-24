import time
from w1thermsensor import W1ThermSensor
from datetime import datetime
import os.path

# to be config params
delay = 1
samples = 10
data_dir = "/home/pi/magneto/data/"

# globals
sensor = W1ThermSensor()

def get_temp_log():
    i = 0
    avg_temp = 0
    while i < samples:
        temperature = sensor.get_temperature()
        avg_temp = avg_temp + temperature
        # print("i=%d   temp=%d" %(i, temperature))
        time.sleep(delay)
        i += 1
    the_temp = avg_temp / samples
    # datetime object containing current date and time
    now = datetime.utcnow()
    # FITS format
    dt_string = now.strftime("%Y-%m-%dT%H:%M:%S")
    log_line = dt_string + ',' + str(the_temp) +'\n'
    # print(log_line, end="")
    return log_line

def do_logging():
    now = datetime.utcnow()
    start_day = now.day
    next_day = now.day
    date_dir_string = now.strftime("%Y/%m/")
    fn_string = now.strftime("%Y%m%d-T.csv")
    log_fname = data_dir + date_dir_string + fn_string
    if os.path.isdir(data_dir + date_dir_string):
        if not os.path.isfile(log_fname):
            with open(log_fname, "a+") as f:
                f.write('DateTime,Temperature\n')
        with open(log_fname, "a+") as f:
            while start_day == next_day:
                f.write(get_temp_log())
                f.flush()
                next_now = datetime.utcnow()
                next_day = next_now.day
    else:
        os.makedirs(data_dir + date_dir_string, exist_ok=True)

if __name__ == "__main__":
   while True: do_logging()

