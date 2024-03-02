Set objShell = CreateObject("WScript.Shell")

' Step 1: Change directory to D:\Python Project\then v0.1.2
objShell.CurrentDirectory = "D:\Python Project\then v0.1.2"

' Step 2: Run the activate.bat script to activate the virtual environment and execute main.py
objShell.Run "cmd /k cd /D ""D:\Python Project\then v0.1.2"" && call ""cuda\Scripts\activate.bat"" && python main.py", 1, True
