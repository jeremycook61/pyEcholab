
"""This a simple example showing how to use the PyQt based echogram_viewer
which is a high level interface to the AFSC QImageViewer library.

This example reads a .raw file, gets Sv, detects bottom, and plots the
echogram and the bottom line.

The data file contains 19066 pings so it is a good test of the pyEcholab
qt plotting libraries. You will need to zoom into the echogram to see the
bottom line. You can pan using the scroll bars or by holding <ALT> and
clicking and dragging.

The QImageViewer library Requires PyQt5.

Controls:

    <CTRL> + Mouse Wheel zooms in/out
    <ALT> + Click and drag will pan


"""

import sys
from matplotlib import pyplot as plt
from PyQt5 import QtWidgets
from echolab2.instruments import EK80
# from echolab2.instruments import EK80
from echolab2.plotting.qt import echogram_viewer
from echolab2.processing import afsc_bot_detector
from echolab2.plotting.matplotlib import echogram

import os


def read_write_callback(filename, cumulative_pct, cumulative_bytes, userref):
    '''
    read_write_callback is a simple example of using the progress_callback
    functionality of the EK60.read_raw and EK60.write_raw methods.
    '''

    if cumulative_pct > 100:
        return

    if cumulative_pct == 0:
        sys.stdout.write(filename)

    if cumulative_pct % 4:
        sys.stdout.write('.')

    if cumulative_pct == 100:
        sys.stdout.write('  done!\n')



# Specify a raw file. This file is big, it takes a bit to load and display.
# rawfiles = ['./data/ES60/L0059-D20140518-T181425-ES60.raw']
rawfiles = ["H:\OOE-EK80Data\D20210810-T050839.raw",
            "H:\OOE-EK80Data\D20210820-T220338.raw",
            "H:\OOE-EK80Data\D20210821-T020658.raw"]
# rawfiles = [
#             "H:\OOE-EK80Data\D20210820-T220338.raw"]
# Create an instance of the EK60 instrument.
# ek60 = EK60.EK60()
ek80 = EK80.EK80()

for raw in rawfiles:
    fig = plt.figure()

    # Read the data. -
    name = os.path.splitext(os.path.basename(raw))[0]
    print('Reading raw file {}:'.format(name))
    # ek60.read_raw(rawfiles, progress_callback=read_write_callback,
    #         frequencies=38000)
    ek80.read_raw(raw, progress_callback=read_write_callback)

    # Get the 38 kHz raw data.
    print('Getting Sv...')
    raw_data = ek80.get_channel_data(frequencies=38000)
    raw_data_38 = raw_data[38000][0]
    print(raw_data_38)

    # Get a calibration object - This returns a cal object that
    # is populated with data from the .raw file. You can change
    # the values as needed.
    cal_obj = raw_data_38.get_calibration()
    cal_obj.transducer_draft = 50

    # Get Sv data.
    Sv_38 = raw_data_38.get_Sv(calibration=cal_obj, return_depth=True)

    # Ccreate an instance of our bottom detector and apply to our data.
    # Note that our data is in depth and Sv so we provide a search
    # min in depth and a backstep in Sv
    print('Running bottom detector...')
    bot_detector = afsc_bot_detector.afsc_bot_detector(search_min=2,
            backstep=35)
    detected_bottom = bot_detector.detect(Sv_38)

    #  set our bottom line cosmetic properties
    detected_bottom.color = [225,200,0]
    detected_bottom.thickness = 2

    print(f'Plotting... {name}.png')
    # Create an axis.
    ax_1 = fig.add_subplot(1, 1, 1)
    echogram_2 = echogram.Echogram(ax_1, Sv_38)
    # plt.show()
    plt.savefig(f'{name}.png')

    # Start event processing.
    # app.exec_()
