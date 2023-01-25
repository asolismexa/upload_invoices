import os
import sys
from utils import (
    find_and_copy_all_xml,
    upload_invoices
)

root_dir = r"C:\Users\Desarrollo\Downloads\COMPLEMENTOS"
dest_dir = os.path.join(r'C:\Users\Desarrollo\Downloads\comp')


def main():
    try:
        if "-f" in sys.argv:
            find_and_copy_all_xml(root_dir, dest_dir)

        upload_invoices(dest_dir)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
