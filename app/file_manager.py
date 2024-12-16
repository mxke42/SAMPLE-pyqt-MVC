import os
import shutil
import time
import subprocess

# Define directories
WATCH_DIR = "/home/m/Projects/custom-resume"
DEST_DIR = "/home/m/Documents/NewJob/Resumes"
OLD_DIR = os.path.join(DEST_DIR, "OLD")


def process_new_resume():
    # Ensure destination and OLD directories exist
    os.makedirs(DEST_DIR, exist_ok=True)
    os.makedirs(OLD_DIR, exist_ok=True)

    # Define the source file
    src_file = os.path.join(WATCH_DIR, "Updated_Resume.pdf")

    # Check if the source file exists
    if not os.path.exists(src_file):
        print(f"No file found at {src_file}. Exiting...")
        return

    # Wait until the file is stable (size stops changing)
    #print("Checking file stability...")
    while True:
        size1 = os.path.getsize(src_file)
        time.sleep(1)  # Wait for 1 second
        size2 = os.path.getsize(src_file)

        if size1 == size2:
            #print(f"File is stable: {src_file}")
            break

    # Define the new name and destination
    new_name = "resume_max_keirn.pdf"
    dest_file = os.path.join(DEST_DIR, new_name)

    # If the destination file exists, move it to the OLD folder with a timestamp
    if os.path.exists(dest_file):
        timestamp = time.strftime("%Y%m%d%H%M%S")
        old_file = os.path.join(OLD_DIR, f"resume_max_keirn_{timestamp}.pdf")
        #print(f"Moving existing file to OLD folder: {dest_file}")
        shutil.move(dest_file, old_file)

    # Rename and move the new file to the destination
    shutil.move(src_file, dest_file)
    subprocess.run(["xdg-open", dest_file])
    #print("File processed successfully.")
