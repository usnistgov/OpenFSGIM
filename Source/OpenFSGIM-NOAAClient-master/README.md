# OpenFSGIM-NOAAClient
The OpenFSGIM-NOAAClient application is used to extract weather
information from the National Oceanic and Atmospheric Administration
using the Weather API Ver 2.0 interface.

## Windows Environment Setup

    {Needs to be updated for Windows Environments}

## Linux Ubuntu 16.04 Environment Setup
Ubuntu 16.04 comes with Python 2.7 and Python 3.5 by default. However, the **OpenFSGIM-NOAAClient**
requires Python version 3.6 as well as required Python library packages to function properly. This requires
the installation of the Python Pip ("Pip installs Packages" or "Pip installs Python")
package management system and Python 3.6.

#### Python 3.6 Installation and Configuration
The latest version of Python 3.6 is available from the [Python Software Foundation](https://www.python.org/downloads/) website.
1.  Access the Python Software Foundation website by clicking on the highlighted link and download the latest
    Python version.
2.  When the download has been completed Open a terminal window via Ctrl+Alt+T or searching for "Terminal"
    from the app launcher.  When it opens, ensure your your Ubuntu environment is up-to-date with all its
    packages.  To do so use the following command:

    ```
    sudo apt update && sudo apt -y upgrade
    ```
    _Type in your password (no visual feedback will appear to ensure security of your password) when it asks and
    hit ENTER. This will update everything on your Ubuntu environment to the latest released version._

3.  You are no ready to install Python 3.6, using the following commands:
    ```
    cd {directory where the Python 3.6 file is saved}
    
    tar -xvf Python-3.6.x.tgz
    
    mv Python-3.6.x {desired directory location}
    
    cd {target directory of "mv" command}
    
    ./configure
    ```
4.  If there are no errors, run the following commands to complete the installation process of Python
    3.6:
    ```
    make
    
    sudo make install
    ```
5.  If you get the following error message:
    ```
    zipimport.ZipImportError: can't compress data; zlib not available
    ```
6.  Install the 'zlib1g-dev' package using the following command:
    ```
    sudo apt install zlib1g-dev
    ```
7.  After the 'zlib1g-dev' package is installed run the following commands:
    ```
    make
    
    sudo make install
    ```
8.  Once it is installed, verify the installed version by using the following command:
    ```
    python3 -V
    ```
    ![Python3%20Version](Python3%20Version.png)
#### Pip Package Installation

1.  Install the Pip package management system using the following command:
    ```
    sudo apt install python-pip
    ```
2.  That's it!  Now the latest version of Pip is installed on your Ubuntu.  You can check which
    version of Pip you installed by using the following command:
    ```
    pip -V
    ```
    ![Pip%20Version](Pip%20Version.png)
#### How to Install Packages Using Pip
Now that Pip is installed on your system, it is time to install some packages.
1.  You can **search for a package** using the following command:
    ```
    pip search {packageName}
    ```
    _Replace {packageName} with the name of the package you are trying to install_.  This command
    will search PyPI (Python Package Index) for packages with the name you provide.
2.  After you find the desired package, you can install it using the following command:
    ```
    pip install {packagName}
    ```
3.  To uninstall it, use the following command:
    ```
    pip uninstall {packageName}
    ```
4.  To see all of the Pip command syntax, use the following command:
    ```
    pip --help
    ```

## Application Setup
Note: You will need to download and install the [OpenFSGIM-NOAAClient](https://github.com/usnistgov/OpenFSGIM-NOAAClient)
application locally (the following instructions utilize Linux commands).

1.  Clone the project from github (requires access permission):
    ```
    git clone https://github.com/usnistgov/OpenFSGIM-NOAAClient
    ```
2.  The OpenFSGIM-NOAAClient requires several library packages to be installed.  Use the following
    command to install the required packages:
    ```
    sudo pip install requests
    
    sudo pip install python-dateutil
    
    sudo pip install python-oauth2
    ```
## Application Execution
The OpenFSGIM-NOAAClient application is designed to be run using the Python Command Line Interface (CLI).  






