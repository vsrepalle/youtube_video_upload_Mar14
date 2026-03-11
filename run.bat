@echo off 
echo Installing dependencies... 
pip install -r requirements.txt 
echo. 
echo Running video generator... 
python run.py --json data.json 
pause 
