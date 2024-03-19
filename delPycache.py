import os
import shutil


def delete_pycache(directory):
    for root, dirs, files in os.walk(directory):
        for d in dirs:
            if d == "__pycache__":
                pycache_path = os.path.join(root, d)
                print("Deleting:", pycache_path)
                try:
                    shutil.rmtree(pycache_path)
                except OSError as e:
                    print("Error:", e)


if __name__ == "__main__":
    current_directory = os.getcwd()
    delete_pycache(current_directory)
