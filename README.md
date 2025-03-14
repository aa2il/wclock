# World Clock

Clock showing GMT time and Gray Line.

![World Clock Screen Shot]( Docs/wclock.png)

# Installation under Linux:

1) Uses python3 and pyqt
2) Clone gitub wclock, libs and data repositories
      
      cd
      mkdir Python
      cd Python
      git clone https://github.com/aa2il/wclock
      git clone https://github.com/aa2il/libs
      git clone https://github.com/aa2il/data
      
3) Install packages needed for wclock:

     cd ~/Python/wclock
     pip3 install -r requirements.txt
     
4) Make sure its executable:

     chmod +x wclock.py
     
5) Set PYTHON PATH so os can find libraries:

   - Under tcsh:      setenv PYTHONPATH $HOME/Python/libs
   - Under bash:      export PYTHONPATH="$HOME/Python/libs"
   
6) Bombs away:

     ./wclock.py

# Installation under Mini-conda:

0) Good video:  https://www.youtube.com/watch?v=23aQdrS58e0&t=552s

1) Point browser to https://docs.conda.io/en/latest/miniconda.html
2) Download and install latest & greatest Mini-conda for your particular OS:
   - I used the bash installer for linux
   - As of July 2023: Conda 23.5.2 Python 3.11.3 released July 13, 2023
   - cd ~/Downloads
   - bash Miniconda3-latest-Linux-x86_64.sh
   - Follow the prompts

   - If you'd prefer that conda's base environment not be activated on startup, 
      set the auto_activate_base parameter to false: 

      conda config --set auto_activate_base false

   - To get it to work under tcsh:
       - bash
       - conda init tcsh
       - This creates ~/.tcshrc - move its contents to .cshrc if need be
       - relaunch tcsh and all should be fine!
       - Test with:
           - conda list

3) Create a working enviroment for ham radio stuff:
   - Check which python version we have:
       - conda list   
   - conda create --name aa2il python=3.11

   - To activate this environment, use:
       - conda activate aa2il
   - To deactivate an active environment, use:
       - conda deactivate

   - conda env list
   - conda activate aa2il

4) Clone gitub wclock, libs and data repositories:

      cd
      mkdir Python
      cd Python
      git clone https://github.com/aa2il/wclock
      git clone https://github.com/aa2il/libs
      git clone https://github.com/aa2il/data

5) Install packages needed by wclock:

     conda activate aa2il
     cd ~/Python/wclock
     pip3 install -r requirements.txt

6) Set PYTHON PATH so os can find libraries:
   - Under tcsh:      setenv PYTHONPATH $HOME/Python/libs
   - Under bash:      export PYTHONPATH="$HOME/Python/libs"

7) To run wclock, we need to specify python interpreter so it doesn't run in
   the default system environment:
   
     cd ~/Python/wclock
     conda activate aa2il
     python wclock.py

8) Known issues using this (as of March 2025):
   - None

# Installation for Windoz:

0) One option is to use miniconda and follow the directions above.
      
1) I had success installing Python (v3.12 as of Oct 2024) from the Microslop Store
   (or directly from python.org).

2) Clone gitub repositories.  There are several tools available for windows
   for fetching git repositories.  I use the command line version from
   
       https://git-scm.com/downloads/win
       
   Find one you like, open a command prompt and effect the following:
   
      cd %userprofile%       (Goto YOUR_HOME_DIRECTORY, very clumsy!)
      mkdir Python
      cd Python
      rmdir /s wclock
      rmdir /s libs
      git clone https://github.com/aa2il/wclock
      git clone https://github.com/aa2il/libs

3) Install dependancies:

      pip install -r requirements.txt

4) Bombs away:

      cd %userprofile%\Python\wclock
      python wclock.py
