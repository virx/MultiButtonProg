#!/usr/bin/python

import os
import py_compile
import subprocess

# make folders in build directory
folder_list = ['build','build/config','build/source','build/source/config']
build_file_copy_list = ['config.txt','README']
build_source_file_copy_list = ['build.py','mbp.py']
for folder in folder_list:
	# try to make log dir
	try:
		os.makedirs(folder)
	except OSError:
		pass
			
# compile
py_compile.compile("mbp.py","build/mbp.pyc")

# make it executable
subprocess.Popen("chmod +x build/mbp.pyc", shell=True)

# copy files to build and source directories
for fn in build_file_copy_list:
	subprocess.Popen("cp -r %r build" % fn, shell=True)
	subprocess.Popen("cp -r %r build/source/" % fn, shell=True)

# copy files only to source directory
for fn in build_source_file_copy_list:
	subprocess.Popen("cp -r %r build/source/" % fn, shell=True)
	
# copy files to config folder
subprocess.Popen("cp -r config/*.* build/source/config", shell=True)

# make file to execute script with mouse click
mbp_sh_msg = """#!/bin/bash
./mbp.pyc"""
with open('build/mbp', 'w') as f:
	f.write(mbp_sh_msg)
f.close()
subprocess.Popen("chmod +x build/mbp", shell=True)

print 'mbp.py build OK'
