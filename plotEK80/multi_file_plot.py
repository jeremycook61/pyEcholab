import plotEK80 as pek80
import glob
import os


# rawfiles = ["H:\OOE-EK80Data\D20210810-T050839.raw",
#             "H:\OOE-EK80Data\D20210820-T220338.raw",
#             "H:\OOE-EK80Data\D20210821-T020658.raw"]

out_path = "H:\\OOE-EK80-OUTPUT"
nav_file = os.path.join(out_path, "navigation.csv")

data_path = "H:\\OOE-EK80Data"
rawfiles = glob.glob(os.path.join(data_path, '*.raw'))
# rawfiles = ["H:\OOE-EK80Data\D20210824-T195424.raw"]

if __name__ == '__main__':

    for raw in rawfiles:
        pek80.plotEK80(raw, outfolder="H:\OOE-EK80-OUTPUT", nav_file=nav_file)