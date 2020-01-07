#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
import cv2
import numpy as np
import os
import face_recognition
from tkinter import messagebox

class Frame_IPTK:
    file_path = ''
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Image Processing Final Project')
        self.window.geometry('810x800')
##############################
        #left side (display)
        lable_origin = tk.Label(self.window, text='Face you want', bg='white', font=('Arial', 20), width=30, height=2)
        lable_origin.place(x=35, y=3)

        self.canvas_origin = tk.Canvas(self.window, bg='white', height=350, width=350)
        self.canvas_origin.place(x=35, y=38, anchor='nw')

        # Frame - match Information
        match_frame = tk.LabelFrame(self.window, text='Search Result', font=('Arial', 15),padx=20, pady=20)
        match_frame.place(x=35, y=395)

        self.canvas_match = tk.Canvas(match_frame, bg='white', height=300, width=300)
        self.canvas_match.grid(column = 0, row = 1)

        # # Match Mode
        # self.button_match_mode = tk.Button(match_frame, text='Match Mode', font=('Arial', 15), command=self.match_mode)
        # self.button_match_mode.grid(column=0, row=3, sticky=tk.W)

        # Nearest Mode
        self.button_nearest_mode = tk.Button(match_frame, text='Search Nearest Result', font=('Arial', 15), command=self.nearst_mode)
        self.button_nearest_mode.grid(column = 0, row=3, sticky=tk.W)


################################
        #right side (selection)
#####
        #Frame - Basic Information
        basic_frame = tk.LabelFrame(self.window, text='Basic Info',font=('Arial', 15))
        basic_frame.place(x=450, y=30)

        #gender
        lable_gender = tk.Label(basic_frame, text='Gender', bg='white', font=('Arial', 15))
        lable_gender.grid(column=0, row=1, sticky=tk.W)
        self.comboxlist_gender = ttk.Combobox(basic_frame, values=["Male", "Female"])
        self.comboxlist_gender.grid(column=1, row=1)

        # skin color
        lable_skin = tk.Label(basic_frame, text='Skin Color', bg='white',font=('Arial', 15))
        lable_skin.grid(column=0, row=2,sticky=tk.W)
        self.comboxlist_skin = ttk.Combobox(basic_frame, values=["Asian", "White", "African American"])
        self.comboxlist_skin.grid(column=1, row=2)
        # self.comboxlist_skin.bind("<<ComboboxSelected>>", self.laplacian)

        # face shape
        lable_fshape = tk.Label(basic_frame, text='Face Shape',bg='white',font=('Arial', 15))
        lable_fshape.grid(column=0, row=3,sticky=tk.W)
        self.comboxlist_fshape = ttk.Combobox(basic_frame, values=["Round", "Square", "Long"])
        self.comboxlist_fshape.grid(column=1, row=3)

        # display origin image
        self.button_origin = tk.Button(basic_frame, text='Show', font=('Arial', 15), command=self.select_origin)
        self.button_origin.grid(column=1, row=4)
