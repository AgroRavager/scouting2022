#!/bin/zsh

# Runs Flask server in production mode
# To run in windows PowerShell: ./scout.ps1
# To run in Mac or Linux: source scout.ps1
$filename =  Get-Date -UFormat "%B_%d_%Y_%H_%M_%S"
$filepath = "./scoutput/"+$filename+".log"
Out-File -Encoding ASCII -FilePath $filepath -NoClobber
python run_scouter.py 192.168.1.1 *> $filepath