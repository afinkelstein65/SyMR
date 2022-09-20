import os.path
import tkinter.filedialog
from tkinter import *
import nibabel as nib
from PIL import ImageTk, Image, ImageOps
import numpy as np
import tkinter.font as tkfont
import matplotlib.pyplot as plt
from matplotlib import cm
#TODO = put in FSE and EPG functions for sequence simulations
#TODO: will need to make executable with pyinstaller.

class GUI(Tk):
    '''General GUI class'''
    def __init__(self, file):
        super().__init__()
        helv20 = tkfont.Font(family='Times', size=25)
        helv16 = tkfont.Font(family='Times', size=18)
        self.color = 'lightgray'

        self.T1, self.T2, self.PD = np.zeros((600,600,400)), np.zeros((600,500,475)), np.zeros((200,200,200))
        self.file = file
        self.window = Toplevel()
        self.window.title('SyMR - Synthetic MR')
        self.window.configure(background=self.color)

        self.window.geometry("1000x1000+10+20")
        self.tmp = np.zeros((200,200))
        # self.window.rowconfigure(2)
        # self.window.columnconfigure(2)

        self.frame1 = self.frame('white', width=1000, height=200)
        self.frame1.grid(row=0,column=0, columnspan=2)
        self.frame1.configure(background=self.color)

        # LOGO
        tmp_img = Image.open("/Users/alanfinkelstein/Documents/PhD/Projects/SyntheticMRIGUI/images/tmp_logo.jpeg")
        tmp_img = tmp_img.resize((100,100))
        self.photo = ImageTk.PhotoImage(tmp_img)
        self.label = Label(self.frame1, image=self.photo)
        self.label.place(y=10,x=875)
        self.ID = Label(self.frame1, text='Created By: Alan Finkelstein\n'
                                          'Department of Biomedical Engineering, University of Rochester')
        self.ID.place(y=5, height=40, width=500, x=50)
        self.ID.configure(font=helv16, background=self.color)


        self.frame2 = self.frame('white', height=800)
        self.frame2.grid(row=1, column=0, rowspan=2, sticky="nswe")
        self.frame2.configure(background=self.color)

        # Image Display
        self.frame3 = self.frame('white', height=800)
        self.frame3.grid(row=1, column=1, rowspan=2, stick="nswe")
        self.frame3.configure(background=self.color)

        self.mapcon = 'Maps'
        self.nslice = 0

        self.slider = Scale(self.frame3, from_=0, to=199, orient='horizontal',
                            command=self.update_slice)
        self.slider.place(y=610, x=50, width=400)
        self.slider.configure(background=self.color)

        self.TE = 0
        self.TElabel = Label(self.frame2,text='TE')
        self.TElabel.place(x=20, y=125, width=50, height=50)
        self.TElabel.configure(background=self.color)
        self.TEslider = Scale(self.frame2, from_=0, to=300, orient = 'horizontal',
                              command=self.update_TE)
        self.TEslider.configure(background=self.color)
        self.TEslider.set(0)
        self.TElabel.config(font=helv20)
        self.TEslider.place(y=125,x=70,width=400, height=50)

        self.TI = 0
        self.TIlabel = Label(self.frame2, text='TI')
        self.TIlabel.place(x=20, y = 200, width=50, height=50)
        self.TIlabel.configure(font=helv20, background=self.color)
        self.TIslider = Scale(self.frame2, from_=0, to=5000, orient='horizontal',
                              command=self.update_TI)
        self.TIslider.place(x=70, y=200, width=400, height=50)
        self.TIslider.configure(background=self.color)

        self.TR = 0
        self.TRlabel = Label(self.frame2, text='TR')
        self.TRlabel.place(x=20, y=275, width=50, height=50)
        self.TRlabel.configure(font=helv20, background =self.color)
        self.TRslider = Scale(self.frame2, from_=0, to=5000, orient= 'horizontal',
                               command=self.update_TR)
        self.TRslider.place(x=70,y=275, width=400,height=50)
        self.TRslider.configure(background=self.color)

        self.FA = 0
        self.FAlabel = Label(self.frame2, text='FA')
        self.FAlabel.place(x=20, y=350, width=50, height=50)
        self.FAlabel.configure(font=helv20, background=self.color)
        self.FAslider = Scale(self.frame2, from_=0, to=180, orient='horizontal',
                              command=self.update_FA)
        self.FAslider.place(x=70, y=350, width=400, height=50)
        self.FAslider.configure(background=self.color)

        self.ESP = 0
        self.ESPlabel = Label(self.frame2, text='ESP')
        self.ESPlabel.place(x=20, y=425, width=50, height=50)
        self.ESPlabel.configure(font=helv20,background=self.color)
        self.ESPslider=Scale(self.frame2, from_=0, to=100, orient='horizontal',
                             command=self.update_ESP)
        self.ESPslider.place(x=70,y=425, width=400, height=50)
        self.ESPslider.configure(background=self.color)

        self.ETL= 0
        self.ETLlabel = Label(self.frame2, text='ETL')
        self.ETLlabel.place(x=20, y=500, width=50, height=50)
        self.ETLlabel.configure(font=helv20, background=self.color)
        self.ETLslider= Scale(self.frame2, from_=0, to=50, orient='horizontal',
                              command=self.update_ETL)
        self.ETLslider.place(x=70, y=500, width=400, height=50)
        self.ETLslider.configure(background=self.color)

        self.T1wBut = Button(self.frame2, text='T1w', command=lambda: self.update_params('T1w'))
        self.T1wBut.place(x=20, y=600)
        self.T1wBut.configure(font=helv20, background=self.color)

        self.T2wBut = Button(self.frame2, text='T2w', command = lambda: self.update_params('T2w'))
        self.T2wBut.place(x=120, y=600)
        self.T2wBut.configure(font=helv20, background=self.color)

        self.PDBut = Button(self.frame2, text='PD', command=lambda: self.update_params('PD'))
        self.PDBut.place(x=220, y=600)
        self.PDBut.configure(font=helv20, background=self.color)

        self.FLAIRBut = Button(self.frame2, text='FLAIR', command=lambda: self.update_params('FLAIR'))
        self.FLAIRBut.place(x=320, y=600)
        self.FLAIRBut.configure(font=helv20, background=self.color)




        # Entry toolbar
        self.subject = Label(self.frame1, text='Subject', relief='raised')
        self.subject.place(height=70, width=100, y=70, x=50)
        self.subject.configure(font=helv20)
        self.entry = Entry(self.frame1,relief='raised')
        self.entry.place(height=70,width=600,x=150, y= 70)

        self.browse = Button(self.frame1, text='Browse', command=self.open_file)
        self.browse.place(height=35, width=100,y=70,x =750)
        self.browse.configure(background=self.color, font=helv20)
        self.submit = Button(self.frame1, text='Submit', command=self.submit)
        self.submit.place(height=35, width=100, y=105,x=750)
        self.submit.configure(font=helv20, background=self.color)

        # self.subject = Entry(self.frame1)

        #Input Parameters

        self.options = ["SE","FSE", "MPRAGE"]
        self.clicked = StringVar()
        self.clicked.set("SE")
        self.seq = OptionMenu(self.frame2, self.clicked, *self.options)
        self.seq.configure(font=helv20, width=31, height=2, background=self.color)
        self.seq.place(x=22, y=50)
        # self.seqname = Label(self.frame2, text='Sequence', relief='raised')
        # self.seqname.place(x=20,y=10, width=100)





        # Image Display
        self.image = ImageTk.PhotoImage(image=Image.fromarray(self.T2[100,:,:]))
        self.label = Label(self.frame3, image=self.image, relief="raised")
        self.label.place(y=100, x =5)


        self.clicked.trace('w',self.update_seq)







        self.orientations = ['Axial','Sagittal','Coronal']
        self.orientation = StringVar()
        self.orientation.set('Axial')
        self.orient = OptionMenu(self.frame2, self.orientation, *self.orientations)
        self.orient.configure(font=helv20,width=31, height=2, background=self.color)
        self.orientation.trace('w',self.update_orientation)
        self.orient.place(x=21, y=5)

        self.T2But = Button(self.frame3, text='T2', command=lambda : self.update_image(choice='T2'),
                            relief=FLAT)
        self.T1But = Button(self.frame3, text='T1', command=lambda: self.update_image(choice='T1'), relief=RAISED)
        self.PDBut = Button(self.frame3, text='PD', command=lambda: self.update_image(choice='PD'), relief=RAISED)

        self.ConsBut = Button(self.frame3, text='Contrasts', command=lambda : self.update_image(choice='Contrasts'))
        self.T1But.place(x=55, y=50)
        self.T1But.configure(font=helv20, background=self.color)
        self.T2But.place(x=140, y=50)
        self.T2But.configure(font=helv20, background=self.color)
        self.PDBut.place(x=220, y=50)
        self.PDBut.configure(font=helv20, background=self.color)
        self.ConsBut.place(x=310, y=50)
        self.ConsBut.configure(font=helv20, background=self.color)





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

    def update_image(self, choice='Contrasts'):
        self.orient = self.orientation.get()
        if choice == 'Contrasts':
            self.mapcon = choice
            self.tmp = self.simulate()
        elif choice == 'T2':
            self.mapcon =choice
            self.tmp = self.T2
            self.tmp[self.tmp>300] = 300
        elif choice == 'T1':
            self.mapcon = choice
            self.tmp = self.T1
        elif choice == 'PD':
            self.mapcon =choice
            self.tmp = self.PD

        if choice != 'Contrasts':
            if self.orient == 'Axial':
                self.tmp = self.tmp[...,self.nslice]
            elif self.orient == 'Sagittal':
                self.tmp = self.tmp[self.nslice, :, :]
            else:
                self.tmp = self.tmp[:,self.nslice,:]



        if self.tmp.max() == 0:
            pass
        else:
            if choice == 'Contrasts':
                self.tmp = 255 * self.tmp/ self.tmp.max()
            elif choice == 'PD':
                self.tmp = (255 * cm.hot(self.tmp / self.tmp.max())).astype(np.uint8)
            else:
                self.tmp = (255*cm.jet(self.tmp/self.tmp.max())).astype(np.uint8)


            if self.orient == 'Axial':
                tmp_img =Image.fromarray(np.flipud(np.rot90(self.tmp)))
            else:
                tmp_img = Image.fromarray(np.fliplr(np.rot90(self.tmp)))
            tmp_img = tmp_img.resize((475, 500))

            self.image = ImageTk.PhotoImage(image=tmp_img)
            self.label = Label(self.frame3, image=self.image, relief='raised')
            self.label.place(y=100, x=5)

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
        self.update_image(choice=self.mapcon)

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

    def update_params(self,seq='T1w',nothing=None):
        if seq == 'T1w':
            self.TE = 15
            self.TR = 390
            self.TI = 5000
        elif seq == 'T2w':
            self.TE = 100
            self.TR = 4800
            self.TI = 5000
        elif seq == 'FLAIR':
            self.TE = 120
            self.TR = 120
            self.TI = 1500
        elif seq == 'PD':
            self.TE = 14
            self.TR = 4500
            self.TI = 5000


        self.TEslider.set(self.TE)
        self.TRslider.set(self.TR)
        self.TIslider.set(self.TI)

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

