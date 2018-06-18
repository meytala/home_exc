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

extract("DM_TH.tgz", "C:/Users/meyta/PycharmProjects/viz_ai")


#################################################################################
###########arranges the files according to the DICOM hierarchy###################
#################################################################################

#Note that patient names were replaced with IDs to protect their privacy.

# patient   (patient name =ID)
# study
# series


#####################################################################
###############read the files########################################
#####################################################################

###got many errors trying to use:
#filename = get_testdata_files("rtplan.dcm")[0]           #is not defined
# filename = get_testdata_files("*.dcm")[0]           #is not defined
##the definition of get_testdata lead to data_manager

###the problem was that I received an empty list. because the path was wrong. the path lead to the path of where I downloaded pydicom
##filename = get_testdata_files("C:\\Users\\meyta\\PycharmProjects\\viz_ai\\*.dcm")[0]
####realized i need the orfer get_files from data_manager, passing the path and the *.dcm


filename = data_manager.get_files("C:\\Users\\meyta\\PycharmProjects\\viz_ai\\", "*.dcm")[3]  ##qa tried 0, 1, 2, 3: Study Instance UID and 1.2.840.113619.2.337.3.2831186181.442.1421722000.427 are equal, SOP Instance UID differ
print(filename)
ds = pydicom.dcmread(filename)
print(ds)
print(ds.dir())       #see the attributes of each ds file



############alternatively:

list_of_files= []
for i in range (0,406):
    filename = "dicom_{0:04}.dcm".format(i)
    ds = pydicom.dcmread(filename)
    list_of_files.append(ds)

# print("first file:", list_of_files[0])              #qa - worked!!

#############a glance to the file




#potential important fields:


# Patient's Name                    PN:  '1.2.840.113619.2.337.3.2831186181.442.1421722000.421'
# Patient's Sex                     CS:  'M' or 'F'
# Patient's Age                     AS:  '011Y'   (11?)
# Study Date                        DA: '20000101' (january 1, 2001?)

# potential variables to idetify study:
# Study Instance UID                UI: 1.2.840.113619.2.337.3.2831186181.442.1421722000.421     (this is the study IUD)
# Study ID                          SH: '2727'

# potential variables to idetify series:
# Series Instance UID               UI: 1.2.840.113619.2.337.3.2831186181.442.1421722000.427     (this is the series IUD)
# Series Number                     IS: '2'

# others:
# SOP Instance UID                  UI: 1.2.840.113619.2.337.3.2831186181.442.1421722000.429.4  (unique for each image)
# Referenced SOP Instance UID       UI: 1.2.840.113619.2.337.3.2831186181.442.1421722000.422    (??????)
# Referenced SOP Instance UID       UI: 1.2.840.113619.2.337.3.2831186181.442.1421722000.426.1  (??????)
# Irradiation Event UID             UI: 1.2.840.113619.2.337.3.2831186181.442.1421722000.428    (??????)
# Frame of Reference UID            UI: 1.2.840.113619.2.337.3.2831186181.442.1421722000.423.6570.1   (??????)

# other potential impotant:
# Study ID                          SH: '2727'
# Series Number                     IS: '2'
# Instance Number                   IS: '4'



####need to make sure what is the study unique id and what is the series unique id


#######################################################################
################create a class named ProcessDCM########################
#######################################################################


"""create a class with methods and define the files as objects.
potential methods in the class:
- Patient_id
- Study_id
- Scan_id 
- age 
- sex """





class ProcessDcm:
    def __init__(self, dcm_file):
        ds = pydicom.dcmread(dcm_file)
        self.dcm = dcm_file
        self.age = ds.PatientAge
        self.sex = ds.PatientSex
        self.patient_id = ds.PatientName
        self.study_id = ds.StudyInstanceUID
        self.series_id = ds.SeriesInstanceUID
        self.instance_id = ds.SOPInstanceUID
        self.hospital = ds.InstitutionName




###########Create a list of object based on ProcessDcm class:

list_of_dcm_objects = [ ]
for i in range (0,406):
    dcm_file_name = "dicom_{0:04}.dcm".format(i)
    list_of_dcm_objects.append(ProcessDcm(dcm_file_name))


# for object in list_of_dcm_objects:                #qa print all patients id - worked!
#     print("list of names based on objects method", object.patient_id)

# print("length of objects", len(list_of_dcm_objects))  ##qa - 406 files


#############create a list of names (IDs)

def list_of_names():
    name_list=[]
    for object in list_of_dcm_objects:
        name_list.append(object.patient_id)
    return name_list

# print("length of list of names", len(list_of_names()))  #qa - 406 names


#############create a list of unique names (IDs)

def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return(unique_list)

# print("number of unique ids", len(unique(list_of_names()))) ####6 unique IDs

unique_id_list = unique(list_of_names())
# print(unique_id_list)         #qa worked!



############################################################
########Create a folder for each unique patient_id##########
########move files of patient to the right folder##########
############################################################


script_dir = os.path.dirname(__file__)

current_directory = os.getcwd()
for object in list_of_dcm_objects:
    patient_directory = os.path.join(current_directory, '{}'.format(object.patient_id))
    study_directory =  os.path.join(patient_directory, '{}'.format(object.study_id))
    series_directory = os.path.join(study_directory, '{}'.format(object.series_id))
    if not os.path.exists(patient_directory):
        os.makedirs(patient_directory)
        os.makedirs(study_directory)
        os.makedirs(series_directory)

    elif not os.path.exists(study_directory):
        os.makedirs(study_directory)
        os.makedirs(series_directory)

    elif not os.path.exists(series_directory):
        os.makedirs(series_directory)

    os.rename("{}\\{}".format(current_directory,object.dcm) , "{}\\{}".format(series_directory,object.dcm))













# # 1) generate a list of patients, their age and sex --- created list of lists
###first chacked if a patient change age during sessions - no one did so I can run over the first study of each patient

demo_list = []
for i in list_of_dcm_objects:
    patient=i.patient_id
    age=i.age
    sex=i.sex
    demo_list.append([patient,age,sex])

first_file_list=[]
for i in demo_list:
    if i not in first_file_list:
        first_file_list.append(i)

print("q1- list of patient's ID, age and sex", first_file_list)


# # 2) how many different hospitals do the data come from?

list_of_hospitals= []
for i in list_of_dcm_objects:
    hospital=i.hospital
    list_of_hospitals.append(hospital)
unique_hospital = set(list_of_hospitals)

print("q2 - there are {} unique hospitals, named {}".format(len(unique_hospital),unique_hospital)) #there are 3 unique hospitals


############################################################################
############################################################################
#####################start from here#######################################
############################################################################
############################################################################
############################################################################


# ----------------------------------------------------------------------------------------------
#

# # write a python script that receives the URL as a command-line argument and:
# # - downloads the file
# # - arranges the files according to the DICOM hierarchy in an appropriate directory structure (patient/study/series). Note that patient names were replaced with IDs to protect their privacy.
# # - performs the following tasks or answers the following questions:
# # 1) generate a list of patients, their age and sex
# # 2) how many different hospitals do the data come from?
# # 3) explore the following DICOM tags, and try to explain what they mean, and the differences and relationships between them. Feel free to use appropriate visualizations as necessary.
# # - 0x0008,0x0013
# # - 0x0008,0x0032
# # - 0x0020,0x0012
# # - 0x0020,0x0013
# # 4) How long does a typical CT scan take?
#
#
#
#
#
#
#
#
#
#
#
#
#
#
