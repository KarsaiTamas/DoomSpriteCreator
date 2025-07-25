import bpy
import mathutils
import math
#def redo(self, context):
#    bpy.ops.ed.undo_redo()
#bpy.types.Scene.moveAnimData='1'
#bpy.types.Scene.idleAnimData=2
#bpy.types.Scene.rangedAttackAnimData=3
#bpy.types.Scene.meleeAttackAnimData=4
#bpy.types.Scene.hitAnimData=5
#bpy.types.Scene.deadAnimData=6
#bpy.types.Scene.extra1AnimData=7
#bpy.types.Scene.extra2AnimData=8
#bpy.types.Scene.extra3AnimData=9
#bpy.types.Scene.extra4AnimData=10
#bpy.types.Scene.extra5AnimData=11

#to remove shadows from render combine the Principled BSDF with Emission shader
#The emission shader should get it's color from the texture colors aka diffuse
def GetCharAnimFramesSize():
    return 12
def ObjectAnimations(self, context):
    l=[]

    if context.scene.objectToRotate:
        for i in range(0,bpy.data.actions.size()):
            l.append(i,context.scene.objectToRotate.actions[i],"")
        return bpy.data.actions
    else:
        return {'no','no','no'}
#https://stackoverflow.com/questions/14982836/rendering-and-saving-images-through-blender-python
def rotate_and_render(output_dir, rotation_angle = 360.0):
    import os
    if bpy.context.scene.objectEmpty:
        subject=bpy.context.scene.objectEmpty
    else:
        subject= bpy.context.scene.objectToRotate
    subject.rotation_euler=(0,0,0)
    chosenAnim=GetCurrentAnimationData(bpy.context.scene)
    rotationSteps=int(chosenAnim.charAngles)
    bpy.context.scene.render.film_transparent = True
    firstLetter=ord(chosenAnim.startFrameLetter.upper())
    
    print(firstLetter)
    for aframe in range(0,GetCharAnimFramesSize()):
        if chosenAnim.charAnimFrames[aframe]==-1:
            continue
        bpy.context.scene.frame_set(chosenAnim.charAnimFrames[aframe])
        bpy.context.scene.camera.location=chosenAnim.camPosition
        for step in range(0, rotationSteps):
            rotationName=""
            aframeName=chr(firstLetter+aframe)
            if rotationSteps==1:
                rotationName=0
            elif rotationSteps==8:
                rotationName=step+1
            elif rotationSteps==4:
                if step==0:
                    rotationName="{num1}{af1}{num2}".format(
                        num1=step+1,af1=aframeName,num2=5)
                else:
                    rotationName="{num1}{af1}{num2}".format(
                        num1=step+1,af1=aframeName,num2=9-step)
            elif rotationSteps==5:
                if step==0 or step==4:
                    rotationName="{num1}".format(
                        num1=step+1)
                else:
                    rotationName="{num1}{af1}{num2}".format(
                        num1=step+1,af1=aframeName,num2=9-step)
            
            outputFileName="{baseName}{animFrame}{animRotation}.png".format(
                baseName=chosenAnim.animBaseName,
                animFrame=aframeName,
                animRotation=rotationName)
            subject.rotation_euler[2] = math.radians(step * 45)
            bpy.context.scene.render.filepath = os.path.join(output_dir, (outputFileName))
            bpy.ops.render.render(write_still = True)
    subject.rotation_euler=(0,0,0)



def GetCurrentAnimationData(scene):
    chosenAnim=scene.moveAnimData
    if scene.animToChoose=='1':
        chosenAnim=scene.moveAnimData
    elif scene.animToChoose=='2':
        chosenAnim=scene.idleAnimData
    elif scene.animToChoose=='3':
        chosenAnim=scene.rangedAttackAnimData
    elif scene.animToChoose=='4':
        chosenAnim=scene.meleeAttackAnimData
    elif scene.animToChoose=='5':
        chosenAnim=scene.hitAnimData
    elif scene.animToChoose=='6':
        chosenAnim=scene.deadAnimData
    elif scene.animToChoose=='7':
        chosenAnim=scene.extra1AnimData
    elif scene.animToChoose=='8':
        chosenAnim=scene.extra2AnimData
    elif scene.animToChoose=='9':
        chosenAnim=scene.extra3AnimData
    elif scene.animToChoose=='10':
        chosenAnim=scene.extra4AnimData
    elif scene.animToChoose=='11':
        chosenAnim=scene.extra5AnimData
    return chosenAnim
        


def item_cb(self, context):  
    return [(ob.name, ob.name, ob.type) for ob in bpy.context.scene.objects]  

