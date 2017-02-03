import bpy
import math
import mathutils
from mathutils import Vector


def addIKTo(armature, poseBoneName, controllerName):
    location = armature.pose.bones[poseBoneName].location

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.empty_add(type='PLAIN_AXES')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_pattern(pattern='Empty*')
    bpy.context.selected_objects[0].name = controllerName
    bpy.context.scene.objects[controllerName].location = location
    bpy.ops.object.select_pattern(pattern=controllerName)

    bpy.ops.object.mode_set(mode='POSE') # Can't get this line working...

    bpy.data.armatures["Armature"].bones.active = armature.pose.bones[poseBoneName].bone 
    bpy.ops.pose.ik_add(with_targets=True)

def getObject(name):
    return bpy.context.scene.objects[name]

def generateWalkAnimation():
    
    armature = bpy.data.objects['Armature']
    bpy.context.scene.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

    calveR = getObject('IKcalveR')
    calveL = getObject('IKcalveL')

    thighR = getObject('IKthighR')
    thighL = getObject('IKthighL')

    armR = getObject('IKarmR')
    armL = getObject('IKarmL')

    thighL.location = (-1.14, -0.40, 7.02)
    thighR.location = (0.95, -0.37, 6.96)

    armBaseHeight = 5
    armOffset = 2
    footOffset = 1.2
    speedFactor = 2
    frameCount = 100
    armAmplitude = 1
    footAmplitude = 2.5

    bpy.data.scenes['Scene'].frame_start = 0
    bpy.data.scenes['Scene'].frame_end = frameCount
    for frame in range(0, frameCount):

        t = (360 / frameCount) * frame
        offset = 180

        calveR.location = (-footOffset, math.cos(math.radians(t * speedFactor)) * footAmplitude, -math.sin(-math.radians(t * speedFactor)) * footAmplitude)
        calveR.keyframe_insert(data_path="location", frame=frame)

        calveL.location = (footOffset, math.cos(math.radians(t * speedFactor - offset)) * footAmplitude, -math.sin(-math.radians(t * speedFactor - offset)) * footAmplitude)
        calveL.keyframe_insert(data_path="location", frame=frame)

        armR.location = (-armOffset, math.cos(math.radians(t * speedFactor - offset)) * armAmplitude, armBaseHeight + -math.sin(-math.radians(t * speedFactor - offset)) * armAmplitude)
        armR.keyframe_insert(data_path="location", frame=frame)

        armL.location = (armOffset, math.cos(math.radians(t * speedFactor)) * armAmplitude, armBaseHeight + -math.sin(-math.radians(t * speedFactor)) * armAmplitude)
        armL.keyframe_insert(data_path="location", frame=frame)


def removeWalkAnimation():
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.transforms_clear()
    bpy.ops.poselib.unlink()
    bpy.ops.pose.select_all(action='DESELECT')

class RemoveWalkAnimOperator(bpy.types.Operator):
    bl_idname = "tz.rmwalk"
    bl_label = "Remove walk anim"
    
    def execute(self, context):
        removeWalkAnimation()
        return {'FINISHED'}

class GenerateWalkAnimOperator(bpy.types.Operator):
    bl_idname = "tz.walkgen"
    bl_label = "Generate walk anim"

    def execute(self, context):
        generateWalkAnimation()
        return {'FINISHED'}

class LayoutDemoPanel(bpy.types.Panel):
    bl_label = "Motion Synthesis Module"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        row = layout.row()
        row.operator("tz.walkgen")
        
        row2 = row.row()
        row2.operator("screen.animation_play", text="Play/Pause Animation")

def register():
    bpy.utils.register_class(GenerateWalkAnimOperator)
    bpy.utils.register_class(LayoutDemoPanel)
    bpy.utils.register_class(RemoveWalkAnimOperator)

def unregister():
    bpy.utils.unregister_class(LayoutDemoPanel)
    bpy.utils.unregister_class(RemoveWalkAnimOperator)
    bpy.utils.unregister_class(LayoutDemoPanel)

if __name__ == "__main__":
    register()
