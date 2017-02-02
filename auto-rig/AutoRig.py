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
    
    bone = Bone("hips", Points["hanche"], Points["hanche"]+Vector((0.1,0.1,0.1)),  "", False)
    skeleton.AddBone(bone)

    #spine01
    headPoint = (Points["cou"] - Points["hanche"]) / 3 + Points["hanche"]
    bone = Bone("spine01", skeleton.GetBoneByName("hips").tail, headPoint,  "hips", True)
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
    bone = Bone("thigh.L", Points["hanche"], Points["genoux.G"], "hips", True)
    skeleton.AddBone(bone)

    #calve.L
    bone = Bone("calve.L", Points["genoux.G"], Points["cheville.G"], "thigh.L", True)
    skeleton.AddBone(bone)

    #foot.L
    bone = Bone("foot.L", Points["cheville.G"], Points["pied.G"], "calve.L", True)
    skeleton.AddBone(bone)

    #thigh.R
    bone = Bone("thigh.R", Points["hanche"], Points["genoux.D"], "hips", True)
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

    #hand.R
    bone = Bone("hand.R", skeleton.GetBoneByName("underarm.R").tail, skeleton.GetBoneByName("underarm.R").tail+Vector((0.1,0.1,0.1)), "underarm.R", True)
    skeleton.AddBone(bone)

    #thumb.R
    bone = Bone("thumb.R", skeleton.GetBoneByName("hand.R").tail,Points["pouce.D"],  "hand.R", True)
    skeleton.AddBone(bone)

    #index.R
    bone = Bone("index.R", skeleton.GetBoneByName("hand.R").tail,Points["index.D"],  "hand.R", True)
    skeleton.AddBone(bone)

    #major.R
    bone = Bone("major.R", skeleton.GetBoneByName("hand.R").tail,Points["majeur.D"],  "hand.R", True)
    skeleton.AddBone(bone)

    #annular.R
    bone = Bone("annular.R", skeleton.GetBoneByName("hand.R").tail,Points["annulaire.D"],  "hand.R", True)
    skeleton.AddBone(bone)

    #atrial.R
    bone = Bone("atrial.R", skeleton.GetBoneByName("hand.R").tail,Points["auriculaire.D"],  "hand.R", True)
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

    #hand.R
    bone = Bone("hand.L", skeleton.GetBoneByName("underarm.L").tail, skeleton.GetBoneByName("underarm.L").tail+Vector((0.1,0.1,0.1)), "underarm.L", True)
    skeleton.AddBone(bone)

    #thumb.L
    bone = Bone("thumb.L", skeleton.GetBoneByName("hand.L").tail,Points["pouce.G"],  "hand.L", True)
    skeleton.AddBone(bone)

    #index.L
    bone = Bone("index.L", skeleton.GetBoneByName("hand.L").tail,Points["index.G"],  "hand.L", True)
    skeleton.AddBone(bone)

    #major.L
    bone = Bone("major.L", skeleton.GetBoneByName("hand.L").tail,Points["majeur.G"],  "hand.L", True)
    skeleton.AddBone(bone)

    #annular.L
    bone = Bone("annular.L", skeleton.GetBoneByName("hand.L").tail,Points["annulaire.G"],  "hand.L", True)
    skeleton.AddBone(bone)

    #atrial.L
    bone = Bone("atrial.L", skeleton.GetBoneByName("hand.L").tail,Points["auriculaire.G"],  "hand.L", True)
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

#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#START OF AUTO RETARGETING--------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------

def importbvh(file_path = "07_02"):
    try:
        file = file_path + ".bvh"
        bpy.ops.import_anim.bvh(filepath=file,
        axis_forward='-Z', axis_up='Y', filter_glob="*.bvh",
        target='ARMATURE', global_scale=1.0, frame_start=1,
        use_fps_scale=False, update_scene_fps=False,
        update_scene_duration=False, use_cyclic=False,
        rotate_mode='NATIVE')
        bvh_armature = bpy.data.objects[file_path[-5:]]
    except:
        print ("Couldn't open file")
    return bvh_armature
    
