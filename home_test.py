import os
import pydicom
from pydicom.data import data_manager
import urllib.request
import urllib
import shutil
import sys
import tarfile




# write a python script that receives the URL as a command-line argument and:
# - downloads the file

####################################################################
#######a function that read the argument from the command line######
#######and download the files to a folder###########################
####################################################################

# https://stackoverflow.com/questions/4033723/how-do-i-access-command-line-arguments-in-python
# https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3/7244263
# https://stackoverflow.com/questions/32832822/download-a-file-to-a-specific-folder-with-python


# def get_url(url, filename, myPath):
#     with urllib.request.urlopen(url) as response, open("DM_TH.tgz", 'wb') as out_file:   ######in thew future, split the file and take the end
#          shutil.copyfileobj(response, out_file)
#          data = response.read() # a `bytes` object
#          out_file.write(data)
#
# print(sys.argv[-1])
# url=sys.argv[-1]
# get_url(url, "DICOM", "C:/Users/meyta/PycharmProjects/viz_ai")

#the command in cmd:  C:\Users\meyta\PycharmProjects\viz_ai>python home_test.py https://s3.amazonaws.com/viz_data/DM_TH.tgz
# now, I have to unzip the tar file



####################################################################
#######a function that extract the tgz folder#######################
####################################################################

##https://stackoverflow.com/questions/6058786/i-want-to-extract-a-tgz-file-and-extract-any-subdirectories-that-have-files-tha

def extract(tar_file, my_path):
    tar = tarfile.open(tar_file, 'r')
    for item in tar:
        tar.extract(item, my_path)
        if item.name.find(".tgz") != -1:
            extract(item.name, "./" + item.name[:item.name.rfind('/')])

# extract("DM_TH.tgz", "C:/Users/meyta/PycharmProjects/viz_ai")





#################################################################################
###########arranges the files according to the DICOM hierarchy###################
#################################################################################

# - arranges the files according to the DICOM hierarchy in an appropriate directory structure (patient/study/series). Note that patient names were replaced with IDs to protect their privacy.

# patient   (patient name =ID)
#
# study
#
# series


#####################################################################
###############trying to read the files##############################
#####################################################################

###got many errors trying to use:
#filename = get_testdata_files("rtplan.dcm")[0]           #is not defined
# filename = get_testdata_files("*.dcm")[0]           #is not defined
##the definition of get_testdata lead to data_manager

###the problem was that I received an empty list. because the path was wrong. the path lead to the path of where I downloaded pydicom
##filename = get_testdata_files("C:\\Users\\meyta\\PycharmProjects\\viz_ai\\*.dcm")[0]
####realized i need the orfer get_files from data_manager, passing the path and the *.dcm


# filename = data_manager.get_files("C:\\Users\\meyta\\PycharmProjects\\viz_ai\\", "*.dcm")[0]
# print(filename)




############alternatively:

###as a first step, will create a list of patients' names

list_of_names = []
for i in range (0,406):
    filename = "dicom_{0:04}.dcm".format(i)
    ds = pydicom.dcmread(filename)
    #print("patient name (ID) is", ds.PatientName)
    list_of_names.append(ds.PatientName)

print(list_of_names)
#print(len(list_of_names))   ######qa, 406


###now, I have to create a list with unique names

def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return(unique_list)

print(len(unique(list_of_names))) ####6 unique IDs

unique_list1 = unique(list_of_names)


####need to create a file for each unique name

script_dir = os.path.dirname(__file__)

for i in unique_list1:
    # file_dir = "{}{}".format(script_dir,i)
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, '{}'.format(i))
    print(final_directory)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)






#######################################################################
#######################################################################
#######################################################################
######################start from here##################################
#######################################################################
#######################################################################
#######################################################################



####find the patients names in the dcm files, and place it in the relevant file






#####documentation of pydicom - https://pydicom.github.io/pydicom/stable/getting_started.html


# filename = get_testdata_files("rtplan.dcm")[0]
# ds = pydicom.dcmread(filename)  # plan dataset
# ds.PatientName
# # 'Last^First^mid^pre'
#
# ds.dir("setup")    # get a list of tags with "setup" somewhere in the name
# # ['PatientSetupSequence']
#
# ds.PatientSetupSequence[0]
# # (0018, 5100) Patient Position                    CS: 'HFS'
# # (300a, 0182) Patient Setup Number                IS: '1'
# # (300a, 01b2) Setup Technique Description         ST: ''
#
#
# ds.PatientSetupSequence[0].PatientPosition = "HFP"
# ds.save_as("rtplan2.dcm")



# write a python script that receives the URL as a command-line argument and:
# - downloads the file
# - arranges the files according to the DICOM hierarchy in an appropriate directory structure (patient/study/series). Note that patient names were replaced with IDs to protect their privacy.
# - performs the following tasks or answers the following questions:
# 1) generate a list of patients, their age and sex
# 2) how many different hospitals do the data come from?
# 3) explore the following DICOM tags, and try to explain what they mean, and the differences and relationships between them. Feel free to use appropriate visualizations as necessary.
# - 0x0008,0x0013
# - 0x0008,0x0032
# - 0x0020,0x0012
# - 0x0020,0x0013
# 4) How long does a typical CT scan take?
