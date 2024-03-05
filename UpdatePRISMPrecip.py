##############################################################################
# This script downloads last thirty years of mothly 4km PRISM data for climatology.
# Uses the pyPRISMClimate library
# Written By;
#  W. Payton Gardner
#  Dept. of Geosciences
#  University of Montana
###############################################################################

from pyPRISMClimate import *
import datetime as dt
import numpy as np

##################################################
# Input path management
##################################################

#top level data directory
data_dir = "/Users/payton.gardner/Library/CloudStorage/Box-Box/FRES/Working-Groups/ARs_22-23/PRISM_Precip"



##################################################
# Download Parameters
##################################################
#last 30 years 
ye = dt.datetime.now().year
mc = dt.datetime.now().month
wyears = np.arange(ye-30,ye+1,dtype=int).tolist() #because of zero based arange...

#all months
wmonths = np.arange(1,13,dtype=int).tolist()

#resolution
res = '4km'

##################################################
# Download Data
##################################################
print('getting ', res, ' PRISM monthlys')
# use prism iterator to download only the needed years and months
plist = prism_iterator(data_dir,recursive=True)

# loop through and download provisional data in case of update
for entry in plist:
    if (entry['status'] == 'provisional')&(entry['type']=='monthly'):
        print('downloading',entry['date_details']['year'],entry['date_details']['month'])
        get_prism_monthlys(variable='ppt', years=[entry['date_details']['year']], months=[entry['date_details']['month']], dest_path=data_dir )

#loop through wyears and wmonths, check to see if the year and month exist in the prism_iterator entries and download if they do not
for year in wyears:
    for month in wmonths:
        if year == ye:
            if month > mc:
                break
        if not any(year == entry['date_details']['year'] and month == entry['date_details']['month'] for entry in plist):
            print('downloading',year,month)
            get_prism_monthlys(variable='ppt', years=[year], months=[month], dest_path=data_dir)