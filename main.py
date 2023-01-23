import os
import shutil

root_dir = r"C:\Users\Desarrollo\Documents\CFDi Manuales\COMPLEMENTOS"
dest_dir = "./comp"


def main():
    counter = 0
    for dirpath, dirnames, files in os.walk(root_dir):
        for file in files:
            if not file.endswith(".xml"):
                continue

            if not file.startswith("PAGO"):
                continue

            if "Copy" in file:
                continue

            if "tmp" in file:
                continue

            filename = os.path.join(dirpath, file)
            shutil.copy(filename, os.path.join(dest_dir, file))
            counter += 1

    print(f"Copied: {counter}")


if __name__ == '__main__':
    main()
