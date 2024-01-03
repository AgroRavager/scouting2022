# Miniconda must be installed before running this setup script.
#
# WINDOWS
#========
# Run this script from an Anaconda Powershell prompt, using the base
# Anaconda environment.
# Command: 
# .\setup_irs22.ps1
#
# MAC AND LINUX
# =============
# Run this command from Terminal.
# Command:
# source setup_irs22.ps1

conda deactivate
conda create --name irs22 -y python=3.9.7

conda activate irs22
conda install -y -c conda-forge nodejs
conda install -y -c conda-forge jupyterlab
conda install -y -c conda-forge flask=2.0.2
conda install -y -c conda-forge flask-socketio=5.1.1
conda install -y -c conda-forge eventlet=0.33.0
conda install -y pandas=1.3.5
conda install -y bokeh=2.4.2
conda install -y -c conda-forge jupyter_bokeh=3.0.4
conda install -y pytest=6.2.5
conda install -y pylint=2.9.6
conda install -y xlsxwriter=3.0.2
