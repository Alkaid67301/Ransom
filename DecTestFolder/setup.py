from cx_Freeze import setup, Executable
import sys

buildOptions = dict(packages = ["sys", "os", "Crypto.Cipher", "Crypto.Hash", "glob"],  # 1
	excludes = [])

exe = [Executable("Dec.py")]  # 2

# 3
setup(
    name='DecTest',
    version = '0.1.0',
    author = "LYE",
    description = "Project",
    options = dict(build_exe = buildOptions),
    executables = exe
)
