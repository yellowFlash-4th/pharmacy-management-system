import barcode
from barcode.writer import ImageWriter

def generate_barcode(code, filename):
    barcode_class = barcode.get_barcode_class('code128')
    my_barcode = barcode_class(code, writer=ImageWriter())
    my_barcode.save(filename)