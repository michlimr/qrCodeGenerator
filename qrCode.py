import segno
import PySimpleGUI as sg
import os
from pathlib import Path

sg.theme('Tan Blue')

# Prompts user for qr code contents
text = sg.popup_get_text('Enter the text or link you would like to convert into a QR code', "QR Code Input")

if not text:
    sg.popup("No text entered. Exiting.")
    exit()

# generate qr code
filename = "qrcode.png"
code = segno.make_qr(text)
code.save(filename, scale=15)

# Layout for the window
layout = [
    [sg.Image(filename, expand_x=True, expand_y=True, enable_events=True, key='-IMAGE-')],
    [sg.Button('Download'), sg.Button('Exit')]
]

window = sg.Window('QR Code', layout)

while True:
    event, values = window.read()

    if event in (None, 'Exit'):
        break

    elif event == 'Download':
        save_path = sg.popup_get_file(
            'Save QR Code As (include .png in the name)',
            'Saving file', 
            save_as=True,
            default_extension='.png', 
            file_types=(("PNG Files", "*.png"),)
        )
        if save_path:
            try:
                os.rename(filename, save_path)
                sg.popup(f"QR Code saved to {save_path}")
            except Exception as e:
                sg.popup(f"Error saving file: {e}")

# Close the window
window.close()

# Cleanup the temporary QR code image
if os.path.exists(filename):
    os.remove(filename)