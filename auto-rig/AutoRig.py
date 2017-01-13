import bpy
from mathutils import Vector

## Default variables ##
# Index vertices
pouceG=[9915]
indexG=[8874]
majeurG=[9151]
annulaireG=[9407]
auriculaireG=[9604]
poignetG=[10398,10397,10768,10767,10773,10771,10766,10765,10406,10405,10410,10687,10394,10393,10400,10772,10770,10769,10764,10712]
coudeG=[10191,10199,10206,10194,10193,10753,10202,10201,10197,10195,10190,10189,10205,10699,10204,10203,10200,10198,10196,10192]
epauleG=[8326,8490,8275,8250]
genouxG=[11381,11379,11378,11380,13155,13156,11371,11370,11373,11372,11367,11366,11377,11376,11365,11364,11369,11368,11375,11374]
chevilleG=[13029,13059,11579]
piedG=[13008,13205,13032,13198]
pouceD=[3245]
indexD=[2215]
majeurD=[2492]
annulaireD=[2774]
auriculaireD=[3025]
poignetD=[4110,4111,3737,3736,4055,4107,4112,4113,4115,3739,3733,3732,4020,3749,3745,3744,4108,4109,4114,4116]
coudeD=[3550,3553,3554,3557,3559,3560,3564,3563,4043,3547,3548,3552,3556,3558,3562,3561,4095,3555,3551,3549]
epauleD=[1648,3974,1846,1872]
genouxD=[4770,4771,4779,4780,4781,4778,4722,4773,4783,4785,4787,4775,4774,4786,6555,6556,4782,4776,4777,4784]
chevilleD=[5011,6429,6459]
piedD=[6264,6609,6627,6601]
tete=[1053,1100,1064,7764,994]
cou=[7500,875,777,824]
hanche=[4384,11100,4540,4480]

# Center of point
Points = {}

# Avatar
avatar = None


## Class ##
class Bone:
	def __init__(self, n, h, t, p, c):
		self.name = n
		self.head = h
		self.tail = t
		self.parent = p
		self.isConnectToParent = c

	def print(self):
		boolean = "True" if self.isConnectToParent else "False"
		print("name : " + self.name + " - head : " + str(self.head) + " - tail : " + str(self.tail) + " - parent : " + self.parent + " - connect : " + boolean + "\n")

class Skeleton:
	def __init__(self):
		self.bones = []

	def AddBone(self, bone):
		self.bones.append(bone)

	def GetBoneByName(self, name):
		for i in self.bones:
			if i.name == name:
				return i
		return None


## Function ##
def CalculateCenter(Vertices):
	sumVector = Vector((0, 0, 0))
	for i in Vertices:
		v = avatar.data.vertices[i].co
		sumVector = sumVector + v
	sumVector = sumVector / len(Vertices)
	return sumVector

def CalculateAnchor():
	Points["pouce.G"] = CalculateCenter(pouceG)
	Points["index.G"] = CalculateCenter(indexG)
	Points["majeur.G"] = CalculateCenter(majeurG)
	Points["annulaire.G"] = CalculateCenter(annulaireG)
	Points["auriculaire.G"] = CalculateCenter(auriculaireG)
	Points["poignet.G"] = CalculateCenter(poignetG)
	Points["coude.G"] = CalculateCenter(coudeG)
	Points["epaule.G"] = CalculateCenter(epauleG)
	Points["genoux.G"] = CalculateCenter(genouxG)
	Points["cheville.G"] = CalculateCenter(chevilleG)
	Points["pied.G"] = CalculateCenter(piedG)
	Points["pouce.D"] = CalculateCenter(pouceD)
	Points["index.D"] = CalculateCenter(indexD)
	Points["majeur.D"] = CalculateCenter(majeurD)
	Points["annulaire.D"] = CalculateCenter(annulaireD)
	Points["auriculaire.D"] = CalculateCenter(auriculaireD)
	Points["poignet.D"] = CalculateCenter(poignetD)
	Points["coude.D"] = CalculateCenter(coudeD)
	Points["epaule.D"] = CalculateCenter(epauleD)
	Points["genoux.D"] = CalculateCenter(genouxD)
	Points["cheville.D"] = CalculateCenter(chevilleD)
	Points["pied.D"] = CalculateCenter(piedD)
	Points["tete"] = CalculateCenter(tete)
	Points["cou"] = CalculateCenter(cou)
	Points["hanche"] = CalculateCenter(hanche)

