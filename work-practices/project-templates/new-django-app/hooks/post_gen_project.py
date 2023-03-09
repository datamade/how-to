import os
import shlex
import shutil
import subprocess

include_react = "{{ cookiecutter.include_react }}" == "True"
include_wagtail = "{{ cookiecutter.include_wagtail }}" == "True"

cwd = os.getcwd()
django_directory =  os.path.join(cwd, "django")
cmd = f"rsync -av {django_directory}/ {cwd}/"
subprocess.run(shlex.split(cmd), check=True)

if include_react:
    print("React included!")

    react_directory =  os.path.join(cwd, "react")
    cmd = f"rsync -av {react_directory}/ {cwd}/"
    subprocess.run(shlex.split(cmd), check=True)

if include_wagtail:
    print("Wagtail included!")

    wagtail_directory =  os.path.join(cwd, "wagtail")
    cmd = f"rsync -av {wagtail_directory}/ {cwd}/"
    subprocess.run(shlex.split(cmd), check=True)

# concatenate requirements, readmes, and django settings; remove unconcatenated versions

# Freeze Python and JavaScript dependencies

for directory in (django_directory, react_directory, wagtail_directory):
    shutil.rmtree(directory)
