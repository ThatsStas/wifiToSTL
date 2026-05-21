## Notes

This code is WIP until the next time I need it. You have to change the SSID and PW vars inside the script 
and have [openSCAD](https://openscad.org/) installed. I don't quite remember but the direct subprocess 
command didn't work out of the box, so some tinkering is required. 

From my history, I got 
```
openscad  --export-format binstl -o wifi_qr_code_with_base.stl wifi_qr_code_with_base.scad
```

so that might help. 
