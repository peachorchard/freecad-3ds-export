#    (c) Copyright 2017 Dale Royer.  All rights reserved.
#
#    This file is part of freecad-3ds-export.
#
#    freecad-3ds-export is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    freecad-3ds-export is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with freecad-3ds-export.  If not, see <http://www.gnu.org/licenses/>.

import FreeCAD,  FreeCADGui

FreeCAD.addExportType("3ds (*.3ds)", "Export3ds")
