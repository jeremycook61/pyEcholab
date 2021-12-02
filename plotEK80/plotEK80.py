import matplotlib.pyplot as plt
from echolab2.instruments import EK80
# for echogram fig
from echolab2.plotting.matplotlib import echogram
from echolab2.processing import afsc_bot_detector
import pandas as pd
import os

# For combined cm
import numpy as np
import colorsys
import matplotlib as mpl

def ensureDir(path): # create subdirectory to be used for plots
    if not os.path.exists(path):
        os.makedirs(path)

def combinedCM(N=52,plot=False):
    # Definition of LSSS's combined colormap
    # Start and end values from Inge Kristian Eliassen
    start = {'H':300,'S':0.1,'B':1}
    end = {'H':0,'S':1,'B':0.5}
    
    colorsHSB = {}
    for typ in start.keys():
        for k in range(N):
            colorsHSB[typ] = np.linspace(start[typ],end[typ],N)
            
    colorsRGB = []
    for k in range(N):
        colorsRGB.append(colorsys.hsv_to_rgb(colorsHSB['H'][k]/360.0,colorsHSB['S'][k],colorsHSB['B'][k]))
    
    mycmap =  mpl.colors.ListedColormap(colorsRGB, name='combined')
    
    if plot:
        plt.imshow([np.arange(0,1,0.01)]*10,aspect='auto',cmap=mycmap)
        
    return mycmap

def plotEK80(files,fig_obj=None, outfolder='.', nav_file=None):
    # FM data
    #files = glob.glob(f'{out_path}\*.raw')
    raw_filename = files
    name = os.path.splitext(os.path.basename(raw_filename))[0]


# Create an instance of the ek80 object.
    ek80obj = EK80.EK80()
    
    # Read the .raw data file.
    print('Reading raw file %s' % (raw_filename))
    ek80obj.read_raw(raw_filename)
    
    # Print some information about the state of the EK80 object.
    print(ek80obj)

    # Look for positional data
    raw_latlon_data = ek80obj.nmea_data.get_datagrams(['GGA', 'GLL'],
                                                   return_fields=['latitude',
                                                                  'longitude'])
    raw_lat = raw_latlon_data['GGA']['latitude']
    raw_lon = raw_latlon_data['GGA']['longitude']
    raw_time = raw_latlon_data['GGA']['time']
    nav_ds = pd.DataFrame(
        {'time': raw_time, 'longitude': raw_lon, 'latitude': raw_lat}
    )
    if not nav_file is None:
        if os.path.isfile(nav_file):
            nav_ds.to_csv(nav_file, mode='a', index = False, header=False)
        else:
            nav_ds.to_csv(nav_file,  index = False, header=True)



    #  info ~ num chans
    print("N channels = %d" % len(ek80obj.channel_ids))

    # Choose 70 kHz for plotting
    channel_id = ek80obj.channel_ids[1]

    ## Plot power from the specified ping from all channels.
    #for channel_id in ek80obj.channel_ids:
    
    # LSSS colors
    ek_cmap = combinedCM()
    ek_cmap.set_under('w', alpha=1.0)

    #  info ~ num chans
    print("N channels = %d" % len(ek80obj.channel_ids))
    fig = plt.figure()

    # Plot power from the specified ping from all channels.
    for channel_id in ek80obj.channel_ids:
        if channel_id in ek80obj.frequency_map[38000.0]: # Just processing 38kHz
            channel_name = channel_id.replace(" ", "_").replace("|", "_")
            channel_folder = os.path.join(outfolder, channel_name)
            out_filename= os.path.join(channel_folder, f'{name}_{channel_name}.png')
            ensureDir(channel_folder)
            # Get a reference to the raw data for this channel.
            raw_data = ek80obj.raw_data[channel_id][0]

            # Convert from raw power to Sv.
            Sv = raw_data.get_Sv()

            # Create echogram plot.
            # fig = plt.figure()
            plt.clf()
            eg = echogram.Echogram(fig, Sv, threshold=[-82, -30], cmap = ek_cmap)
            titstr = 'Sv Echogram, %s' % channel_id
            eg.axes.set_title( titstr )
            plt.savefig(out_filename)
            # fig.show()
            # End iteration through channel ids.