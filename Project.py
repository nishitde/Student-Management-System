from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import cx_Oracle
import pandas as pd
from matplotlib import pyplot as plt
import time
from PIL import Image, ImageTk
import bs4
import requests
import socket
from io import BytesIO

res = requests.get("https://www.brainyquote.com/quote_of_the_day.html")
soup = bs4.BeautifulSoup(res.text,"lxml")
img = soup.find('img',{"class":"p-qotd"})
image = img['data-img-url']

s1 = "https://www.brainyquote.com"
s2= str(image)
s = s1 + s2

response = requests.get(s)
img1 = Image.open(BytesIO(response.content))

root = Tk()
root.title("Student Management System")
root.geometry("500x500+700+250")
root.iconbitmap('Student.ico')
root.withdraw()

splash = Toplevel(root)
splash.title("Splash Screen")
splash.geometry("1300x675+300+175")
splash.iconbitmap('Student.ico')

img3 = ImageTk.PhotoImage(img1)
imglabel = Label(splash, image = img3, width = 1200, height = 500).place(x = 650, y = 265, anchor = CENTER)

try:
	socket.create_connection(("google.com",80))
	res = requests.get("https://ipinfo.io/")
	data = res.json()
	city = 'Mumbai'
	citylabel = Label(splash, text = "City: " + str(city), width = 10, height = 1, font = ("Calibri", 20)).place(x = 425, y = 555)
	api_address = "https://api.openweathermap.org/data/2.5/weather?units=metric"+"&q="+city+"&appid=d594bf35b29e0714b237023612085f10"
	res1 = requests.get(api_address)
	wdata = requests.get(api_address).json()
	temp = wdata['main']['temp']
	wthlabel = Label(splash, text = "Temperature: " + str(temp) + " °C", width = 20, height = 1, font = ("Calibri", 20)).place(x = 600, y = 555)

except OSError:
	messagebox.showerror("Network error!")

splash.update()
time.sleep(3)
splash.destroy()
root.deiconify()

def f1():
    root.withdraw()
    addSt.deiconify()

def f2():
	root.withdraw()
	con = None
	cursor = None
	con = cx_Oracle.connect("system/abc123")
	cursor = con.cursor()
	sql = "Select * from Student_New order by rno"
	cursor.execute(sql)
	data = cursor.fetchall()
	msg = ""
	stViewData.configure(state = 'normal')
	stViewData.delete(1.0, END)
	for d in data:
		msg = msg + "Roll No.: " + str(d[0]) + " | Name: " + str(d[1]) + " | Marks: " + str(d[2]) + "\n"
	stViewData.insert(INSERT, msg)
	stViewData.configure(state = 'disabled')
	if cursor is not None:
		cursor.close()
	if con is not None:
		con.close()
	viewSt.deiconify()

def f3():
    root.withdraw()
    updSt.deiconify()

def f4():
    root.withdraw()
    delSt.deiconify()

def f13():
    root.destroy()
    sys.exit()

def f12():
	con = None
	cursor = None
	con = cx_Oracle.connect("system/abc123")
	cursor = con.cursor()
	cursor.execute("Select rno, name, mark from Student_New order by 1")
	file = open("Database.csv", "w")
	file.write("RNO" + "," + "NAME" + "," + "MARK" + "\n")
	for row in cursor:
		file.write(str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "\n");
	file.close()
	cursor.close()
	con.close()

	# Plotting the GRAPH
	data = pd.read_csv("Database.csv")
	rno = data['RNO'].tolist()
	name = data['NAME'].tolist()
	mark = data['MARK'].tolist()
	plt.plot(name, mark, label = 'MARKS', marker = 'o')
	plt.xlabel("NAME")
	plt.ylabel("MARKS")
	plt.legend()
	plt.show()

btnAdd = Button(root, text = "ADD", width = 10, font = ('Calibri',10), command = f1)
btnView = Button(root, text = "VIEW", width = 10, font = ('Calibri',10), command = f2)
btnUpdate = Button(root, text = "UPDATE", width = 10, font = ('Calibri',10), command = f3)
btnDelete = Button(root, text = "DELETE", width = 10, font = ('Calibri',10), command = f4)
btnGraph = Button(root, text = "GRAPH", width = 10, font = ('Calibri',10), command = f12)
btnExit = Button(root, text = "EXIT", width = 10, font = ('Calibri',10), command = f13)

