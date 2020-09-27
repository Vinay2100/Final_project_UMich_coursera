#!/usr/bin/env python
# coding: utf-8

# # FINAL CODE CLUBBED ALTOGETHER INTO SINGLE CELL

# In[4]:



import zipfile

from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

'''
Your task is to write python code
which allows one to search through the images
looking for the occurrences of keywords and faces

E.g. if you search for "pizza",
it will return a contact sheet of all of the faces
which were located on the newspaper page which mentions "pizza".
'''

images = {} # dictionary of lists indexed with filenames

name_list = [] # list of filenames

def unzip_images(zip_name):
    '''
    iterates over images in a zipfile and extracts and modifies global dictionary for all
    also creates a namelist containing all names of all images in the zipfile
    '''
    zf = zipfile.ZipFile(zip_name)
    for each in zf.infolist():
        images[each.filename] = [Image.open(zf.open(each.filename))]
        name_list.append(each.filename)
        
if __name__ == '__main__':
    
    unzip_images('readonly/images.zip')
    
    for name in name_list:
        img = images[name][0]
        
        images[name].append(pytesseract.image_to_string(img).replace('-\n',''))

        
        if 'Mark' in images[name][1]: 
            print('Results found in file',name)
            
            try:
                faces = (face_cascade.detectMultiScale(np.array(img),1.35,4)).tolist()

                images[name].append(faces)

                faces_in_each = []
                
                for x,y,w,h in images[name][2]:
                    faces_in_each.append(img.crop((x,y,x+w,y+h)))
                
                contact_sheet = Image.new(img.mode, (550,110*int(np.ceil(len(faces_in_each)/5))))
                x = 0
                y = 0

                for face in faces_in_each:
                    face.thumbnail((110,110))
                    contact_sheet.paste(face, (x, y))
                    
                    if x+110 == contact_sheet.width:
                        x=0
                        y=y+110
                    else:
                        x=x+110
                        
                display(contact_sheet)
            except:
                print('But there were no faces in that file!')


# In[ ]:




