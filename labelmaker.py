
import os
import logging

from simple_zpl2 import NetworkPrinter
from simple_zpl2 import ZPLDocument
from simple_zpl2 import Code128_Barcode
from simple_zpl2 import QR_Barcode

class labelprinter:

    DPI203 = 8 #dots per mm
    DPI300 = 12 #dots per mm

    def __init__(self, ip, width=2.625, height=1, imperialunits=True, dpi=DPI203, font='C', bigtextsize=30):
        self._ip = ip
        self._dpi = dpi
        self._barcodeheight = int(self._dpi * 2)
        self._bigtextsize = int(max(bigtextsize,self._dpi*2))
        self._smalltextsize = int(max(bigtextsize/2,self._dpi))
        self._font = font
        if imperialunits:
            self._width = int(width * 25.4 * self._dpi)
            self._height = int(height * 25.4 * self._dpi)
        else:
            self._width = int(width * self._dpi)
            self._height = int(height * self._dpi)

    def printlabel(self, bigtext: str, littletextleft: str = '', littletextright: str = '', barcodedata: str = '', barcodetype: str = 'code128', quantity: int = 1, preview: bool = False):

        prn = NetworkPrinter(self._ip)
        zpl = ZPLDocument()
        zpl.add_print_quantity(quantity)

        #if we have our newline character already ignore some 'smart' formatting
        if '$CR' not in bigtext:
            # center the big text a bit
            if littletextright == '' and littletextleft == '':
                bigtext = '$CR$CR' + bigtext
            elif len(bigtext) <= 40 and len(bigtext) > 20:
                bigtext = '$CR' + bigtext
            elif len(bigtext) <= 20:
                bigtext = '$CR$CR' + bigtext

        # y coords for some things
        bigtextYoffset = int(self._dpi*1.5)
        bigtextXoffset = int(self._dpi*1)
        barcodeYoffset = int(self._dpi*3+self._barcodeheight)
        smalltextYoffset = int(barcodeYoffset+self._dpi+self._smalltextsize)

        zpl.add_field_origin(bigtextXoffset, bigtextYoffset)
        zpl.add_font(self._font, zpl._ORIENTATION_NORMAL, self._bigtextsize)
#        zpl.add_field_data(self._wraptext_big(bigtext), True)
        if len(littletextleft) > 0 or len(littletextright) > 0 or len(barcodedata) > 0:
            zpl.add_field_block(self._width-int(2*bigtextXoffset),3,text_justification='C')
        else:
            #if no lower text, allow expanded big text data
            zpl.add_field_block(self._width-int(2*bigtextXoffset),5,text_justification='C')
        zpl.add_field_data(bigtext.strip().replace('$CR','\n'), replace_newlines=True)

        zpl.add_field_origin(self._dpi, self._height-smalltextYoffset, justification='0')
        zpl.add_font(self._font, zpl._ORIENTATION_NORMAL, self._smalltextsize)
        zpl.add_field_data(littletextleft.strip())

        zpl.add_field_origin(self._width-self._dpi, self._height-smalltextYoffset, justification='1')
        zpl.add_font(self._font, zpl._ORIENTATION_NORMAL, self._smalltextsize)
        zpl.add_field_data(littletextright.strip())

        if(len(barcodedata) > 0):
            zpl.add_field_origin(self._dpi, self._height-barcodeYoffset)
            if 'code128' in barcodetype:
                bc = Code128_Barcode(barcodedata.strip(), 'N', self._barcodeheight, 'Y')
                zpl.add_barcode(bc)
            elif 'qr' in barcodetype:
                bc = QR_Barcode(barcodedata, 'N', self._barcodeheight, 'Y')
                zpl.add_barcode(bc)

        if preview:
            renderpng = zpl.render_png((self._width/self._dpi/25.4),(self._height/self._dpi/25.4),self._dpi)
            logging.warn(type(renderpng), renderpng)
            return renderpng
        else:
            prn.print_zpl(zpl)

        return True

if __name__ == "__main__":
    lp = labelprinter(os.getenv('PRINTER_IP'))
    lp.printlabel('THIS IS A TEST', '|< left', 'right >|', barcodedata='12345')
