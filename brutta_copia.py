fileName = "/home/pierluigi/Sviluppo/slope-seismic/test_data/dtm20.asc"
fileInfo = QFileInfo(fileName)
baseName = fileInfo.baseName()
rlayer = QgsRasterLayer(fileName, baseName)
if not rlayer.isValid():
  print "Layer failed to load!"
  
rlayer.rasterType()
#algoritmo processing
processing.alghelp("gdalogr:slope")

outRaster = processing.runalg("gdalogr:slope", rlayer, 1, True, True, False, 1.0, None)


out1=processing.runalg('gdalogr:rastercalculator',
                       slopeLayer,'1',
                       None,'1',None,'1',None,'1',None,'1',None,'1',
                       '1*(A>15)',None,5,None,None)

out1=processing.runalg('gdalogr:rastercalculator',
                       rlayer,'1', #A
                       None,'1', #B
                       None,'1', #C
                       None,'1', #D
                       None,'1', #E
                       None,'1', #F
                       '5*(A>350.0)', #formula
                       '-9999',
                       5,
                       None,
                       '/tmp/pippo3.tif')


out2 = processing.runalg('gdalogr:sieve',
                         outSelection['OUTPUT'],
                         20,
                         0,
                         output
                         )

processing.alghelp('gdalogr:polygonize')
ALGORITHM: Polygonize (raster to vector)
	INPUT <ParameterRaster>
	FIELD <ParameterString>
	OUTPUT <OutputVector>


>> processing.alghelp('gdalogr:translate')
ALGORITHM: Translate (convert format)
	INPUT <ParameterRaster>
	OUTSIZE <ParameterNumber>
	OUTSIZE_PERC <ParameterBoolean>
	NO_DATA <ParameterString>
	EXPAND <ParameterSelection>
	SRS <ParameterCrs>
	PROJWIN <ParameterExtent>
	SDS <ParameterBoolean>
	RTYPE <ParameterSelection>
	COMPRESS <ParameterSelection>
	JPEGCOMPRESSION <ParameterNumber>
	ZLEVEL <ParameterNumber>
	PREDICTOR <ParameterNumber>
	TILED <ParameterBoolean>
	BIGTIFF <ParameterSelection>
	TFW <ParameterBoolean>
	EXTRA <ParameterString>
	OUTPUT <OutputRaster>


EXPAND(Espandi)
	0 - none
	1 - gray
	2 - rgb
	3 - rgba
RTYPE(Tipo di raster in uscita)
	0 - Byte
	1 - Int16
	2 - UInt16
	3 - UInt32
	4 - Int32
	5 - Float32
	6 - Float64
COMPRESS(Opzioni GeoTIFF. Tipo compressione:)
	0 - NONE
	1 - JPEG
	2 - LZW
	3 - PACKBITS
	4 - DEFLATE
BIGTIFF(Verifica se il file creato è un BigTIFF o un TIFF classico)
	0 -
	1 - YES
	2 - NO
	3 - IF_NEEDED
	4 - IF_SAFER