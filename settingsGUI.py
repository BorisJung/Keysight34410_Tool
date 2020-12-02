#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Simple GUI to execute measurements on Keysight 34410 digital multimeters"""
#
#
import os
from Keysight_34410_Measurements import *
from tkinter import *
#
# Doku infos
__author__ = "Boris Jung"
__version__ = "0.1"
__maintainer__ = "Boris Jung"
__email__ = "Boris.Jung@femto.de"
__status__ = "Prototype"
#
# Fenstergröße
w = 1000; h = 400
#
#
root = Tk()
root.title('Einstellungen')
root.configure()#background='black')
# root.state('zoomed')
#root.geometry("%dx%d+0+0" % (w, h))
#
fpath = StringVar()
fpath.set("Y:\\Messdaten_Ablage\\")
# DMM Adresse
DMM_IP_address = StringVar()
DMM_IP_address.set('10.53.51.119')
DMM_address = 'TCPIP0::' + DMM_IP_address.get() + '::inst0::INSTR'
# Range setting DMM
V_range = 10.0 # 0.1, 1, 10, 100, 1000, AUTO
NoPoints = IntVar()
NoPoints.set(100)
dt = DoubleVar()
dt.set(0.5)
tMeas = DoubleVar()
tMeas.set("{:.2f}".format(NoPoints.get() * dt.get() / 3600))
measType = StringVar()
measType.set('DC Spannung')
messFunktionen = ['DC Spannung', 'Frequenz']
ylim_unten = DoubleVar()
ylim_unten.set(0)
ylim_oben = DoubleVar()
ylim_oben.set(0)

#
def call_meas(event=None):
    if measType.get() == 'DC Spannung':
        if ylim_unten.get() == 0 and ylim_oben.get() == 0:
            print('auto grenzen')
            longt_DCV(NoPoints.get(), dt.get(), DMM_address, V_range, fpath.get())
        else:
            longt_DCV(NoPoints.get(), dt.get(), DMM_address, V_range, fpath.get(), ylim_unten.get(), ylim_oben.get())
    elif measType.get() == 'Frequenz':
        if ylim_unten.get() == 0 and ylim_oben.get() == 0:
            longt_FREQ(NoPoints.get(), dt.get(), DMM_address, V_range, fpath.get())
        else:
            longt_FREQ(NoPoints.get(), dt.get(), DMM_address, V_range, fpath.get(), ylim_unten.get(), ylim_oben.get())
#
#
# Berechnung der Gesamtzeit
def calc_tMeas(*args):
    try:
        NoP = float(NoPoints.get())
        deltaT = float(dt.get())
    except ValueError:
        return
    tMeas.set("{:.2f}".format(NoP * deltaT / 3600))

#
# Variablen tracen (Eingaben in den Textfeldern führen zu live updates)
dt.trace("w", calc_tMeas)
NoPoints.trace("w", calc_tMeas)
#
# Header Text Label
explanation = """Keysight 34410 DMM \nLangzeit Messung"""
w1 = Label(root, justify=CENTER, padx = 10, text=explanation, font = "Arial 16 bold")#.pack(side="top")
w1.grid(row=0, column=0, columnspan=5, sticky='n')
#
# Versionsnummer Text Label
w2 = Label(root, padx = 10, text='v' + __version__, font = "Arial 8")#.pack(side="top")
w2.grid(row=0, column=6, columnspan=1, sticky='e')
#
#
# Eingabefeld DMM Adresse
l_IP_add = Label(root, text='DMM IP-Adresse: ', anchor="e")
l_IP_add.grid(row=1, column=1, sticky="e")
e_IP_add = Entry(root, textvariable=DMM_IP_address)
e_IP_add.grid(row=1, column=3, sticky="e")
#
# Dropdown Menü für Messfunktion erstellen, füllen und anzeigen
l_ddMenu = Label(root, text='Messfunktion:', anchor="e")
l_ddMenu.grid(row=2, column=1, sticky="e")
ddMenu = OptionMenu(root, measType, *messFunktionen) # * wird zum auspacken des containers (/List) verwendet
ddMenu.grid(row=2, column=3, columnspan=1, sticky='w')
#
#
# Eingabefeld Speicherort
l_fpath = Label(root, text='Speicherort: ', anchor="e")
l_fpath.grid(row=4, column=1, sticky="e")
e_fpath = Entry(root, textvariable=fpath)
e_fpath.grid(row=4, column=3, sticky="e")
#
# Eingabefeld Anzahl Punkte
l_NoPoints = Label(root, text='Anzahl Messpunkte:', anchor="e")
l_NoPoints.grid(row=6, column=1, sticky="e")
e_NoPoints = Entry(root, textvariable=NoPoints)
e_NoPoints.grid(row=6, column=3, sticky="e")
#
# Eingabefeld Zeitabstand zwischen zwei Punkten
l_dt = Label(root, text='Zeitlicher Abstand [s]:')
l_dt.grid(row=8, column=1, sticky="e")
e_dt = Entry(root, textvariable=dt)
e_dt.grid(row=8, column=3, sticky="e")
#

#
# Label mit berechneter Gesamtdauer der Messung
l_tM = Label(root, text="Gesamtdauer der Messung [h]: ")
l_tM.grid(row=9, column=1, columnspan=1, sticky="e")
l_tMeas = Label(root, textvariable=tMeas)
l_tMeas.grid(row=9, column=3, columnspan=1, sticky="w")
#
#
# Eingabefeld Y-Achsen Grenzen
l_ylim = Label(root, text='Y-Achsen Grenze unten:')
l_ylim.grid(row=10, column=1, sticky="e")
e_ylim = Entry(root, textvariable=ylim_unten)
e_ylim.grid(row=10, column=3, sticky="e")
l_ylim = Label(root, text='Y-Achsen Grenze oben:')
l_ylim.grid(row=11, column=1, sticky="e")
e_ylim = Entry(root, textvariable=ylim_oben)
e_ylim.grid(row=11, column=3, sticky="e")
#
#
# START Button
startbutton = Button(root, text="START", command=call_meas)
startbutton.grid(row=13, column=1, columnspan=1)
root.bind('<Return>', call_meas)
#
# QUIT Button
quitbutton = Button(root, text="Beenden", command=root.quit)
quitbutton.grid(row=13, column=3, columnspan=1, sticky='s')
root.bind('<Escape>', lambda x: root.destroy())
#
#
# Grid Einstellungen (Leer-Reihen etc.)
root.grid_rowconfigure(3, minsize=20)
root.grid_rowconfigure(5, minsize=20)
root.grid_rowconfigure(8, minsize=20)
root.grid_rowconfigure(9, minsize=20)
root.grid_rowconfigure(11, minsize=20)
root.grid_rowconfigure(12, minsize=20)
root.grid_rowconfigure(14, minsize=20)
root.grid_columnconfigure(0, minsize=60)
root.grid_columnconfigure(2, minsize=20)
root.grid_columnconfigure(4, minsize=60)
#
# Main Loop
root.mainloop()