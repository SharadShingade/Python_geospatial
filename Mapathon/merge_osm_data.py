#!/bin/python
# -*- coding: UTF-8 -*-
# Author: B. Herfort, 2016, GIScience Heidelberg
###########################################

import sys
import os
import time

def get_all_files(directory,extension):

	#create list for all selected files
	selected_files = []
	
	#iterate over all items in directory and check file extension
	for item in os.listdir(directory):
		#change directory
		#os.chdir(directory)
		#get file extension of current item
		#item_ext = item.split(".")[-1]

		
        #check whether item is a file and has right file extension
		selected_files.append(item)
			#selected_files.append(item)
        

	return selected_files


def main(directory,output_file,extension):
	
	#Take start time
	start_time = time.time()
	
	selected_files = get_all_files(directory,extension)
	cmd_middle = ''
	cmd_suffix = ''
	
	for i in range(0,len(selected_files)):
    
	
		#copy first file
		if i == 0:	
			filename = directory + '\\' + selected_files[i]
			
			cwd = os.getcwd()
			osmosis = r'D:\Github\Python_geospatial\Mapathon\osmosislatest\x08in\\osmosis.bat'
			cmd_1 = r"%s +  --read-xml file=%s --sort --write-xml file="'%s'""  % (osmosis,filename,output_file)
			os.system("%s +  --read-xml file=%s --sort --write-xml file="'%s'""  % (osmosis,filename,output_file))
    
			
		else:
			filename = directory + '\\' + selected_files[i]
			cmd_middle = cmd_middle + '--read-xml file="'+filename+'" --sort '
			cmd_suffix = cmd_suffix + '--merge '
			
			if (i%50 == 0 ) or (i == (len(selected_files)-1)):
				print i
				osmosis = r'D:\Github\Python_geospatial\Mapathon\osmosislatest\x08in\\osmosis.bat' #os.path.dirname(cwd) + '\\osmosis-latest\\bin\\osmosis.bat'
				cmd_prefix = osmosis +' --read-xml file="'+output_file+'" --sort '
				cmd = cmd_prefix + cmd_middle + cmd_suffix + ' --write-xml file="'+output_file+'" -q'
				os.system("%s +  --read-xml file=%s --sort --write-xml file="'%s'"-q"  % (osmosis,filename,output_file))
				cmd = ''
				cmd_middle = ''
				cmd_suffix = ''
		
	#Take end time and calculate program run time
	end_time = time.time()
	run_time = end_time - start_time
	
	print '############ END ######################################'
	print '##'
	print '## output file: '+output_file
	print '##'
	print '## runtime: '+str(run_time)+' s'
	print '##'
	print '## B. Herfort, GIScience Research Group'
	print '##'
	print '#######################################################'
	
if __name__ == "__main__":

    #
    # example run : $ python merge_osm_data.py D:/temp/osm_data merge.osm osm
    #
    directory = r"D:\Github\Python_geospatial\Mapathon\Output"
    output_file='merge.osm'
    extension='osm'
    main( directory, output_file, extension)	
