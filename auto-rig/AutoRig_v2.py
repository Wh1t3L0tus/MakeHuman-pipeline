import bpy
import json
from mathutils import Vector

avatar = None

class Polygroup:
	def __init__(self):
		self.name = ""
		self.vertex = []
		self.barycentre = Vector((0,0,0))

	def __init__(self, n, v):
		self.name = n
		self.vertex = v
		self.barycentre = 0
		self.CalculBarycentre()

	def CalculBarycentre(self):
		print("a")
		sumVector = Vector((0, 0, 0))
		for i in self.vertex:
			v = avatar.data.vertices[i].co
			sumVector = sumVector + v
		self.barycentre = sumVector / len(self.vertex)

	def print(self):
		print("Name :",self.name,"Vertex :",self.vertex,"Barycentre :",self.barycentre)

def GetPolygroup():
	polygroups = []
	file = open("F:/4A_3DJV/Blender/Rig/polygroup.init", "r")
	text = file.read()
	line = text.split('\n')
	for l in line:
		content = l.split(',')
		name = content[0]
		vertex = []
		for v in content[1::]:
			vertex.append(int(v))
		polygroups.append(Polygroup(name, vertex))
	return polygroups


## MAIN ##
if __name__ == '__main__':
	avatar = bpy.data.objects[0]
	polygroups = GetPolygroup()
	for i in polygroups:
		i.print()