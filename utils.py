import os
import shutil
from api import (
    get_info_from_xml,
    send_complemento_to_menfis
)
from errors import save_errors_file


def find_and_copy_all_xml(root_dir: str, output_dir: str):
    """
    Find all xml files in root_dir and copy them to dest_dir
    :param root_dir: str - root directory to search for xml files
    :param output_dir: str - destination directory
    :return: list - list of xml files found
    """

    xml_list = []
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
            xml_list.append(filename)
            shutil.copy(filename, os.path.join(output_dir, file))

    return xml_list


def upload_invoices(root_dir: str) -> None:
    """
    Uploads all the invoices in root_dir to menfis
    :param root_dir: directory where the invoices are located
    """

    errors = []
    files = os.listdir(root_dir)
    for file in files:
        try:
            invoice_path = os.path.join(root_dir, file)
            menfis_data, validate = get_info_from_xml(invoice_path)
            if validate:
                response = send_complemento_to_menfis(menfis_data)
                if not response['validate']:
                    errors.append({
                        "file": file,
                        "error": response['error_message']
                    })
                    continue
                print(response)
        except Exception as ex:
            print(ex)
            errors.append({
                "file": file,
                "error": ex
            })
            continue

    print("Total errors: ", len(errors))
    print(errors)
    save_errors_file(errors)
