#!/usr/bin/env python3
# imports

from tkinter import *
import tkinter.messagebox
import os
from PIL import ImageTk,Image
from tkinter import ttk  
import time
from tkinter.messagebox import _show 

# voice: https://ttsmp3.com/




## Main screen
master = Tk()
master.title('Banking app')
master.resizable(0,0)
## icon for ubuntu
photo = PhotoImage(file = "images/icon.png")
master.iconphoto(False, photo)

## Functions
def finish_reg():
	name = temp_name.get()
	age = temp_age.get()
	gender = temp_gender.get()
	password = temp_password.get()
	pin = temp_pin.get()

	all_accounts = os.listdir()


	if name == "" or age == "" or gender == "" or password == "" or pin == "":
		notif.config(fg="red", text = "All fields are required *")
		return
	for name_check in all_accounts:
		if name == name_check:
			notif.config(fg="red",text="Account already exists")
			return
		else:
			new_file =open(name,'w')
			new_file.write(name+'\n')
			new_file.write(password+'\n')
			new_file.write(age+'\n')
			new_file.write(gender+'\n')
			new_file.write('0'+'\n')
			new_file.write(pin)

			new_file.close()

			notif.config(fg="green", text="Account is created successfully")
			

			





def register():
	# Vars
	global temp_name
	global temp_age
	global temp_gender
	global temp_password
	global temp_pin
	global notif
	global register_screen
	temp_name = StringVar()
	temp_age = StringVar()
	temp_gender = StringVar()
	temp_password = StringVar()
	temp_pin = StringVar()


	#Register Screen
	register_screen = Toplevel(master)
	register_screen.title("Register")
	register_screen.resizable(0,0)


	# Label
	Label(register_screen, text = "Please enter your details to register" , font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
	
	Label(register_screen, text = "Name" , font=('Calibri',9)).grid(row=1,sticky=W)
	Label(register_screen, text = "Age" , font=('Calibri',9)).grid(row=2,sticky=W)
	Label(register_screen, text = "Gender" , font=('Calibri',9)).grid(row=3,sticky=W)
	Label(register_screen, text = "Password" , font=('Calibri',9)).grid(row=4,sticky=W)
	Label(register_screen, text = "Secret Pin" , font=('Calibri',9)).grid(row=5,sticky=W)

	notif = Label(register_screen, font=('Calibri',9))
	notif.grid(row=8,sticky=N,pady=10)


	## Entries

	Entry(register_screen,textvariable=temp_name).grid(row=1,column=0)
	Entry(register_screen,textvariable=temp_age).grid(row=2,column=0)
	Entry(register_screen,textvariable=temp_gender).grid(row=3,column=0)
	Entry(register_screen,textvariable=temp_password,show="*").grid(row=4,column=0)
	Entry(register_screen,textvariable=temp_pin).grid(row=5,column=0)
	# Button
	btn = Button(register_screen,text="Register",command=finish_reg,font=('Calibri',12))
	btn.grid(row=7,sticky=N,pady=10)
	

def login_session():
	#Vars
	global login_name
	global password
	global mid
	all_accounts = os.listdir()
	login_name = temp_login_name.get()
	login_password = temp_login_password.get()

	for name in all_accounts:
		if name == login_name:
			file = open(name,"r")
			file_data = file.read()
			file_data = file_data.split('\n')
			password = file_data[1]

			#Account Dashboard
			if login_password == password:
				login_screen.destroy()
				account_dashboard = Toplevel(master)
				account_dashboard.title('Dashboard')
				account_dashboard.resizable(0,0)
				#Label
				Label(account_dashboard,text='Account Dashboard',font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
				Label(account_dashboard,text='Welcome '+name,font=('Calibri',12)).grid(row=1,sticky=N,pady=5)
				#Buttons
				Button(account_dashboard, text='Personal Details', command=personal_details,width=30, font=('Calibri',12)).grid(row=2,sticky=N,padx=10)

				Button(account_dashboard,text='Deposit',font=('Calibri',12),width=30,command=deposit).grid(row=3,sticky=N,padx=10)
				Button(account_dashboard,text='Withdraw',font=('Calibri',12),width=30,command=withdraw).grid(row=4,sticky=N,padx=10)
				Label(account_dashboard).grid(row=5,sticky=N,pady=10)
				return
			else:
				login_notif.config(fg='red',text="Invalid details")
				return
	login_notif.config(fg='red', text='Account not found')

def deposit():
	#Vars
	global amount
	global deposit_notif
	global current_balance_label

	amount = StringVar()
	file = open(login_name , 'r')
	file_data = file.read()
	user_details = file_data.split('\n')
	details_balance = user_details[4]

	#Deposit Screen
	deposit_screen = Toplevel(master)
	deposit_screen.title('Deposit')

	#Label
	Label(deposit_screen, text='Deposit', font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
	current_balance_label = Label(deposit_screen, text='Current Balance: ₹'+details_balance, font=('Calibri',12))
	current_balance_label.grid(row=1,sticky=W)

	Label(deposit_screen, text='Amount: ', font=('Calibri',12)).grid(row=2,sticky=W)
	deposit_notif = Label(deposit_screen,font = ('Calibri',12))
	deposit_notif.grid(row=4, sticky=N,pady=5)

	#Entry
	Entry(deposit_screen, textvariable=amount).grid(row=2,column=1)
	#Button
	Button(deposit_screen,text="Finish",font=('Calibri',12),command=finish_deposit).grid(row=3,sticky=W,pady=5)



def finish_deposit():
	if amount.get() == '':
		deposit_notif.config(fg='red',text='Amount required')
		return
	if float(amount.get()) <=0:
		deposit_notif.config(fg='red',text='Invalid amount')
		return
	file = open(login_name,'r+')
	file_data = file.read()
	details = file_data.split('\n')
	current_balance = details[4]
	updated_balance = current_balance
	updated_balance = float(updated_balance) + float(amount.get())
	file_data       = file_data.replace(current_balance,str(updated_balance))
	file.seek(0) # empty the previous file
	file.truncate(0) # start from 0
	file.write(file_data)

	current_balance_label.config(fg = "green",text="Current Balance: ₹"+str(updated_balance))
	deposit_notif.config(fg='green',text='Amount is Deposited')



		
def withdraw():
	#Vars
	global withdraw_amount
	global withdraw_notif
	global current_balance_label

	withdraw_amount = StringVar()
	file = open(login_name , 'r')
	file_data = file.read()
	user_details = file_data.split('\n')
	details_balance = user_details[4]

	#Deposit Screen
	withdraw_screen = Toplevel(master)
	withdraw_screen.title('Withdraw')

	#Label
	Label(withdraw_screen, text='Withdraw', font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
	current_balance_label = Label(withdraw_screen, text='Current Balance: ₹'+details_balance, font=('Calibri',12))
	current_balance_label.grid(row=1,sticky=W)

	Label(withdraw_screen, text='Amount: ', font=('Calibri',12)).grid(row=2,sticky=W)
	withdraw_notif = Label(withdraw_screen,font = ('Calibri',12))
	withdraw_notif.grid(row=4, sticky=N,pady=5)

	#Entry
	Entry(withdraw_screen, textvariable=withdraw_amount).grid(row=2,column=1)
	#Button
	Button(withdraw_screen,text="Finish",font=('Calibri',12),command=finish_withdraw).grid(row=3,sticky=W,pady=5)


def finish_withdraw():
	if withdraw_amount.get() == '':
		withdraw_notif.config(fg='red',text='Amount required')
		return
	if float(withdraw_amount.get()) <=0:
		withdraw_notif.config(fg='red',text='Invalid amount')
		return
	file = open(login_name,'r+')
	file_data = file.read()
	details = file_data.split('\n')
	current_balance = details[4]

	if float(withdraw_amount.get()) > float(current_balance):
		withdraw_notif.config(fg="red", text="Insufficient Funds!!")
		return


	updated_balance = current_balance
	updated_balance = float(updated_balance) - float(withdraw_amount.get())
	file_data       = file_data.replace(current_balance,str(updated_balance))
	file.seek(0) # empty the previous file
	file.truncate(0) # start from 0
	file.write(file_data)

	current_balance_label.config(fg = "green",text="Current Balance: ₹"+str(updated_balance))
	withdraw_notif.config(fg='green',text='Amount is withdrawn')

def personal_details():
	global details_password
	#Vars
	file = open(login_name,"r")
	file_data = file.read()
	user_details = file_data.split('\n')
	



	details_name = user_details[0]
	details_age = user_details[2]
	details_gender = user_details[3]
	details_password = user_details[1]
	details_balance = user_details[4]



	#Personal details screen
	personal_details_screen = Toplevel(master)

	personal_details_screen.title('Personal Details')
	personal_details_screen.geometry('300x200')
	personal_details_screen.resizable(0,0)
	Label(personal_details_screen,text='Personal details',font=('Calibri',12)).grid(row=0,sticky=W,pady=10)
	Label(personal_details_screen,text='Name: '+details_name,font=('Calibri',12)).grid(row=1,sticky=W)
	Label(personal_details_screen,text='Age: '+details_age,font=('Calibri',12)).grid(row=2,sticky=W)
	Label(personal_details_screen,text='Gender: '+details_gender,font=('Calibri',12)).grid(row=3,sticky=W)
	Label(personal_details_screen,text='Password: '+details_password,font=('Calibri',12)).grid(row=4,sticky=W)
	Label(personal_details_screen,text='Balance: ₹'+details_balance,font=('Calibri',12)).grid(row=5,sticky=W)


def login():
	#Vars
	global temp_login_name
	global temp_login_password
	global login_notif
	global login_screen

	temp_login_name = StringVar()
	temp_login_password = StringVar()


	#Login Screen
	login_screen = Toplevel(master)
	login_screen.title('Login')
	login_screen.resizable(0,0)

	#Labels
	Label(login_screen, text="Login to your account", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
	Label(login_screen, text="Username", font=('Calibri',12)).grid(row=2,sticky=W)

	Label(login_screen, text="Password", font=('Calibri',12)).grid(row=3,sticky=W)
	login_notif = Label(login_screen, font = ('Calibri',12))
	login_notif.grid(row=6,sticky=N)
	#Entries
	
	Entry(login_screen,textvariable=temp_login_name).grid(row=2,column=1,padx=5)
	Entry(login_screen,textvariable=temp_login_password,show="*").grid(row=3,column=1,padx=5)

	# Buttons
	Button(login_screen, text='Login', command=login_session,width=15, font=('Calibri',12)).grid(row=4,sticky=W,pady=5,padx=5)
	Button(login_screen, text='Forgot Password', command=Forgot,width=15, font=('Calibri',12)).grid(row=5,sticky=W,pady=5,padx=5)


def Forgot():
	## Vars
	global new_username
	global Forgot_notif
	global new_pin
	new_username = StringVar()
	new_pin = StringVar()


	# forgot screen
	Forgot_screen = Toplevel(master)
	Forgot_screen.title('Forgot password')
	Forgot_notif = Label(Forgot_screen,font = ('Calibri',12))
	Forgot_notif.grid(row=4, sticky=N,pady=5)

	# Label
	Label(Forgot_screen, text="Both fields required", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)

	Label(Forgot_screen, text="Enter your Username", font=('Calibri',12)).grid(row=1,sticky=W)
	Label(Forgot_screen, text="Enter the Secret pin", font=('Calibri',12)).grid(row=2,sticky=W)

	# Entry
	Entry(Forgot_screen,textvariable=new_username).grid(row=1,column=1,padx=5)
	Entry(Forgot_screen,textvariable=new_pin).grid(row=2,column=1,padx=5)


	#Button
	Button(Forgot_screen, text='Find', command=passwd,width=15, font=('Calibri',12)).grid(row=3,sticky=W,pady=5,padx=5)
	Label(Forgot_screen).grid(row=5,sticky=N,pady=10)



def passwd():

	##Vars
	name = new_username.get()
	pin = new_pin.get()

	all_accounts = os.listdir()
	for j in all_accounts:
		if j == name:


			file = open(name,'r')
			file_data = file.read()
			user_details = file_data.split('\n')
			pin2 = user_details[5]


	for i in all_accounts:
		if i == name and pin == pin2:
			file = open(name,'r')
			file_data = file.read()
			user_details = file_data.split('\n')
			pas = user_details[1]
			Forgot_notif.config(fg='green',text='Your password is: '+pas)
			
		elif i == "" or pin == "":
			Forgot_notif.config(fg='red',text='Invalid username or pin')
		else:
			pass


def acc():
	## Vars
	global name_del
	global del_pin
	global delnote
	global paso
	global captcha
	name_del = StringVar()
	del_pin = StringVar()
	paso = StringVar()
	captcha = StringVar()



	del_screen = Toplevel(master)
	del_screen.title("Delete your account")

	##Label
	Label(del_screen, text="All fields required", font=('Calibri',12)).grid(row=0,sticky=W)
	Label(del_screen, text="Enter the name", font=('Calibri',12)).grid(row=1,sticky=W)

	Label(del_screen, text="Enter the Secret pin", font=('Calibri',12)).grid(row=2,sticky=W,pady=10)
	Label(del_screen, text="Enter the password", font=('Calibri',12)).grid(row=3,sticky=W,pady=10)
	Label(del_screen, text="Enter the captcha", font=('Calibri',12)).grid(row=4,sticky=W,pady=10)



	delnote = Label(del_screen, font=('Calibri',12))
	delnote.grid(row=6,sticky=N,pady=10)

	##Entry
	Entry(del_screen,textvariable=name_del).grid(row=1,column=1,padx=5)
	Entry(del_screen,textvariable=del_pin).grid(row=2,column=1,padx=5)
	Entry(del_screen,textvariable=paso,show="*").grid(row=3,column=1,padx=5)

	





	## Button
	Button(del_screen, text='Delete', command=delete,width=15, font=('Calibri',12)).grid(row=4,sticky=N,pady=10)


def delete():
	usr = name_del.get()
	pin3 = del_pin.get()
	pasd = paso.get()

	account_details = os.listdir()
	

	for k in account_details:
		if k == usr:


			file = open(usr,'r')
			file_data = file.read()
			user_details = file_data.split('\n')
			pin4 = user_details[5]
			pasw = user_details[1]
			file.close()
		else:
			pass

	for q in account_details:
		if q == usr and pin3 == pin4 and pasd == pasw:
			delnote.config(fg='red',text='')
			box = tkinter.messagebox.askquestion("Warning","Are you sure, do you want to delete?")
			if box == "yes":
				os.remove(usr)
				delnote.config(fg='green',text='Account Removed Successfully')
				return

		
		else: 
			delnote.config(fg='red',text='Invalid details !')

## image import

img = Image.open('images/img.png')
img = img.resize((150,150))
img = ImageTk.PhotoImage(img)

## Labels
Label(master, text = "Welcome to PyBank" , font=('Calibri',14)).grid(row=0,sticky=N,pady=10)

Label(master, text = "The most secure Bank in this world" , font=('Calibri',12)).grid(row=1,sticky=N)

Label(master, image=img).grid(row=2,sticky=N,pady=15)



## Buttons
Button(master, text="Register", fg='white' ,bg='black' ,font=('Calibri',12),width=20,command=register).grid(row=3,sticky=N)
Button(master, text="Login" ,fg='white' ,bg='black', font=('Calibri',12),width=20,command=login).grid(row=4,sticky=N,pady=10)
Button(master, text="Delete account" , fg='white' ,bg='black',font=('Calibri',12),width=20,command=acc).grid(row=5,sticky=N)

Label(master,font=('Calibri',14)).grid(row=6,sticky=N,pady=10)

#master.after(5000, lambda : _show(h)) 



# Create the menubar
def about_us():
    tkinter.messagebox.showinfo('About PyBank', 'Credits \nLogin and Register explained by Umesh\n\nDashboard working process explained by Mithun\n\nExecution of the code by Mounish.')

menubar = Menu(master) 
file = Menu(menubar, tearoff=0,)   
menubar.add_command(label="About Us!", command=about_us)  

  
# display the menu  
master.config(menu=menubar) 
master.mainloop()
