@set HERE=%~dp0
@call %HERE%\venv\Scripts\activate.bat
python %HERE%\main.py %*
@deactivate