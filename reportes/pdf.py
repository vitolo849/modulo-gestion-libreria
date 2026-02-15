from fpdf import FPDF
import os
import subprocess
import sys

TABLE_DATAejemplo = (
    ("First name", "Last name", "Age", "City"),
    ("Jules", "Smith", "34", "San Juan"),
    ("Mary", "Ramos", "45", "Orlando"),
    ("Carlson", "Banks", "19", "Los Angeles"),
    ("Lucas", "Cimon", "31", "Angers"),
)

def getPdfTable(TABLE_DATA):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    
    with pdf.table() as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum)
    
    nombre_archivo = 'table.pdf'
    pdf.output(nombre_archivo)
    
    if sys.platform == 'win32':
        os.startfile(nombre_archivo)
    elif sys.platform == 'darwin':
        subprocess.run(['open', nombre_archivo])
    else:
        subprocess.run(['xdg-open', nombre_archivo])
    
    print(f"PDF generado y abierto: {nombre_archivo}")

