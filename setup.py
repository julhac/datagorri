import sys
import os

base = None
if sys.platform == "win32":
    from cx_Freeze import setup, Executable

    os.environ['TCL_LIBRARY'] = "C:\\Users\\ga47dop\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
    os.environ['TK_LIBRARY'] = "C:\\Users\\ga47dop\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"

    build_exe_options = {"packages": ["tkinter","bs4","requests","json","csv","os","hashlib","time","datetime","urllib.parse","sys","copy"],"include_msvcr": False,"bin_excludes":["VCRUNTIME140.dll"],"include_files":["tcl86t.dll","tk86t.dll","samples","docs"]}
    
    base = "Win32GUI"

    setup(name="DataGorri",         # Edited by JH
          version="1.1",            # Edited by JH
          options={"build_exe": build_exe_options},
          executables=[Executable("datagorri/DataGorri.py",
                                  shortcutName="DataGorri",
                                  shortcutDir="DesktopFolder",
                                  base=base,
                                  icon="favicon.ico"
                                  )
                       ]
          )

if sys.platform == "linux" or sys.platform == "linux2":    
    from setuptools import setup, find_packages

    setup(
        name="DataGorri",
        version="1.2",
        description="Application to extract data from tables and lists located on websites",
        url="https://github.com/julhac/datagorri",
        packages=find_packages(),
        entry_points={
            'gui_scripts': ['datagorri=datagorri.DataGorri']
        },
        data_files=[
            ('share/applications/', ['datagorri.desktop'])
        ]
    )
