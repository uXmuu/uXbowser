import json
import os
import sys
o = os.getcwd()
o = o.replace("packages","")

with open(o+"/config.json","r") as f:
	f = json.load(f)


f["app_style"] = "background-color: red; color: yellow"
f["navbar_style"] = "background-color: red; color: yellow"
f["body_background-color"] = "red"
f["body_color"] = "yellow"


with open(o+"/config.json","w") as a:
	json.dump(f, a)
