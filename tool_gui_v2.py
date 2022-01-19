import tkinter as tk
import glob
import matplotlib.pyplot as plt
import json
from PIL import Image
import os
import argparse
from tkinter import *
# import tkMessageBox
from PIL import ImageTk,Image
from tkinter.messagebox import showinfo

idx=0
ls_img = []
ls_json= []

parser = argparse.ArgumentParser(description='Labeling tool for license plate OCR')
parser.add_argument('--dataset', type=str, required=True,
                        help='Path of dataset')
args = parser.parse_args()
for img_name in os.listdir(args.dataset):
	label_fn = os.path.join(args.dataset, img_name.rsplit(".")[0] + '.json')
	if os.path.exists(label_fn):
		continue
	ls_json.append(label_fn)
	ls_img.append(os.path.join(args.dataset, img_name))

def show_selected_size(msg):
    showinfo(
        title='Result',
        message=msg
    )
def chooseImage():
	global idx,image_idm,canvas1,current_path
	label = entry1.get()
	if len(label):
		try:
			idx = int(label)
			if idx==len(ls_img):
				show_selected_size("Job Done! Thank you !!!")
				return
			current_path.set("Current Path: {}                      ID: {}".format(ls_img[idx],idx))
			img0 = Image.open(ls_img[idx])
			w,h= img0.size
			side_max = max(w,h)
			side_min = min(w,h)
			if (side_max>640):
				side_max_1 = 640
				side_min_1 = int((640*side_min)/side_max)
				if side_min==h:
					img0 = img0.resize((side_max_1,side_min_1))
				else:
					img0 = img0.resize((side_min_1,side_max_1))
			elif (side_max<300):
				side_max_1 = 300
				side_min_1 = int((300*side_min)/side_max)
				if side_min==h:
					img0 = img0.resize((side_max_1,side_min_1))
				else:
					img0 = img0.resize((side_min_1,side_max_1))
			img_ = ImageTk.PhotoImage(img0)
			canvas1.img= img_
			canvas1.itemconfig(image_id, image=img_)
		except:
			show_selected_size("Your input must be integer")
	entry1.delete(0, "end")

def prevImage(event=None):
	global idx, image_id, canvas1, v_expression,v_gender,v_occlusion,current_path
	idx-=1
	if idx<0:
		show_selected_size("Can't back")
		return
	current_path.set("Current Path: {}                      ID: {}".format(ls_img[idx],idx))
	v_expression.set("0")
	v_gender.set("0")
	v_occlusion.set("0")
	img0 = Image.open(ls_img[idx])
	w,h= img0.size
	side_max = max(w,h)
	side_min = min(w,h)
	if (side_max>640):
		side_max_1 = 640
		side_min_1 = int((640*side_min)/side_max)
		if side_min==h:
			img0 = img0.resize((side_max_1,side_min_1))
		else:
			img0 = img0.resize((side_min_1,side_max_1))
	elif (side_max<300):
		side_max_1 = 300
		side_min_1 = int((300*side_min)/side_max)
		if side_min==h:
			img0 = img0.resize((side_max_1,side_min_1))
		else:
			img0 = img0.resize((side_min_1,side_max_1))
	img_ = ImageTk.PhotoImage(img0)
	canvas1.img= img_
	canvas1.itemconfig(image_id, image=img_)

def nextImage(event=None):
	global idx, image_id, canvas1,expression_label,gender_label,occlusion_label,v_expression,v_gender,v_occlusion,current_path
	if len(expression_label):
		with open(ls_json[idx], 'w',encoding='utf-8') as f:
			res = {"expression": expression_label,"gender":gender_label,"occlusion":occlusion_label,"path": ls_img[idx]}
			json.dump(res, f, ensure_ascii=False)
	idx+=1
	if idx==len(ls_img):
		show_selected_size("Job Done! Thank you !!!")
		return
	current_path.set("Current Path: {}                      ID: {}".format(ls_img[idx],idx))
	v_expression.set("0")
	v_gender.set("0")
	v_occlusion.set("0")
	img0 = Image.open(ls_img[idx])
	w,h= img0.size
	side_max = max(w,h)
	side_min = min(w,h)
	if (side_max>320):
		side_max_1 = 320
		side_min_1 = int((320*side_min)/side_max)
		if side_min==h:
			img0 = img0.resize((side_max_1,side_min_1))
		else:
			img0 = img0.resize((side_min_1,side_max_1))
	elif (side_max<300):
		side_max_1 = 300
		side_min_1 = int((300*side_min)/side_max)
		if side_min==h:
			img0 = img0.resize((side_max_1,side_min_1))
		else:
			img0 = img0.resize((side_min_1,side_max_1))
	
	img_ = ImageTk.PhotoImage(img0)
	canvas1.img= img_
	canvas1.itemconfig(image_id, image=img_)

root= tk.Tk()
root.geometry("1000x700")
label1 = tk.Label(root, text='Emotion LABEL TOOL ')
label1.config(font=('helvetica', 14))
label1.pack(ipady=20)
frame1 = Frame(root)
frame1.pack()
canvas1 = tk.Canvas(frame1, width = 320, height = 320,  relief = 'raised')
canvas1.pack(padx=5,pady=5)
img0= Image.open(ls_img[idx])
w,h= img0.size
side_max = max(w,h)
side_min = min(w,h)
if (side_max>320):
	side_max_1 = 320
	side_min_1 = int((320*side_min)/side_max)
	if side_min==h:
		img0 = img0.resize((side_max_1,side_min_1))
	else:
		img0 = img0.resize((side_min_1,side_max_1))
