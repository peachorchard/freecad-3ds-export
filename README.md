# freecad-3ds-export
3ds file export for FreeCAD with color information
## Install
For Ubuntu put the files in a sub-directory of `~/.FreeCAD/Mod`.
For example `~/.FreeCAD/Mod/3dsFileExport`.
Then start/restart FreeCAD.
The .3ds file export format should now be available as an option when exporting.
## Notes:
Face colors should be preserved.  Materials are created based on the Diffuse color at the moment.  Diffuse colors with the same values are mapped to the same material.  Geometry is created face by face to preserve the color mapping.  Therefore the vertex positions may not be mapped exactly correctly at the moment.
