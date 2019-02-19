import adsk.core, adsk.fusion, adsk.cam, traceback
from random import randint

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Create a new document.
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)        
        des = adsk.fusion.Design.cast(doc.products.itemByProductType('DesignProductType'))
        root = des.rootComponent

        # Get a reference to an appearance in the library.
        lib = app.materialLibraries.itemByName('Fusion 360 Appearance Library')
        libAppear = lib.appearances.itemByName('Plastic - Matte (Yellow)')

        numParts = 6
        for i in range(numParts):
            # Create an extrusion.
            sk = root.sketches.add(root.xYConstructionPlane)
            sk.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(i*3,0,0), 1)
            prof = sk.profiles.item(0)
            ext = root.features.extrudeFeatures.addSimple(prof, adsk.core.ValueInput.createByReal(4), adsk.fusion.FeatureOperations.NewComponentFeatureOperation)
            comp = ext.parentComponent
            
            # Get the single occurrence that references the component.
            occs = root.allOccurrencesByComponent(comp)
            occ = occs.item(0)
           
            # Create a copy of the existing appearance.
            newAppear = des.appearances.addByCopy(libAppear, 'Color ' + str(i+1))
            
            # Edit the "Color" property by setting it to a random color.
            colorProp = adsk.core.ColorProperty.cast(newAppear.appearanceProperties.itemByName('Color'))
            red = randint(0,255)
            green = randint(0,255)
            blue = randint(0,255)
            colorProp.value = adsk.core.Color.create(red, green, blue, 1)          
            
            # Assign the new color to the occurrence.
            occ.appearance = newAppear


            
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))