elif (side_max<300):
	side_max_1 = 300
	side_min_1 = int((300*side_min)/side_max)
	if side_min==h:
		img0 = img0.resize((side_max_1,side_min_1))
	else:
		img0 = img0.resize((side_min_1,side_max_1))

img = ImageTk.PhotoImage(img0)
image_id =canvas1.create_image(160,160, anchor='center', image=img)
expression_label = ""
gender_label = ""
occlusion_label = ""
frame2 = Frame(root)
frame2.pack()
canvas2 = tk.Canvas(frame2, width = 700, height = 300,  relief = 'raised')
canvas2.pack()
def clicked():
	global expression_label,gender_label,occlusion_label
	expression_label = v_expression.get()
	gender_label = v_gender.get()
	occlusion_label = v_occlusion.get()

v_expression = StringVar(canvas2, "0")
v_gender = StringVar(canvas2, "0")
v_occlusion = StringVar(canvas2, "0")

#expression_values = ['Uncertain', 'None', 'Happy','Contempt','Surprised','Sadness','Disgusted','Fear','Angry','Neutral']
expression_values = ['Uncertain', 'None', 'Positive','Surprised','Negative','Neutral']
icon_size = (40,40)
icon_photos = {
	'Uncertain': ImageTk.PhotoImage(Image.open("./emotion_icon/uncertain.png").resize(icon_size)),
	'None': ImageTk.PhotoImage(Image.open("./emotion_icon/none.png").resize(icon_size)),
	'Positive': ImageTk.PhotoImage(Image.open("./emotion_icon/happy.jpg").resize(icon_size)),
	#'Contempt': ImageTk.PhotoImage(Image.open("./emotion_icon/contempt.jpg").resize(icon_size)),
	'Surprised': ImageTk.PhotoImage(Image.open("./emotion_icon/surprise.png").resize(icon_size)),
	#'Sadness': ImageTk.PhotoImage(Image.open("./emotion_icon/sad.jpg").resize(icon_size)),
	#'Disgusted': ImageTk.PhotoImage(Image.open("./emotion_icon/disgust.jpg").resize(icon_size)),
	#'Fear': ImageTk.PhotoImage(Image.open("./emotion_icon/fear.jpg").resize(icon_size)),
	'Negative': ImageTk.PhotoImage(Image.open("./emotion_icon/angry.jpg").resize(icon_size)),
	'Neutral': ImageTk.PhotoImage(Image.open("./emotion_icon/neutral.png").resize(icon_size))
}
gender_values = ['Male', 'Female']
#Occlusion_values = ['None','Watermarks','Other']


for i in range(len(expression_values)):
	lab = Label(canvas2,image=icon_photos[expression_values[i]])
	lab.image = icon_photos[expression_values[i]]
	lab.grid(row=0,column=i,sticky=N)

for i in range(len(expression_values)):
	rdbtn = Radiobutton(canvas2,text=expression_values[i],variable=v_expression,value = expression_values[i],font="Arial",fg='green',height=2,command = clicked)
	#rdbtn.config(image=icon_photos[expression_values[i]])
	rdbtn.grid(row=1,column=i,sticky=W)

for i in range(len(gender_values)):
	rdbtn = Radiobutton(canvas2,text=gender_values[i], variable=v_gender,value = gender_values[i],font="Arial",fg='green',height=2,command = clicked)
	rdbtn.grid(row=2,column=i,sticky=W)

# for i in range(len(Occlusion_values)):
# 	rdbtn = Radiobutton(canvas2,text=Occlusion_values[i], variable=v_occlusion,value = Occlusion_values[i],font="Arial",fg='green',height=2,command = clicked)
# 	rdbtn.grid(row=3,column=i,sticky=W)


#root.bind('<Return>', nextImage)
root.bind('<Left>', prevImage)
root.bind('<Right>',nextImage)
select_number = Label(root,text="Image number")
select_number.pack(side=LEFT,ipadx = 10,ipady=5,padx=5)
entry1 = tk.Entry(root, width=30)
entry1.pack(side=LEFT,ipadx = 10,ipady=5,padx=5)
current_path = StringVar()
current_path.set("Current Path: {}                      ID: {}".format(ls_img[idx],idx))
#current_path = Label(root,text=current_path,font=("Arial",10,'bold'))
image_current_path = Label(root,textvariable = current_path,font=("Arial",10,'bold'))
image_current_path.place(anchor=NW)
button1 = tk.Button(root,text="Go", command=chooseImage, bg='brown', fg='white', font=('helvetica', 9, 'bold'),width=5)
button2 = tk.Button(root,text='Next', command=nextImage, bg='brown', fg='white', font=('helvetica', 9, 'bold'),width=5)
button3 = tk.Button(root,text='Prev', command=prevImage, bg='brown', fg='white', font=('helvetica', 9, 'bold'),width=5)
button1.pack(side=LEFT,ipadx = 10,ipady=5,padx=5)
button2.pack(side = RIGHT,ipadx = 10, padx = 25)
button3.pack(side = RIGHT,ipadx = 10, padx = 25)

root.mainloop()
