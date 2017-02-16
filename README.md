# Create a Flow Table from adjacent Watershed Basins

![flowtable](https://cloud.githubusercontent.com/assets/7052993/23041753/d67abf22-f44a-11e6-965d-cc83a8314089.PNG)

The image above describes lake boundaries and their respective watershed basins  


The array_shift script will creae a flow table of zone connections from a zone raster by comparing it's shifted values with a flow direction raster. The output being a flowtable like you see in the image above. Adjacent zones which flow into one another are connected through the ID given to the zone.

### Input Data:
* Zone Raster -
  + local - area basins to a given group of pour points
* Flow Direction Raster (fdr) -
  + raster of flow direction from each cell to its steepest downslope neighbor