#####

        # Adjustment

        ### Frame - Eye
        self.eye_frame = tk.LabelFrame(self.window, text='Eye', font=('Arial', 15))
        self.eye_frame.place(x=450, y=160)
        #eye style
        lable_eyestyle = tk.Label(self.eye_frame, text='Eye Style', bg='white', font=('Arial', 15))
        lable_eyestyle.grid(column=0, row=1, sticky=tk.W)
        self.comboxlist_eyestyle = ttk.Combobox(self.eye_frame, values=["Style 1", "Style 2", "Style 3"], )
        self.comboxlist_eyestyle.grid(column=1, row=1, sticky=tk.W)
        self.comboxlist_eyestyle.bind("<<ComboboxSelected>>", self.select_eye_style)

        #eye position
        lable_eyepos = tk.Label(self.eye_frame, text='Eye Position', bg='white', font=('Arial', 15))
        lable_eyepos.grid(column=0, row=2, sticky=tk.W)
        self.scale_eyepos = tk.Scale(self.eye_frame,  from_=-7, to=7, orient=tk.HORIZONTAL, length = 200, showvalue=9, tickinterval=2, resolution=1, command = self.select_eye_position)
        self.scale_eyepos.grid(column=1, row=2, sticky=tk.W)

        #eye size
        lable_eyesize = tk.Label(self.eye_frame, text='Eye Size', bg='white', font=('Arial', 15))
        lable_eyesize.grid(column=0, row=3, sticky=tk.W)
        self.scale_eyesize = tk.Scale(self.eye_frame, from_=-5, to=5, orient=tk.HORIZONTAL, length=200, showvalue=5,tickinterval=2, resolution=1, command=self.select_eye_size)
        self.scale_eyesize.grid(column=1, row=3, sticky=tk.W)

        ### Frame - Nose
        self.nose_frame = tk.LabelFrame(self.window, text='Nose', font=('Arial', 15))
        self.nose_frame.place(x=450, y=330)
        # nose style
        lable_nosestyle = tk.Label(self.nose_frame, text='Nose Style', bg='white', font=('Arial', 15))
        lable_nosestyle.grid(column=0, row=1, sticky=tk.W)
        self.comboxlist_nosestyle = ttk.Combobox(self.nose_frame, values=["Style 1", "Style 2", "Style 3"], )
        self.comboxlist_nosestyle.grid(column=1, row=1, sticky=tk.W)
        self.comboxlist_nosestyle.bind("<<ComboboxSelected>>", self.select_nose_style)

        # nose position - Left /Right
        lable_nosepos1 = tk.Label(self.nose_frame, text='Left/Right', bg='white', font=('Arial', 15))
        lable_nosepos1.grid(column=0, row=2, sticky=tk.W)
        self.scale_nosepos1 = tk.Scale(self.nose_frame, from_=-7, to=7, orient=tk.HORIZONTAL, length=200, showvalue=9, tickinterval=2, resolution=1, command=self.select_nose_position)
        self.scale_nosepos1.grid(column=1, row=2, sticky=tk.W)

        # mouth position - Up / Down
        lable_nosepos2 = tk.Label(self.nose_frame, text='Up/Down', bg='white', font=('Arial', 15))
        lable_nosepos2.grid(column=0, row=3, sticky=tk.W)
        self.scale_nosepos2 = tk.Scale(self.nose_frame, from_=-7, to=7, orient=tk.HORIZONTAL, length=200, showvalue=9, tickinterval=2, resolution=1, command=self.select_nose_position_up_down)
        self.scale_nosepos2.grid(column=1, row=3, sticky=tk.W)

        # nose size
        lable_eyesize = tk.Label(self.nose_frame, text='Nose Size', bg='white', font=('Arial', 15))
        lable_eyesize.grid(column=0, row=4, sticky=tk.W)
        self.scale_nosesize = tk.Scale(self.nose_frame, from_=-5, to=5, orient=tk.HORIZONTAL, length=200, showvalue=5, tickinterval=2, resolution=1, command=self.select_nose_size)
        self.scale_nosesize.grid(column=1, row=4, sticky=tk.W)

        ###Frame - Mouth
        self.mouth_frame = tk.LabelFrame(self.window, text='Mouth', font=('Arial', 15))
        self.mouth_frame.place(x=450, y=560)
        # mouth style
        lable_mouthstyle = tk.Label(self.mouth_frame, text='Mouth Style', bg='white', font=('Arial', 15))
        lable_mouthstyle.grid(column=0, row=1, sticky=tk.W)
        self.comboxlist_mouthstyle = ttk.Combobox(self.mouth_frame, values=["Style 1", "Style 2", "Style 3"], )
        self.comboxlist_mouthstyle.grid(column=1, row=1, sticky=tk.W)
        self.comboxlist_mouthstyle.bind("<<ComboboxSelected>>", self.select_mouth_style)

        # mouth position - Left / Right
        lable_mouthpos = tk.Label(self.mouth_frame, text='Left/Right', bg='white', font=('Arial', 15))
        lable_mouthpos.grid(column=0, row=2, sticky=tk.W)
        self.scale_mouthpos = tk.Scale(self.mouth_frame, from_=-7, to=7, orient=tk.HORIZONTAL, length=200, showvalue=9, tickinterval=2, resolution=1, command=self.select_mouth_position)
        self.scale_mouthpos.grid(column=1, row=2, sticky=tk.W)

        #mouth position - Up / Down
        lable_mouthpos2 = tk.Label(self.mouth_frame, text='Up/Down', bg='white', font=('Arial', 15))
        lable_mouthpos2.grid(column=0, row=3, sticky=tk.W)
        self.scale_mouthpos2 = tk.Scale(self.mouth_frame, from_=-7, to=7, orient=tk.HORIZONTAL, length=200, showvalue=9, tickinterval=2, resolution=1, command=self.select_mouth_position_up_down)
        self.scale_mouthpos2.grid(column=1, row=3, sticky=tk.W)

        # mouth size
        lable_mouthsize = tk.Label(self.mouth_frame, text='Mouth Size', bg='white', font=('Arial', 15))
        lable_mouthsize.grid(column=0, row=4, sticky=tk.W)
        self.scale_mouthsize = tk.Scale(self.mouth_frame, from_=-5, to=5, orient=tk.HORIZONTAL, length=200, showvalue=5, tickinterval=2, resolution=1, command=self.select_mouth_size)
        self.scale_mouthsize.grid(column=1, row=4, sticky=tk.W)

        self.window.mainloop()

