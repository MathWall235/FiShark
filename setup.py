from cx_Freeze import setup, Executable

executables = [Executable("main.py")]

setup(
    name="FiShark",
    version="1.0",
    description="FiShark Game",
    options={"build_exe": {"packages": ["pygame"]}},
    executables=executables
)
