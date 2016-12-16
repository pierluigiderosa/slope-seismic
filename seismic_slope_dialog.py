# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SeismicSlopeDialog
                                 A QGIS plugin
 QGIS tool for locate instable zone for 1 level of seismic microzonation

                             -------------------
        begin                : 2016-11-04
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Pierluigi De Rosa
        email                : pierluigi.derosa@gfosservices.it
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic

from qgis._core import QgsMapLayer
from qgis._core import QgsMapLayerRegistry

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'seismic_slope_dialog_base.ui'))


class SeismicSlopeDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(SeismicSlopeDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        #self.shapeButton.clicked.connect(self.writeTxt)
        self.setupUi(self)
        self.setup_gui()


    def setup_gui(self):
        """ Function to combos creation """
        self.shapeButton.clicked.connect(self.writeTxt)
        self.rasterCombo.clear()
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        layerRasters = []
        layerVectors = []
        for layer in layers:
            if layer.type() == QgsMapLayer.RasterLayer:
                self.rasterCombo.addItem(layer.name(), layer)


    def writeTxt(self):
        """Function to writhe the path for shapefile"""
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save SHP file',
                                               "", ".shp (*.shp);;All files (*)")
        fileName = os.path.splitext(str(fileName))[0] + '.shp'
        self.shapeSave.setText(fileName)
        self.textfile = fileName

