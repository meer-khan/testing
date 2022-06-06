''' Copyright (C) 2022 by SeQuenX  - All Rights Reserved

* This file is part of the ComplyVantage product development,

* and is released under the "Commercial License Agreement".

*

* You should have received a copy of the Commercial License Agreement license with

* this file. If not, please write to: legal@sequenx.com, or visit www.sequenx.com

'''
import sys 
import argparse
import pathlib #Python Default
from zipfile import ZipFile #Python Default
import os #Python Default
import pandas as pd
from guesslang import Guess, GuesslangError
from guesslang.model import DATASET
import time
import datetime 


def making_new_DIR(fileDirectoryPath , filepath):
    global projectName

    if os.path.isdir(fileDirectoryPath):
        newDirPath = os.path.join(fileDirectoryPath, "ComplyVantage")
        fileName = pathlib.Path(filepath).stem
        projectName = fileName.title
        newDirPathNamedasProject = os.path.join(newDirPath,fileName)

        if os.path.isdir(newDirPath):
            # NEW CODE

            if os.path.isdir(newDirPathNamedasProject):
                raise Exception(fileName+" folder name already exists")
            
            else:
                os.mkdir(newDirPathNamedasProject)
            
            return newDirPathNamedasProject

        else:
            os.mkdir(newDirPath)
            if os.path.isdir(newDirPathNamedasProject):
                raise Exception("Project folder name already exists")
            
            else:
                os.mkdir(newDirPathNamedasProject)
            return newDirPathNamedasProject


def un_zipping_compressed_files(filePath, extractedDirPath = None):
    '''
    This function uncompresses the file
    Checks if given file name is valid, and then extracts its directory path then
    unzip the path, if user provided the directory path for extraction then it will 
    extract all the files there otherwise, extract all the files in the directory 
    where zipped file extists.
    it will create a new folder named as ComplyVantage and unzip all the files there 
    '''
    # check if path 

    if os.path.isfile(filePath):
        folderName = os.path.dirname(filePath)

    else: 
        raise Exception("No such File exists to unzip!")

    try:
        with ZipFile(filePath, 'r') as zip:
    # printing all the contents of the zip file
            zip.printdir()
            if extractedDirPath == None : 
                newDir = making_new_DIR(folderName , filePath)
                # extracting files at default location
                print('Extracting all the files at: ' + newDir)
                zip.extractall(newDir)
                print('Extraction Done!\n'
                    "GuessLang Started...")
                return newDir
            
            elif extractedDirPath is not None:
                if os.path.isdir(extractedDirPath):
                    newDir = making_new_DIR(extractedDirPath, filePath)

                    if  os.path.isdir(newDir):
                    # extracting all the files at the given location
                        print('Extracting all the files at: ' + newDir)
                        zip.extractall(newDir)
                        print('Unzipping Done!\n'
                            "GuessLang Started")
                        return newDir
                
                    else:
                        raise Exception("No such Directory exists to extract the Files!")
                else:
                    raise Exception("Not A valid Folder path for Unzipping")
                
            else:
                raise Exception("Internal Error")
    
    except OSError as e:
        raise Exception("No such Directory exists to unzip!")


def parsing_all_files_and_folders(extractedFilesDirectory):
    '''
    This function parse through all the files and stores the 
    file names and root directories in the lists
    '''
    global DIRRoots
    global DIRfiles
    for root, dirs, files in os.walk(extractedFilesDirectory):
        for filename in files:
            DIRRoots.append(root)
            DIRfiles.append(filename)


def getting_complete_path():
    '''
    This function creates the complete path using the output of "parsing_all_files_and_folders"
    and stores the complete path in list
    '''
    global completePath
    global DIRfiles
    for index, files in enumerate(DIRfiles):
    # Getting complete path of all the files in the directory
        completePath.append(os.path.join(DIRRoots[index], files))


def get_file_and_check_extension(file_path):
    '''
    This function gets the complete path of the files 
    and checks for its extension
    '''
    file_extension = pathlib.Path(file_path).suffix
    f = open(file_path, "r" , encoding = "utf-8", errors = "ignore")
    code_txt = f.read()
    return code_txt , file_extension

    
def language_detection(code):
    '''
    Guesslang model for the prediction of programming language
    '''
    return guess.language_name(code)


