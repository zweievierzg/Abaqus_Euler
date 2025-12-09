import import_test
import numpy as np

import abaqus
from abaqus import *
from abaqusConstants import *
import parameters as p
reload(p)
import os
import sys

def create_cantilever_model(folder_name, nx,ny,nz):

    ## Create Base Model for Cantilever Beam


    # ensures that the model is empty
    mdb.Model(name='temp', modelType=STANDARD_EXPLICIT)
    assembly_= mdb.models['temp'].rootAssembly
    assembly_= mdb.models['Model-1'].rootAssembly
    del mdb.models['Model-1']
    assembly_= mdb.models['temp'].rootAssembly
    mdb.Model(name='Model-1', modelType=STANDARD_EXPLICIT)
    assembly_= mdb.models['Model-1'].rootAssembly
    assembly_= mdb.models['temp'].rootAssembly
    del mdb.models['temp']
    assembly_= mdb.models['Model-1'].rootAssembly


    
    sketch_ = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    sketch_geometry, sketch_vertices, sketch_dimensions, sketch_constraints = sketch_.geometry, sketch_.vertices, sketch_.dimensions, sketch_.constraints
    sketch_.setPrimaryObject(option=STANDALONE)
    sketch_.rectangle(point1=(0.0, 0.0), point2=(50.0, 50.0))
    part_ = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    part_ = mdb.models['Model-1'].parts['Part-1']
    part_.BaseSolidExtrude(sketch=sketch_, depth=100.0)
    sketch_.unsetPrimaryObject()
    part_ = mdb.models['Model-1'].parts['Part-1']
    del mdb.models['Model-1'].sketches['__profile__']
    mdb.models['Model-1'].Material(name='Placeholder')
    mdb.models['Model-1'].materials['Placeholder'].Elastic(table=((10.0, 0.3), ))
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
        material='Placeholder', thickness=None)
    part_ = mdb.models['Model-1'].parts['Part-1']
    c = part_.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region = part_.Set(cells=cells, name='Set-1')
    part_ = mdb.models['Model-1'].parts['Part-1']
    part_.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    assembly_= mdb.models['Model-1'].rootAssembly
    assembly_= mdb.models['Model-1'].rootAssembly
    assembly_.DatumCsysByDefault(CARTESIAN)
    part_ = mdb.models['Model-1'].parts['Part-1']
    assembly_.Instance(name='Part-1-1', part=part_, dependent=ON)
    p1 = mdb.models['Model-1'].parts['Part-1']

    ## specify the number of elements in each direction
    part_ = mdb.models['Model-1'].parts['Part-1']
    e = part_.edges
    pickedEdges = e.getSequenceFromMask(mask=('[#10 ]', ), )
    part_.seedEdgeByNumber(edges=pickedEdges, number= nx, constraint=FINER)
    part_ = mdb.models['Model-1'].parts['Part-1']
    e = part_.edges
    pickedEdges = e.getSequenceFromMask(mask=('[#80 ]', ), )
    part_.seedEdgeByNumber(edges=pickedEdges, number= ny , constraint=FINER)
    part_ = mdb.models['Model-1'].parts['Part-1']
    e = part_.edges
    pickedEdges = e.getSequenceFromMask(mask=('[#20 ]', ), )
    part_.seedEdgeByNumber(edges=pickedEdges, number= nz, constraint=FINER)
    part_ = mdb.models['Model-1'].parts['Part-1']
    part_.generateMesh()



    # part_.seedPart(size=5.0, deviationFactor=0.1, minSizeFactor=0.1)
    # part_ = mdb.models['Model-1'].parts['Part-1']
    # part_.generateMesh()
    assembly_= mdb.models['Model-1'].rootAssembly
    assembly_.regenerate()

    assembly_= mdb.models['Model-1'].rootAssembly
    f1 = assembly_.instances['Part-1-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#10 ]', ), )
    region = assembly_.Set(faces=faces1, name='Fixed_Face')
    mdb.models['Model-1'].EncastreBC(name='BC-1', createStepName='Initial', 
        region=region, localCsys=None)

    assembly_= mdb.models['Model-1'].rootAssembly
    assembly_.ReferencePoint(point=(0.0, -20.0, 100.0))
    assembly_= mdb.models['Model-1'].rootAssembly
    assembly_.features['RP-1'].setValues(xValue=25.0)
    assembly_= mdb.models['Model-1'].rootAssembly
    assembly_.regenerate()
    assembly_= mdb.models['Model-1'].rootAssembly
    r1 = assembly_.referencePoints
    refPoints1=(r1[5], )
    assembly_.Set(referencePoints=refPoints1, name='Reference_Point')
    assembly_= mdb.models['Model-1'].rootAssembly
    region1= assembly_.sets['Reference_Point']
    assembly_= mdb.models['Model-1'].rootAssembly
    e1 = assembly_.instances['Part-1-1'].edges
    edges1 = e1.getSequenceFromMask(mask=('[#400 ]', ), )
    region2= assembly_.Set(edges=edges1, name='Load_Edge')
    mdb.models['Model-1'].Coupling(name='Constraint-1', controlPoint=region1, 
        surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
        alpha=0.0, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)

    mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')

    assembly_= mdb.models['Model-1'].rootAssembly
    region = assembly_.sets['Reference_Point']
    mdb.models['Model-1'].ConcentratedForce(name='Load-1', createStepName='Step-1', 
        region=region, cf2=-1.0, distributionType=UNIFORM, field='', 
        localCsys=None)

    assembly_= mdb.models['Model-1'].rootAssembly
    f1 = assembly_.instances['Part-1-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#20 ]', ), )
    assembly_.Set(faces=faces1, name='Fixed_Face')

    mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
        'CDISP', 'CF', 'CSTRESS', 'LE', 'PE', 'PEEQ', 'PEMAG', 'RF', 'S', 'U', 
        'SENER', 'EVOL'))
    

    working_directory = os.path.join(p.work_path, folder_name)
    if not os.path.exists(working_directory):
        os.makedirs(working_directory)

    file_name = folder_name + "_base_model.cae"
    file_path = os.path.join(working_directory, file_name)


    mdb.saveAs(pathName=file_path)


def main():
    message_single_cantilever_step = "Test Message.\n"
    sys.__stdout__.write(message_single_cantilever_step)
    sys.__stdout__.flush()
    print("Running main function...")
    arr = np.array([1, 2, 3])
    print("Numpy array:", arr)
    import_test.test_array()


