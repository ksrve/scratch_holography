
import os

try:
	from Tkinter import *	# Python 2.X
except ImportError:
	from tkinter import *	# Python 3.X
try:
	from 		tkColorChooser import askcolor
except ImportError:
	from		tkinter.colorchooser import askcolor
try:
	import 	tkFileDialog as FileDialog
except ImportError:
	import	tkinter.filedialog as FileDialog
try:
	import 	tkMessageBox as MessageBox
except ImportError:
	import	tkinter.messagebox as MessageBox
try:
	import 	ttk
	from 		ttk import *
except ImportError:
	from		tkinter import ttk
	from 		tkinter.ttk import *

try:
	import 	tkFont
except ImportError:
	import	tkinter.font

# sudo apt-get install python3-pil.imagetk
import PIL
from PIL import Image, ExifTags
try:
	from PIL import ImageTk
except ImportError:
	raise ("ImageTk not installed. If running Python 3.x\n" \
			 "Use: sudo apt-get install python3-pil.imagetk")

from ImageChooser import *
from ImagePreparator import *

## SETTINGS
ROOT_DIR = os.path.abspath("../")
IMAGE_DIR = os.path.join(ROOT_DIR, "assets/")

ITMO_LOGO_PATH  = os.path.join(IMAGE_DIR, "itmo_logo_white_rus.png")
ROTATE_SIGN_PATH = os.path.join(IMAGE_DIR, "rotate.png")

choosed_photo_path = ''


SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0