def DrawAnimationSelectUI(layout,animUI):
    #print(animUI)
    col = layout.column()
    row=layout.row()
    col.prop(animUI,"animBaseName")
    col.prop(animUI,"startFrameLetter")
    #col.prop(animUI,"animationToSelect")
    col.prop(animUI,"camPosition")
    col.prop(animUI,"charAngles")
    row.prop(animUI,"charAnimFrames")
    

class OBJECT_OT_SetCamPos(bpy.types.Operator):
    bl_idname = "object.setcamposbutton"
    bl_label = "Set Cam Position"
    bl_description="Set the render position data for the camera for this animation"

    def execute(self, context):
        obj = context.object
        chosenAnim=GetCurrentAnimationData(context.scene)
        chosenAnim.camPosition=bpy.context.scene.camera.location
        return {'FINISHED'}

class OBJECT_OT_GiveEmptyParentToObject(bpy.types.Operator):
    bl_idname = "object.giveemptyparenttoobject"
    bl_label = "OBJ Into Empty"
    bl_description="Put 'Object To Rotate' into an empty"

    def execute(self, context):
        obj= context.scene.objectToRotate
        
        bpy.ops.object.empty_add(type="PLAIN_AXES", location=obj.location)
        context.scene.objectEmpty = bpy.context.view_layer.objects.active
        obj.parent=context.scene.objectEmpty
        obj.location = (0, 0, 0)
        return {'FINISHED'}


class ObjectsDropDown(bpy.types.Operator) :  
    bl_idname = "mesh.objectsdropdown"  
    bl_label = "Object To Rotate"  
    bl_options = {"REGISTER", "UNDO"}  
    objname = bpy.props.EnumProperty(
        items=item_cb,  
        name = "Object",  
        description = "Choose object here")                               
                                       
    def execute(self, context) :  
        print("object name", self.objname)  
 
        return {"FINISHED"}  
 
class OBJECT_OT_DoomSpriteMakerData(bpy.types.Operator):
    bl_idname = "object.doom_sprite_maker"
    bl_label = "Make Sprites For This Animation"
    bl_description="Starts rendering the sprites for the selected animation"
    bl_options = {'REGISTER', 'UNDO'}
    
#    def SetCameraDistance(self,value):
#        self["cameraDistance"]=value

#    def SetCharAngles(self,value):
#        self["charAngles"]=value
        
#    def SetCharAnimFrames(self,value):
#        self["charAnimFrames"]=value

    def execute(self, context):
        
        
        #self.cameraDistance = context.scene.cameraDistance
        #self.charAngles = context.scene.charAngles
        #self.charAnimFrames = context.scene.charAnimFrames
        #bpy.context.scene.frame_set(2)
        #bpy.context.scene.camera.location=[context.scene.cameraDistance,0,0]
        
        #bpy.context.scene.camera.animation_data.action
        #bpy.context.scene.camera.keyframe_insert(data_path='location', frame=1)
        
        rotate_and_render(context.scene.renderLocation)
        return {'FINISHED'}


class OBJECT_PT_DoomSpriteMakerData(bpy.types.Panel):
    bl_idname = "OBJECT_PT_doomSpriteMakerData"
    bl_label = "Doom Sprite Maker"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GZD"
    
    def draw(self,context):
        op = context.active_operator
        layout = self.layout
        col = layout.column()
        row = layout.row()
        #dataListItems = col.operator('object.adddoomdatalistitem')
        col = layout.column()

        row.operator('object.giveemptyparenttoobject')
        row.operator('object.setcamposbutton')
        col = layout.column()
        row = layout.row()
        
        #dropDown= col.operator('mesh.objectsdropdown')
        #dropDown.objname
        
        #context.Scene.dsmData; 
        #context.Scene.numOfAnims
        row.prop(context.scene,"objectToRotate")
        row.prop(context.scene,"objectEmpty")
        
        col.prop(context.scene,"renderLocation")
        col.prop(context.scene, "animToChoose")
        col.operator('object.doom_sprite_maker')
        
        #Move animation selected
        chosenAnim=GetCurrentAnimationData(context.scene)
        
        DrawAnimationSelectUI(layout,chosenAnim)
        
        #col.prop(context.scene, "cameraDistance")
        #col.prop(context.scene, "charAngles",slider=True)
        #col.prop(context.scene, "charAnimFrames",slider=True)
        #props.cameraDistance = context.scene.cameraDistance
        #props.charAngles = context.scene.charAngles
        #props.charAnimFrames = context.scene.charAnimFrames


class DSMDataProperties(bpy.types.PropertyGroup):
    
    camPosition:bpy.props.FloatVectorProperty(
        name="Camera Position",
        size=3,
        default=(0.0,0.0,0.0),
        min=(-20.0),
        max=(20.0))
        #1 2 4 5 8 name Angles
    charAngles: bpy.props.EnumProperty(
        items=[
            ('1',"1","1 angle sprite"),
            ('4',"4","4 angles sprite"),
            ('5',"5","5 angles sprite"),
            ('8',"8","8 angles sprite"),
        ],
        name="Angle Count",
        description="Select angle count"
    )
    animBaseName: bpy.props.StringProperty(
        name="Base Sprite Name",
        description="The first 4 letters of the name of the sprite.",
        maxlen=4,
        default="TNT1")
    startFrameLetter: bpy.props.StringProperty(
        name="Start Frame Letter",
        description="The program starts naming the frame letters from here aka in TNT1A it's the letter A.",
        maxlen=1,
        default="A")

    charAnimFrames:bpy.props.IntVectorProperty(
        size=GetCharAnimFramesSize(),
        name="Frames",
        description="Select the animation frames which you want to make sprites from. Each number represents a frame for an animation. Go from left to right. -1 means no sprite will be made. ",
        min=(-1),
        default=[(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1)])
    #animationToSelect:bpy.props.EnumProperty(items=ObjectAnimations,name="Animation to use",description="Choose animation to use.") 
    
    #bpy.context.selected_objects[0].animation_data.action = bpy.data.actions[0]
    #object.animation_data.action = the_action
    
classes = [
    DSMDataProperties,
    ObjectsDropDown,
    OBJECT_OT_DoomSpriteMakerData,
    OBJECT_PT_DoomSpriteMakerData,
    OBJECT_OT_SetCamPos,
    OBJECT_OT_GiveEmptyParentToObject,
    ]
def register():
    print("doing stuff")
    for cls in classes:
        bpy.utils.register_class(cls)
    #bpy.types.Object.test_settings = bpy.props.CollectionProperty(type=OBJECT_PG_test)
    bpy.types.Scene.renderLocation= bpy.props.StringProperty(name="Render location",description="ex: D:\\Folder1\\Folder2")
    bpy.types.Scene.objectToRotate= bpy.props.PointerProperty(type=bpy.types.Object, name="Object To Rotate")
    bpy.types.Scene.objectEmpty= bpy.props.PointerProperty(
        type=bpy.types.Object, 
        name="Empty For The Object",
        description="This is here if you need an empty for your object. Leaving this to be editable so if it contains wrong data you can change it manually.")

    bpy.types.Scene.moveAnimData = bpy.props.PointerProperty(type=DSMDataProperties) 
    bpy.types.Scene.idleAnimData = bpy.props.PointerProperty(type=DSMDataProperties) 
    bpy.types.Scene.rangedAttackAnimData = bpy.props.PointerProperty(type=DSMDataProperties) 
    bpy.types.Scene.meleeAttackAnimData = bpy.props.PointerProperty(type=DSMDataProperties) 
    bpy.types.Scene.hitAnimData = bpy.props.PointerProperty(type=DSMDataProperties) 
    bpy.types.Scene.deadAnimData = bpy.props.PointerProperty(type=DSMDataProperties) 
    bpy.types.Scene.extra1AnimData = bpy.props.PointerProperty(type=DSMDataProperties) 
    bpy.types.Scene.extra2AnimData = bpy.props.PointerProperty(type=DSMDataProperties) 
    bpy.types.Scene.extra3AnimData = bpy.props.PointerProperty(type=DSMDataProperties) 
    bpy.types.Scene.extra4AnimData = bpy.props.PointerProperty(type=DSMDataProperties) 
    bpy.types.Scene.extra5AnimData = bpy.props.PointerProperty(type=DSMDataProperties) 
    
    bpy.types.Scene.animToChoose = bpy.props.EnumProperty(
        items=[
            ('1',"moveAnimData","Describe"),
            ('2',"idleAnimData","Describe"),
            ('3',"rangedAttackAnimData","Describe"),
            ('4',"meleeAttackAnimData","Describe"),
            ('5',"hitAnimData","Describe"),
            ('6',"deadAnimData","Describe"),
            ('7',"extra1AnimData","Describe"),
            ('8',"extra2AnimData","Describe"),
            ('9',"extra3AnimData","Describe"),
            ('10',"extra4AnimData","Describe"),
            ('11',"extra5AnimData","Describe"),
        ],
        name="Animation",
        description="Select animation"
    )
#    bpy.types.Scene.numOfAnims= bpy.props.EnumProperty(name="Number of animations",min=0,default=0,max=10,soft_max=10)
#   bpy.types.Scene.objectToRotate :  bpy.props.EnumProperty(items=item_cb,  
#                                            name = "Object",  
#                                            description = "Choose object here")    
#   for i in range(10):


if __name__ == "__main__":
    register()
#def SetCameraDistance(self,value):
#    self["cameraDistance"]=value
#    bpy.context.scene.camera.location=[value,0,0]
