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
In order to get watershed boundaries for our new raster, we'll need to find appropriate pour points.  This is best done using QGIS.  Open up a map fill your filled, burned DEM, along with the Rattlesnake Flowlines shape file and the original Rattlesnake Watershed shapefile.  So, for some context, first of all the NHD flowlines that make up the Rattlesnake flowlines aren't perfect.  They were our best guess at the channel sometime in the past.  Riley knows that channels move.  They probably weren't correct everywhere to begin with.  But now, our DEM is not really the same as the real world any way, so we're going to have to do some sleuthing to find the correct pour points.  

#### Create Shapefiles in Q
1. Create a new layer: Layer->Create Layer->New Shapefile Layer
    * Call it Rattlesnake.shp or something
    * Make the geometry `point`
    * Make its coordinate system UTM 12N
    * Save it in your `data/gis/` folder
    * I add a field called `Drainage` where I will store an identifying name.
2. Find the pour point.
    * use the information pointer tool, to identify the lowest elevation cell at the mouth of the drainage.  
    * hint: I change the symbology of the DEM to pseudo color, and rescale the min-max to the current canvas after I zoomed into the area near the mouth.
    * Edit the shapefile
      * Add a point in the middle of cell of lowest elevation.
      * label the drainage "Main Rattlesnake Creek" or something like that
      * Save edits
3. Create another shapefile called RattlesnakeSubSheds.shp
    * Using the same procedure as above, add pour points for all branching drainages seen in flow lines (except the irrigation ditches).
    * The pour points need to be above the main Rattlesnake channel, but as close as you can get to it.  It takes some clicking around to figure out what's going on.
    * You can figure out the name of the subwatershed for labeling by using the information pointer on the flowlines shapes file.
    * Hint:  you might want to rescale the symbology occasionally to help visualize elevation differences near a given confluence.
#### Run ProcessWatershed.py
This script calculates the uplope areas for all your different pour points.  It it needs the name of your Rattlesnake pour point shape file made above and the subsheds shapefile name made above.  It should produce a figure with the different watershed areas, as well write some file for our use later.

### 4) Process Streams and Cascades

### 5) MODFLOW - time to build the subsurface!

### 6) MODFLOW SFR

### MODFLOW SIMULATIONS

#### 7) SOIL