def scalebvh(bvh_armature, armature):
    perf_bones = bvh_armature.data.bones
    end_bones = armature.data.bones
    def calculateBoundingRadius(bones):
        center = sum((bone.head_local for bone in bones), Vector())
        center /= len(bones)
        radius = max((bone.head_local - center).length for bone in bones)
        return radius
    perf_rad = calculateBoundingRadius(perf_bones)
    end_rad = calculateBoundingRadius(end_bones)
    factor = end_rad / perf_rad
    bvh_armature.scale = factor * Vector((1, 1, 1))
    return factor

#tentative de retargeting n°2 (non fonctionnel)
"""
def createMap(bvh_arm, arm):
    map = {}
    bpy.ops.object.mode_set(mode='EDIT')
    for bone in bvh_arm.data.bones:
        if("L." in bone.name or "Left" in bone.name or "L " in bone.name or ".L" in bone.name):
            if("hand" in bone.name.lower()):
                map["hand.L"] = bone.name
            elif("foot" in bone.name.lower() or "toe" in bone.name.lower()):
                map["foot.L"] = bone.name
        elif("R." in bone.name or "Right" in bone.name or "R " in bone.name or ".R" in bone.name):
            if("hand" in bone.name.lower()):
                map["hand.R"] = bone.name
            elif("foot" in bone.name.lower() or "toe" in bone.name.lower()):
                map["foot.R"] = bone.name
        else:
            if("head" in bone.name.lower()):
                map["head"] = bone.name
            elif("hips" in bone.name.lower()):
                map["hips"] = bone.name
    if("hand.L" in map and "hand.R" in map and "foot.L" in map and "foot.R" in map and "head" in map and "hips" in map):
        bpy.ops.object.mode_set(mode="OBJECT")
        return map
    else:
        map = {}
        return "ERROR"

def completeMap(bvh_arm, arm, map):
    bvh_cpt = 0
    bvh_pbone = bvh_arm.data.bones[map["head"]]
    while bvh_pbone.name != "hips":
        bvh_pbone = bvh_pbone.parent
        bvh_cpt += 1
    cpt = 0
    pbone = arm.data.bones["head"]
    while pbone.name != "hips":
        pbone = pbone.parent
        cpt += 1
    temp = bvh_cpt // cpt
    
    pbone = arm.data.bones["head"]
    bvh_pbone = bvh_arm.data.bones[map["head"]]
    while pbone.name != "hips":
        for i in range (0, temp, 1) and pbone.name != "hips":
            pbone = pbone.parent
            bvh_pbone = bvh_pbone.parent
            if pbone.name != "hips":
                map[pbone.name] = bvh_pbone.name
"""            
    
    
    
