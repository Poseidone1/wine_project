# EGM722 Remote Sensing Project: Wine Production Analysis

## 1. Overview
The focus of this project is to collect infornation of wine producers from Douro and Alentejio regions such as location of the vinery, type of grapes cultivated, analyse their productions and evalaute against the temperature and precipitation data extracted from gridded climate data.

## 2. Starting point
In order to use the script, [`git`](https://git-scm.com/downloads)  and [`Anconda`](https://docs.anaconda.com/anaconda/install/) need to be installed. The installation instructions can be followed in the corresponding webiste

## 3. Download and clone the repository
Once the application are installed and the **folder** structure, where to save the repository, has been create, the project can be **cloned** on the local computer. Below the steps:
###### GitHub desktop
   Open GitHub Desktop and select **File**, then **Clone Repository**. Select, then the **URL** tab, then enter the follwoing URL for this repository `https://github.com/Poseidone1/wine_project`
###### Command line
   Open **Git Bash** (from the **Start** menu if installed on **`Windows`**), then navigate to the folder where the repository will be cloned and execute the following command: `git clone https://github.com/Poseidone1/wine_project`. Some messages
   about downloading/unpacking files will be displyed and once terminated, the repository is set up.
###### GitHub webpage
   This repository can be installed from the GitHub reposiroty's page by clicking the **`clone or download`** button and select **`download ZIP`** at the bottom of the menu. Once it's downloaded, unzip the file.
   
## 4. Create a conda environment

Once the respository has been successfully cloned, the next sept is to create a **conda environment** to work through the project.
The *environment.yml* file provided in repository will help to setup the enviroment.
There are 2 options: 
- Anaconda Navigator: from the bottom of the **Environmwents** panel, select **Import**
- Command line: From the folder where the respository has been installed the following command needs to be run: `conda env create -f environment.yml`

## 5. Run Jupyter Notebook
There are 2 options in order to launch *Jupyter Notebook*
##### 1. Anaconda Navigator
From the dashboard Jupyter Notebook can be launched directly and then navigate to the folder where the repository is installed. 
**Note**
*Check that the environment created for the project has been activated*
##### 2. Command line
Open terminal and navigate to the folder where the repository is installed; activate the enviroment typing `conda activate <nameoftheenvironment>`; type `jupyter-notebook` (if windows is used) or `notebook` ( if Mac/Linux is used). A web page will open showing the current folder