def CreateSkeleton():
	skeleton = Skeleton()

	#spine01
	headPoint = (Points["cou"] - Points["hanche"]) / 3 + Points["hanche"]
	bone = Bone("spine01", Points["hanche"], headPoint,  "", False)
	skeleton.AddBone(bone)

	#spine02
	headPoint = (Points["cou"] - Points["hanche"]) / 3 + skeleton.GetBoneByName("spine01").tail
	bone = Bone("spine02", skeleton.GetBoneByName("spine01").tail,headPoint,  "spine01", True)
	skeleton.AddBone(bone)
	
	#spine03
	headPoint = (Points["cou"] - Points["hanche"]) / 3 + skeleton.GetBoneByName("spine02").tail
	bone = Bone("spine03", skeleton.GetBoneByName("spine02").tail,headPoint,  "spine02", True)
	skeleton.AddBone(bone)

	#head
	bone = Bone("head", skeleton.GetBoneByName("spine03").tail,Points["tete"],  "spine03", True)
	skeleton.AddBone(bone)

	#thigh.L
	bone = Bone("thigh.L", Points["hanche"], Points["genoux.G"], "", True)
	skeleton.AddBone(bone)

	#calve.L
	bone = Bone("calve.L", Points["genoux.G"], Points["cheville.G"], "thigh.L", True)
	skeleton.AddBone(bone)

	#foot.L
	bone = Bone("foot.L", Points["cheville.G"], Points["pied.G"], "calve.L", True)
	skeleton.AddBone(bone)

	#thigh.R
	bone = Bone("thigh.R", Points["hanche"], Points["genoux.D"], "", True)
	skeleton.AddBone(bone)

	#calve.R
	bone = Bone("calve.R", Points["genoux.D"], Points["cheville.D"], "thigh.R", True)
	skeleton.AddBone(bone)

	#foot.R
	bone = Bone("foot.R", Points["cheville.D"], Points["pied.D"], "calve.R", True)
	skeleton.AddBone(bone)

	#clavicle.R
	tailPoint = (Points["cou"] - Points["hanche"]) / 6 + skeleton.GetBoneByName("spine02").tail
	bone = Bone("clavicle.R", tailPoint,Points["epaule.D"],  "spine02", True)
	skeleton.AddBone(bone)

	#arm.R
	bone = Bone("arm.R", skeleton.GetBoneByName("clavicle.R").tail,Points["coude.D"],  "clavicle.R", True)
	skeleton.AddBone(bone)

	#underarm.R
	bone = Bone("underarm.R", skeleton.GetBoneByName("arm.R").tail,Points["poignet.D"],  "arm.R", True)
	skeleton.AddBone(bone)

	#thumb.R
	bone = Bone("thumb.R", skeleton.GetBoneByName("underarm.R").tail,Points["pouce.D"],  "underarm.R", True)
	skeleton.AddBone(bone)

	#index.R
	bone = Bone("index.R", skeleton.GetBoneByName("underarm.R").tail,Points["index.D"],  "underarm.R", True)
	skeleton.AddBone(bone)

	#major.R
	bone = Bone("major.R", skeleton.GetBoneByName("underarm.R").tail,Points["majeur.D"],  "underarm.R", True)
	skeleton.AddBone(bone)

	#annular.R
	bone = Bone("annular.R", skeleton.GetBoneByName("underarm.R").tail,Points["annulaire.D"],  "underarm.R", True)
	skeleton.AddBone(bone)

	#atrial.R
	bone = Bone("atrial.R", skeleton.GetBoneByName("underarm.R").tail,Points["auriculaire.D"],  "underarm.R", True)
	skeleton.AddBone(bone)

	#clavicle.L
	tailPoint = (Points["cou"] - Points["hanche"]) / 6 + skeleton.GetBoneByName("spine02").tail
	bone = Bone("clavicle.L", tailPoint,Points["epaule.G"],  "spine02", True)
	skeleton.AddBone(bone)

	#arm.L
	bone = Bone("arm.L", skeleton.GetBoneByName("clavicle.L").tail,Points["coude.G"],  "clavicle.L", True)
	skeleton.AddBone(bone)

	#underarm.L
	bone = Bone("underarm.L", skeleton.GetBoneByName("arm.L").tail,Points["poignet.G"],  "arm.L", True)
	skeleton.AddBone(bone)

	#thumb.L
	bone = Bone("thumb.L", skeleton.GetBoneByName("underarm.L").tail,Points["pouce.G"],  "underarm.L", True)
	skeleton.AddBone(bone)

	#index.L
	bone = Bone("index.L", skeleton.GetBoneByName("underarm.L").tail,Points["index.G"],  "underarm.L", True)
	skeleton.AddBone(bone)

	#major.L
	bone = Bone("major.L", skeleton.GetBoneByName("underarm.L").tail,Points["majeur.G"],  "underarm.L", True)
	skeleton.AddBone(bone)

	#annular.L
	bone = Bone("annular.L", skeleton.GetBoneByName("underarm.L").tail,Points["annulaire.G"],  "underarm.L", True)
	skeleton.AddBone(bone)

	#atrial.L
	bone = Bone("atrial.L", skeleton.GetBoneByName("underarm.L").tail,Points["auriculaire.G"],  "underarm.L", True)
	skeleton.AddBone(bone)

	return skeleton

def GetBoneByName(amt, name):
	if name == "":
		return None
	b = amt.edit_bones[name]
	return b

	

def DrawSkeleton(skeleton):
	bpy.ops.object.armature_add()
	bpy.ops.transform.rotate(value=1.5708, axis=(1,0,0))
	ob = bpy.context.object
	amt = ob.data
	
	bpy.ops.object.mode_set(mode='EDIT')

	# Get base bone
	base = amt.edit_bones['Bone']
	base.tail = skeleton.bones[0].tail
	base.head = skeleton.bones[0].head
	base.name = skeleton.bones[0].name

	for bone in skeleton.bones[1::]:
		tip = amt.edit_bones.new(bone.name) # name=tip
		tip.head = bone.head
		tip.tail = bone.tail
		tip.parent = GetBoneByName(amt, bone.parent)
		tip.use_connect = bone.isConnectToParent

	return ob

## MAIN ##
if __name__ == '__main__':
	bpy.context.scene.cursor_location = Vector((0.0,0.0,0.0))
	avatar = bpy.data.objects[0]
	CalculateAnchor()
	skeleton = CreateSkeleton()
	armature = DrawSkeleton(skeleton)
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_all(action='DESELECT')
	avatar.select = True
	armature.select = True
	bpy.ops.object.parent_set(type='ARMATURE_AUTO')