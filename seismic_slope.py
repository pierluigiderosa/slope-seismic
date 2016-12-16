# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SeismicSlope
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
from qgis.utils import iface

from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from qgis.gui import QgsMessageBar
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from seismic_slope_dialog import SeismicSlopeDialog
import os.path
import processing
from tempfile import mkdtemp,TemporaryFile


class SeismicSlope:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SeismicSlope_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Seismic slope tool')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'SeismicSlope')
        self.toolbar.setObjectName(u'SeismicSlope')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SeismicSlope', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = SeismicSlopeDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToRasterMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/SeismicSlope/slide_32.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Slope Seismic'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginRasterMenu(
                self.tr(u'&Seismic slope tool'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()

        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            index = self.dlg.rasterCombo.currentIndex()
            rlayer = self.dlg.rasterCombo.itemData(index)
            shapeFinal = self.dlg.shapeSave.text()
            self.iface.messageBar().pushMessage("Layer", rlayer.name(),
                                           level=QgsMessageBar.WARNING)
            if not rlayer.isValid():
                self.iface.messageBar().pushMessage("ERROR:", rlayer.name()+' is not valid',
                                                    level=QgsMessageBar.ERROR)
            directory_temp = mkdtemp(prefix='seismic_')
            # calculating the slope
            outRaster = processing.runalg("gdalogr:slope",
                                          rlayer, 1, True, True, False, 1.0,
                                          os.path.join(
                                              directory_temp,'slope.tif'
                                          ))
            # slope selection
            outSelection = processing.runalg('gdalogr:rastercalculator',
                                     outRaster['OUTPUT'], '1',  # A
                                     None, '1',  # B
                                     None, '1',  # C
                                     None, '1',  # D
                                     None, '1',  # E
                                     None, '1',  # F
                                     '1*(A>15.0)',  # formula
                                     '-9999',
                                     5,
                                     None,
                                     os.path.join(directory_temp,'sel.tif'))
            #sieve -- aggregating data
            outSieve = processing.runalg('gdalogr:sieve',
                                     outSelection['OUTPUT'],
                                     20,
                                     0,
                                     os.path.join(directory_temp,'sieve.tif')
                                     )
            # outNodata = processing.runalg('gdalogr:translate',
            #                               outSieve['OUTPUT'],
            #
            #                               )
            #convert raster to vector
            outVector=processing.runalg('gdalogr:polygonize',
                                        outSieve['OUTPUT'],
                                        'DN',
                                        shapeFinal
                                        #os.path.join(directory_temp,'final.shp')
                                        )

            #TODO -- add layer
            if self.dlg.autoload.isChecked():
                from qgis._core import QgsMapLayerRegistry,QgsRasterLayer,QgsVectorLayer
                shpName = os.path.basename(shapeFinal)
                vlayer = QgsVectorLayer(shapeFinal, shpName, "ogr")
                QgsMapLayerRegistry.instance().addMapLayer(vlayer)




