# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SeismicSlope
                                 A QGIS plugin
 QGIS tool for locate instable zone for 1 level of seismic microzonation

                             -------------------
        begin                : 2016-11-04
        copyright            : (C) 2016 by Pierluigi De Rosa
        email                : pierluigi.derosa@gfosservices.it
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load SeismicSlope class from file SeismicSlope.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .seismic_slope import SeismicSlope
    return SeismicSlope(iface)
