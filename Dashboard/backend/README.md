# Vehicle Traffic Analysis 

## Installation Guide
### 1 : Clone the github repo to your prefered directory using
```
https://github.com/Suwi-inc/Traffic-Analysis.git
```
### 2 : Navigate to the root directory of the project
```
cd Traffic-Analysis
```
### 3 : Install dependncies 
#### 3.1 : Preferbly create a virtual environment

```
Python -m venv venvironment
```
```
venvironment/Scripts/Activate 
```
#### 3.2 : Install project dependencies from requirements.txt
```
pip install -r requirements.txt
```
#### 3.3 : Install CUDA for pytrorch if running on a GPU
#####  Check if cuda is installed 
```
nvcc --version
``` 
Should produce an output with
```nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2025 NVIDIA Corporation
Built on xxx_Pacific_Standard_Time_2025
Cuda compilation tools, release version.subversion, Vversion.subversion
Build cuda_xx.x/compiler.xxx
```
If cuda is not installed you should get an output like
```
The program 'nvcc' is currently not installed. 
```
And you have to install CUDA to run the project using your GPU.

We need the cuda version and subverson and we will use that to install the corresponding pytorch version at ``https://pytorch.org/get-started/locally/``
for cuda 12.8 we use
```
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128
```
### 4 : Running the project 
### Make sure the input video is in the ``assets`` and the yolo detection model is in ``models`` directory or you can change the asset directories in ``Auto_Lane_With_Detector/main.py``
#### Navigate to ``Auto_Lane_With_Detector``
```
cd Auto_Lane_With_Detector
```
#### Start the project with
```
python main.py 
```
#### Optionally you can disbake some parameters wiuth 
```
python main.py --lanes=no --counter=no --vehicles=yes
```

