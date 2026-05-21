import qrcode
import numpy as np
from solid import *
from solid.utils import *
import subprocess
from PIL import Image

ssid = ""
password = ""

encryption = "WPA"  # Use "WEP", "WPA", or leave empty for no encryption

# Generate Wi-Fi QR Code
wifi_string = f"WIFI:S:{ssid};T:{encryption};P:{password};;"
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(wifi_string)
qr.make(fit=True)
img = qr.make_image(fill="black", back_color="white")

# Save QR Code image
img.save("wifi_qr_code.png")

# Convert QR code image to numpy array
img = img.convert("L")
qr_array = np.array(img)
size_x, size_y = qr_array.shape

# Parameters for 3D model
pixel_size = .1  # size of one pixel in the QR code in mm
base_thickness = 3  # thickness of the base in mm
qr_height = 1      # height of the raised QR code in mm
margin = 3  # margin around the QR code on the base

# Overall plate size
plate_length = (pixel_size * size_x) + 2 * margin
plate_width = (pixel_size * size_y) + 2 * margin

def generate_qr_stl(qr_array, pixel_size, base_thickness, qr_height, margin):
    # Create the base plate with margins
    base = cube([plate_length, plate_width, base_thickness])

    qr_code_3d = []
    for i in range(size_x):
        for j in range(size_y):
            if qr_array[i, j] == 0:  # black pixel
                qr_code_3d.append(
                    translate(
                        [margin + i * pixel_size, margin + j * pixel_size, base_thickness]
                    )(
                        cube([pixel_size, pixel_size, qr_height])
                    )
                )

    # Combine the base and the raised QR code pixels
    return base + union()(*qr_code_3d)

# Generate the OpenSCAD model
qr_3d_model = generate_qr_stl(qr_array, pixel_size, base_thickness, qr_height, margin)

# Save the .scad file
scad_file = 'wifi_qr_code_with_base.scad'
stl_file = 'wifi_qr_code_with_base.stl'
print(f"Rendering to file: {scad_file}")
scad_render_to_file(qr_3d_model, scad_file)

# Automatically call OpenSCAD to generate the STL file
#print(f"Exporting to stl: {stl_file}")

# subprocess.run(['openscad', '-o', stl_file, scad_file])

#print(f"STL file generated: {stl_file}")