class CNCApp (Frame):

	def __init__(self, root):
		Frame.__init__(self, root)
		self.root = root
		self.root.title("CNC Image Converter")

		master = root

		# Left pane with all control pages
		pw_left = PanedWindow(master,orient=VERTICAL,takefocus=True)
		pw_left.grid(row=0,column=0,sticky="NSEW")
		pw_left.rowconfigure(2,weight=1)
		pw_left.columnconfigure(0,weight=1)


		LeftTopFrame = Frame(pw_left)
		LeftTopFrame.grid(row=0,column=0,sticky="NSEW", padx = 22, pady = 22)
		LeftTopFrame.rowconfigure(4,weight=1)
		LeftTopFrame.columnconfigure(4,weight=1)
		# Logo picture
		img = Image.open(ITMO_LOGO_PATH).resize((500, 255))
		itmoLogo = ImageTk.PhotoImage(img)
		labelLogo = Label(LeftTopFrame,image=itmoLogo)
		labelLogo.image = itmoLogo
		labelLogo.grid(row=0,column=0, padx = 10, pady = 5)
		# Title
		label = Label(LeftTopFrame,text="Преобразователь растровых изображений", font=("Calibri", 16))
		label.grid(row=1, column=0, padx = 10,pady = 5)


		#------------ Notebook with all control pages -----------
		n = Notebook(pw_left,padding=(5,5,5,5))
		n.grid(row=1,column=0,rowspan=2,sticky=(N,E,W,S), padx = 10, pady = 20)
		n.columnconfigure(0,weight=1)
		n.enable_traversal()

		# Control window
		LeftBottomFrame = Frame(n)
		LeftBottomFrame.grid(row=0,column=0,sticky="NSEW", padx = 20, pady = 20)
		LeftBottomFrame.rowconfigure(4,weight=1)
		LeftBottomFrame.columnconfigure(4,weight=1)

		# Control window
		CNCParamsFrame = Frame(n)
		LeftBottomFrame.grid(row=0,column=0,sticky="NSEW", padx = 20, pady = 20)
		LeftBottomFrame.rowconfigure(4,weight=1)
		LeftBottomFrame.columnconfigure(4,weight=1)

		#========================
		frame_choose = LabelFrame(LeftBottomFrame, text='Выбор и обработка изображения',padding=(5,5,5,5))
		frame_choose.grid(row=0,column=0,columnspan=2,sticky='NSEW',padx = 10, pady=20)
		# ВЫБОР ФАЙЛА
		label_choose = Label(frame_choose,text="Выберите изображение", font=("Calibri", 10))
		label_choose.grid(row=0,column=0,sticky='W',padx = 20, pady = 10)
		btn_choose = Button(frame_choose,command=self.import_image)
		btn_choose.grid(row=0,column=1, sticky='W', padx = 20, pady = 10)
		label_choose_1 = Label(frame_choose,text="Форматы: *.png, *.jpg, *.bmp", font=("Calibri", 8))
		label_choose_1.grid(row=0,column=2,sticky='W',padx = 20, pady = 10)

		# СКЕЛЕТИРОВАНИЕ
		label_skel = Label(frame_choose,text="Обработать изображение", font=("Calibri", 10))
		label_skel.grid(row=1,column=0,sticky='W',padx = 20, pady = 10)
		btn_skel = Button(frame_choose, command=self.processtheimage)
		btn_skel.grid(row=1,column=1, sticky='W', padx = 20, pady = 10)

		#========================
		params_choose = LabelFrame(LeftBottomFrame, text="Выбор параметров",padding=(5,5,5,5))
		params_choose.grid(row=2,column=0,columnspan=2,sticky='NSEW',padx = 10, pady=20)
		# ШАГ КОНУТРА
		label_step = Label(params_choose,text="Шаг контура", font=("Calibri", 10))
		label_step.grid(row=2,column=1,sticky='W', padx = 20, pady = 10)
		# TODO change from/to
		self.ch_step_var = IntVar()
		ch_step = Scale(params_choose,from_=1,to=30,orient='horizontal',length=200, command=self.stepScale)
		ch_step.grid(row=2,column=2,sticky='E', padx = 5)
		ch_step.set(255)
		self.label_stepscale = Label(params_choose,text=0, textvariable=self.ch_step_var,font=("Calibri", 10))
		self.label_stepscale.grid(row=2,column=3,sticky='W')
		# РАДИУС ОКРУЖНОСТИ
		label_rad = Label(params_choose,text="Радиус окужности", font=("Calibri", 10))
		label_rad.grid(row=3,column=1,sticky='W', padx = 20, pady = 10)
		# TODO change from/to
		self.ch_rad_var = IntVar()
		ch_rad = Scale(params_choose,from_=1,to=100,orient='horizontal',length=200,command=self.radScale)
		ch_rad.grid(row=3,column=2,sticky='E', padx = 5)
		ch_rad.set(255)
		self.label_ch_rad = Label(params_choose,text=0, textvariable=self.ch_rad_var,font=("Calibri", 10))
		self.label_ch_rad.grid(row=3,column=3,sticky='W')
		##
		label_proc = Label(params_choose,text="Обработать изображение", font=("Calibri", 10))
		label_proc.grid(row=4,column=1,sticky='W',padx = 20, pady = 10)
		btn_proc = Button(params_choose, command= lambda: self.circleprocess(self.ch_step_var,self.ch_rad_var))
		btn_proc.grid(row=4,column=2, sticky='W', padx = 20, pady = 10)

		n.add(LeftBottomFrame ,text='Базовые настройки обработки',underline=0)
		n.add(CNCParamsFrame ,text='Настройка параметров ЧПУ',underline=0)


		menu = Menu(master)
		new_item = Menu(menu)
		new_item.add_command(label='Новый')
		menu.add_cascade(label='Файл', menu=new_item)
		menu.add_cascade(label='Справка', menu=new_item)
		menu.add_cascade(label='Выйти', menu=new_item)
		root.config(menu=menu)


	def createright(self, image):
		print("Here")
		master = self.root

		pw_right = PanedWindow(master,orient=VERTICAL,style='TPanedwindow',takefocus=True)
		pw_right.grid(row=0,column=1,sticky="NSEW")
		pw_right.rowconfigure(3,weight=1)
		pw_right.columnconfigure(0,weight=1)

		# +/- размер изображения,
		RightTopFrame = Frame(pw_right)
		RightTopFrame.grid(row=0,column=0,sticky="NSEW", padx = 20, pady = 20)
		RightTopFrame.rowconfigure(0,weight=1)
		RightTopFrame.columnconfigure(4,weight=1)

		change_choose = Frame(RightTopFrame,relief=GROOVE)
		change_choose.grid(row=0,column=0,columnspan=4,sticky='NSEW', padx = 5, pady = 5)
		# Уменьшение/увеличение
		label_sz = Label(change_choose,text="Размер изображения")
		label_sz.grid(row=0,column=1,sticky='W',padx = 20, pady = 5)
		self.ch_size_var = IntVar()
		ch_size = Scale(change_choose,from_=1,to=30,orient='horizontal',length=100, command=self.sizeScale)
		ch_size.grid(row=0,column=2,sticky='W',padx = 5)
		ch_size.set(255)
		self.label_size = Label(change_choose,text=0, textvariable=self.ch_size_var)
		self.label_size.grid(row=0,column=3,sticky='W')

		self.var_view = BooleanVar()
		cb_view = Checkbutton(change_choose, text="Показать изображение", variable=self.var_view, command=self.viewClick)
		cb_view.grid(row=0,column=4,sticky='W',padx = 20)

		RightMiddleFrame = Frame(pw_right,relief=GROOVE)
		RightMiddleFrame.grid(row=1,column=0,sticky="NSEW", padx = 20, pady = 20)
		RightMiddleFrame.rowconfigure(0,weight=1)
		RightMiddleFrame.columnconfigure(0,weight=1)



		#img = Image.open(choosed_photo_path).resize((500, 255))
		img = PIL.Image.fromarray(image)
		img = img.resize((400, 400), PIL.Image.ANTIALIAS)
		openedimg = PIL.ImageTk.PhotoImage(image=img)
		labelimg = Label(RightMiddleFrame,image=openedimg)
		labelimg.image = openedimg
		labelimg.grid(row=0,column=0, padx = 10, pady = 10)




	def stepScale(self, val):
		v = int(float(val))
		self.ch_step_var.set(v)

	def radScale(self, val):
		v = int(float(val))
		self.ch_rad_var.set(v)

	def sizeScale(self, val):
		v = int(float(val))
		self.ch_size_var.set(v)

	def viewClick(self):
		if self.var_view.get() == True:
			print("ok")
		else:
			print("")

	def import_image(self):
		global choosed_photo_path
		master = self.root
		file_name = FileDialog.askopenfilename(
		parent=master,
		initialdir=ROOT_DIR,
		title='Выберите файл',
		filetypes=[('png images', '*.png'),
					   ('jpeg images', '*.jpg'),
					   ('bitmap images', '*.bmp')]
			)
		choosed_photo_path = file_name
		print(choosed_photo_path)

	def processtheimage(self):
		global choosed_photo_path
		image = process_image(choosed_photo_path, 0, 0)
		self.createright(image)

	def circleprocess(self,step,rad):
		global choosed_photo_path
		print(step.get(), rad.get())
		image = process_image(choosed_photo_path, step.get(), rad.get())
		self.createright(image)



def run():
	global SCREEN_WIDTH, SCREEN_HEIGHT
	try:
		root = Tk()
	except:
		print ( "Error initializing Tkinter!\n\nShutting down\n\nPress any key" )
		return

	SCREEN_WIDTH = root.winfo_screenwidth() # ширина экрана
	SCREEN_HEIGHT = root.winfo_screenheight() # высота экрана
	w = SCREEN_WIDTH // 2
	h = SCREEN_HEIGHT // 2
	w = w - 250
	h = h - 300
	print(SCREEN_WIDTH)
	print(SCREEN_HEIGHT)
	#root.geometry('{0}x{1}+0+0'.format(SCREEN_WIDTH, SCREEN_HEIGHT))
	root.resizable(width=True, height=True)
	#root.geometry('{0}x{1}+0+0'.format(w, h))
	root.geometry('1200x900')
	#root.resizable(width=False, height=False)
	app = CNCApp(root)
	root.mainloop()


if __name__ == '__main__':
	print ( 'running....' )
	run()
