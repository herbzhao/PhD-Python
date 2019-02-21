import adsk.core, adsk.fusion, adsk.cam, traceback
import math, random

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent

        # Draw a box.
        length = 20
        width = 10
        height = 15
        
        boxOcc = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        boxComp = boxOcc.component
        boxSketch = boxComp.sketches.add(boxComp.xYConstructionPlane)
        lines = []
        linesCol = boxSketch.sketchCurves.sketchLines
        lines.append(linesCol.addByTwoPoints(adsk.core.Point3D.create(0,0,0),
                                             adsk.core.Point3D.create(length,0,0)))
        lines.append(linesCol.addByTwoPoints(lines[0].endSketchPoint,
                                             adsk.core.Point3D.create(length,width,0)))
        lines.append(linesCol.addByTwoPoints(lines[1].endSketchPoint,
                                             adsk.core.Point3D.create(0,width,0)))
        lines.append(linesCol.addByTwoPoints(lines[2].endSketchPoint,
                                             lines[0].startSketchPoint))

        boxComp.features.extrudeFeatures.addSimple(boxSketch.profiles.item(0),
                                                adsk.core.ValueInput.createByReal(height),
                                                adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                                                
        # Draw a sphere.
        radius = 3

        spheres = []        
        spheres.append(root.occurrences.addNewComponent(adsk.core.Matrix3D.create()))
        sphereComp = spheres[0].component
        sphereSketch = sphereComp.sketches.add(sphereComp.xYConstructionPlane)
        arc = sphereSketch.sketchCurves.sketchArcs.addByCenterStartSweep(adsk.core.Point3D.create(0,0,0),
                                                                        adsk.core.Point3D.create(0,-radius,0),
                                                                        math.pi)
        line = sphereSketch.sketchCurves.sketchLines.addByTwoPoints(arc.startSketchPoint, arc.endSketchPoint)                                        
        
        sphereInput = sphereComp.features.revolveFeatures.createInput(sphereSketch.profiles.item(0),
                                                        line, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        sphereInput.setAngleExtent(False, adsk.core.ValueInput.createByReal(math.pi * 2))
        sphereComp.features.revolveFeatures.add(sphereInput)
        
        # Create several instances of the sphere randomly placed within the box.
        for i in range(25):
            x = random.random()*length
            y = random.random()*width
            z = random.random()*height
            
            trans = adsk.core.Matrix3D.create()
            trans.translation = adsk.core.Vector3D.create(x,y,z)
            spheres.append(root.occurrences.addExistingComponent(sphereComp, trans))
        
        
        target = boxComp.bRepBodies.item(0).createForAssemblyContext(boxOcc)
        tools = adsk.core.ObjectCollection.create()
        for i in range(len(spheres)):
            tools.add(sphereComp.bRepBodies.item(0).createForAssemblyContext(spheres[i]))
        combInput = root.features.combineFeatures.createInput(target, tools)
        combInput.isKeepToolBodies = False
        combInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        root.features.combineFeatures.add(combInput)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))