def checking_extensions_languages_of_all_files():
    '''
    this functions passes the files to the functions "get_file_and_check_extension" and language_detection
    and append the outputs to the lists for further processings
    '''
    
    global extensions
    global isJava
    global predictions
    global completePath

    for path in completePath:
        if path == None: 
            predictions.append("")
            extensions.append("")
            isJava.append("")
            continue

        code , extension = get_file_and_check_extension(path)
     
        if not code:
            predictions.append("Empty Source File")
            extensions.append(extension)
            isJava.append(False)
        elif code != False:
            language_returned = language_detection(code)
            predictions.append(language_returned)
            extensions.append(extension)
            if language_returned == "Java":
                isJava.append(True)
            else:
                isJava.append(False)


def writing_to_csv():

    '''
    This function saves the CSV with date and time stamp

    '''
    global csvDirectory
    global userDict
    global projectName

    df = pd.DataFrame(userDict)
    # print(df)
    ct = datetime.datetime.now()
    if os.path.isdir(csvDirectory):
        newCSVDirectory = os.path.join(csvDirectory, 'ComplyVantage_Date_%d_%d_%d_Time_%d_%d_%d'%(ct.day,ct.month,ct.year,ct.hour,ct.minute,ct.second)+'.csv')
        try:
            df.to_csv(newCSVDirectory,index=False)
            print("CSV Created Successfully!")
            print("CSV created at: " + newCSVDirectory)
        
        except Exception as e:
            print(e)
            print("CSV Creation Failed!")
    else: 
        raise Exception("Directory doesnot exist for CSV")


def global_variable_setter(args):

    '''
    this function sets the values for the global variables 
    and assigns the value to the "directorytoCheck" variable if "directoryFilesAreToBeExtracted" or "CSVPath" 
    variable is missing
    '''
    global directorytoCheck
    global directoryFilesAreToBeExtracted
    global csvDirectory

    directorytoCheck = args.file
    if args.extractionPath == None:
        directoryFilesAreToBeExtracted = os.path.dirname(directorytoCheck)
    else:
        
        directoryFilesAreToBeExtracted = args.extractionPath

    if args.CSVPath is not None: 
        csvDirectory = args.CSVPath
    
    elif args.CSVPath == None and args.extractionPath is not None: 
        csvDirectory = args.extractionPath
    
    elif args.CSVPath == None and args.extractionPath == None: 
        csvDirectory = os.path.dirname(directorytoCheck)

def version_check():
    '''
    function for checking the version of CLI 
    '''
    print(__version__)

'''
START of PROGRAMME
'''
# start time of program to calculate the time taken to run the program
startTime = time.time()


if __name__ == '__main__':


    directorytoCheck:str
    directoryFilesAreToBeExtracted:str
    csvDirectory:str
    projectName:str
    # Mention version of CLI here
    __version__ = '1.0'

    parser = argparse.ArgumentParser(prog="ComplyVantage", description="Tool for Compliance")
    parser.add_argument('file',type=str , default=None , help="enter zipped folder for validation" , )
    '''
    These are optional Parameters 
    but if we want to make them cumpolsory, required=True argument can be added in add_argument() 
    "dest" argument is used for mentioning variable name to store the value in 
    '''
    parser.add_argument('-f', dest='extractionPath', type=str , default=None , help="enter path for unzipping the folder" )
    parser.add_argument('-csv',dest="CSVPath", type=str , default=None , help="enter path for saving the CSV" , )
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    args = parser.parse_args()
    global_variable_setter(args)

    DIRRoots = [] #Root paths of every file in the zipped folder
    DIRfiles = [] #Names of every file in the zipped folder
    completePath = [] #Complete paths of every file in the zipped folder
    extensions = [] #Extensions of every file in the zipped folder
    isJava = [] #Bool array for storing the True and False on the basis of Guess Lang Prediction, either its a java code or not
    predictions = [] #Predictions of GuessLang

    extractedFilesDirectory = un_zipping_compressed_files(directorytoCheck, directoryFilesAreToBeExtracted)
    parsing_all_files_and_folders(extractedFilesDirectory)
    getting_complete_path()  
    guess = Guess()
    checking_extensions_languages_of_all_files()
    userDict = {'File Name': DIRfiles,'Extension': extensions, 'Prediction': predictions ,'Root Path': DIRRoots, 'Complete Path':completePath, 'Is Java': isJava, }
    writing_to_csv()
    # print(userDict)

    # end time of program to calculate the time taken to run the program
    endTime = time.time()
    completeTime = endTime - startTime
    print(f"Time of execution is: {completeTime} seconds")
    print("Validation Done!")





