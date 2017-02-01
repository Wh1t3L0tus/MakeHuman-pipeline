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

    footOrigR = (0, 0, 10)

    for frame in range(0, 100):

        t = 3.6 * frame
        offset = 180

        calveR.location = (-1.2, math.cos(math.radians(t * 2)) * 2.5, -math.sin(-math.radians(t * 2)) * 2.5)
        calveR.keyframe_insert(data_path="location", frame=frame)

        calveL.location = (1.2, math.cos(math.radians(t * 2 - offset)) * 2.5, -math.sin(-math.radians(t * 2 - offset)) * 2.5)
        calveL.keyframe_insert(data_path="location", frame=frame)

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
        row2.operator("tz.rmwalk")

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
