from PIL import Image
import requests
import subprocess, sys

opener = "open" if sys.platform == "darwin" else "xdg-open"

full_json = requests.get("http://128.138.165.181:5000/fieldview/getAllJson").content

print full_json.__str__()
#os.startfile(img_url)

#img.show()

