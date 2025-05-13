import os
import platform
import subprocess
import sys

def build_executable():
    # Get the current platform
    current_platform = platform.system().lower()
    
    # Define the entry point
    entry_point = "src/pygame/main.py"
    
    # Common PyInstaller options
    common_options = [
        "--name=particle_simulation",
        "--onefile",  # Create a single executable
        "--noconsole",  # Don't show console window
        "--clean",  # Clean PyInstaller cache
        f"--add-data=src:src",  # Include source files
        "--hidden-import=pydantic",  # Explicitly include pydantic
        "--hidden-import=pygame",  # Explicitly include pygame
        "--hidden-import=numpy",  # Explicitly include numpy
        "--hidden-import=PIL",  # Explicitly include Pillow
    ]
    
    # Platform specific options
    if current_platform == "windows":
        icon_option = "--icon=assets/icon.ico" if os.path.exists("assets/icon.ico") else ""
    else:
        icon_option = "--icon=assets/icon.png" if os.path.exists("assets/icon.png") else ""
    
    if icon_option:
        common_options.append(icon_option)
    
    # Build command
    build_command = ["pyinstaller"] + common_options + [entry_point]
    
    print(f"Building for {current_platform}...")
    print("Running command:", " ".join(build_command))
    
    # Run PyInstaller
    subprocess.run(build_command, check=True)
    
    print("\nBuild completed!")
    print(f"Executable can be found in the 'dist' directory")

if __name__ == "__main__":
    build_executable() 