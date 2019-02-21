#Author-
#Description-

import adsk.core, adsk.fusion, traceback
import math
#  unable to import library from other python environment


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

        # Draw some circles.
        #  a method to create sphere from xyz and radius
        def create_sphere(center=(0,0,0), r=5, angle=360):
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
            central_line = revolves.createInput(circle_prof, circle_axisLine, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)

            # Define that the extent is an angle of pi to get half of a torus.
            angle = adsk.core.ValueInput.createByReal(angle/360*2*math.pi) 
            central_line.setAngleExtent(False, angle)

            # Create the extrusion.
            ext = revolves.add(central_line)
            # a component that allows further manipulation
            comp = ext.parentComponent
            return comp
        
        # Draw some arcs.
        #  a method to create sphere from xyz and radius
        #  NOTE: change to point1,2,3,  and use a differnt code to decide the coordinates
        def create_arc_3d(point1=(0,-2,0), point2=(-2,0,0), point3=(0,2,0), angle=360):
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
            central_line = revolves.createInput(arc_prof, arc_axisLine, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)

            # Define that the extent is an angle of pi to get half of a torus.
            angle = adsk.core.ValueInput.createByReal(angle/360*2*math.pi) 
            central_line.setAngleExtent(False, angle)

            # Create the extrusion.
            ext = revolves.add(central_line)

            # a component that allows further manipulation
            comp = ext.parentComponent
            return comp

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


        def combine_bodies(target_component, tool_components=[], operation='cut', keep_tool=True):
            # https://forums.autodesk.com/t5/fusion-360-api-and-scripts/combine-cut-via-api/td-p/6673937
            # https://forums.autodesk.com/t5/fusion-360-api-and-scripts/how-do-i-cut-an-occurrence-out-of-a-component/td-p/8354550
            target_component_occ = rootComp.allOccurrencesByComponent(target_component).item(0)
            target = target_component.bRepBodies.item(0).createForAssemblyContext(target_component_occ)

            tools = adsk.core.ObjectCollection.create()
            tool_component_occ = []
            for tool_component in tool_components:
                tool_component_occ.append(rootComp.allOccurrencesByComponent(tool_component).item(0))
                tools.add(tool_component.bRepBodies.item(0).createForAssemblyContext(tool_component_occ[-1]))

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

        sphere = create_sphere(center=(0,0,0),r=5,angle=360)

        change_appearance(sphere, rgb=(123,123,123), base_appearance_name='Aluminum - Anodized Glossy (Grey)', new_appearance_name=sphere)
        arcs_points = shell_around_core(central_sphere=(0,0,0,5), pitch=1, k=3, number_of_layers=10)

        arc_3d = {}
        for layer, angle in zip(range(7), [270-15*i for i in range(7)]):
            layer+=1
            arc_3d[layer] = create_arc_3d(*arcs_points[layer], angle=angle)

             # NOTE: Due to the way we created arc_3d, we need to create some tools to remove the overlapping volume
            if layer > 1:
                # create some tools to remove the overlapping volumewith 360 degrees
                arc_3d_tool = create_arc_3d(*arcs_points[layer-1], angle=360)
                combine_bodies(target_component=arc_3d[layer], tool_components=[arc_3d_tool], operation='cut', keep_tool=False)

            change_appearance(arc_3d[layer], rgb=(int(layer*255/7),0, int(layer*255/7)), new_appearance_name='arc_{}'.format(layer))

            

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))