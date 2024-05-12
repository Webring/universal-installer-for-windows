pyinstaller --onefile --clean -i icon.ico --distpath dev/ -n uifw main.py
del uifw.spec
rd /s /q "build"