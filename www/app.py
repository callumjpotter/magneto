from flask import Flask
from flask import render_template, redirect
import astropy
from astropy.io import ascii
from astropy.time import Time
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import quantity_support
from astropy.visualization import time_support
import astropy.units as u
import os.path
from datetime import date, timedelta
import shutil


quantity_support() 
time_support() 

def do_T_plot(yyyymmdd=None):
    # work out input file name
    data_dir = '/home/pi/magneto/data/'
    if yyyymmdd:
        yyyy = yyyymmdd[0:4]
        mm = yyyymmdd[4:6]
        csvfile = data_dir + yyyy + '/' + mm + '/' + yyyymmdd + '-T.csv'
        plotfile = '/home/pi/magneto/www/static/plots/' + yyyymmdd + '-T.png'
        # print(csvfile)
        if os.path.isfile(csvfile):
            data = ascii.read(csvfile, format='csv')
            x = []
            y = []
            x = Time(data['DateTime'], format='fits')
            date_zero = x[0].to_value('iso', subfmt='date')
            midnight = Time(date_zero)
            x2 = (x - midnight).sec / 3600
            y = data['Temperature']
            # print(plotfile)
            plt.figure(figsize=(10,5))
            # plt.axis([0, 24, 0, 30])
            plt.xlim(0, 24)
            plt.plot(x2,y)
            plt.title('Bredons Hardwick Magnetometer (52.02N,2.13W)')
            plt.xlabel('Date Time ' + date_zero )
            plt.ylabel('Temperature [Celsius]')
            plt.savefig(plotfile, bbox_inches='tight')
        else:
            # copy no data file
            shutil.copyfile('/home/pi/magneto/www/static/no-data.png', plotfile)
    return


def do_M_plot(yyyymmdd=None):
    # work out input file name
    data_dir = '/home/pi/magneto/data/'
    if yyyymmdd:
        yyyy = yyyymmdd[0:4]
        mm = yyyymmdd[4:6]
        csvfile = data_dir + yyyy + '/' + mm + '/' + yyyymmdd + '-M.csv'
        plotfile = '/home/pi/magneto/www/static/plots/' + yyyymmdd + '-M.png'
        # print(csvfile)
        if os.path.isfile(csvfile):
            data = ascii.read(csvfile, format='csv')
            x = []
            y = []
            x = Time(data['DateTime'], format='fits')
            date_zero = x[0].to_value('iso', subfmt='date')
            midnight = Time(date_zero)
            x2 = (x - midnight).sec / 3600
            y = data['Frequency']
            # print(plotfile)
            plt.figure(figsize=(10,5))
            # plt.axis([0, 24, 0, 30])
            # plt.axis([0, 24, 64000, 68000])
            plt.xlim(0, 24)
            plt.plot(x2,y)
            plt.title('Bredons Hardwick Magnetometer (52.02N,2.13W)')
            plt.xlabel('Date Time ' + date_zero )
            plt.ylabel('Magnetic Field [Hz]')
            plt.savefig(plotfile, bbox_inches='tight')
        else:
            # copy no data file
            shutil.copyfile('/home/pi/magneto/www/static/no-data.png', plotfile)
    return           

app = Flask(__name__)

@app.route('/')
def index():
    tday = date.today()
    yyyymmdd = tday.strftime('%Y%m%d')
    return redirect('/display/' + yyyymmdd )

@app.route('/display/')
@app.route('/display/<yyyymmdd>')
def period(yyyymmdd=None):
    tplotfilename = yyyymmdd + '-T.png'
    mplotfilename = yyyymmdd + '-M.png'
    if not os.path.isfile('/home/pi/magneto/www/static/plots/' + tplotfilename):
        tplotfilename = 'no-image.png'
    if not os.path.isfile('/home/pi/magneto/www/static/plots/' + mplotfilename):
        mplotfilename = 'no-image.png'
    prevd = date(int(yyyymmdd[0:4]),int(yyyymmdd[4:6]),int(yyyymmdd[6:8])) - timedelta(days=1)
    prevday = prevd.strftime('%Y%m%d')
    nextd = date(int(yyyymmdd[0:4]),int(yyyymmdd[4:6]),int(yyyymmdd[6:8])) + timedelta(days=1)
    nextday = nextd.strftime('%Y%m%d')
    return render_template('display.html', date=yyyymmdd, mplotfile=mplotfilename, tplotfile=tplotfilename, prev=prevday, next=nextday)

@app.route('/gen/<yyyymmdd>')
def gen(yyyymmdd):
    do_T_plot(yyyymmdd)
    do_M_plot(yyyymmdd)
    return redirect('/display/' + yyyymmdd )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


