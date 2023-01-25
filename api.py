import requests
from datetime import datetime
import base64
import json

# XML ElementTree
import xml.etree.ElementTree as ET


def get_info_from_xml(file_dir):
    """
    Gets the information from the XML
    :param file_dir: file directory
    :return: tuple - data and if the data is valid
    """
    menfis_data = dict()
    complemento_data = dict()
    fact_data = list()
    file_data = dict()

    try:
        # Abrimos el XML
        tree = ET.parse(file_dir)
        root = tree.getroot()

        # Registramos los datos del XML en un dict
        complemento_data['Serie'] = root.attrib['Serie']
        complemento_data['Folio'] = root.attrib['Folio']
        complemento_data['Time'] = str(datetime.strptime(root.attrib['Fecha'], '%Y-%m-%dT%H:%M:%S'))
        complemento_data['Identifier'] = root[3][1].attrib['UUID']
        complemento_data['Issued_View_Template_Id'] = 11
        complemento_data['Invoice'] = complemento_data['Serie'] + complemento_data['Folio']
        complemento_data['Warnings'] = 0
        complemento_data['Errors'] = 0
        complemento_data['Is_Invalid'] = 0
        complemento_data['Issued_Status_Id'] = 1
        complemento_data['Exchange_Rate'] = -1
        complemento_data['Subtotal'] = 0
        complemento_data['Discount'] = 0
        complemento_data['Ret_IVA'] = 0
        complemento_data['Ret_ISR'] = 0
        complemento_data['Tras_IVA'] = 0
        complemento_data['Tras_IEPS'] = 0
        complemento_data['Total'] = 0
        complemento_data['Invoice_XML'] = ''
        complemento_data['PDF_URI'] = ''
        complemento_data['PDF_Is_Fake'] = 0
        complemento_data['Attachs'] = 0
        complemento_data['Last_Modified_On'] = str(datetime.now(tz=None))
        complemento_data['InHouse'] = 0
        complemento_data['Has_Observations'] = 0
        complemento_data['PAC_Id'] = 4
        complemento_data['Object_Id'] = 0
        complemento_data['PaymentMethod_Id'] = 3
        complemento_data['Payment_Status_Id'] = 3
        complemento_data['Payment_Balance'] = 0
        complemento_data['Payment_Number'] = 0
        complemento_data['Issuer_Zip_Code'] = root.attrib['LugarExpedicion']
        complemento_data['Client_Issued_Name'] = root[1].attrib['Nombre']
        complemento_data['Moneda'] = root.attrib['Moneda']
        complemento_data['TipoComprobante'] = root.attrib['TipoDeComprobante']
        complemento_data['Version'] = root.attrib['Version']
        complemento_data['rfc_emisor'] = root[0].attrib['Rfc']
        complemento_data['rfc_receptor'] = root[1].attrib['Rfc']
        complemento_data['MonedaP'] = root[3][0][0].attrib['MonedaP']
        complemento_data['FormaDePagoP'] = root[3][0][0].attrib['FormaDePagoP']
        complemento_data['Monto'] = root[3][0][0].attrib['Monto']
        try:
            complemento_data['TipoCambioP'] = root[3][0][0].attrib['TipoCambioP']

        except:
            complemento_data['TipoCambioP'] = 1.0

        complemento_data['FechaPago'] = str(datetime.strptime(root[3][0][0].attrib['FechaPago'], '%Y-%m-%dT%H:%M:%S'))
        complemento_data['FechaTimbrado'] = str(
            datetime.strptime(root[3][1].attrib['FechaTimbrado'], '%Y-%m-%dT%H:%M:%S'))
        complemento_data['file_name'] = complemento_data['rfc_emisor'] + '_' + complemento_data['Invoice'] + '.xml'

        # Obtenemos los datos de las facturas
        aux = 0
        for data in root[3][0][0]:
            fact_dict = dict()
            fact_dict['IdDocumento'] = root[3][0][0][aux].attrib['IdDocumento']
            fact_dict['NumParcialidad'] = root[3][0][0][aux].attrib['NumParcialidad']
            fact_dict['ImpSaldoAnt'] = root[3][0][0][aux].attrib['ImpSaldoAnt']
            fact_dict['ImpPagado'] = root[3][0][0][aux].attrib['ImpPagado']
            fact_dict['ImpSaldoInsoluto'] = root[3][0][0][aux].attrib['ImpSaldoInsoluto']
            fact_dict['MonedaDr'] = root[3][0][0][aux].attrib['MonedaDR']
            fact_data.append(fact_dict)
            aux += 1

        with open(file_dir, 'rb') as xmlfile:
            xml_encoded = base64.encodebytes(xmlfile.read()).decode('utf-8')

        file_data['xml_encoded'] = xml_encoded

        menfis_data['complemento_data'] = complemento_data
        menfis_data['facts_data'] = fact_data
        menfis_data['file_data'] = file_data

        validate = True

    except Exception as ex:
        validate = False

    return menfis_data, validate


def send_complemento_to_menfis(menfis_data):
    """
    Sends complement data to menfis
    :param menfis_data: data from the file
    :return: response from menfis
    """

    dict_response = dict()
    dict_response['validate'] = bool

    try:
        url = 'http://buzon.mensajeriafiscal.com/test.invoices/api/v3.3/external/payment/nofolio'

        headers = {
            'Accept': 'application/json',
            'Authorization': 'Basic YWRtaW46bTN4NDIwMjA=',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, data=json.dumps(menfis_data), headers=headers)

        if response.status_code == 200:
            menfis_response = response.json()

            dict_response['Invoice_Id'] = menfis_response['Id']
            dict_response['Date'] = menfis_response['Fecha']
            dict_response['Folio'] = menfis_response['Folio']

            dict_response['validate'] = True

        else:
            dict_response['validate'] = False
            dict_response[
                'error_message'] = f'Error al cargar informacion en servicio. Status: {response.status_code}, {response.content}'

    except:
        dict_response['validate'] = False
        dict_response['error_message'] = 'EXCEPT: Error al consumir servicio de cargar de complementos '

    return dict_response
