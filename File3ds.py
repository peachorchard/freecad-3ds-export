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

import struct

def writeWord(stream, i):
    stream.write(struct.pack('<H', i))

def writeInt(stream, i):
    stream.write(struct.pack('<I', i))    

class CHUNK(object):
    def __init__(self):
        self.id = 0x0000
        self.subchunks = []

    def getLength(self):
        rlen = 6+len(self.getData())
        for sc in self.subchunks:
            rlen += sc.getLength()
        return rlen
        
    def addSubChunk(self, chunk):
        self.subchunks.append(chunk)
        
    def write(self, stream):
        writeWord(stream, self.id)
        writeInt(stream, self.getLength())
        stream.write(self.getData())
        for sc in self.subchunks:
            sc.write(stream)

    def getData(self):
        return ''
        
class MainChunk(CHUNK):
    def __init__(self):
        super(MainChunk, self).__init__()
        self.id = 0x4D4D

class VersionChunk(CHUNK):
    def __init__(self):
        super(VersionChunk, self).__init__()
        self.id = 0x0002
        
    def getData(self):
        return struct.pack('<I', 3)

class EditorChunk(CHUNK):
    def __init__(self):
        super(EditorChunk, self).__init__()
        self.id = 0x3D3D

class ObjectBlock(CHUNK):
    def __init__(self, name):
        super(ObjectBlock, self).__init__()
        self.id = 0x4000
        self.name = name
        
    def getData(self):
        a = self.name.encode('ascii', 'ignore')
        data = bytearray(a)
        data.append(struct.pack('<B', 0))
        return data

class Mesh(CHUNK):
    def __init__(self):
        super(Mesh, self).__init__()
        self.id = 0x4100

class Verts(CHUNK):
    def __init__(self, verts):
        super(Verts, self).__init__()
        self.id = 0x4110
        self.numVerts = len(verts)
        self.verts = verts
    
    def getData(self):
        data = struct.pack('<H', self.numVerts)
        for v in self.verts:
            data += struct.pack('<f', v[0])
            data += struct.pack('<f', v[1])
            data += struct.pack('<f', v[2])
        return data

class Faces(CHUNK):
    def __init__(self, faces):
        super(Faces, self).__init__()
        self.id = 0x4120
        self.numFaces = len(faces)
        self.faces = faces
    
    def getData(self):
        data = struct.pack('<H', self.numFaces)
        for f in self.faces:
            data += struct.pack('<H',  int(f[0]))
            data += struct.pack('<H',  int(f[1]))
            data += struct.pack('<H',  int(f[2]))
            data += struct.pack('<H',  0x0000)
        return data

class FaceMaterials(CHUNK):
    def __init__(self, matname, facesIdx):
        super(FaceMaterials, self).__init__()
        self.id = 0x4130
        self.matname = matname
        self.numEntries = len(facesIdx)
        self.entries = facesIdx
    
    def getData(self):
        data = bytearray(self.matname.encode('ascii', 'ignore'))
        data += struct.pack('<B', 0);
        data += struct.pack('<H', self.numEntries)
        for e in self.entries:
            data += struct.pack('<H', e)
        return data

class RGBFloat(CHUNK):
    def __init__(self, rgb):
        super(RGBFloat, self).__init__()
        self.id = 0x0010
        self.rgb = rgb
    
    def getData(self):
        data = struct.pack('<f', self.rgb[0])
        data += struct.pack('<f', self.rgb[1])
        data += struct.pack('<f', self.rgb[2])
        return data

class MaterialChunk(CHUNK):
    def __init__(self):
        super(MaterialChunk, self).__init__()
        self.id = 0xAFFF

class MaterialName(CHUNK):
    def __init__(self, name):
        super(MaterialName, self).__init__()
        self.id = 0xA000
        self.name = name
    
    def getData(self):
        data = bytearray(self.name.encode('ascii', 'ignore'))
        data += struct.pack('<B', 0)
        return data

class MaterialAmbient(CHUNK):
    def __init__(self):
        super(MaterialAmbient, self).__init__()
        self.id = 0xA010

