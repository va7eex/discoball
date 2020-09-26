import os

from simple_zpl2 import NetworkPrinter
from simple_zpl2 import ZPLDocument
from simple_zpl2 import Code128_Barcode
from simple_zpl2 import QR_Barcode

class labelprinter:

    def __init__(self, ip):
        self._ip = ip

    def _wraptext_big(self,text):
        if len(text) > 20:
            text = text[:20] + '\n' + text[20:]
            print(text)
            return text
        return text

    def printlabel(self, bigtext, littletextleft='', littletextright='', barcodedata='', barcodetype='code128'):

        prn = NetworkPrinter(self._ip)
        zpl = ZPLDocument()

        zpl.add_field_origin(10, 10)
        zpl.add_font('C', zpl._ORIENTATION_NORMAL, 30)
#        zpl.add_field_data(self._wraptext_big(bigtext), True)
        zpl.add_field_block(460,3,text_justification='C')
        zpl.add_field_data(bigtext)

        zpl.add_field_origin(0, 120, justification='0')
        zpl.add_font('C', zpl._ORIENTATION_NORMAL, 15)
        zpl.add_field_data(littletextleft)

        zpl.add_field_origin(460, 120, justification='1')
        zpl.add_font('C', zpl._ORIENTATION_NORMAL, 15)
        zpl.add_field_data(littletextright)

        if(barcodedata != ''):
            zpl.add_field_origin(20, 150)
            if 'code128' in barcodetype:
                bc = Code128_Barcode(barcodedata, 'N', 30, 'Y')
                zpl.add_barcode(bc)
            elif 'qr' in barcodetype:
                bc = QR_Barcode(barcodedata, 'N', 30, 'Y')
                zpl.add_barcode(bc)


        prn.print_zpl(zpl)
        return True

if __name__ == "__main__":
    lp = labelprinter(os.getenv('PRINTER_IP'))
    lp.printlabel('THIS IS A TEST', 'left', 'right', barcodedata='12345')
