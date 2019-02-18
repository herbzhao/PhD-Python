import adsk.core, adsk.fusion, traceback
import csv, math


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
        sketches = rootComp.sketches;
        xyPlane = rootComp.xYConstructionPlane;

        #  a method to create sphere from xyz and radius
        def create_sphere(xyzr =  [0, 0, 0, 5]):
            sketch = sketches.add(xyPlane)

            # Draw a circle.
            circles = sketch.sketchCurves.sketchCircles
            circle = circles.addByCenterRadius(adsk.core.Point3D.create(xyzr[0], xyzr[1], xyzr[2]), xyzr[3])

            # Draw a line to use as the axis of revolution.
            lines = sketch.sketchCurves.sketchLines
            circle_axisLine = lines.addByTwoPoints(adsk.core.Point3D.create(xyzr[0]-xyzr[3], xyzr[1], xyzr[2]), adsk.core.Point3D.create(xyzr[0]+xyzr[3], xyzr[1], xyzr[2]))

            # Get the profile defined by the circle.
            circle_prof = sketch.profiles.item(0)

            # Create an revolution input to be able to define the input needed for a revolution
            # while specifying the profile and that a new component is to be created
            revolves = rootComp.features.revolveFeatures
            circle_revInput = revolves.createInput(circle_prof, circle_axisLine, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)

            # Define that the extent is an angle of pi to get half of a torus.
            angle = adsk.core.ValueInput.createByReal(2*math.pi) 
            circle_revInput.setAngleExtent(False, angle)

            # Create the extrusion.
            ext = revolves.add(circle_revInput)
        

        #  read xyzr from the csv generated from SEM image
        max_radius = 32
        xs = []
        ys = []
        zs = []
        with open(r'C:\Users\My Pc\Documents\GitHub\PhD-Python\dongpo\{}.csv'.format(max_radius), newline='\n') as file:
            csv_reader = csv.reader(file, delimiter=',')
            next(csv_reader, None)
            for row in csv_reader:
                x,y,z,r = [float(row[0]), float(row[1]), float(row[2]), float(row[3])]
                xs.append(x)
                ys.append(y)
                zs.append(z)

            min_x, max_x = [min(xs), max(xs)]
            min_y, max_y = [min(xs), max(xs)]

        for x, y, z in zip(xs, ys, zs):
            # radius is the maximum of the sphere
            create_sphere([x, y, z, max_radius])

        # create cross section
        cross_section_sketch = sketches.add(xyPlane)
        lines = cross_section_sketch.sketchCurves.sketchLines;
        recLines = lines.addTwoPointRectangle(adsk.core.Point3D.create(min_x-max_radius, min_y-max_radius, 0), adsk.core.Point3D.create(max_x+max_radius, max_y+max_radius, 0))
        



    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))