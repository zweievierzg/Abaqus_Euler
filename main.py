import import_test
import numpy as np

import abaqus
from abaqus import *
from abaqusConstants import *




import os
import sys

def Euler_Test_Model(file_path):
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.rectangle(point1=(0.0, 0.0), point2=(50.0, 50.0))
    p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Part-1']
    p.BaseSolidExtrude(sketch=s, depth=50.0)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    mdb.models['Model-1'].Material(name='Material-1')
    mdb.models['Model-1'].materials['Material-1'].Elastic(table=((20.0, 0.48), ))
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
        material='Material-1', thickness=None)
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(cells=cells, name='Set-1')
    p = mdb.models['Model-1'].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=OFF, 
        constraints=OFF, connectors=OFF, engineeringFeatures=OFF)
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['Part-1']
    a.Instance(name='Part-1-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF, mesh=ON)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    p1 = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-1'].parts['Part-1']
    p.seedPart(size=5.0, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models['Model-1'].parts['Part-1']
    p.generateMesh()
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, connectors=ON)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=129.037, 
        farPlane=240.192, width=119.492, height=60.5523, cameraPosition=(
        36.492, -31.9049, 200.26), cameraUpVector=(-0.471156, 0.88092, 
        -0.0446285), cameraTarget=(26.049, 22.9021, 26.049))
    a = mdb.models['Model-1'].rootAssembly
    f1 = a.instances['Part-1-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#8 ]', ), )
    region = a.Set(faces=faces1, name='Set-1')
    mdb.models['Model-1'].EncastreBC(name='BC-1', createStepName='Initial', 
        region=region, localCsys=None)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
        predefinedFields=OFF, connectors=OFF, adaptiveMeshConstraints=ON)
    mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=121.206, 
        farPlane=246.063, width=112.24, height=56.8777, cameraPosition=(
        78.2338, 115.244, 175.82), cameraUpVector=(-0.616751, 0.572147, 
        -0.540617), cameraTarget=(26.4305, 24.2471, 25.8256))
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['Part-1-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#2 ]', ), )
    region = a.Surface(side1Faces=side1Faces1, name='Surf-1')
    mdb.models['Model-1'].Pressure(name='Load-1', createStepName='Step-1', 
        region=region, distributionType=UNIFORM, field='', magnitude=0.1, 
        amplitude=UNSET)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
        predefinedFields=OFF, connectors=OFF)
    
    mdb.saveAs(pathName=file_path)


    mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, numThreadsPerMpiProcess=1, 
        multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)
    mdb.jobs['Job-1'].submit(consistencyChecking=OFF)

    
    



def main():
    ## testing outputs and imports

    message_single_cantilever_step = "Test Message.\n"
    sys.__stdout__.write(message_single_cantilever_step)
    sys.__stdout__.flush()
    sys.__stdout__.write(message_single_cantilever_step)
    sys.__stdout__.flush()
    arr1 = np.array([1, 2, 3])
    sys.__stdout__.write('arr1'+str(arr1) + "\n")
    sys.__stdout__.flush()
    arr2 = import_test.test_array()
    sys.__stdout__.write('arr2'+str(arr2) + "\n")
    sys.__stdout__.flush()


    ## windows path for blade server
    # working_directory = r"C:\Users\langw\Desktop\ETH sache\Semester Project\Scripts_Local\Abaqus_Euler"

    ## unix path for Euler
    home = os.path.expanduser("~")
    working_directory = os.path.join(home, "Abaqus_Euler")

    # Create directory if it doesn't exist
    if not os.path.exists(working_directory):
        os.makedirs(working_directory)

    folder_name = "Euler_Test"
    file_name = folder_name + "_model.cae"
    file_path = os.path.join(working_directory, file_name)

    
    # create an abaqus model
    # create_cantilever_model("Cantilever_Test", 4,4,8, file_path)
    Euler_Test_Model(file_path)


    # mdb.saveAs(pathName=file_path)



if __name__ == "__main__":
    main()