def associateArmature(bvh_arm, arm):
    map = {}
    bpy.ops.object.mode_set(mode='EDIT')
    for bone in bvh_arm.data.bones:
        test = False
        if("L." in bone.name or "Left" in bone.name or "L " in bone.name or ".L" in bone.name):
            if("upleg" in bone.name.lower() or "thigh" in bone.name.lower()):
                map["thigh.L"] = bone.name
            elif("leg" in bone.name.lower() or "calve" in bone.name.lower()):
                map["calve.L"] = bone.name
            elif("foot" in bone.name.lower() or "toe" in bone.name.lower()):
                map["foot.L"] = bone.name
            elif("thumb" in bone.name.lower()):
                map["thumb.L"] = bone.name
            elif("forearm" in bone.name.lower() or "underarm" in bone.name.lower()):
                map["underarm.L"] = bone.name
            elif("arm" in bone.name.lower()):
                map["arm.L"] = bone.name
            elif("shoulder" in bone.name.lower() or "clavicle" in bone.name.lower()):
                map["clavicle.L"] = bone.name
            else :
                test = True
        elif("R." in bone.name or "Right" in bone.name or "R " in bone.name or ".R" in bone.name):
            if("upleg" in bone.name.lower() or "thigh" in bone.name.lower()):
                map["thigh.R"] = bone.name
            elif("leg" in bone.name.lower() or "calve" in bone.name.lower()):
                map["calve.R"] = bone.name
            elif("foot" in bone.name.lower() or "toe" in bone.name.lower()):
                map["foot.R"] = bone.name
            elif("thumb" in bone.name.lower()):
                map["thumb.R"] = bone.name
            elif("forearm" in bone.name.lower() or "underarm" in bone.name.lower()):
                map["underarm.R"] = bone.name
            elif("arm" in bone.name.lower()):
                map["arm.R"] = bone.name
            elif("shoulder" in bone.name.lower() or "clavicle" in bone.name.lower()):
                map["clavicle.R"] = bone.name
            else :
                test = True
        else:
            if("head" in bone.name.lower()):
                map["head"] = bone.name
            elif("spine" in bone.name.lower()):
                map["spine02"] = bone.name
            elif("back" in bone.name.lower()):
                map["spine01"] = bone.name
            elif("hips" in bone.name.lower()):
                map["hips"] = bone.name
            elif("neck" in bone.name.lower()):
                map["spine03"] = bone.name
            else:
                test = True
    bpy.ops.object.mode_set(mode="OBJECT")
    return map

def createAnim(bvh_arm, arm, map):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    arm.select = True 
    arm.animation_data_create()
    try:
        arm.animation_data.action = bpy.data.actions.new("temp")
        arm.animation_data.action.use_fake_user = True
    except:
        print("no need to create new action")

def copyTranslate(bvh_arm, arm, map, factor):
    #on deselect tous les objets
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    #on select l'armature et plus précisément le hips
    arm.select = True
    bpy.context.scene.objects.active = arm
    #on set la frame à 2 (le début de l'anim)
    current_frame = 2
    bpy.data.scenes["Scene"].frame_set(current_frame)
    bpy.data.scenes["Scene"].tool_settings.use_keyframe_insert_auto = True
    #boucle de parcours des keyframes
    Tprev = bvh_arm.pose.bones[map['hips']].location.copy()
    for current_frame in range (2,330,1):
        bpy.data.scenes["Scene"].frame_set(current_frame)
        Tnext = bvh_arm.pose.bones[map['hips']].location.copy()
        T = Vector(((Tnext[0] - Tprev[0])*factor, -(Tnext[2] - Tprev[2])*factor, (Tnext[1] - Tprev[1])*factor))
        bpy.ops.transform.translate(value=T, constraint_axis=(False,False,False), constraint_orientation='GLOBAL')
        Tprev = bvh_arm.pose.bones[map['hips']].location.copy()
    #On stop le record d'animation et on déselectionne tous les objets
    bpy.data.scenes["Scene"].tool_settings.use_keyframe_insert_auto = False
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

