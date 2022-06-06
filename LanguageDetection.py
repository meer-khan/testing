''' Copyright (C) 2022 by SeQuenX  - All Rights Reserved

* This file is part of the ComplyVantage product development,

* and is released under the "Commercial License Agreement".

*

* You should have received a copy of the Commercial License Agreement license with

* this file. If not, please write to: legal@sequenx.com, or visit www.sequenx.com

'''




from msilib.schema import Directory
import pathlib #Python Default
from zipfile import ZipFile #Python Default
import os #Python Default
import pandas as pd
from guesslang import Guess, GuesslangError
from guesslang.model import DATASET
import time
import datetime 

def making_new_directory(filePath, extractedFilesPath = None):

    if extractedFilesPath != None and os.path.dir(extractedFilesPath):
        # Making a new directory to extract the files
        newExtractedFilesPath = os.path.join(extractedFilesPath, "ComplyVantage")
        os.mkdir(newExtractedFilesPath)
        return True , newExtractedFilesPath 

    elif os.path.isdir(filePath): 
        newFilePath = os.path.join(filePath, "ComplyVantage")
        os.mkdir(newFilePath)
        return True , newFilePath
    
    else: 
        return False
    
    


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
                    # END CODE
            # raise Exception("Directory already exists as ComplyVantage Name!")
            # return newDirPath

        else:
            os.mkdir(newDirPath)
            if os.path.isdir(newDirPathNamedasProject):
                raise Exception("Project folder name already exists")
            
            else:
                os.mkdir(newDirPathNamedasProject)
            return newDirPathNamedasProject
            # return newDirPath

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
    global DIRRoots
    global DIRfiles
    for root, dirs, files in os.walk(extractedFilesDirectory):
        for filename in files:
            DIRRoots.append(root)
            DIRfiles.append(filename)


def getting_complete_path():
    global completePath
    global DIRfiles
    for index, files in enumerate(DIRfiles):
    # Getting complete path of all the files in the directory
        completePath.append(os.path.join(DIRRoots[index], files))




def get_file_and_check_extension(file_path):
    file_extension = pathlib.Path(file_path).suffix
    f = open(file_path, "r" , encoding = "utf-8", errors = "ignore")
    code_txt = f.read()
    return code_txt , file_extension
    
def language_detection(code):
    # print("Guess langugae initiated...")
    return guess.language_name(code)


def checking_extensions_languages_of_all_files():
    global extensions
    global isJava
    global predictions
    global completePath

    for path in completePath:
        # print("#"*50)
        # print(path)
        if path == None: 
            predictions.append("")
            extensions.append("")
            isJava.append("")
            continue

        code , extension = get_file_and_check_extension(path)
     
        # print(extensions)
        if not code:
            # print("Empty Source File")
            predictions.append("Empty Source File")
            extensions.append(extension)
            isJava.append(False)
        elif code != False:
            language_returned = language_detection(code)
            # print(f"This code is written in {language_returned} language ")
            predictions.append(language_returned)
            extensions.append(extension)
            if language_returned == "Java":
                isJava.append(True)
            else:
                isJava.append(False)


def writing_to_csv():
    global userDict
    df = pd.DataFrame(userDict)
    print(df)
    # df.to_csv(csvDirectory, index=False)
    ct = datetime.datetime.now()
    try:
        df.to_csv('D:\XYLEXA\ValidatorTesting\ComplyVantageResults_Date_%d_%d_%d_Time_%d_%d_%d'%(ct.day,ct.month,ct.year,ct.hour,ct.minute,ct.second)+'.csv',index=False)
        print("CSV Created Successfully!")
    
    except Exception as e:
        print(e)
        print("CSV Creation Failed!")



'''
START of PROGRAMME
'''
# start time of program to calculate the time taken to run the program
startTime = time.time()

DIRRoots = []
DIRfiles = []
completePath = []
extensions = []
isJava = []
predictions = []


directorytoCheck = 'D:\XYLEXA\ValidatorTesting\DependencyCheck-main.zip'
directoryFilesAreToBeExtracted = 'D:\XYLEXA\ValidatorTesting' # OPTIONAL
csvDirectory = 'D:\XYLEXA\ValidatorTesting\ComplyVantage.csv' # OPTIONAL

extractedFilesDirectory = un_zipping_compressed_files('D:\XYLEXA\ValidatorTesting\DependencyCheck-main.zip', 'D:\XYLEXA\ValidatorTesting')
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



















# with open('D:\XYLEXA\ValidatorTesting\FIRST.csv', 'w') as csvfile: 
#     # creating a csv writer object 
#     csvwriter = csv.writer(csvfile) 
        
#     # writing the fields 
#     csvwriter.writerow(fields)
#     csvwriter.writerow(DIRfiles) 
        
#     # writing the data rows 
#     csvwriter.writerows(rows)



# # fields = ['Name', 'Branch', 'Year', 'CGPA'] 
    
# # # data rows of csv file 
# # rows = [ ['Nikhil', 'COE', '2', '9.0'], 
# #          ['Sanchit', 'COE', '2', '9.1'], 
# #          ['Aditya', 'IT', '2', '9.3'], 
# #          ['Sagar', 'SE', '1', '9.5'], 
# #          ['Prateek', 'MCE', '3', '7.8'], 
# #          ['Sahil', 'EP', '2', '9.1']] 
    
# # # name of csv file 
# # filename = "university_records.csv"

# # with open('D:\XYLEXA\ValidatorTesting\FIRST.csv', 'w') as csvfile: 
# #     # creating a csv writer object 
# #     csvwriter = csv.writer(csvfile) 
        
# #     # writing the fields 
# #     csvwriter.writerow(fields) 
        
# #     # writing the data rows 
# #     csvwriter.writerows(rows)



