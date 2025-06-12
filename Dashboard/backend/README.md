# Vehicle Traffic Analysis 

## Installation Guide
### 1 : Clone the github repo to your prefered directory using
```
https://github.com/Suwi-inc/Dashboard.git
```
### 2 : Navigate to the root directory of the backend
```
cd Dashboard/backend
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
Make sure you have the following key files
#### 1: predefined_lanes.json in the src directory, this file can be made using the manual_plot.py file, instructions on how to use this can be found in [this Readme.](plot/README.md)
After this, run
```
python main.py 
```
to start the backend server.