def copyRotate(bvh_arm, arm, map, factor) :
    #On selectionne l'armature
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    arm.select = True
    bpy.context.scene.objects.active = arm
    bpy.ops.object.mode_set(mode='POSE')
    #On démarre le record de keyframe
    bpy.data.scenes["Scene"].tool_settings.use_keyframe_insert_auto = True
    #On boucle sur toutes les clés de la map
    for key in map :
        current_frame = 2
        bpy.data.scenes["Scene"].frame_set(current_frame)
        #boucle qui copie les keyframe du pose bone courant une a une
        Rprev = bvh_arm.pose.bones[map[key]].rotation_euler.copy()
        for current_frame in range (2,330,10):
            arm.data.bones[key].select = True
            arm.pose.bones[key].rotation_mode = bvh_arm.pose.bones[map[key]].rotation_mode
            bpy.data.scenes["Scene"].frame_set(current_frame)
            Rnext = bvh_arm.pose.bones[map[key]].rotation_euler.copy()
            #print(arm.data.bones[key].name + " is rotate by : " + str(Vector((-(Rnext[0]-Rprev[0]), -(Rnext[2]-Rprev[2]), -(Rnext[1]-Rprev[1])))))
            bpy.ops.transform.rotate(value=-(Rnext[0]-Rprev[0]), axis=(1,0,0), constraint_axis=(False,False,False), constraint_orientation = 'GLOBAL')
            bpy.ops.transform.rotate(value=-(Rnext[2]-Rprev[2]), axis=(0,1,0), constraint_axis=(False,False,False), constraint_orientation = 'GLOBAL')
            bpy.ops.transform.rotate(value=-(Rnext[1]-Rprev[1]), axis=(0,0,1), constraint_axis=(False,False,False), constraint_orientation = 'GLOBAL')
            bvh_arm.pose.bones[map[key]].bbone_rollin = bvh_arm.pose.bones[map[key]].bbone_rollin
            bvh_arm.pose.bones[map[key]].bbone_rollout = bvh_arm.pose.bones[map[key]].bbone_rollout
            Rprev = bvh_arm.pose.bones[map[key]].rotation_euler.copy()
            arm.data.bones[key].select = False
    #on stop le record
    bpy.data.scenes["Scene"].tool_settings.use_keyframe_insert_auto = False
    #on deselectionne tous les objets
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

#fonction qui permet de set la position initiale
def changeArmPose(bvh_arm, arm, map, factor):
    #selection de l'armature
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    arm.select = True
    bpy.context.scene.objects.active = arm
    #copy de la position initial
    #End = bvh_arm.pose.bones[map['hips']].location.copy()*factor
    #Start = arm.pose.bones['hips'].location.copy()
    #T = Vector((End[0] - Start[0], End[2] - Start[1], End[1] - Start[2]))
    #bpy.ops.transform.translate(value=T, constraint_axis=(False,False,False), constraint_orientation='GLOBAL')
    #copy des rotations initiales
    bpy.ops.object.mode_set(mode='POSE')
    current_frame = 2
    bpy.data.scenes["Scene"].frame_set(current_frame)
    for key in map :
        arm.data.bones[key].select = True
        Rbvharm = bvh_arm.pose.bones[map[key]].rotation_euler.copy()
        Rarm = arm.pose.bones[key].rotation_euler.copy()
        bpy.ops.transform.rotate(value=-(factor*Rbvharm[0]-Rarm[0]), axis=(1,0,0), constraint_axis=(False,False,False), constraint_orientation = 'GLOBAL')
        bpy.ops.transform.rotate(value=-(factor*Rbvharm[2]-Rarm[1]), axis=(0,1,0), constraint_axis=(False,False,False), constraint_orientation = 'GLOBAL')
        bpy.ops.transform.rotate(value=-(factor*Rbvharm[1]-Rarm[2]), axis=(0,0,1), constraint_axis=(False,False,False), constraint_orientation = 'GLOBAL')
        arm.data.bones[key].select = False
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    
"""
def rename(bvh_arm, arm, map) :
    for key in map :
        if map[key] in arm.data.bones :
            arm.data.bones[map[key]].name = bvh_arm.data.bones[key].name
        if map[key] in arm.pose.bones :
            arm.pose.bones[map[key]].name = bvh_arm.pose.bones[key].name
"""

def playbvh():
    bpy.data.scenes["Scene"].frame_start = 2
    bpy.data.scenes["Scene"].frame_end = 330
    bpy.ops.screen.animation_play()
    

#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#END OF AUTO RETARGETING--------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------





## MAIN ##
if __name__ == '__main__':
    #autorig
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
    #retarget
    bvh_armature = importbvh("BVH/01/01_01")
    factor = scalebvh(bvh_armature, armature)
    map = associateArmature(bvh_armature, armature)
    changeArmPose(bvh_armature, armature, map, factor)
    copyTranslate(bvh_armature, armature, map, factor)
    copyRotate(bvh_armature, armature, map, factor)
    print(str(map))
    playbvh()