## GSFLOW Modeling Notes

### 0) Prepare Datasets
We need some GIS data sets to get us started.  We'll need a DEM, flow lines, and a watershed boundary to start.  We'll need more as time goes on, but these are needed to get us started.  I've provided started data from USGS.  All of this data is in NAD83, geographic coordinates.  It needs to be project to a flat earth.  We can do this reprojection a variety of ways, but let's play with using python to do it.  Check out ReprojectWithPython.pynb. 

### 1) ProcessesFishNet.py Resampling Hydro Proc DEM using GSFLOW builder
This script resamples the DEM to a desired grid for simulation. 
* After we run this script, we'll have a resampled dem.  However, the resampling is going to create artifacts and needs to be processed for surface flow calculations.  We'll do this using the SAGA tool kit in QGIS.
*  Processing Steps in QGIS using SAGA:
    1. Fill Sinks -> needs: resampled dem; produces: filled dem
       * Use the planchon/darbou - minimun slope set to 0.01
    2. Catchment Area -> needs: filled dem: produces: upslope accumulated area
       * Use recursive, D8, no manual sinks.
    3. Channel Network -> needs: filled dem, upslope accumulated area (for initiation points); produces stream network (raster and shape)
       * Experiment with initiation threshold.  5e5 is a reasonable minimum starting point I've found. 
    4. Burn Stream Network
       * epsilion 0.5, method [1] -> needs filled dem, stream network raster, flow direction raster


### 2) ProcessSurfaceFlow.py - calculate Flowaccumulation and direction
* Does some further reprocessing of the DEM and then plots flow accumulation and flow directions using the GSFLOW utilities, to get everything ready for modflow/gsflow.

### 3) ProcessWatersheds.py - get full watershed, and subwatersheds.

### 4) Process Streams and Cascades

#### 5) MODFLOW - time to build the subsuface!

#### 6) MODFLOW SFR

#### MODFLOW SIMULATIONS

#### 7) SOIL
