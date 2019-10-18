d:
cd D:\dev\python3\EasyOM_Work_Assistant

del *.spec
rd /s /q build 
rd /s /q dist

pyinstaller -w -i "src/easyOM.ico" "EasyOM_WA.py" --hidden-import PyQT5.sip --key 1987623450675681

xcopy src dist\EasyOM_WA\src\ /s
xcopy conf dist\EasyOM_WA\conf\ /s

del *.spec
rd /s /q build

pause