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

import ntpath
import FreeCAD,  FreeCADGui
import File3ds

class Export3ds:
    def Activated(self):
        FreeCAD.Console.PrintMessage('Activated 3ds export')
    
    def GetResources(self):
        return {'Pixmap':'',  'MenuText':'Export 3ds',  'Tooltip':'Export 3ds'}

def export(objs, filename):
    file = File3ds.File3ds()
    for o in objs:
        if o.ViewObject.isVisible():
            file.addObject(o)
    with open(filename,  "wb") as outputfile:
        file.write(outputfile)

