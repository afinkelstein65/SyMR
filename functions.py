import os.path
import tkinter.filedialog
from tkinter import *
import nibabel as nib
from PIL import ImageTk, Image, ImageOps
import numpy as np
import tkinter.font as tkfont
import matplotlib.pyplot as plt

#TODO = put in FSE and EPG functions for sequence simulations
#TODO: will need to make executable with pyinstaller.

class GUI(Tk):
    '''General GUI class'''
    def __init__(self, file):
        super().__init__()
        helv20 = tkfont.Font(family='Helvetica', size=25)
        self.T1, self.T2, self.PD = np.zeros((400,400,400)), np.zeros((400,400,400)), np.zeros((200,200,200))
        self.file = file
        self.window = Toplevel()
        self.window.title('SyMR - Synthetic MR')

        self.window.geometry("1000x1000+10+20")
        self.tmp = np.zeros((200,200))
        # self.window.rowconfigure(2)
        # self.window.columnconfigure(2)

        self.frame1 = self.frame('white', width=1000, height=200)
        self.frame1.grid(row=0,column=0, columnspan=2)

        # LOGO
        tmp_img = Image.open("images/tmp_logo.jpeg")
        tmp_img = tmp_img.resize((100,100))
        self.photo = ImageTk.PhotoImage(tmp_img)
        self.label = Label(self.frame1, image=self.photo)
        self.label.place(y=10,x=875)
        self.ID = Label(self.frame1, text='Created By: Alan Finkelstein\n'
                                          'Department of Biomedical Engineering, University of Rochester')
        self.ID.place(y=5, height=40, width=500, x=50)


        self.frame2 = self.frame('white', height=800)
        self.frame2.grid(row=1, column=0, rowspan=2, sticky="nswe")

        # Image Display
        self.frame3 = self.frame('white', height=800)
        self.frame3.grid(row=1, column=1, rowspan=2, stick="nswe")


        self.nslice = 0
        self.slider = Scale(self.frame3, from_=0, to=199, orient='horizontal',
                            command=self.update_slice)
        self.slider.place(y=600, x=50, width=400)

        self.TE = 0
        self.TElabel = Label(self.frame2,text='TE')
        self.TElabel.place(x=20, y=150, width=50, height=50)
        self.TEslider = Scale(self.frame2, from_=0, to=300, orient = 'horizontal',
                              command=self.update_TE)
        self.TEslider.set(0)
        self.TElabel.config(font=helv20)
        self.TEslider.place(y=150,x=70,width=400, height=50)

        self.TI = 0
        self.TIlabel = Label(self.frame2, text='TI')
        self.TIlabel.place(x=20, y =250, width=50, height=50)
        self.TIlabel.config(font=helv20)
        self.TIslider = Scale(self.frame2, from_=0, to=5000, orient='horizontal',
                              command=self.update_TI)
        self.TIslider.place(x=70, y=250, width=400, height=50)

        self.TR = 0
        self.TRlabel = Label(self.frame2, text='TR')
        self.TRlabel.place(x=20, y=350, width=50, height=50)
        self.TRlabel.config(font=helv20)
        self.TRslider = Scale(self.frame2, from_=0, to=5000, orient= 'horizontal',
                               command=self.update_TR)
        self.TRslider.place(x=70,y=350, width=400,height=50)

        self.FA = 0
        self.FAlabel = Label(self.frame2, text='FA')
        self.FAlabel.place(x=20, y=450, width=50, height=50)
        self.FAlabel.config(font=helv20)
        self.FAslider = Scale(self.frame2, from_=0, to=180, orient='horizontal',
                              command=self.update_FA)
        self.FAslider.place(x=70, y=450, width=400, height=50)

        self.ESP = 0
        self.ESPlabel = Label(self.frame2, text='ESP')
        self.ESPlabel.place(x=20, y=550, width=50, height=50)
        self.ESPlabel.config(font=helv20)
        self.ESPslider=Scale(self.frame2, from_=0, to=100, orient='horizontal',
                             command=self.update_ESP)
        self.ESPslider.place(x=70,y=550, width=400, height=50)

        self.ETL= 0
        self.ETLlabel = Label(self.frame2, text='ETL')
        self.ETLlabel.place(x=20, y=650, width=50, height=50)
        self.ETLlabel.config(font=helv20)
        self.ETLslider= Scale(self.frame2, from_=0, to=50, orient='horizontal',
                              command=self.update_ETL)
        self.ETLslider.place(x=70, y=650, width=400, height=50)




        # Entry toolbar
        self.subject = Label(self.frame1, text='Subject')
        self.subject.place(height=50, width=100, y=50, x=50)
        self.entry = Entry(self.frame1)
        self.entry.place(height=50,width=600,x=150, y= 50)
        self.browse = Button(self.frame1, text='Browse', command=self.open_file)
        self.browse.place(height=25, width=100,y=50,x =750)
        self.submit = Button(self.frame1, text='Submit', command=self.submit)
        self.submit.place(height=25, width=100, y=75,x=750)

        # self.subject = Entry(self.frame1)

        #Input Parameters
        helv20 = tkfont.Font(family='Helvetica', size=25)
        self.options = ["SE","FSE", "MPRAGE"]
        self.clicked = StringVar()
        self.clicked.set("SE")
        self.seq = OptionMenu(self.frame2, self.clicked, *self.options)
        self.seq.config(font=helv20, width=29, height=2)
        self.seq.place(x=20, y=30)
        # self.seqname = Label(self.frame2, text='Sequence', relief='raised')
        # self.seqname.place(x=20,y=10, width=100)





        # Image Display
        self.image = ImageTk.PhotoImage(image=Image.fromarray(self.T2[100,:,:]))
        self.label = Label(self.frame3, image=self.image, relief="raised")
        self.label.place(y=150, x =50)
        self.title = Label(self.frame3, text='Synthetic MRI', font=('Helvetica',24))
        self.title.place(y=50,x=175)
        self.clicked.trace('w',self.update_seq)

        self.subtitle = Label(self.frame3, text='Sequence: {}'.format(self.clicked.get()), font=('Helvetica',24))
        self.subtitle.place(y=100,x=165)

        self.orientations = ['Axial','Sagittal','Coronal']
        self.orientation = StringVar()
        self.orientation.set('Axial')
        self.orient = OptionMenu(self.frame3, self.orientation, *self.orientations)
        self.orient.config(font=helv20,width=25, height=2)
        self.orientation.trace('w',self.update_orientation)
        self.orient.place(x=50, y=700)





        # self.button1 = self.button(self.frame1,'Hello','red')
        # self.button2 = self.button(self.frame2, "Bye",  'blue')
        # self.button3 = self.button(self.frame3, 'Lemon', 'green')

        # self.window.grid_rowconfigure(0, weight=1)
        # self.window.grid_rowconfigure(1, weight=25)
        # self.window.grid_columnconfigure(0, weight=1)
        # self.window.grid_columnconfigure(1, weight=1)
        # self.window.grid_columnconfigure(0, weight=1)


    def frame(self, color,width=500,height=300):
        frame = Frame(self.window, bg=color, width=width, height=height)
        return frame

    def open_file(self):
        file = tkinter.filedialog.askdirectory()
        print(os.path.abspath(file))
        data_dir = os.path.abspath(file)
        # try:
        self.T1, self.T2, self.PD = nib.load(os.path.join(data_dir, 'T1.nii')).get_fdata(), \
                       nib.load(os.path.join(data_dir, 'T2.nii')).get_fdata(), \
                       nib.load(os.path.join(data_dir,'PD.nii')).get_fdata()
        print('Done')
        self.update_image()
        # except:
        #     print("Incorrect Directory Chosen!")

        return None

    def submit(self):
        data = self.entry.get()
        print(data)

    def update_image(self):
        self.orient = self.orientation.get()
        self.tmp = self.simulate()
        if self.tmp.max() == 0:
            pass
        else:
            self.tmp = 255*self.tmp/self.tmp.max()
            if self.orient == 'Axial':
                tmp_img =Image.fromarray(np.flipud(np.rot90(self.tmp)))
            else:
                tmp_img = Image.fromarray(np.fliplr(np.rot90(self.tmp)))
            tmp_img = tmp_img.resize((400,400))
            self.image = ImageTk.PhotoImage(image=tmp_img)
            self.label = Label(self.frame3, image=self.image)
            self.label.place(y=150, x=50)

    def simulate(self):
        if self.orient == 'Axial':
            T1, T2, PD = self.T1[:,:, self.nslice], self.T2[:,:,self.nslice], self.PD[...,self.nslice]
        elif self.orient == 'Sagittal':
            T1, T2, PD = self.T1[self.nslice,: ,:], self.T2[self.nslice, :, :], self.PD[self.nslice, :, :]
        else:
            T1, T2, PD = self.T1[:, self.nslice, :], self.T2[:, self.nslice,:], self.PD[:, self.nslice,:]

        TE = self.TE
        TI = self.TI
        TR = self.TR
        FA = self.FA
        ETL = self.ETL
        ESP = self.ESP
        tmp = np.zeros_like(T1)

        if self.T1.max() == 0:
            pass
        else:
            for i in range(T1.shape[0]):
                for j in range(T1.shape[1]):
                    if self.clicked.get()== 'SE':
                        tmp[i,j] = PD[i,j]*np.exp(-TE/T2[i,j])*(1-np.exp(-TR/T1[i,j]))*(1-2*np.exp(-TI/T1[i,j]))
                    elif self.clicked.get() == 'FSE':
                        tmp[i, j] = PD[i, j] * np.exp(-TE / T2[i, j]) * (1 - np.exp(-(TR -ETL*ESP) / T1[i, j])) * (
                                    1 - 2 * np.exp(-TI / T1[i, j]))

        return tmp



    def update_slice(self, nothing=None):
        self.nslice = self.slider.get()
        self.update_image()

    def update_TE(self,nothing=None):
        self.TE = self.TEslider.get()
        self.update_image()

    def update_TI(self, nothing=None):
        self.TI = self.TIslider.get()
        self.update_image()

    def update_TR(self, nothing=None):
        self.TR = self.TRslider.get()
        self.update_image()

    def update_FA(self, nothing=None):
        self.FA = self.FAslider.get()
        self.update_image()

    def update_ESP(self, nothing=None):
        self.ESP = self.ESPslider.get()
        self.update_image()

    def update_ETL(self,nothing=None):
        self.ETL = self.ETLslider.get()
        self.update_image()

    def update_seq(self, none=None, cheese='cheese',fry='fry'):
        print(self.clicked.get())
        self.clicked.set(self.clicked.get())
        self.subtitle.destroy()
        self.subtitle = Label(self.frame3, text='Sequence: {}'.format(self.clicked.get()), font=('Helvetica', 24))
        self.subtitle.place(y=100, x=165)

    def update_orientation(self, none=None, cheese='cheese',fry='fry'):
        self.orientation.set(self.orientation.get())
        self.update_image()

    def run(self):
        window = self.window
        window.mainloop()

