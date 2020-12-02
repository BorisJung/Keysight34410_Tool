#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" This module contains various functions for (triggered) measurements using the Keysight 34410 DMM
"""
# Imports
import pyvisa as visa
import csv
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

def longt_DCV(AnzahlPunkte, dt, DMM_address, V_range, fpath, *args):
    print(args)
    # Timestamp
    tStamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # VISA
    rm = visa.ResourceManager()
    multimeter = rm.open_resource(DMM_address)
    multimeter.write('*RST') # Reset
    multimeter.write('*CLS') # Clear Event Register
    multimeter.write(':CONFigure:SCALar:VOLTage:DC %G' % (V_range)) # Set DMM to DC Voltage measurement mode with specified range
    multimeter.write(':TRIGger:SEQuence:SOURce %s' % ('IMMediate')) # Set Trigger mode to immediate triggering after placement into "wait-for-trigger" mode
    #multimeter.write(':TRIGger:SEQuence:DELay %G' % (0.00002)) # Set Trigger delay
    multimeter.write(':SAMPle:COUNt %d' % (1)) # Set the number of readings/samples the meter takes per trigger
#
    readings = [] # initialise list variable
    plt.figure() # create plot figure
#
    # Measurement Loop
    while (AnzahlPunkte != 0):
        t = time.time()
        # Take a measurement value
        multimeter.write(':INITiate:IMMediate')
        temp_values = multimeter.query_ascii_values(':FETCh?')
        readings.append(temp_values[0])
        # live plotting
        plt.clf()
        if args:
            plt.ylim(args[0], args[1])
        plt.plot(np.linspace(0,(len(readings)-1)*dt,len(readings),endpoint=True),readings)
        plt.grid(True)
        plt.xlabel("Zeit in s"); plt.ylabel("Spannung in V"); plt.tight_layout()
        elapsed = time.time() - t
        print(elapsed)
        if dt > elapsed:
            pauseT = dt - elapsed
            plt.pause(pauseT)
        else:
            pauseT = 0
            plt.pause(1e-3)
        print(pauseT)

        AnzahlPunkte -= 1 # decrementing loop variable
#
    fig_name = fpath + tStamp + "___DC_Messergebnisse" # filename for figure saved as .png
    plt.savefig(fig_name) # save figure
    multimeter.close() # close connection to device
    rm.close() # close VISA resource manager
#
    # Printout and csv-export
    print(readings)
#
    filename = fpath + tStamp + "___DC_Messergebnisse.csv"
    with open(filename, 'w') as out_f: # Python 3
        w = csv.writer(out_f, lineterminator='\n')        # override for tab delimiter
        for val in readings:
            w.writerow([val])

def longt_FREQ(AnzahlPunkte, dt, DMM_address, V_range, fpath, *args):
    print(args)
    # Timestamp
    tStamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # VISA
    rm = visa.ResourceManager()
    multimeter = rm.open_resource(DMM_address)
    multimeter.write('*RST')
    multimeter.write('*CLS')
    multimeter.write(':CONFigure:SCALar:FREQuency %G' % (13500.0))
    multimeter.write(':TRIGger:SEQuence:SOURce %s' % ('IMMediate'))
    #multimeter.write(':TRIGger:SEQuence:DELay %G' % (0.01))
    multimeter.write(':SAMPle:COUNt %d' % (1))
    readings = []
    plt.figure()
    while (AnzahlPunkte != 0):
        multimeter.write(':INITiate:IMMediate')
        temp_values = multimeter.query_ascii_values(':FETCh?')
        readings.append(temp_values[0])
        print(readings)
        # plotten während der Messung
        plt.clf()
        if args:
            plt.ylim(args[0], args[1])
        plt.plot(np.linspace(0,(len(readings)-1)*dt,len(readings),endpoint=True),readings)
        plt.grid(True)
        plt.xlabel("Zeit in s"); plt.ylabel("Frequenz in Hz"); plt.tight_layout()
        plt.pause(dt)
        AnzahlPunkte -= 1
        #
    # end of M3441x_Triggered_Measure
    print(readings)
    #
    fig_name = fpath + tStamp + "___FREQ_Messergebnisse"  # filename for figure saved as .png
    plt.savefig(fig_name)  # save figure
    multimeter.close()  # close connection to device
    rm.close()  # close VISA resource manager
    #
    #
    filename = tStamp + "___FREQ_Messergebnisse.csv"
    with open(filename, 'w') as out_f: # Python 3
        w = csv.writer(out_f, delimiter=";")        # override for tab delimiter
        w.writerow(readings)