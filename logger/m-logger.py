# magnetic field logger
# read freq from Pi Pico
import time
from datetime import datetime
import os.path
import serial

# to be config params
delay = 5
samples = 10
data_dir = "/home/pi/magneto/data/"

# globals
ser = serial.Serial('/dev/serial0', 115200, timeout=5)

def get_mag_log():
    i = 0
    avg_freq = 0
    cmd = 1
    # ser.reset_input_buffer()
    # time.sleep(0.01)
    # reqest batch of 10
    while i < samples:
        input = ser.read_until()
        sub_input = input.decode("utf-8").split(',')
        if len(sub_input) == 2:
            try:
                freq = float(sub_input[1])
            except ValueError:
                print("unable to convert float:", input)
                continue
            else:
                avg_freq = avg_freq + freq
                # print("i=%d   freq=%d" %(i, freq))
                i += 1
        else:
            print("read bad line: ", input)
    the_freq = avg_freq / samples
    # datetime object containing current date and time
    now = datetime.utcnow()
    # FITS format
    dt_string = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
    log_line = dt_string + ',' + str(the_freq) +'\n'
    # print(log_line, end="")
    return log_line

def do_logging():
    now = datetime.utcnow()
    start_day = now.day
    next_day = now.day
    date_dir_string = now.strftime("%Y/%m/")
    fn_string = now.strftime("%Y%m%d-M.csv")
    log_fname = data_dir + date_dir_string + fn_string
    if os.path.isdir(data_dir + date_dir_string):
        if not os.path.isfile(log_fname):
            with open(log_fname, "a+") as f:
                f.write('DateTime,Frequency\n')
        with open(log_fname, "a+") as f:
            while start_day == next_day:
                f.write(get_mag_log())
                f.flush()
                next_now = datetime.utcnow()
                next_day = next_now.day
                time.sleep(delay)
    else:
        os.makedirs(data_dir + date_dir_string, exist_ok=True)

if __name__ == "__main__":
   while True: do_logging()

