#Author-
#Description-


import adsk.core, adsk.fusion, traceback
import math
from random import randint

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
        def create_sphere(x=0, y=0, z=0, r=5, angle=360):
            sketch = sketches.add(xyPlane)

            # Draw a circle.
            circles = sketch.sketchCurves.sketchCircles
            circle = circles.addByCenterRadius(adsk.core.Point3D.create(x, y, z), r)

            # Draw a line to use as the axis of revolution.
            lines = sketch.sketchCurves.sketchLines
            circle_axisLine = lines.addByTwoPoints(adsk.core.Point3D.create(x, y-r, z), adsk.core.Point3D.create(x, y+r, z))

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
        def create_arc_3d(x=0, y=0, z=0, r=5, angle=360, pitch=1, k=3, layer=1):
            ''' k determines the ratio of 3 points 
            - i.e. 1 means everything is the same distance from core, 2 is twice form top and 1 from bot, 1.5 for the left    ''' 
            sketch = sketches.add(xyPlane)

            # Draw a circle.
            arcs = sketch.sketchCurves.sketchArcs;
            arc = arcs.addByThreePoints(adsk.core.Point3D.create(x, y-r-pitch*layer, z), adsk.core.Point3D.create(x-r-pitch*layer*(k+1)/2, y, z), adsk.core.Point3D.create(x, y+r+pitch*layer*k, z))

            # Draw a line to use as the axis of revolution.
            lines = sketch.sketchCurves.sketchLines
            arc_axisLine = lines.addByTwoPoints(adsk.core.Point3D.create(x, y-r-pitch*layer, z), adsk.core.Point3D.create(x, y+r+pitch*layer*k, z))

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
            color_property.value = adsk.core.Color.create(rgb[0], rgb[1], rgb[2], 1) 
            
            # Assign the new color to the occurrence.
            occurrence.appearance = new_appearance


        sphere = create_sphere(x=0,y=0,z=0,r=5,angle=360)
        change_appearance(sphere, rgb=(123,123,123), base_appearance_name='Aluminum - Anodized Glossy (Grey)', new_appearance_name=sphere)

        for angle, layer in zip([180+90,180+75,180+60,180+45,180+30,180+15,180], [1, 2,3,4,5,6,7]):
            # offset the z a bit otherwise the model overlapse too much
            arc = create_arc_3d(x=0, y=0, z=layer*0.01, r=5, angle=angle, pitch=1, k=2, layer=layer)
            change_appearance(arc, rgb=(int(layer*255/7),0, int(layer*255/7)), new_appearance_name='arc_{}'.format(layer))

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))