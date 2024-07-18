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
        
        # Clean up copied user_program.py after running once
        os.remove('/user_program.py')
        if os.path.isfile('/user_program.py'):
            print("Failed to remove user_program.py from pod.")
        else:
            print("Successfully removed user_program.py from pod.")
    else:
        # print("user_program.py not found, continuing to watch...")
        return

def main():
    """
    Main loop to watch for the user program.
    """
    print("Starting watcher...")
    while True:
        run_user_program()
        # Check every 5 seconds
        time.sleep(5)  

if __name__ == "__main__":
    main()
