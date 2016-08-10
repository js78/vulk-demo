#!/usr/bin/env python3.5
import importlib.util
import os
import shutil
import subprocess
import tarfile
import urllib.request

# Parameters
app_module = "vulkdemo"
app_name = "Vulk Demo"
out_folder_name = "www"
brython_name = "brython3.2.7"
brython_url_name = "3.2.7/Brython3.2.7-20160621-184325.tar.gz"
brython_base_url = "https://github.com/brython-dev/brython/releases/download/"
brython_url = brython_base_url + brython_url_name

# Output of build
base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        out_folder_name)
lib_path = os.path.join(base_dir, brython_name, "Lib", "site-packages")

# Clean and prepare directory
try:
    os.makedirs(base_dir)
except FileExistsError:
    pass

# Check if brython is last version
if not brython_name in os.listdir(base_dir):
    # Download brython to temp file
    gz_path, _ = urllib.request.urlretrieve(brython_url)
    with tarfile.open(gz_path, 'r:gz') as gz:
        extracted_name = os.path.dirname(gz.getmembers()[0].name)
        extracted_folder = os.path.dirname(gz_path)
        gz.extractall(extracted_folder)
        os.rename(os.path.join(extracted_folder, extracted_name),
                  os.path.join(base_dir, brython_name))


# Copy vulk
vulk_module = "vulk"
vulk_path = os.path.dirname(importlib.util.find_spec(vulk_module).origin)
try:
    shutil.copytree(vulk_path, os.path.join(lib_path, vulk_module))
except FileExistsError:
    pass

# Copy application
app_path = os.path.dirname(importlib.util.find_spec(app_module).origin)
try:
    shutil.rmtree(os.path.join(base_dir, app_module))
except FileNotFoundError:
    pass
shutil.copytree(app_path, os.path.join(base_dir, app_module))

# Create index.html
html_template = '''
<!doctype html>
<html>
    <head>
        <meta charset="UTF-8">
        <script type="text/javascript" src="''' + brython_name + '''/brython.js"></script>
    </head>

    <body onload="brython()">
        <canvas id="app_canvas" width="640" height="480">
            No HTML5 support
        </canvas>

        <script type="text/python">
            from vulk.container.webcontainer import WebContainer
            from ''' + app_module + ''' import App

            container = WebContainer(App)
            container.run()
        </script>
    </body>
</html>
'''

with open(os.path.join(base_dir, "index.html"), "w") as html_file:
    html_file.write(html_template)

# Clean build folder
subprocess.run(["py3clean", base_dir])
