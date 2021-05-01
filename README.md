# EGM722 Remote Sensing Project: Wine Production Analysis

## 1. Overview
The scope of this script is to prepare,organise and visualise spatial data of wine producers of Douro region located in Portugal; in the following steps weather data will be used to analyses the impact of climate change on the whole wine production of the region and on the single grapes used in the area

## 2. Starting point: software installation
In order to use the script, [`git`](https://git-scm.com/downloads)  and [`Anconda`](https://docs.anaconda.com/anaconda/install/) need to be installed. The installation instructions can be followed in the corresponding webiste

## 3. Download and clone the repository
Once the application have been installed and the **folder** structure, where to save the repository, has been created, the project can be **cloned** on the local computer by following one of  the steps mentioned below::
###### GitHub desktop
   Open GitHub Desktop and select **File**, then **Clone Repository**. Select, then the **URL** tab, then enter the following URL for this repository `https://github.com/Poseidone1/wine_project`
###### Command line
   Open **Git Bash** (from the **Start** menu if installed on **`Windows`**) or open **Terminal** if Mac/Linux is used; navigate to the folder where the repository will be cloned and execute the following command: `git clone https://github.com/Poseidone1/wine_project`. Some messages about downloading/unpacking files will be displyed and once terminated, the repository is set up.
###### GitHub webpage
   This repository can be installed from the GitHub repository page by clicking the **`clone or download`** button and select **`download ZIP`** at the bottom of the menu. Once it's been downloaded, unzip the file.
   
## 4. Create a conda environment

Once the repository has been successfully cloned, the next sept is to create a **conda environment** to work through the project.
The *environment.yml* file provided in repository will help to setup it.
There are 2 options: 
- Anaconda Navigator: from the bottom of the **Environments** panel, select **Import** and then choose the *environment.yml* file.
- Command line: From the folder where the repository has been installed the following command needs to be run: `conda env create -f environment.yml`

## 5. Run Jupyter Notebook
There are 2 options in order to launch *Jupyter Notebook*
##### 1. Anaconda Navigator
From the dashboard Jupyter Notebook can be launched directly and then navigate to the folder where the repository is installed. 
**Note**
*Check that the environment created for the project has been activated*
##### 2. Command line
Open terminal and navigate to the folder where the repository is installed; activate the enviroment typing `conda activate wine_project` for Mac/Linux pc or `activate wine_project` for Windows pc. Type `jupyter-notebook` or `notebook` if Windows or Mac/Linux are respectively used. A web page will open showing the current folder