btnAdd.pack(pady = 10)
btnView.pack(pady = 10)
btnUpdate.pack(pady = 10)
btnDelete.pack(pady = 10)
btnGraph.pack(pady = 10)
btnExit.pack(side = 'bottom', pady = 50)

# Creating ADD Window
addSt = Toplevel(root)
addSt.title("Add Students")
addSt.geometry("500x500+700+250")
addSt.iconbitmap('Student.ico')
addSt.withdraw()

def f5():
    addSt.withdraw()
    root.deiconify()

def f9():
    con = None
    cursor = None
    try:
        con = cx_Oracle.connect("system/abc123")
        rno = int(entAddNo.get())
        name = entAddName.get()
        mark = int(entAddMark.get())
        cursor = con.cursor()
        sql = "Insert into Student_New values('%d','%s','%d')"
        if type(name) == str and len(name) != 0 and name.isalpha():
            args = (rno, name, mark)
            cursor.execute(sql % args)
            con.commit()
            msg = str(cursor.rowcount) + " Row(s) Inserted"
            messagebox.showinfo("Success!", msg)
            entAddNo.delete(0, END)
            entAddName.delete(0, END)
            entAddMark.delete(0, END)
        else:
            messagebox.showerror("Failure!", "Name Field should contain a STRING only")
            entAddNo.delete(0, END)
            entAddName.delete(0, END)
            entAddMark.delete(0, END)

    except cx_Oracle.DatabaseError as e:
        try:
            messagebox.showerror("Error!", "Insert Issues", e)
            con.rollback()

        except TypeError:
            print("Roll No. already exists!")

    except ValueError:
        messagebox.showerror("Failure!", "Roll No./Marks should be INTEGER only")
        entAddNo.delete(0, END)
        entAddName.delete(0, END)
        entAddMark.delete(0, END)

    finally:
        if cursor is not None:
            cursor.close()
        if con is not None:
            con.close()

lblAddNo = Label(addSt, text = "ENTER ROLL NUMBER")
entAddNo = Entry(addSt, bd = 2)
entAddNo.focus_set()
lblAddName = Label(addSt, text = "ENTER NAME")
entAddName = Entry(addSt, bd = 2)
lblAddMark = Label(addSt, text = "ENTER THE MARKS")
entAddMark = Entry(addSt, bd = 2)
btnAddSave = Button(addSt, text = "SAVE", width = 10, font = ('Calibri',10), command = f9)
btnAddBack = Button(addSt, text = "BACK", width = 10, font = ('Calibri',10), command = f5)
btnAddExit = Button(addSt, text = "EXIT", width = 10, font = ('Calibri',10), command = f13)

lblAddNo.pack()
entAddNo.pack(pady = 5)
lblAddName.pack()
entAddName.pack(pady = 5)
lblAddMark.pack()
entAddMark.pack(pady = 5)
btnAddSave.pack(pady = 10)
btnAddBack.pack(pady = 10)
btnAddExit.pack(side = 'bottom', pady = 50)

# Creating VIEW Window
viewSt = Toplevel(root)
viewSt.title("View Students")
viewSt.geometry("500x500+700+250")
viewSt.iconbitmap('Student.ico')
viewSt.withdraw()

def f6():
    viewSt.withdraw()
    root.deiconify()

stViewData = scrolledtext.ScrolledText(viewSt, width = 45, height = 15)
btnViewBack = Button(viewSt, text = "BACK", width = 10, font = ('Calibri',10), command = f6)
btnViewExit = Button(viewSt, text = "EXIT", width = 10, font = ('Calibri',10), command = f13)

stViewData.pack(pady = 10)
btnViewBack.pack(pady = 10)
btnViewExit.pack(pady = 32)

# Creating UPDATE Window
updSt = Toplevel(root)
updSt.title("Update Students")
updSt.geometry("500x500+700+250")
updSt.iconbitmap('Student.ico')
updSt.withdraw()

def f7():
    updSt.withdraw()
    root.deiconify()

