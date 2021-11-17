import matplotlib.pyplot as plt
from echolab2.instruments import EK80
# for echogram fig
from echolab2.plotting.matplotlib import echogram
from echolab2.processing import afsc_bot_detector

def plotEK80(files,fig_obj=None):
    # FM data
    #files = glob.glob(f'{out_path}\*.raw')
    raw_filename = files
    
    # Create an instance of the ek80 object.
    ek80obj = EK80.EK80()
    
    # Read the .raw data file.
    print('Reading raw file %s' % (raw_filename))
    ek80obj.read_raw(raw_filename)
    
    # Print some information about the state of the EK80 object.
    print(ek80obj)
    
    #  info ~ num chans
    print("N channels = %d" % len(ek80obj.channel_ids))

    # Choose 70 kHz for plotting
    channel_id = ek80obj.channel_ids[1]

    ## Plot power from the specified ping from all channels.
    #for channel_id in ek80obj.channel_ids:
    
    #  info ~ num chans
    print("N channels = %d" % len(ek80obj.channel_ids))

    # Plot power from the specified ping from all channels.
    for channel_id in ek80obj.channel_ids:

        # Get a reference to the raw data for this channel.
        raw_data = ek80obj.raw_data[channel_id][0]

        # Convert from raw power to Sv.
        Sv = raw_data.get_Sv()

        # Create echogram plot.
        fig = plt.figure()
        eg = echogram.Echogram(fig, Sv, threshold=[-82, -30])
        titstr = 'Sv Echogram, %s' % channel_id
        eg.axes.set_title( titstr )

        fig.show()

        # End iteration through channel ids.