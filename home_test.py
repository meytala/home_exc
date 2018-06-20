import os
import pydicom
from pydicom.data import data_manager
import urllib.request
import urllib
import shutil
import sys
import tarfile
import pandas as pd
import seenopsis
import matplotlib.pyplot as plt
import json


# write a python script that receives the URL as a command-line argument and:
# - downloads the file

####################################################################
#######a function that read the argument from the command line######
#######and download the files to a folder###########################
####################################################################

def get_url(url, filename, myPath):
    with urllib.request.urlopen(url) as response, open("DM_TH.tgz", 'wb') as out_file:
         shutil.copyfileobj(response, out_file)
         data = response.read() # a `bytes` object
         out_file.write(data)

# # print(sys.argv[-1])  ##qa
url=sys.argv[-1]
get_url(url, "DICOM", "C:/Users/meyta/PycharmProjects/viz_ai")  ### !!!!! this works on my computer. need to modify path to match the user computer

#the command in cmd:  C:\Users\meyta\PycharmProjects\viz_ai>python home_test.py https://s3.amazonaws.com/viz_data/DM_TH.tgz

####################################################################
#######a function that extract the tgz folder#######################
####################################################################

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

######got many errors trying to use:
#filename = get_testdata_files("rtplan.dcm")[0]           #is not defined
# filename = get_testdata_files("*.dcm")[0]           #is not defined

#the problem was that I received an empty list., ecause the path was wrong (lead to the path of where I downloaded pydicom
#in the computer I was working on, the path is "C:\\Users\\meyta\\PycharmProjects\\viz_ai\\*.dcm")

##need to modify the follow to work in a nother computer, based on file location:
# filename = data_manager.get_files("C:\\Users\\meyta\\PycharmProjects\\viz_ai\\", "*.dcm")[3]  ##qa tried 0, 1, 2, 3: Study Instance UID and 1.2.840.113619.2.337.3.2831186181.442.1421722000.427 are equal, SOP Instance UID differ
# print(filename)           ##qa
# ds = pydicom.dcmread(filename)   ####reading the file
# print(ds)
# print(ds.dir())          #see the attributes of each ds file
# print(ds.keys())       #see all available keys


############alternatively, this will work in any computer for the spesific set:

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



##running through the samples, I nade sure what is the study unique id and what is the series unique id



#######################################################################
################create a class named ProcessDCM########################
#######################################################################

"""create a class with methods and define the files as objects"""

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
        self.acquisition_time = ds.AcquisitionTime
        self.acquisition_number = ds.AcquisitionNumber
        self.instance_number = ds.InstanceNumber
        self.content_time = ds.ContentTime
        try:
            self.creation_time = ds.InstanceCreationTime  ####somthing is wrong in here - some of the object do not have this attribute
        except AttributeError as error:
            self.creation_time = None   ##### if this attribute was missing, I replaced it with none


###########Create a list of object based in the ProcessDcm class:

list_of_dcm_objects = [ ]
for i in range (0,406):
    dcm_file_name = "dicom_{0:04}.dcm".format(i)   ####this will work in any computer, but only for this spesific set
    list_of_dcm_objects.append(ProcessDcm(dcm_file_name))


# for object in list_of_dcm_objects:               ##qa print all patients id - worked!
#     print("list of names based on objects method", object.patient_id)

print("This dataset has {} dcm files".format (len(list_of_dcm_objects)))  ##qa - 406 files - perfect!


#############create a list of patients' names (IDs) based on the objects in the class ProcessDcm

def list_of_names():
    name_list=[]
    for object in list_of_dcm_objects:
        name_list.append(object.patient_id)
    return name_list

# print("length of list of names", len(list_of_names()))  ##qa - 406 names - worked


#############create a list of unique names (IDs) - to see how many unique patients are available in this set

def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return(unique_list)

print("The dataset contain {} unique ids".format (len(unique(list_of_names())))) ####6 unique IDs

unique_id_list = unique(list_of_names())
# print(unique_id_list)         #qa worked!



############################################################
########Create a folder for each unique patient_id #########
########Create a subfolder for each unique study ###########
########Create a subfolder for each unique series ##########
########move files of patient to the right folder ##########
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




############################################################################
##########################  Q1 #############################################
############################################################################

# # 1) generate a list of patients, their age and sex --- created list of lists
###first chacked if a patient change age during sessions - no one did so I can run over the first study of each patient

demographic_list = []
for i in list_of_dcm_objects:
    patient=i.patient_id
    age=i.age
    sex=i.sex
    demographic_list.append([patient,age,sex])

first_file_list=[]
for i in demographic_list:
    if i not in first_file_list:
        first_file_list.append(i)

print("Q1 - the follwing is list of (lists of) patient's ID, age and sex", first_file_list) ###list of lists


############################################################################
##########################  Q2 #############################################
############################################################################

# # 2) how many different hospitals do the data come from?

list_of_hospitals= []
for i in list_of_dcm_objects:
    hospital=i.hospital
    list_of_hospitals.append(hospital)
unique_hospital = set(list_of_hospitals)

print("Q2 - there are {} unique hospitals, named {}".format(len(unique_hospital),unique_hospital)) #there are 3 unique hospitals