def f10():
    con = None
    cursor = None
    try:
        con = cx_Oracle.connect("system/abc123")
        rno = int(entUpdNo.get())
        name = entUpdName.get()
        mark = int(entUpdMark.get())
        cursor = con.cursor()
        sql = "Update Student_New set name = '%s',mark = '%d' where rno = '%d'"
        if type(name) == str and len(name) != 0 and name.isalpha():
            args = (name, mark, rno)
            cursor.execute(sql % args)
            con.commit()
            msg = str(cursor.rowcount) + " Row(s) Updated"
            messagebox.showinfo("Success!", msg)
            entUpdNo.delete(0, END)
            entUpdName.delete(0, END)
            entUpdMark.delete(0, END)
        else:
            messagebox.showerror("Failure!", "Name Field should contain a STRING only")
            entUpdNo.delete(0, END)
            entUpdName.delete(0, END)
            entUpdMark.delete(0, END)

    except cx_Oracle.DatabaseError as e:
        try:
            messagebox.showerror("Error!", "Update Issues", e)
            con.rollback()

        except TypeError:
            print("Roll No. already exists!")

    except ValueError:
        messagebox.showerror("Failure!", "Roll No./Marks should be INTEGER only")
        entUpdNo.delete(0, END)
        entUpdName.delete(0, END)
        entUpdMark.delete(0, END)

    finally:
        if cursor is not None:
            cursor.close()
        if con is not None:
            con.close()

lblUpdNo = Label(updSt, text = "ENTER ROLL NUMBER")
entUpdNo = Entry(updSt, bd = 2)
entUpdNo.focus_set()
lblUpdName = Label(updSt, text = "UPDATE NAME")
entUpdName = Entry(updSt, bd = 2)
lblUpdMark = Label(updSt, text = "UPDATE MARKS")
entUpdMark = Entry(updSt, bd = 2)
btnUpdSave = Button(updSt, text = "SAVE", width = 10, font = ('Calibri',10), command = f10)
btnUpdBack = Button(updSt, text = "BACK", width = 10, font = ('Calibri',10), command = f7)
btnUpdExit = Button(updSt, text = "EXIT", width = 10, font = ('Calibri',10), command = f13)

lblUpdNo.pack()
entUpdNo.pack(pady = 5)
lblUpdName.pack()
entUpdName.pack(pady = 5)
lblUpdMark.pack()
entUpdMark.pack(pady = 5)
btnUpdSave.pack(pady = 10)
btnUpdBack.pack(pady = 10)
btnUpdExit.pack(side = 'bottom', pady = 50)

# Creating DELETE Window
delSt = Toplevel(root)
delSt.title("Delete Students")
delSt.geometry("500x500+700+250")
delSt.iconbitmap('Student.ico')
delSt.withdraw()

def f8():
    delSt.withdraw()
    root.deiconify()

def f11():
    con = None
    cursor = None
    try:
        con = cx_Oracle.connect("system/abc123")
        rno = int(entdelNo.get())
        cursor = con.cursor()
        sql = "Delete from Student_New where rno = '%d'"
        args = (rno)
        cursor.execute(sql % args)
        con.commit()
        msg = str(cursor.rowcount) + " Row(s) Deleted"
        messagebox.showinfo("Success!", msg)
        entdelNo.delete(0, END)

    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Error!", "Delete Issue", e)
        con.rollback()

    except ValueError:
        messagebox.showerror("Failure!", "Roll No. should contain INTEGER only")
        entdelNo.delete(0, END)

    finally:
        if cursor is not None:
            cursor.close()
        if con is not None:
            con.close()

lbldelNo = Label(delSt, text = "ENTER ROLL NUMBER")
entdelNo = Entry(delSt, bd = 2)
entdelNo.focus_set()
btndelDelete = Button(delSt, text = "DELETE", width = 10, font = ('Calibri',10), command = f11)
btndelBack = Button(delSt, text = "BACK", width = 10, font = ('Calibri',10), command = f8)
btndelExit = Button(delSt, text = "EXIT", width = 10, font = ('Calibri',10), command = f13)

lbldelNo.pack()
entdelNo.pack(pady = 5)
btndelDelete.pack(pady = 10)
btndelBack.pack(pady = 10)
btndelExit.pack(side = 'bottom', pady = 50)

root.mainloop()
