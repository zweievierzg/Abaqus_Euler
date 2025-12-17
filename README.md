# Abaqus_Euler
Should run Abaqus on Euler HPC. The purpose is to check on how execute a python script with abaqus. Imports of code files need to work as the real coding project consists of a lot of separate files.

- Windows:
    - works
    - to run on windows make sure the windows working_directory is uncommented in main() in main.py. Then open a command prompt and navigate to the Abaqus_Euler folder. In the command prompt type 'abaqus cae noGUI=main.py'. This should create and run an abaqus model. A '.cae' file and 'Job-1.*' files will be created. 'Job-1.odb' is the output database (results) of the model. To check abaqus runtime outputs check the 'abaqus.rpy' file.

- To run on Euler the path was changed to a unix path. Check in main() in main.py. To run on Euler: 1. git clone repo 2. type 'sbatch run_main.slurm'. Running on Euler leads to following error:
    ![alt text](image.png)


    