############################################################################
##########################  Q3 #############################################
############################################################################

#3) explore the following DICOM tags, and try to explain what they mean, and the differences and relationships between them.
# Feel free to use appropriate visualizations as necessary.

# # - 0x0008,0x0013 - Instance​Creation​Time
# # - 0x0008,0x0032 - Acquisition​Time
# # - 0x0020,0x0012 - Acquisition​Number
# # - 0x0020,0x0013 - Instance​Number


####to answer this question, I created a sub_dataset with the relevant variables

sub_dataset=[]
for object in list_of_dcm_objects:
    sub_dataset.append([object.dcm, object.creation_time, object.acquisition_time, object.acquisition_number, object.instance_number])

sub_dataset = pd.DataFrame(sub_dataset)   ###sub_dataset is a pandas file
sub_dataset.columns = ["object name", "Instance​Creation​Time", "Acquisition​Time", "Acquisition​Number", "Instance​Number"]

## as a first step, I explored the variables, using my program named seenopsis.
## the programm for seenopsis is in the github. I modified it to fit this spesific dataset
# seenopsis.process_pandas_df(sub_dataset)
## seenopss output is also in the git, if the seenopsis doesn't run

print("Q3 - what the DICOM tags mean?\n"
      "reading the lit, this is the doccumentation:\n"
      "0x0008,0x0013 - Instance​Creation​Time - value represenation:TM - A string of characters of the format hhmmss - Time the Protocol SOP Instance was created\n" 
      "0x0008,0x0032 - Acquisition​Time -  value represenation:TM - A string of characters of the format hhmmss.ffffff (fractional seconds) - The time that the acquisition of data that resulted in this instance started.\n" 
      "0x0020,0x0012 - Acquisition​Number -the official doccumentation: A number identifying the single continuous gathering of data over a period of time that resulted in this instance - this is vague\n"
      # "you can read about the differences between instance number and Acquisition​Number in here: https://clearcanvas.ca/Home/Community/OldForums/tabid/526/aff/8/aft/1378/afv/topic/Default.aspx\n"
      "0x0020,0x0013 - Instance​Number - A number that identifies a spesific image\n"
      "It is important to notice that in this spesific dataset: the attribute Instance​Creation​Time is missing in 70 dcm files (17.2% of files)")

# I looked in the spesific dataset, to see what does it contain in practice:

#print(sub_dataset)

#sub_dataset.corr()[1:3]
print("In practice, I would aregue that the Acquisition​Time is when the data was started to gather while Instance​Creation​Time is the time the data was started to being written (created)")
print("Statisticlly, they do not correlation (pearson correlation of: 0.424306)")

print("The Instance​Number is a serial based on number of images taking in a series \n"
      "The Acquisition​Number sub devide the Instance​Number to smaler groups, not sure based on what\n"
      "maybe it just devide the writing on the file based on groups of every 3/4 images")

###IT MIGHT BE NICE TO LOOK ON THE DISTRIBUTION OF THE DIFFERENCES BETWEEN THE VALUES. - did not do that



# # 4) How long does a typical CT scan take?

###potential indicator for length of CT scan
#Exposure Time??
#Exposure
#revolution time??
#[Mid Scan Time [sec]]
#[Duration of X-ray on]

## I could not find an attribute that indicate the end time in the DICOM files
## my strategy: calculate the dif between time of first imag to time of last image within each patient's study

print("Q4 -  length of CT scans - I do not have answer from the dataset, but I do have strategy how to gather the answer\n"
      "To understand how long does a CT scan take, I would calculate the time difference between the start time of the first and last imaging in each series\n"
      "then, I would average the lengths upon patients")

###this did not worked:
# min_time = {}
# for object in list_of_dcm_objects:
#     if object.patient_id in min_time:
#         if object.study_id in min_time[object.patient_id]:
#             if object.series_id in min_time[object.patient_id][object.study_id]:
#                 if object.acquisition_time < min_time[object.patient_id][object.study_id][object.series_id]:
#                     min_time[object.patient_id][object.study_id][object.series_id] = object.acquisition_time
#             else: min_time[object.patient_id][object.study_id] = {object.series_id:object.acquisition_time}
#         else: min_time[object.patient_id] = {object.study_id:{object.series_id:object.acquisition_time}}
#     else: min_time.update({object.patient_id:{object.study_id:{object.series_id:object.acquisition_time}}})
#
# print(min_time)
#
# max_time = {}
# for object in list_of_dcm_objects:
#     if object.patient_id in max_time:
#         if object.study_id in max_time[object.patient_id]:
#             if object.series_id in max_time[object.patient_id][object.study_id]:
#                 if object.acquisition_time > max_time[object.patient_id][object.study_id][object.series_id]:
#                     max_time[object.patient_id][object.study_id][object.series_id] = object.acquisition_time
#             else: max_time[object.patient_id][object.study_id] = {object.series_id:object.acquisition_time}
#         else: max_time[object.patient_id] = {object.study_id:{object.series_id:object.acquisition_time}}
#     else: max_time.update({object.patient_id:{object.study_id:{object.series_id:object.acquisition_time}}})
#
# print(max_time)

