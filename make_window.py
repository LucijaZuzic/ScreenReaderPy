from tkinter import *
import numpy as np
import cv2
from mss import mss
import pytesseract
import win32gui

class window2:

    def __init__(self,master1):

        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        self.loop_active = False
        self.inside_loop = False

        self.panel2 = Frame(master1)
        self.panel2.grid()
 
        self.vcmd = (self.panel2.register(self.callback))

        self.label_top = Label(self.panel2, text = "Top: ")
        self.label_top.grid(row = 0, column = 0)

        self.text_top = Entry(self.panel2, validate = "all", validatecommand = (self.vcmd, '%P')) 
        self.text_top.grid(row = 0, column = 1)

        self.label_left = Label(self.panel2, text = "Left: ")
        self.label_left.grid(row = 0, column = 2)

        self.text_left = Entry(self.panel2, validate = "all", validatecommand = (self.vcmd, '%P')) 
        self.text_left.grid(row = 0, column = 3)

        self.label_width = Label(self.panel2, text = "Width: ")
        self.label_width.grid(row = 0, column = 4)

        self.text_width = Entry(self.panel2, validate = "all", validatecommand = (self.vcmd, '%P')) 
        self.text_width.grid(row = 0, column = 5)

        self.label_height = Label(self.panel2, text = "Height: ")
        self.label_height.grid(row = 0, column = 6)

        self.text_height = Entry(self.panel2, validate = "all", validatecommand = (self.vcmd, '%P')) 
        self.text_height.grid(row = 0, column = 7)

        self.buttong = Button(self.panel2,text = "Start", command = self.start_loop)
        self.buttong.grid(row = 1, column = 0, columnspan = 4)

        self.buttong = Button(self.panel2,text = "End", command = self.end_loop)
        self.buttong.grid(row = 1, column = 4, columnspan = 4)

        sct = mss()
        self.widths_heights = ""
        
        for i in range(len(sct.monitors)):
            monitor = sct.monitors[i]
            if i == 0:
                self.total_width = monitor["width"]
                self.total_height = monitor["height"]
                self.bounding_box = {'top': 0, 'left': 0, 'width': self.total_width, 'height': self.total_height}
                
                self.text_top.delete(0, END)
                self.text_left.delete(0, END)
                self.text_width.delete(0, END)
                self.text_height.delete(0, END)
                
                self.text_top.insert(0, "0")
                self.text_left.insert(0, "0")
                self.text_width.insert(0, str(self.total_width))
                self.text_height.insert(0, str(self.total_height))
            self.widths_heights += "Monitor " + str(i + 1) + ": " + str(monitor["width"]) + " x " + str(monitor["height"]) + "\n" 
 
        self.label_px = Text(self.panel2)
        self.label_px.grid(row = 2, column = 0, columnspan = 8)

        self.scrollbay = Scrollbar(self.panel2, command = self.label_px.yview)
        self.scrollbax = Scrollbar(self.panel2, command = self.label_px.xview)
        self.label_px['yscrollcommand'] = self.scrollbay.set
        self.label_px['xscrollcommand'] = self.scrollbax.set

        self.label_text = Text(self.panel2)
        self.label_text.grid(row = 3, column = 0, columnspan = 8)

        self.scrollby = Scrollbar(self.panel2, command = self.label_text.yview)
        self.scrollbx = Scrollbar(self.panel2, command = self.label_text.xview)
        self.label_text['yscrollcommand'] = self.scrollby.set
        self.label_text['xscrollcommand'] = self.scrollbx.set

        win32gui.EnumWindows(self.window_vals, None)
 
    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
        
    def window_vals(self, hwnd, extra):
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        if w > 0 and h > 0:
            self.widths_heights += "Window " + win32gui.GetWindowText(hwnd) + ": top: " + str(y) + " left: " + str(x) + " width: " + str(w) + " height: " + str(h) + "\n"

        self.label_px.delete(1.0, END)
        self.label_px.insert(END, self.widths_heights)
        
    def get_value(self):
        
        if len(self.text_top.get()) > 0:
            
            top_dim = int(self.text_top.get())

            if top_dim > self.total_height:

                top_dim = 0

        else:

            top_dim = 0

        if len(self.text_left.get()) > 0:
            
            left_dim = int(self.text_left.get())

            if left_dim > self.total_width:

                left_dim = 0

        else:

            left_dim = 0
        
        if len(self.text_width.get()) > 0:
            
            width_dim = int(self.text_width.get())

            if left_dim + width_dim > self.total_width:

                width_dim = self.total_width - left_dim

        else:

            width_dim = self.total_width - left_dim

        if len(self.text_height.get()) > 0:
            
            height_dim = int(self.text_height.get())

            if top_dim + height_dim > self.total_height:

                height_dim = self.total_height - top_dim

        else:

            height_dim = self.total_height - top_dim

        self.text_top.delete(0, END)
        self.text_left.delete(0, END)
        self.text_width.delete(0, END)
        self.text_height.delete(0, END)

        self.text_top.insert(0, str(top_dim))
        self.text_left.insert(0, str(left_dim))
        self.text_width.insert(0, str(width_dim))
        self.text_height.insert(0, str(height_dim))

        self.bounding_box = {'top': top_dim, 'left': left_dim, 'width': width_dim, 'height': height_dim}
        
    def start_loop(self):
            
        self.loop_active = True  
        
        if not self.inside_loop:

            self.one_loop()

    def end_loop(self):

        self.loop_active = False
        cv2.destroyAllWindows()

    def one_loop(self):

        self.inside_loop = True

        cv2.destroyAllWindows()
        sct = mss()
        self.get_value()
        sct_img = sct.grab(self.bounding_box)
        np_img = np.array(sct_img)
        cv2.imshow('screen', np_img)
        
        # Convert the image to gray scale
        gray = cv2.cvtColor(np_img, cv2.COLOR_BGR2GRAY)
        
        # Performing OTSU threshold
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        
        # Specify structure shape and kernel size. 
        # Kernel size increases or decreases the area 
        # of the rectangle to be detected.
        # A smaller value like (10, 10) will detect 
        # each word instead of a sentence.
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        
        # Applying dilation on the threshold image
        dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
        
        # Finding contours
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, 
                                                        cv2.CHAIN_APPROX_NONE)
        
        # Creating a copy of image
        im2 = np_img.copy()
        
        # Looping through the identified contours
        # Then rectangular part is cropped and passed on
        # to pytesseract for extracting text from it
        # Extracted text is then written into the text file
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Drawing a rectangle on copied image
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Cropping the text block for giving input to OCR
            cropped = im2[y:y + h, x:x + w]
            
            # Open the file in append mode
            file = open("recognized.txt", "a")
            
            # Apply OCR on the cropped image
            text_ocr = pytesseract.image_to_string(cropped)
            
            # Appending the text into the text box
            self.label_text.delete(1.0, END)
            self.label_text.insert(END, text_ocr)
            
            # Close the file
            file.close

        self.inside_loop = False 
        
root1=Tk()
window2(root1)
root1.mainloop()