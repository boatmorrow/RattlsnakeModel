###############################################################################
# Hydrologic Processing for GSFLOW GRID - surface flow routing
# Rattlesnake Modeling project
# W. Payton Gardner
# University of Montana
# Dept. of Geosciences
###############################################################################

#calculate flow accumulation and flow directions for the Rattlesnake GSFLOW model

#imports
import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pdb
import flopy
from gsflow.builder import GenerateFishnet
from gsflow.builder import FlowAccumulation


##################################################
# Input path management
##################################################

# set our cell size in meters.  #I'll start out with 100m for now, but will likely refine
cellsize=100
method = "nearest"

#model name
model_name = "RattlesnakeCreek_%3im"%cellsize+method

#toplevel ouput path
model_path = os.path.join("models",model_name)

#derived gis output path
gis_derived_path = os.path.join(model_path,"gis_deriv")

# define the modelgrid and resampled DEM data paths
mg_file = os.path.join(model_path, "grid.bin")

# Reprocessed, resampled DEM with SAGA needs to be used for flow accumulation
dem_data = os.path.join(gis_derived_path, "YourResampledFilledBurnedDEMName.tif")

#######################################################
#PROCESS FLOW ACCUMULATION
#######################################################

# load modelgrid
modelgrid = GenerateFishnet.load_from_file(mg_file)
#dem_data = np.genfromtxt(dem_data) #can be used to load an array

#load the post processed SAGA file
dem_data = flopy.utils.Raster.load(dem_data)
dem_data = dem_data.get_array(1)

# instantiate the FlowAccumulation object
fa = FlowAccumulation(
    dem_data,
    modelgrid.xcellcenters,
    modelgrid.ycellcenters,
    verbose=True
)

# use a small breaching tolerance and dijkstra's algorithm in this example
flow_directions = fa.flow_directions(dijkstra=True, breach=.001)

qx, qy = fa.get_vectors

# plot the flow directions as a quiver map
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1, aspect="equal")

pmv = flopy.plot.PlotMapView(modelgrid=modelgrid, ax=ax)
pmv.plot_array(
    dem_data, vmin=dem_data.min(), vmax=dem_data.max()
)
plt.quiver(modelgrid.xcellcenters, modelgrid.ycellcenters, qx, qy,scale=100)
plt.title("Rattlesnake 100m flow direction vectors")
plt.tight_layout()
plt.show()

# run flow accumulation
flow_accumulation = fa.flow_accumulation()

# plot the flow accumulation array
fig = plt.figure(figsize=(10, 8))
ax2 = fig.add_subplot(1, 1, 1, aspect="equal")

pmv = flopy.plot.PlotMapView(modelgrid=modelgrid, ax=ax2)
pmv.plot_array(
    dem_data, vmin=dem_data.min(), vmax=dem_data.max(), cmap='Greys'
)
pc = pmv.plot_array(flow_accumulation,alpha=0.4)

plt.title("Rattlesnake Creek %3i flow accumulation array" %cellsize)
plt.colorbar(pc, shrink=0.7)
plt.show()

##############################################
#Save GIS for later
##############################################
#flow dir
np.savetxt(
    os.path.join(gis_derived_path, "flowdir.txt"), 
    flow_directions.astype(int), 
    delimiter="  ", 
    fmt="%d")

np.savetxt(
    os.path.join(gis_derived_path, "flowacc.txt"),
    flow_accumulation,
    delimiter="  "
)

dfname = "DEMResampledFA.txt"
dem_file = os.path.join(gis_derived_path, dfname)

np.savetxt(dem_file, dem_data, delimiter="  ")
