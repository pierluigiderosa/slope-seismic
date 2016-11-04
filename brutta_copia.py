fileName = "/home/pierluigi/Sviluppo/slope-seismic/test_data/dtm20.asc"
fileInfo = QFileInfo(fileName)
baseName = fileInfo.baseName()
rlayer = QgsRasterLayer(fileName, baseName)
if not rlayer.isValid():
  print "Layer failed to load!"
  
rlayer.rasterType()
#algoritmo processing
processing.alghelp("gdalogr:slope")

outRaster = '/tmp/out.tif'

processing.runalg("gdalogr:slope", rlayer, 1, True, True, False, 1.0, outRaster)
