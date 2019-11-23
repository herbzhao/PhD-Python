#Author- Tianheng
#Description-
# https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-DE98632B-3DC0-422B-A1C6-8A5A15C99E11

import adsk.core, adsk.fusion, traceback
import math
#  unable to import library from other python environment
# import numpy as np



def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)

        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        yzPlane = rootComp.yZConstructionPlane
        xzPlane = rootComp.xZConstructionPlane

        # Draw some circles.
        #  a method to create sphere from xyz and radius
        def create_sphere(center=(0,0,0), r=5, angle=360, name='sphere'):
            sketch = sketches.add(xyPlane)

            # Draw a circle.
            circles = sketch.sketchCurves.sketchCircles
            circle = circles.addByCenterRadius(adsk.core.Point3D.create(*center), r)

            # Draw a line to use as the axis of revolution.
            lines = sketch.sketchCurves.sketchLines
            circle_axisLine = lines.addByTwoPoints(adsk.core.Point3D.create(center[0], center[1]-r, center[2]), adsk.core.Point3D.create(center[0], center[1]+r, center[2]))

            # Get the profile defined by the circle.
            circle_prof = sketch.profiles.item(0)

            # Create an revolution input to be able to define the input needed for a revolution
            # while specifying the profile and that a new component is to be created
            revolves = rootComp.features.revolveFeatures
            revolves_input = revolves.createInput(circle_prof, circle_axisLine, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)

            # Define that the extent is an angle of pi to get half of a torus.
            angle = adsk.core.ValueInput.createByReal(angle/360*2*math.pi) 
            revolves_input.setAngleExtent(False, angle)

            # Create the extrusion.
            ext = revolves.add(revolves_input)
            # a component that allows further manipulation
            comp = ext.parentComponent
            comp.name = name
            return comp
    

        # Draw some circles.
        #  a method to create sphere from xyz and radius
        def create_CNC(center=(0,0,0), length=10, width=5, name='CNC'):
            sketch = sketches.add(xyPlane)

            # Draw a circle.
            ellipses = sketch.sketchCurves.sketchEllipses
            CNC_profile = ellipses.add(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(0, length/2, 0), adsk.core.Point3D.create(width/2, 0, 0))
 
            # Draw a line to use as the axis of revolution.
            lines = sketch.sketchCurves.sketchLines
            circle_axisLine = lines.addByTwoPoints(adsk.core.Point3D.create(center[0], center[1]-length/2, center[2]), adsk.core.Point3D.create(center[0], center[1]+length/2, center[2]))

            # Get the profile defined by the circle.
            circle_prof = sketch.profiles.item(0)

            # Create an revolution input to be able to define the input needed for a revolution
            # while specifying the profile and that a new component is to be created
            revolves = rootComp.features.revolveFeatures
            revolves_input = revolves.createInput(circle_prof, circle_axisLine, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)

            # Define that the extent is an angle of pi to get half of a torus.
            angle = adsk.core.ValueInput.createByReal(360/360*2*math.pi) 
            revolves_input.setAngleExtent(False, angle)

            # Create the extrusion.
            ext = revolves.add(revolves_input)
            # a component that allows further manipulation
            comp = ext.parentComponent
            comp.name = name
            return comp
    
        

        # Draw some arcs.
        #  a method to create sphere from xyz and radius
        #  NOTE: change to point1,2,3,  and use a differnt code to decide the coordinates
        def create_arc_3d(point1=(0,-2,0), point2=(-2,0,0), point3=(0,2,0), angle=360, name='arc_3d'):
            ''' k determines the ratio of 3 points 
            - i.e. 1 means everything is the same distance from core, 2 is twice form top and 1 from bot, 1.5 for the left    ''' 
            sketch = sketches.add(xyPlane)

            # Draw a circle.
            arcs = sketch.sketchCurves.sketchArcs;
            # (*point1) - * unpacking operator:
            arc = arcs.addByThreePoints(adsk.core.Point3D.create(*point1), adsk.core.Point3D.create(*point2), adsk.core.Point3D.create(*point3))

            # Draw a line to use as the axis of revolution.
            lines = sketch.sketchCurves.sketchLines
            arc_axisLine = lines.addByTwoPoints(adsk.core.Point3D.create(*point1), adsk.core.Point3D.create(*point3))

            # Get the profile defined by the circle.
            arc_prof = sketch.profiles.item(0)

            # Create an revolution input to be able to define the input needed for a revolution
            # while specifying the profile and that a new component is to be created
            revolves = rootComp.features.revolveFeatures
            revolves_input = revolves.createInput(arc_prof, arc_axisLine, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)

            # Define that the extent is an angle of pi to get half of a torus.
            angle = adsk.core.ValueInput.createByReal(angle/360*2*math.pi) 
            revolves_input.setAngleExtent(False, angle)

            # Create the extrusion.
            ext = revolves.add(revolves_input)

            # a component that allows further manipulation
            comp = ext.parentComponent
            comp.name = name
            return comp


        def move_feature(comp, distance=(20, 0, 0), rotation = (90, 0, 0), copy = True):
            # https://adndevblog.typepad.com/manufacturing/2017/08/fusion-360-api-transform-component-.html
            # choose the occurance (instance of the comp) 
            comp_occ = rootComp.allOccurrencesByComponent(comp).item(0)

            # Get the current transform of the first occurrence
            transform = comp_occ.transform

            # transformation matrices but they're commonly used in computer graphics.  
            # Using matrix functionality you can build up a matrix using multiple rotations and then use that to create a Move feature. 
            axes = ((1,0,0), (0,1,0), (0,0,1))
            for angle, axis in zip(rotation, axes):
                rotation = adsk.core.Matrix3D.create()
                rotation.setToRotation(angle/360*2*math.pi, adsk.core.Vector3D.create(*axis), adsk.core.Point3D.create(0,0,0))
                transform.transformBy(rotation)

            
            # translation
            vector = adsk.core.Vector3D.create(*distance)
            transform.translation = vector

            # Now apply the actual transformation
            comp_occ.transform = transform

            # capture the position
            # https://forums.autodesk.com/t5/fusion-360-api-and-scripts/transformation-on-occurrence-getting-reset/td-p/8394257
            # if distance != (0,0,0) or rotation !=(0,0,0):
            try:
                design.snapshots.add()
            except RuntimeError:
                pass

        def copy_component(comp, new_comp='', name='item'):
            # comp_copy = rootComp.occurrences.addByInsert(comp, adsk.core.Matrix3D.create(), False)
            #  create an empty comp
            # new_comp = adsk.core.ObjectCollection.create()
            if new_comp == '':
                new_comp = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
                new_comp.component.name = name + '_copy'
                new_comp = new_comp.component

            # https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-1dad75dc-4bf8-11e7-bf09-005056c00008
            # Get the first body in sub component 1  
            bodies = []
            for i in range(comp.bRepBodies.count):
                bodies.append(comp.bRepBodies.item(i))

            # Copy/paste body from sub component 1 to sub component 2
            for body in bodies:
                copyPasteBody = new_comp.features.copyPasteBodies.add(body)

            return new_comp

        def delete_component(comp):
            for occurrence in rootComp.occurrencesByComponent(comp):
                 occurrence.deleteMe()

        def change_appearance(comp, rgb=(0,0,0), base_appearance_name='Plastic - Translucent Glossy (Yellow)', new_appearance_name='new_color'):
            # https://ekinssolutions.com/setting-colors-in-fusion-360/
            # Get the single occurrence that references the component.
            occurrences = rootComp.allOccurrencesByComponent(comp)
            occurrence = occurrences.item(0)
           
            # Get a reference to an appearance in the library.
            materials_library = app.materialLibraries.itemByName('Fusion 360 Appearance Library')
            base_appearance = materials_library.appearances.itemByName(base_appearance_name)

            # Create a copy of the existing appearance for the glossy etc.
            new_appearance = design.appearances.addByCopy(base_appearance, str(new_appearance_name))
            
            # Edit the "Color" property by setting it to a random color.
            color_property= adsk.core.ColorProperty.cast(new_appearance.appearanceProperties.itemByName('Color'))
            color_property.value = adsk.core.Color.create(*rgb, 1) 
            
            # Assign the new color to the occurrence.
            occurrence.appearance = new_appearance


        def combine_bodies(target_component, tool_components: list = [], operation='cut', keep_tool=True):
            # https://forums.autodesk.com/t5/fusion-360-api-and-scripts/combine-cut-via-api/td-p/6673937
            # https://forums.autodesk.com/t5/fusion-360-api-and-scripts/how-do-i-cut-an-occurrence-out-of-a-component/td-p/8354550
            target_component_occ = rootComp.allOccurrencesByComponent(target_component).item(0)
            target = target_component.bRepBodies.item(0).createForAssemblyContext(target_component_occ)

            tools = adsk.core.ObjectCollection.create()
            tool_component_occ = []
            for tool_component in tool_components:
                tool_component_occ.append(rootComp.allOccurrencesByComponent(tool_component).item(0))
                for i in range(tool_component.bRepBodies.count):
                    tools.add(tool_component.bRepBodies.item(i).createForAssemblyContext(tool_component_occ[-1]))

            combine_features = rootComp.features.combineFeatures
            combine_features_input = combine_features.createInput(target, tools)
            if operation == 'cut':
                combine_features_input.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
            elif operation == 'join':
                combine_features_input.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
            elif operation == 'intersect':
                combine_features_input.operation = adsk.fusion.FeatureOperations.IntersectFeatureOperation

            combine_features_input.isKeepToolBodies = keep_tool

            combine_features.add(combine_features_input)

            return target_component

    
        def cross_section(plane='xy', offset=5, direction = -1):
            # create a plane from (0,0,0) to point, and extend to large area
            if plane == 'xy':
                sketch = sketches.add(xyPlane)
            elif plane =='xz':
                sketch = sketches.add(xzPlane)
            elif plane =='yz':
                sketch = sketches.add(yzPlane)

            # Draw a huge circle for extrusion.
            circles = sketch.sketchCurves.sketchCircles
            circle = circles.addByCenterRadius(adsk.core.Point3D.create(0,0,0), 100)
            # Get the profile defined by the circle.
            circle_prof = sketch.profiles.item(0)

            # Extrude to remove the             
            # https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-CB1A2357-C8CD-474D-921E-992CA3621D04
            extrudes = rootComp.features.extrudeFeatures
            extrudeInput = extrudes.createInput(circle_prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
            extrude_distance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(100*direction))
            # Create a start extent that starts from a brep face with an offset of 10 mm.
            start_offset = adsk.fusion.OffsetStartDefinition.create(adsk.core.ValueInput.createByReal(offset))

            # Create a start extent that starts from a brep face with an offset of 10 mm.
            # taperAngle should be 0 because extrude start face is not a planar face in this case
            extrudeInput.startExtent = start_offset
            extrudeInput.setOneSideExtent(extrude_distance, adsk.fusion.ExtentDirections.PositiveExtentDirection)        
            # Create the extrusion
            extrude = extrudes.add(extrudeInput)


        def shell_around_core(central_sphere=(0,0,0,5), pitch=1, k=3, number_of_layers=5):
            ''' a specific function to generates three points for shell arcs '''
            x, y, z, r = central_sphere
            arcs_points = {}
            for layer in range(number_of_layers):
                # offset the z a bit otherwise the model overlapse too much to cause rendering issue
                point1 = (x, y-r-pitch*layer, z)
                point2 = (x-r-pitch*layer*(k+1)/2, y, z)
                point3 = (x, y+r+pitch*layer*k, z)
                arcs_points[layer] = (point1, point2, point3)

            return arcs_points



    # GAP: ------------------------------------------------------------------
    # NOTE:  Actual code for drawing is here
        def building_CNC(half_pitch=10, rods_per_half_pitch=5, tactoids_circular=6, layers=5):
            # Create first full helix
            CNC = []
            repeats = range(rods_per_half_pitch)
            #starting at 90 degrees and finish half pitch 
            angles = [180/(len(repeats)-1)*i+90 for i in repeats]
            print(angles) 

            for i, angle in zip(repeats, angles):
                CNC.append(create_CNC(length=20, width=2))
                move_feature(CNC[i], distance=(i*half_pitch/(len(repeats)-1), 0, 0), rotation=(angle, 0, 0))
                # print('created {} cnc'.format(i))

            # NOTE: making a half pitch
            # join and copy the full helix to a new body
            combined_CNC = combine_bodies(CNC[0], CNC[1:], 'join', False)
            # combined_CNC_2 = copy_component(combined_CNC, CNC[1])
            combined_CNC = copy_component(combined_CNC)

            # Remove the fundamental components as they are empty now
            for comp in CNC:
                delete_component(comp)

            # NOTE: making a few layers repeat of half pitch
            #  this propogates along the axis
            repeats = range(layers)
            distances = [half_pitch*i for i in repeats]
            print(distances)
            
            # FIRST we create few repeats along x_axis and then we rotate the whole thing along z axis
            combined_CNC_layers = []
            for j, distance in zip(repeats, distances):
                combined_CNC_layers.append(copy_component(combined_CNC))
                move_feature(combined_CNC_layers[j], distance=(distance, 0, 0), rotation=(0, 0, 0))

            # join and remove the individual components
            combined_CNC_2 = combine_bodies(combined_CNC_layers[0], combined_CNC_layers[1:], 'join', False)
            combined_CNC_2 = copy_component(combined_CNC_2)
            # Remove the fundamental components as they are empty now
            for comp in combined_CNC_layers:
                delete_component(comp)

            # NOTE: making the circular pattern
            # this determines the circular pattern
            repeats = range(tactoids_circular)
            angles = [360/(len(repeats))*i for i in repeats]
            print(angles)

            combined_CNCs_circular = []
            for i, angle in zip(repeats, angles):
                combined_CNCs_circular.append(copy_component(combined_CNC_2))
                move_feature(combined_CNCs_circular[i], distance=(0, 0, 0), rotation=(0, 0, angle))

            # join and remove the individual components
            combined_CNC_3 = combine_bodies(combined_CNCs_circular[0], combined_CNCs_circular[1:], 'join', False)
            combined_CNC_3 = copy_component(combined_CNC_3)
            # Remove the fundamental components as they are empty now
            for comp in combined_CNCs_circular:
                delete_component(comp)

        def building_onion_ring_droplet(half_pitch=10, layers=5):
            spheres = []            
            for i in range(layers):
                spheres.append(create_sphere(center=(0,0,0), r=half_pitch*(i+1), angle=180, name='sphere'))
    

        def building_onion_ring_shell_droplet(half_pitch=10, layers=5, angle=180):
            sphere_shell_list = []
            for i in range(layers):
                # create a outer sphere and inner sphere with tiny radius difference and cut to make a shell
                spheres_outer = create_sphere(center=(0,0,0), r=half_pitch*(i+1), angle=angle, name='sphere')
                spheres_inner = create_sphere(center=(0,0,0), r=(half_pitch*(i+1)-half_pitch*0.1), angle=angle, name='sphere')
                sphere_shell_list.append(combine_bodies(spheres_outer, [spheres_inner], 'cut', False))

            # join the shells to be one component?
            joined_shell = combine_bodies(sphere_shell_list[0], sphere_shell_list, 'join', False)


        building_CNC(half_pitch=20, rods_per_half_pitch=8, tactoids_circular=2, layers=2)
        # building_onion_ring_shell_droplet(half_pitch=20, layers=5)

    except:
        if ui:
            print('Failed: {}'.format(traceback.format_exc()))
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
    