class MaterialDiffuse(CHUNK):
    def __init__(self):
        super(MaterialDiffuse, self).__init__()
        self.id = 0xA020

class MaterialSpecular(CHUNK):
    def __init__(self):
        super(MaterialSpecular, self).__init__()
        self.id = 0xA030

class MaterialShininess(CHUNK):
    def __init__(self):
        super(MaterialShininess, self).__init__()
        self.id = 0xA040

class MaterialShininessStrength(CHUNK):
    def __init__(self, name):
        super(MaterialShininessStrength, self).__init__()
        self.id = 0xA041

def arrayPrecisionStr(floatArray, prec):
    s = ''
    for f in floatArray:
        s += ('{:.'+str(prec)+'f}').format(f)+' '
    return s
    
class FreeCADShape:
    def __init__(self, obj):
        shape = obj.Shape
        faces = obj.Shape.Faces
        faceColors = obj.ViewObject.DiffuseColor
        if len(faceColors) != len(obj.Shape.Faces):
            faceColors = [obj.ViewObject.DiffuseColor[0]]*len(obj.Shape.Faces)
        self.points = []
        self.coordIndex = []
        self.colorIndex = []
        self.colors = faceColors
        self.name = obj.Label
        
        reducedVerts = {}
        
        prec = 4
        vis = []
        idx = 0
        for fi in range(0, len(faces)):
            f = faces[fi]
            vi = f.tessellate(15)
            vis.append(vi)
            for v in vi[0]:
                if not (arrayPrecisionStr(v, prec) in reducedVerts):
                    reducedVerts[arrayPrecisionStr(v, prec)] = idx
                    self.points.append(v)
                    idx = idx + 1
        for fi in range(0, len(faces)):
            for i in vis[fi][1]:
                a = reducedVerts[arrayPrecisionStr(vis[fi][0][i[0]], prec)];
                b = reducedVerts[arrayPrecisionStr(vis[fi][0][i[1]], prec)];
                c = reducedVerts[arrayPrecisionStr(vis[fi][0][i[2]], prec)];
                self.coordIndex.append([a, b, c])
                self.colorIndex.append([fi, fi, fi])

class File3ds:
    def __init__(self):
        self.mainChunk = MainChunk()
        self.mainChunk.addSubChunk(VersionChunk())
        self.editorChunk = EditorChunk()
        self.mainChunk.addSubChunk(self.editorChunk)
        self.colorsReduced = {}
        self.cr = 0

    def addObject(self, obj):
        freeCADShape = FreeCADShape(obj)
        
        colorsToAdd = []
        materialFaces = {}
        sc = 0
        fm = {}
        for c in freeCADShape.colors:
            cs = arrayPrecisionStr(c, 3)
            if  not (cs in self.colorsReduced):
                self.colorsReduced[cs] = self.cr
                self.cr = self.cr + 1
                colorsToAdd.append(c)
            materialFaces[cs] = []
            sc = sc + 1

        for c in colorsToAdd:
            material = MaterialChunk()
            materialName = MaterialName(arrayPrecisionStr(c, 3))
            material.addSubChunk(materialName)
            diffuse = MaterialDiffuse()
            material.addSubChunk(diffuse)
            rgb = RGBFloat(c)
            diffuse.addSubChunk(rgb)
            self.editorChunk.addSubChunk(material)
        
        objBlock = ObjectBlock(freeCADShape.name)
        mesh = Mesh()
        objBlock.addSubChunk(mesh)
        vertBlock = Verts(freeCADShape.points)
        mesh.addSubChunk(vertBlock)
        faceBlock = Faces(freeCADShape.coordIndex)
        mesh.addSubChunk(faceBlock)
        
        for fi in range(0, len(freeCADShape.colorIndex)):
            fci = freeCADShape.colorIndex[fi][0]
            materialFaces[arrayPrecisionStr(freeCADShape.colors[fci], 3)].append(fi)
        for matname in materialFaces:
            facesMat = FaceMaterials(matname, materialFaces[matname])
            faceBlock.addSubChunk(facesMat)
        self.editorChunk.addSubChunk(objBlock)

    def write(self, stream):
        print(len(self.colorsReduced))
        self.mainChunk.write(stream)

