import os

from simple_zpl2 import NetworkPrinter
from simple_zpl2 import ZPLDocument
from simple_zpl2 import Code128_Barcode
from simple_zpl2 import QR_Barcode

def printlabel(bigtext, littletextleft='', littletextright='', barcodedata='', barcodetype='code128'):

    prn = NetworkPrinter(os.getenv('PRINTER_IP'))
    zpl = ZPLDocument()

    zpl.add_field_origin(10, 10)
    zpl.add_font('C', zpl._ORIENTATION_NORMAL, 30)
    zpl.add_field_data(bigtext)

    zpl.add_field_origin(0, 40, justification='0')
    zpl.add_font('C', zpl._ORIENTATION_NORMAL, 15)
    zpl.add_field_data(littletextleft)

    zpl.add_field_origin(400, 40, justification='1')
    zpl.add_font('C', zpl._ORIENTATION_NORMAL, 15)
    zpl.add_field_data(littletextright)

    if 'code128' in barcodetype:
        zpl.add_field_origin(20, 20)
        bc = Code128_Barcode(barcodedata, 'N', 30, 'Y')
        zpl.add_barcode(bc)
    elif 'qr' in barcodetype:
        zpl.add_field_origin(20, 20)
        bc = QR_Barcode(barcodedata, 'N', 30, 'Y')
        zpl.add_barcode(bc)


    prn.print_zpl(zpl)
    return True

if __name__ == "__main__":
    printlabel('THIS IS A TEST', 'left', 'right', barcodedata='12345')
