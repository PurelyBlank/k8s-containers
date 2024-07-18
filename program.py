import os
import time
import subprocess

def run_user_program():
    """
    Run the user program if it exists.
    """
    if os.path.isfile('/user_program.py'):
        print("Found user_program.py, running it...")
        try:
            subprocess.run(['python', '/user_program.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the script: {e}")
        print("Finished running user_program.py.")
    else:
        print("user_program.py not found, continuing to watch...")

def main():
    """
    Main loop to watch for the user program.
    """
    print("Starting watcher...")
    while True:
        run_user_program()
        time.sleep(5)  # Check every 5 seconds


if __name__ == "__main__":
    main()