##################################################################################
    ##############################################################################

    def match_mode(self):
        if(self.comboxlist_gender.get() == "Female"):
            list_dir = 'image/female'
        else:
            list_dir = 'image/male'
        images = os.listdir(list_dir)
        image_to_be_matched = face_recognition.load_image_file(self.file_path)
        image_to_be_matched_encoded = face_recognition.face_encodings(image_to_be_matched)[0]
        flag = False
        print("working...")
        for img in images:
            current_image = face_recognition.load_image_file(list_dir+'/' + img)
            current_image_encoded = face_recognition.face_encodings(current_image)[0]

            result = face_recognition.compare_faces([image_to_be_matched_encoded], current_image_encoded, tolerance=0.5)
            # result = face_recognition.compare_faces([image_to_be_matched_encoded], current_image_encoded)
            if result[0] == True:
                messagebox.showinfo("Result", "Match" + img[:-4])
                im = Image.open(list_dir + '/'+img, mode='r')
                self.img_matched = ImageTk.PhotoImage(im.resize((300, 300), Image.ANTIALIAS))
                self.canvas_match.create_image(0, 0, anchor='nw', image=self.img_matched)
                flag = True

        if (flag == False):
            messagebox.showinfo("Result", "No match!")

    def nearst_mode(self):
        if (self.comboxlist_gender.get() == "Female"):
            list_dir = 'image/female'
        else:
            list_dir = 'image/male'
        images = os.listdir(list_dir)
        image_to_be_matched = face_recognition.load_image_file(self.file_path)
        image_to_be_matched_encoded = face_recognition.face_encodings(image_to_be_matched)[0]
        flag = False
        print("working...")
        for img in images:
            current_image = face_recognition.load_image_file(list_dir + '/' + img)
            current_image_encoded = face_recognition.face_encodings(current_image)[0]

            result = face_recognition.compare_faces([image_to_be_matched_encoded], current_image_encoded, tolerance=0.5)
            # result = face_recognition.compare_faces([image_to_be_matched_encoded], current_image_encoded)
            if result[0] == True:
                messagebox.showinfo("Result", "Nearest one is: " + img[:-4])
                im = Image.open(list_dir + '/'+img, mode='r')
                self.img_matched = ImageTk.PhotoImage(im.resize((300, 300), Image.ANTIALIAS))
                self.canvas_match.create_image(0, 0, anchor='nw', image=self.img_matched)
                flag = True

        if (flag == False):
            res = ""
            min_dist = 100000000
            for img in images:
                current_image = face_recognition.load_image_file(list_dir + '/'+ img)
                current_image_encoded = face_recognition.face_encodings(current_image)[0]
                dist = np.linalg.norm(image_to_be_matched_encoded - current_image_encoded)
                if (dist < min_dist):
                    res = img
                    min_dist = dist
            messagebox.showinfo("Result", "Nearest one is: " + res[:-4])
            im = Image.open(list_dir +"/"+res, mode='r')
            self.img_matched = ImageTk.PhotoImage(im.resize((300, 300), Image.ANTIALIAS))
            self.canvas_match.create_image(0, 0, anchor='nw', image=self.img_matched)



    def select_mouth_size(self, k):
        img = cv2.imread(self.file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mouth_cascade = cv2.CascadeClassifier( "/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_mcs_mouth.xml")
        mouth = mouth_cascade.detectMultiScale(gray, 1.3, 30)[0]
        mouth_img = img[mouth[1] - 1:mouth[1] + mouth[3] + 1, mouth[0] - 1:mouth[0] + mouth[2] + 1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mouth_img = cv2.morphologyEx(mouth_img, cv2.MORPH_OPEN, kernel)
        img = self.remove_origin_nose_or_mouth(img, mouth)
        mouth_img = cv2.resize(mouth_img, dsize=(mouth[2] + 2 + 2 * int(k), mouth[3] + 2 + 2 * int(k)))

        # left eye
        mask = 255 * np.ones(mouth_img.shape, mouth_img.dtype)
        center = (mouth[0] + int(mouth[2] / 2), mouth[1] + int(mouth[3] / 2))
        img = cv2.seamlessClone(mouth_img, img, mask, center, cv2.MIXED_CLONE)
        img = cv2.fastNlMeansDenoisingColored(img, None, 3, 3, 7, 21)

        self.save_img = img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img)
        # cv2.imwrite("temp.jpg", img)
        self.img_show = ImageTk.PhotoImage(image.resize((350, 350), Image.ANTIALIAS))
        self.canvas_origin.create_image(0, 0, anchor='nw', image=self.img_show)
        self.button_confirm_mouthsize = tk.Button(self.mouth_frame, text='Save', font=('Arial', 15), command=self.save)
        self.button_confirm_mouthsize.grid(column=3, row=4)



    def select_mouth_position_up_down(self, k):
        img = cv2.imread(self.file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mouth_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_mcs_mouth.xml")
        mouth = mouth_cascade.detectMultiScale(gray, 1.3, 30)[0]
        mouth_img = img[mouth[1] - 1:mouth[1] + mouth[3] + 1, mouth[0] - 1:mouth[0] + mouth[2] + 1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mouth_img = cv2.morphologyEx(mouth_img, cv2.MORPH_OPEN, kernel)
        img = self.remove_origin_nose_or_mouth(img, mouth)

        img[mouth[1] - 1 + int(k): mouth[1] + 1 + mouth[3]+int(k), mouth[0] - 1:mouth[0] + 1 + mouth[2]] = mouth_img

        #img = cv2.fastNlMeansDenoisingColored(img, None, 5, 5, 7, 21)
        self.save_img = img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img)
        # cv2.imwrite("temp.jpg", img)
        self.img_show = ImageTk.PhotoImage(image.resize((350, 350), Image.ANTIALIAS))
        self.canvas_origin.create_image(0, 0, anchor='nw', image=self.img_show)
        self.button_confirm_mouthpos_u_d = tk.Button(self.mouth_frame, text='Save', font=('Arial', 15), command=self.save)
        self.button_confirm_mouthpos_u_d.grid(column=3, row=3)


    def select_mouth_position(self, k):
        img = cv2.imread(self.file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mouth_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_mcs_mouth.xml")
        mouth = mouth_cascade.detectMultiScale(gray, 1.3, 30)[0]
        mouth_img = img[mouth[1] - 1:mouth[1] + mouth[3] + 1, mouth[0] - 1:mouth[0] + mouth[2] + 1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mouth_img = cv2.morphologyEx(mouth_img, cv2.MORPH_OPEN, kernel)
        img = self.remove_origin_nose_or_mouth(img, mouth)

        img[mouth[1] - 1: mouth[1] + 1 + mouth[3], mouth[0] - 1 + int(k):mouth[0] + 1 + int(k) + mouth[2]] = mouth_img

        #img = cv2.fastNlMeansDenoisingColored(img, None, 5, 5, 7, 21)
        self.save_img = img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img)
        # cv2.imwrite("temp.jpg", img)
        self.img_show = ImageTk.PhotoImage(image.resize((350, 350), Image.ANTIALIAS))
        self.canvas_origin.create_image(0, 0, anchor='nw', image=self.img_show)
        self.button_confirm_mouthpos = tk.Button(self.mouth_frame, text='Save', font=('Arial', 15), command=self.save)
        self.button_confirm_mouthpos.grid(column=3, row=2)

    def select_mouth_style(self,*args):
        img = cv2.imread(self.file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mouth_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_mcs_mouth.xml")
        mouth = mouth_cascade.detectMultiScale(gray,1.3,30)[0]
        img = self.remove_origin_nose_or_mouth(img, mouth)

        new_mouth = np.ones((3, 2))
        if (self.comboxlist_mouthstyle.get() == 'Style 1'):
            new_mouth = cv2.imread('use/Anne-mouth.jpg')
        else:
            new_mouth = cv2.imread('use/jack-mouth.jpg')
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # new_mouth = cv2.morphologyEx(new_mouth, cv2.MORPH_OPEN, kernel)
        new_mouth = cv2.resize(new_mouth,dsize=(mouth[2],mouth[3]))
        mask_mouth = 255 * np.ones(new_mouth.shape, new_mouth.dtype)
        center = (mouth[0]+int(mouth[2]/2), mouth[1]+int(mouth[3]/2)-5)
        img = cv2.seamlessClone(new_mouth, img, mask_mouth, center, cv2.NORMAL_CLONE)
        img = cv2.fastNlMeansDenoisingColored(img, None, 5, 5, 7, 21)

        cv2.imwrite("temp.jpg", img)
        self.file_path = 'temp.jpg'
        self.open()


    def select_nose_size(self, k):
        img = cv2.imread(self.file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        nose_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_mcs_nose.xml")
        nose = nose_cascade.detectMultiScale(gray, 1.3, 12)[0]
        nose_img = img[nose[1] - 1:nose[1] + nose[3] + 1, nose[0] - 1:nose[0] + nose[2] + 1]
        img = self.remove_origin_nose_or_mouth(img, nose)
        nose_img = cv2.resize(nose_img, dsize=(nose[2] + 2 + 2 * int(k), nose[3] + 2 + 2 * int(k)))

        nose_img = cv2.resize(nose_img, dsize=(nose[2] + 2 + 2 * int(k), nose[3] + 2 + 2 * int(k)))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        nose_img = cv2.morphologyEx(nose_img, cv2.MORPH_OPEN, kernel)
        mask = 255 * np.ones(nose_img.shape, nose_img.dtype)
        center = (nose[0] + int(nose[2] / 2), nose[1] + int(nose[3] / 2))
        img = cv2.seamlessClone(nose_img, img, mask, center, cv2.MIXED_CLONE)
        img = cv2.fastNlMeansDenoisingColored(img, None, 3, 3, 7, 21)

        self.save_img = img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img)
        # cv2.imwrite("temp.jpg", img)
        self.img_show = ImageTk.PhotoImage(image.resize((350, 350), Image.ANTIALIAS))
        self.canvas_origin.create_image(0, 0, anchor='nw', image=self.img_show)
        self.button_confirm_nosesize = tk.Button(self.nose_frame, text='Save', font=('Arial', 15), command=self.save)
        self.button_confirm_nosesize.grid(column=3, row=4)

    def select_nose_position_up_down(self, k):
        img = cv2.imread(self.file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        nose_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_mcs_nose.xml")
        nose = nose_cascade.detectMultiScale(gray, 1.3, 12)[0]
        nose_img = img[nose[1] - 1:nose[1] + nose[3] + 1, nose[0] - 1:nose[0] + nose[2] + 1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        nose_img = cv2.morphologyEx(nose_img, cv2.MORPH_OPEN, kernel)
        img = self.remove_origin_nose_or_mouth(img, nose)

        img[nose[1] - 1+int(k): nose[1] + 1 + nose[3]+int(k), nose[0] - 1 :nose[0] + 1 + nose[2]] = nose_img

        #img = cv2.fastNlMeansDenoisingColored(img, None, 5, 5, 7, 21)
        self.save_img = img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img)
        # cv2.imwrite("temp.jpg", img)
        self.img_show = ImageTk.PhotoImage(image.resize((350, 350), Image.ANTIALIAS))
        self.canvas_origin.create_image(0, 0, anchor='nw', image=self.img_show)
        self.button_confirm_nosepos = tk.Button(self.nose_frame, text='Save', font=('Arial', 15), command=self.save)
        self.button_confirm_nosepos.grid(column=3, row=3)

    def select_nose_position(self,k):
        img = cv2.imread(self.file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        nose_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_mcs_nose.xml")
        nose = nose_cascade.detectMultiScale(gray, 1.3, 12)[0]
        nose_img = img[nose[1] - 1:nose[1] + nose[3] + 1, nose[0] - 1:nose[0] + nose[2] + 1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        nose_img = cv2.morphologyEx(nose_img, cv2.MORPH_OPEN, kernel)
        img = self.remove_origin_nose_or_mouth(img, nose)

        img[nose[1] - 1: nose[1] + 1 + nose[3],nose[0] - 1 + int(k):nose[0] + 1 + int(k) + nose[2]] = nose_img

        #img = cv2.fastNlMeansDenoisingColored(img, None, 5, 5, 7, 21)
        self.save_img = img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img)
        # cv2.imwrite("temp.jpg", img)
        self.img_show = ImageTk.PhotoImage(image.resize((350, 350), Image.ANTIALIAS))
        self.canvas_origin.create_image(0, 0, anchor='nw', image=self.img_show)
        self.button_confirm_nosepos = tk.Button(self.nose_frame, text='Save', font=('Arial', 15), command=self.save)
        self.button_confirm_nosepos.grid(column=3, row=2)

    def select_nose_style(self,*args):
        img = cv2.imread(self.file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        nose_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_mcs_nose.xml")
        nose = nose_cascade.detectMultiScale(gray, 1.3, 12)[0]
        img = self.remove_origin_nose_or_mouth(img, nose)

        new_nose = np.ones((3, 2))
        if (self.comboxlist_nosestyle.get() == 'Style 1'):
            new_nose = cv2.imread('use/Anne-nose.jpg')
        else:
            new_nose = cv2.imread('use/jack-nose.jpg')
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        new_nose = cv2.morphologyEx(new_nose, cv2.MORPH_OPEN, kernel)
        new_nose = cv2.resize(new_nose,dsize=(nose[2],nose[3]))
        mask_nose = 255 * np.ones(new_nose.shape, new_nose.dtype)
        center = (nose[0]+int(nose[2]/2),nose[1] + int(nose[3]/2)-10)
        #center = (nose[0]+int(nose[2]/2),nose[1]+int(nose[3]/2)-10)
        img = cv2.seamlessClone(new_nose, img, mask_nose, center, cv2.NORMAL_CLONE)
        img = cv2.fastNlMeansDenoisingColored(img, None, 5, 5, 7, 21)
        cv2.imwrite("temp.jpg", img)
        self.file_path = 'temp.jpg'
        self.open()

    # nose 和 mouth 都一样
    def remove_origin_nose_or_mouth(self, img, nose):
        fill_img = self.make_fill_blank()
        fill_img = cv2.resize(fill_img, dsize=(nose[2], nose[3]))
        mask_eye = 255 * np.ones(fill_img.shape, fill_img.dtype)
        center = (nose[0] + int(nose[2] / 2), nose[1] + int(nose[3] / 2))
        img = cv2.seamlessClone(fill_img, img, mask_eye, center, cv2.NORMAL_CLONE)
        return img

    def select_eye_size(self,k):
        img = cv2.imread(self.file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        eye_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_eye.xml")
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 12)
        if (eyes[0, 0] < eyes[1, 0]):
            left_eye = eyes[0]
            right_eye = eyes[1]
        else:
            left_eye = eyes[1]
            right_eye = eyes[0]

        left_eye_img = img[left_eye[1]-1:left_eye[1] + left_eye[3]+1, left_eye[0]-1:left_eye[0] + left_eye[2]+1]
        right_eye_img = img[right_eye[1]-2:right_eye[1] + right_eye[3]+2, right_eye[0]-2:right_eye[0] + right_eye[2]+2]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        left_eye_img = cv2.morphologyEx(left_eye_img, cv2.MORPH_OPEN, kernel)
        right_eye_img = cv2.morphologyEx(right_eye_img, cv2.MORPH_OPEN, kernel)
        img = self.remove_origin_eye(img, left_eye, right_eye)

        left_eye_img = cv2.resize(left_eye_img,dsize=(left_eye[2]+2+2*int(k),left_eye[3]+2+2*int(k)))
        right_eye_img = cv2.resize(right_eye_img,dsize=(right_eye[2]+2+2*int(k),right_eye[3]+2+2*int(k)))
        # left eye
        mask_l = 255 * np.ones(left_eye_img.shape, left_eye_img.dtype)
        center = (left_eye[0] + int(left_eye[2] / 2), left_eye[1] + int(left_eye[3] / 2))
        img = cv2.seamlessClone(left_eye_img, img, mask_l, center, cv2.MIXED_CLONE)
        # right eye
        mask_r = 255 * np.ones(right_eye_img.shape, right_eye_img.dtype)
        center = (right_eye[0] + int(right_eye[2] / 2), right_eye[1] + int(right_eye[3] / 2))
        img = cv2.seamlessClone(right_eye_img, img, mask_r, center, cv2.MIXED_CLONE)
        img = cv2.fastNlMeansDenoisingColored(img, None, 3, 3, 7, 21)
        self.save_img = img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img)
        # cv2.imwrite("temp.jpg", img)
        self.img_show = ImageTk.PhotoImage(image.resize((350, 350), Image.ANTIALIAS))
        self.canvas_origin.create_image(0, 0, anchor='nw', image=self.img_show)
        self.button_confirm_eyesize = tk.Button(self.eye_frame, text='Save', font=('Arial', 15), command=self.save)
        self.button_confirm_eyesize.grid(column=3, row=3)


    def select_eye_position(self,k):
        img = cv2.imread(self.file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        eye_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_eye.xml")
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 12)
        if (eyes[0, 0] < eyes[1, 0]):
            left_eye = eyes[0]
            right_eye = eyes[1]
        else:
            left_eye = eyes[1]
            right_eye = eyes[0]

        left_eye_img = img[left_eye[1]-1:left_eye[1] + left_eye[3]+1, left_eye[0]-1:left_eye[0] + left_eye[2]+1]
        right_eye_img = img[right_eye[1]-1:right_eye[1] + right_eye[3]+1, right_eye[0]-1:right_eye[0] + right_eye[2]+1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        left_eye_img = cv2.morphologyEx(left_eye_img, cv2.MORPH_OPEN, kernel)
        right_eye_img = cv2.morphologyEx(right_eye_img, cv2.MORPH_OPEN, kernel)

        img = self.remove_origin_eye(img, left_eye, right_eye)
        #move
        img[left_eye[1]-1: left_eye[1]+1 + left_eye[3], left_eye[0]-1 + int(k):left_eye[0]+1 + int(k) + left_eye[2]] = left_eye_img
        img[right_eye[1]-1: right_eye[1]+1 + right_eye[3], right_eye[0]-1 - int(k):right_eye[0]+1 - int(k) + right_eye[2]] = right_eye_img

        #img = cv2.fastNlMeansDenoisingColored(img, None, 5, 5, 7, 21)
        self.save_img = img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img)
        #cv2.imwrite("temp.jpg", img)
        self.img_show = ImageTk.PhotoImage(image.resize((350, 350), Image.ANTIALIAS))
        self.canvas_origin.create_image(0, 0, anchor='nw', image=self.img_show)
        self.button_confirm_eyepos = tk.Button(self.eye_frame, text='Save', font=('Arial', 15), command = self.save)
        self.button_confirm_eyepos.grid(column=3, row=2)

    def select_eye_style(self, *args):
        img = cv2.imread(self.file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # define classifier
        eye_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_eye.xml")
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 12)
        if (eyes[0, 0] < eyes[1, 0]):
            left_eye = eyes[0]
            right_eye = eyes[1]
        else:
            left_eye = eyes[1]
            right_eye = eyes[0]

        #remove origin eyes
        img = self.remove_origin_eye(img, left_eye, right_eye)

        new_eye_l = np.ones((3, 2))
        new_eye_r = np.ones((3, 2))
        if(self.comboxlist_eyestyle.get() == 'Style 1'):
            new_eye_l = cv2.imread('use/Anne-left-eye.jpg')
            new_eye_r = cv2.imread('use/Anne-right-eye.jpg')
        else:
            new_eye_l = cv2.imread('use/jack-left-eye.jpg')
            new_eye_r = cv2.imread('use/jack-right-eye.jpg')

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        new_eye_l = cv2.morphologyEx(new_eye_l, cv2.MORPH_OPEN, kernel)
        new_eye_r = cv2.morphologyEx(new_eye_r, cv2.MORPH_OPEN, kernel)

        new_eye_l = cv2.resize(new_eye_l, dsize=(left_eye[2], left_eye[3]))
        new_eye_r = cv2.resize(new_eye_r, dsize=(right_eye[2], right_eye[3]))
        #left eye
        mask_l = 255 * np.ones(new_eye_l.shape, new_eye_l.dtype)
        center = (left_eye[0] + int(left_eye[2] / 2), left_eye[1] + int(left_eye[3] / 2))
        img = cv2.seamlessClone(new_eye_l, img, mask_l, center, cv2.MIXED_CLONE)
        #right eye
        mask_r = 255 * np.ones(new_eye_r.shape, new_eye_r.dtype)
        center = (right_eye[0] + int(right_eye[2] / 2), right_eye[1] + int(right_eye[3] / 2))
        img = cv2.seamlessClone(new_eye_r, img, mask_r, center, cv2.MIXED_CLONE)
        img = cv2.fastNlMeansDenoisingColored(img, None, 5, 5, 7, 21)
        cv2.imwrite("temp.jpg", img)
        self.file_path = 'temp.jpg'
        self.open()

    def remove_origin_eye(self,img,left_eye, right_eye):
        eye_img = self.make_fill_blank()
        # eye_img = cv2.resize(eye_img,dsize=(right_eye[2] + right_eye[0] - left_eye[0]+10,right_eye[3]))
        #mask_eye = 255 * np.ones(eye_img.shape, eye_img.dtype)
        # x = int((right_eye[0] - left_eye[0] - left_eye[2])/2) + left_eye[0] + left_eye[2]
        # y = left_eye[1] + int(left_eye[3]/2)
        # center = (x, y)
        # img = cv2.seamlessClone(eye_img, img, mask_eye, center, cv2.NORMAL_CLONE)
        left_eye_img = cv2.resize(eye_img, dsize=(left_eye[2], left_eye[3]))
        l_mask_eye = 255 * np.ones(left_eye_img.shape, left_eye_img.dtype)
        l_center = (left_eye[0] + int(left_eye[2]/2), left_eye[1] + int(left_eye[3]/2))
        img = cv2.seamlessClone(left_eye_img, img, l_mask_eye, l_center, cv2.NORMAL_CLONE)

        right_eye_img = cv2.resize(eye_img, dsize=(right_eye[2], right_eye[3]))
        r_mask_eye = 255 * np.ones(right_eye_img.shape, right_eye_img.dtype)
        r_center = (right_eye[0] + int(right_eye[2] / 2), right_eye[1] + int(right_eye[3] / 2))
        img = cv2.seamlessClone(right_eye_img, img, r_mask_eye, r_center, cv2.NORMAL_CLONE)
        #img = cv2.fastNlMeansDenoisingColored(img, None, 8, 8, 7, 21)
        # cv2.imwrite("temp.jpg", img)
        # self.file_path = 'temp.jpg'
        return img

    def make_fill_blank(self):
        img = cv2.imread(self.file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml")
        eye_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_eye.xml")

        face = face_cascade.detectMultiScale(gray, 1.3, 12)[0]
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 12)
        if (eyes[0, 0] < eyes[1, 0]):
            left_eye = eyes[0]
            right_eye = eyes[1]
        else:
            left_eye = eyes[1]
            right_eye = eyes[0]
        fill_img = img[face[1] + 10:face[1] + int(right_eye[3] / 2), left_eye[0] + left_eye[2]:right_eye[0]]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(fill_img, cv2.MORPH_OPEN, kernel)
        return opening


    def select_origin(self):
        if (self.comboxlist_skin.get() == 'White' and self.comboxlist_fshape.get() == 'Long' and self.comboxlist_gender.get() == 'Female'):
            self.file_path = 'standard/long-white-female.jpg'
            #print("get")
        else:
            self.file_path = 'standard/square-asia-male.jpg'
        self.scale_eyepos.set(0)
        self.scale_eyesize.set(0)
        self.scale_mouthpos.set(0)
        self.scale_mouthpos2.set(0)
        self.scale_mouthsize.set(0)
        self.scale_nosepos1.set(0)
        self.scale_nosepos2.set(0)
        self.scale_nosesize.set(0)
        self.comboxlist_eyestyle.set('')
        self.comboxlist_mouthstyle.set('')
        self.comboxlist_nosestyle.set('')
        self.open()

    def save(self):
        self.file_path = 'temp.jpg'
        cv2.imwrite("temp.jpg", self.save_img)

    def open(self):
        #self.file_path = askopenfilename()
        #print(self.file_path)
        im = Image.open(self.file_path, mode='r')
        self.img_origin = ImageTk.PhotoImage(im.resize((350, 350), Image.ANTIALIAS))
        self.canvas_origin.create_image(0, 0, anchor='nw', image=self.img_origin)
