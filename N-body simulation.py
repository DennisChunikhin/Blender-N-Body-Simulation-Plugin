bl_info = {
    "name": "N-body simulation",
    "description": "A simulation of objects that interact through gravity.",
    "author": "Dennis Chunikhin",
    "version": (0, 0, 2),
    "blender": (2, 70, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}

import bpy
import numpy as np
import random
from bpy.types import (
    AddonPreferences,
    Operator,
    Panel,
    PropertyGroup,
)
from bpy.props import (StringProperty,
    BoolProperty,
    IntProperty,
    FloatProperty,
    EnumProperty,
    PointerProperty,
)

class OBJECT_OT_random_bodies(Operator):
    bl_label = "Generate random bodies"
    bl_idname = "object.n_random_bodies"
    bl_description = "Generates random bodies ready for simulation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER', 'UNDO'}
    
    amnt = bpy.props.IntProperty(
        name = "Amount",
        description = "Amount of bodies to generate",
        default = 1,
        min = 0,
        )
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        
        body = bpy.data.objects
        
        for i in range(self.amnt):
            bpy.ops.mesh.primitive_uv_sphere_add()
            
            body[-1]['Active'] = True
            body[-1]["mass"] = np.float64(random.randrange(100000000000,1000000000000))
            body[-1].dimensions = ((body[-1]["mass"] / 400000000000)**(1/3), (body[-1]["mass"] / 400000000000)**(1/3), (body[-1]["mass"] / 400000000000)**(1/3))
            body[-1]['velocity'] = (np.float64(random.randrange(-3, 3)), np.float64(random.randrange(-3, 3)), np.float64(random.randrange(-3, 3)))
            body[-1].location = (np.float64(random.randrange(-self.amnt*2, self.amnt*2)), np.float64(random.randrange(-self.amnt*2, self.amnt*2)), np.float64(random.randrange(-self.amnt*2, self.amnt*2)))

        return {'FINISHED'}


class OBJECT_OT_n_body_setup(Operator):
    bl_label = "Setup n body simulation"
    bl_idname = "object.n_body_create"
    bl_description = "Set up all objects for simulation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        # Add missing properties to objects
        
        for body in bpy.data.objects:
            
            if body.get('Active') is None:
                body['Active'] = 0
                
            if body.get('mass') is None:
                body["mass"] = np.float64(random.randrange(100000000000,1000000000000))
                
            if body.get('velocity') is None:
                body["velocity"] = (np.float64(random.randrange(-3, 3)), np.float64(random.randrange(-3, 3)), np.float64(random.randrange(-3, 3)))
            
            body.dimensions = ((body["mass"] / 400000000000)**(1/3), (body["mass"] / 400000000000)**(1/3), (body["mass"] / 400000000000)**(1/3))
        
        return {'FINISHED'}

class OBJECT_OT_n_body_simulate(Operator):
    bl_label = "Simulate (n body simulation)"
    bl_idname = "object.n_body_simulate"
    bl_description = "Simulate the system. All objects with the property 'Active' set to 1 will be part of the simulation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    scale = bpy.props.IntProperty(
        name = "Distance Scale",
        description = "Scale all distances",
        default = 1,
        min = 0,
        )

    step = bpy.props.FloatProperty(
        name = "Time Step",
        description = "The number of iterations that happen in a unit of time. Larger time steps result in more accurate simulations",
        default = 10,
        min = 0,
        )
        
    iter = bpy.props.IntProperty(
        name = "Iterations",
        description = "The number of times a calculation is performed",
        default = 500,
        min = 0,
        )
        
    interval = bpy.props.IntProperty(
        name = "Interval",
        description = "The number of iterations per frame",
        default = 1,
        min = 0,
        )
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        
        # SIMULATION SCRIPT START
        
        step = self.step
        iter = self.iter
        interval = self.interval
        G = 6.67408/10**11

        body = bpy.data.objects
        
        for obj in body:
            if obj.get('Active') is not None and obj.get('mass') is not None and obj.get('velocity') is not None and obj.get('Active') == 1:
                obj.dimensions = ((obj["mass"] / 400000000000)**(1/3) / self.scale, (obj["mass"] / 400000000000)**(1/3) / self.scale, (obj["mass"] / 400000000000)**(1/3) / self.scale)
                obj.animation_data_clear()

        def Collision(b1, b2):
            # New velocity and position
            v = (b1['mass'] * np.asarray(b1['velocity']) + b2['mass'] + np.asarray(b2['velocity'])) / (b1['mass'] + b2['mass'])
            pos = (b1['mass'] * np.asarray(b1.location) + b2['mass'] * np.asarray(b2.location)) / (b1['mass'] + b2['mass'])
            # New object properties
            return {"r": ((b1['mass'] + b2['mass'])/400000000000)**(1/3) / self.scale, "m": b1['mass'] + b2['mass'],"v": v, "pos": pos}

        for x in range(iter):
        
            to_remove = []
            to_add = []
            
            # For center of mass
            M = 0
            sum = np.asarray([np.float64(0), np.float64(0), np.float64(0)])
            
            for obj in body:
                
                if obj.get('Active') is None or obj.get('mass') is None or obj.get('velocity') is None:
                    continue
                
                if obj['Active'] == 1:
                    # Body 1
                    pos1 = np.asarray(obj.location)
                    
                    for other in body:
                        
                        if other.get('Active') is None or other.get('mass') is None or other.get('velocity') is None:
                            continue
                        
                        if other != obj and other['Active'] == 1:
                            # Body 2
                            pos2 = np.asarray(other.location)
                            m = other["mass"]
                            
                            dist = ((pos2-pos1)**2).sum()**0.5
                            
                            if dist < obj.dimensions[0]/2 + other.dimensions[0]/2:
                                # Collision
                                if obj not in to_remove and other not in to_remove:
                                    to_remove.append(obj)
                                    to_remove.append(other)
                                    to_add.append(Collision(obj, other))
                            else:
                                # Acceleration
                                a = G*m/dist**2*(pos2-pos1)/dist
                            
                                obj["velocity"] = tuple(np.asarray(obj["velocity"]) + a/step)
                
    
                    # Center of mass
                    pos = np.asarray([np.float64(obj.location[0]), np.float64(obj.location[1]), np.float64(obj.location[2])])
                
                    M += obj["mass"]
                    sum += obj['mass'] * pos
                
            R = sum/M
            
            # Move and keyframe
            for obj in body:
                if obj.get('Active') is None or obj.get('mass') is None or obj.get('velocity') is None:
                    continue
                
                if obj['Active'] == 1:
                    loc = np.asarray(obj.location) + np.asarray(obj['velocity'])/step - R
                    obj.location = tuple(loc/self.scale)
                    obj.keyframe_insert(data_path="location", frame=x/interval)
                    obj.location = tuple(loc)

            # For collisions
            for rm in to_remove:
                rm.keyframe_insert(data_path="scale", frame=(x-1)/interval)
                rm.dimensions = (0, 0, 0)
                rm.keyframe_insert(data_path="scale", frame=x/interval)
                
                rm['Active'] = 0
            
            for new in to_add:
                bpy.ops.mesh.primitive_uv_sphere_add()
                body[-1].dimensions = (0, 0, 0)
                body[-1].keyframe_insert(data_path="scale", frame=(x-1)/interval)
                
                body[-1]['Active'] = 1
                body[-1]['mass'] = new['m']
                body[-1]['velocity'] = new['v']
                body[-1].location = new['pos']
                body[-1].dimensions = (new['r'], new['r'], new['r'])
                
                body[-1].keyframe_insert(data_path="scale", frame=x/interval)
                body[-1].keyframe_insert(data_path="location", frame=x/interval)
            
        # SIMULATION SCRIPT END
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_n_body_setup)
    bpy.utils.register_class(OBJECT_OT_n_body_simulate)
    bpy.utils.register_class(OBJECT_OT_random_bodies)
        
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_n_body_setup)
    bpy.utils.unregister_class(OBJECT_OT_n_body_simulate)
    bpy.utils.unregister_class(OBJECT_OT_random_bodies)
    
if __name__ == "__main__":
    register()
