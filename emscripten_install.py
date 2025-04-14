import os
import sys
import subprocess
import platform

def check_command(cmd):
    try:
        subprocess.run([cmd, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        return False

def run_command(cmd, shell=False):
    print("Running:", " ".join(cmd) if isinstance(cmd, list) else cmd)
    result = subprocess.run(cmd, shell=shell)
    if result.returncode != 0:
        print("Error: Command failed:", cmd)
        sys.exit(result.returncode)

def clone_or_update_emsdk():
    if os.path.isdir("emsdk"):
        print("The 'emsdk' directory exists. Updating repository...")
        os.chdir("emsdk")
        run_command(["git", "pull"])
        os.chdir("..")
    else:
        print("Cloning the emsdk repository...")
        run_command(["git", "clone", "https://github.com/emscripten-core/emsdk.git"])

def install_emsdk():
    os.chdir("emsdk")
    print("Installing the latest Emscripten version...")
    # On Windows, the executable scripts are .bat; on Unix, they're shell scripts.
    if os.name == 'nt':
        run_command(["emsdk.bat", "install", "latest"], shell=True)
        print("Activating the latest Emscripten version...")
        run_command(["emsdk.bat", "activate", "latest"], shell=True)
        print("\nFor Windows, to load the Emscripten environment, run:")
        print("    emsdk_env.bat")
    else:
        run_command(["./emsdk", "install", "latest"])
        print("Activating the latest Emscripten version...")
        run_command(["./emsdk", "activate", "latest"])
        print("\nTo load the Emscripten environment in your current shell, run:")
        print("    source ./emsdk_env.sh")
    os.chdir("..")

def main():
    if not check_command("git"):
        print("Error: Git is not installed. Please install Git and try again.")
        sys.exit(1)
    
    clone_or_update_emsdk()
    install_emsdk()

if __name__ == "__main__":
    main()
