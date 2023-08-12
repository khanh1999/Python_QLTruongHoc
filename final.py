from tkinter import *
import tkinter as tk
from tkinter import ttk,filedialog
import mysql.connector
from tkinter import messagebox
from datetime import datetime
import pandas as pd
import openpyxl

db = mysql.connector.connect(
  host="localhost",
  user="root",
  database="QL_TH"
)
if db.is_connected():
  print("Kết nối tới MySQL thành công!")
else:
  print("Không thể kết nối tới MySQL.")

# Tạo cửa sổ Tkinter đầu tiên
window4 = tk.Tk()
window4.geometry("500x300")
window4.title("Login")
window4.resizable(width=False, height=False) #lock win size

def switch_window(old_window):
    
    if userEntry.get()=="admin" and passEntry.get()=="123":
        messagebox.showinfo("Thông báo","Đăng nhập thành công")
        old_window.withdraw()
        window.deiconify() 
    else:
        messagebox.showerror("Lỗi","Đăng nhập thất bại")

# Tạo một nút để chuyển sang cửa sổ Tkinter thứ hai
lab = Label(window4,text="LOGIN", font="arial 20", fg="blue").pack(side=TOP)


userlab = Label(window4, text="Username:", font="arial 10").place(x=60,y=90)
passlab = Label(window4, text="Password:", font="arial 10").place(x=60,y=140)

userEntry = Entry(window4,font="arial 10", width=30)
userEntry.place(x=140,y=90)
passEntry = Entry(window4,font="arial 10", width=30,show='*')
passEntry.place(x=140,y=140)

loginBut = Button(window4,text="Enter",font="arial 10",width=8,command=lambda: switch_window(window4))
loginBut.place(x=140 , y=200)
exitBut = Button(window4,text="Exit",font="arial 10", width=8,command=window4.destroy)
exitBut.place(x= 250, y=200)


# Tạo cửa sổ Tkinter thứ hai và ẩn nó
window = tk.Toplevel()
window.withdraw()
window.geometry("900x600")
window.title("Quản lý nhân viên")
window.resizable(width=False, height=False) #lock win size  

########### Load table

query="select * from phongban"
q_show=db.cursor()
q_show.execute(query)
rows = q_show.fetchall()

query2="select manv,hoten, ngaysinh,gioitinh, sdt, tenpb from nhanvien,phongban where nhanvien.phongban = mapb"
q_show2=db.cursor()
q_show2.execute(query2)
rows2 = q_show2.fetchall()

###########

########### Xu ly button PB

def addPB():
    query="INSERT INTO phongban VALUES (%s, %s);"
    val = (maPBentr.get(),tenPBentr.get())
    q_add=db.cursor()
    q_add.execute(query,val)
    db.commit()
    
    for i in pbTree.get_children():
        pbTree.delete(i)
    
    query2="select * from phongban"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        pbTree.insert('','end',iid=i[0],values=i)
    pbTree.place(x=10,y=110,width=200,height=100)

def xoaPB():
    selected = pbTree.selection()[0]
    query = "delete from phongban where MaPB=%s"
    data =(selected,)
    q_del = db.cursor()
    q_del.execute(query,data)
    db.commit()
    pbTree.delete(selected)
    
def suaPB():
    query="update phongban set TenPB=%s where MaPB=%s;"
    val = (tenPBentr.get(),maPBentr.get())
    q_add=db.cursor()
    q_add.execute(query,val)
    db.commit()
    
    for i in pbTree.get_children():
        pbTree.delete(i)
    
    query2="select * from phongban"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        pbTree.insert('','end',iid=i[0],values=i)
    pbTree.place(x=10,y=110,width=200,height=100)

###########

##########XU LY BUTTON NHAN VIEN

def addNV():
    query="INSERT INTO nhanvien VALUES (%s, %s, %s, %s, %s, %s);"
    val = (idEntr.get(),nameEntr.get(),datetime.strptime(dayEntr.get(), "%d/%m/%Y"),gtEntr.get(),phoneEntr.get(),pbEntr.get())
    q_add=db.cursor()
    q_add.execute(query,val)
    db.commit()
    
    for i in nvTree.get_children():
        nvTree.delete(i)
    
    query2="select manv,hoten, ngaysinh,gioitinh, sdt, tenpb from nhanvien,phongban where nhanvien.phongban = mapb"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        nvTree.insert('','end',iid=i[0],values=i)
    nvTree.place(x=20,y=320, width=700,height=250)
    
    idEntr.delete(0,'end')
    nameEntr.delete(0,'end')
    dayEntr.delete(0,'end')
    gtEntr.delete(0,'end')
    phoneEntr.delete(0,'end')
    pbEntr.delete(0,'end')
    
def delNV():
    selected = nvTree.selection()[0]
    query = "delete from nhanvien where manv=%s"
    data =(selected,)
    q_del = db.cursor()
    q_del.execute(query,data)
    db.commit()
    nvTree.delete(selected)
    
def changeNV():
    query="update nhanvien set hoten=%s,ngaysinh=%s,gioitinh=%s,sdt=%s, phongban=%s where manv=%s;"
    val = (nameEntr.get(),datetime.strptime(dayEntr.get(), "%d/%m/%Y"),gtEntr.get(),phoneEntr.get(),pbEntr.get(),idEntr.get())
    q_add=db.cursor()
    q_add.execute(query,val)
    db.commit()
    
    for i in nvTree.get_children():
        nvTree.delete(i)
    
    query2="select manv,hoten, ngaysinh,gioitinh, sdt, tenpb from nhanvien,phongban where nhanvien.phongban = mapb"
    q_show=db.cursor()  
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        nvTree.insert('','end',iid=i[0],values=i)
    nvTree.place(x=20,y=320, width=700,height=250)
    
def findNV():
    for i in nvTree.get_children():
        nvTree.delete(i)   
    query2="select manv,hoten, ngaysinh,gioitinh, sdt, tenpb from nhanvien,phongban where nhanvien.phongban = mapb and hoten like '%"+nameEntr.get()+"%'"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        nvTree.insert('','end',iid=i[0],values=i)
    nvTree.place(x=20,y=320, width=700,height=250)
    
def clearNV():
    for i in nvTree.get_children():
        nvTree.delete(i)   
        
    query2="select manv,hoten, ngaysinh,gioitinh, sdt, tenpb from nhanvien,phongban where nhanvien.phongban = mapb"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        nvTree.insert('','end',iid=i[0],values=i)
    nvTree.place(x=20,y=320, width=700,height=250)
    idEntr.delete(0,'end')
    nameEntr.delete(0,'end')
    dayEntr.delete(0,'end')
    gtEntr.delete(0,'end')
    phoneEntr.delete(0,'end')
    pbEntr.delete(0,'end')
    maPBentr.delete(0,'end')
    tenPBentr.delete(0,'end')

def xuatDL():
    # Lấy dữ liệu từ Treeview
        data = []
        for child in nvTree.get_children():
            data.append(tuple(nvTree.item(child)["values"]))
        
        # Tạo DataFrame và lưu ra file Excel
        df = pd.DataFrame(data, columns=["Mã NV", "Họ Tên", "Ngày Sinh", "Giới Tính", "SDT", "Phòng Ban"])
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if file_path:
            df.to_excel(file_path, index=False)
            tk.messagebox.showinfo("Export", "Data exported to Excel file successfully.")
##########

########## Loc Thong tin

def lcShow():
    for i in nvTree.get_children():
        nvTree.delete(i)   
    query2="select manv,hoten, ngaysinh,gioitinh, sdt, tenpb from nhanvien,phongban where nhanvien.phongban = mapb and mapb ='LC'"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        nvTree.insert('','end',iid=i[0],values=i)
    nvTree.place(x=20,y=320, width=700,height=250)
    
def bvShow():
    for i in nvTree.get_children():
        nvTree.delete(i)   
    query2="select manv,hoten, ngaysinh,gioitinh, sdt, tenpb from nhanvien,phongban where nhanvien.phongban = mapb and mapb ='BV'"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        nvTree.insert('','end',iid=i[0],values=i)
    nvTree.place(x=20,y=320, width=700,height=250)

def gvShow():
    for i in nvTree.get_children():
        nvTree.delete(i)   
    query2="select manv,hoten, ngaysinh,gioitinh, sdt, tenpb from nhanvien,phongban where nhanvien.phongban = mapb and mapb ='GV'"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        nvTree.insert('','end',iid=i[0],values=i)
    nvTree.place(x=20,y=320, width=700,height=250)
    
def gvcnShow():
    for i in nvTree.get_children():
        nvTree.delete(i)   
    query2="select manv,hoten, ngaysinh,gioitinh, sdt, tenpb from nhanvien,phongban,lophoc where nhanvien.phongban = mapb and gvcn =manv"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        nvTree.insert('','end',iid=i[0],values=i)
    nvTree.place(x=20,y=320, width=700,height=250)
    
def gvbmShow():
    for i in nvTree.get_children():
        nvTree.delete(i)   
    query2="select manv,hoten, ngaysinh,gioitinh, sdt, tenpb from nhanvien,phongban,tomon where nhanvien.phongban = mapb and nhanvien.manv = tomon.magv and chucvu ='GVBM'"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        nvTree.insert('','end',iid=i[0],values=i)
    nvTree.place(x=20,y=320, width=700,height=250)

def ldShow():
    for i in nvTree.get_children():
        nvTree.delete(i)   
    query2="select manv,hoten, ngaysinh,gioitinh, sdt, tenpb from nhanvien,phongban,tomon where nhanvien.phongban = mapb and nhanvien.manv = tomon.magv and chucvu !='GVBM'"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        nvTree.insert('','end',iid=i[0],values=i)
    nvTree.place(x=20,y=320, width=700,height=250)

##########
######## Chuyển giao diện##########

def switch_windowTM(old_window):
  old_window.withdraw()
  window2.deiconify()

def switch_windowLH(old_window):
  old_window.withdraw()
  window3.deiconify()

###########################

##########

lab = Label(window,text="QUẢN LÝ NHÂN VIÊN", font="arial 25").pack()

nhapFrame = LabelFrame(window,text="Nhập thông tin",width=550,height=270)
nhapFrame.place(x=10,y=40)
phongbanFrame = LabelFrame(window,text="Phòng ban",width=320,height=270)
phongbanFrame.place(x=580,y=40)

#Frame thông tin nhân viên
idLab = Label(nhapFrame,text="Mã NV:", font="arial 10").place(x=10,y=5)
nameLab = Label(nhapFrame,text="Tên NV:", font="arial 10").place(x=10,y=40)
dayLab = Label(nhapFrame,text="Ngày sinh:", font="arial 10").place(x=10,y=75)
gtLab = Label(nhapFrame,text="Giới tính:", font="arial 10").place(x=10,y=110)
phoneLab = Label(nhapFrame,text="SĐT:", font="arial 10").place(x=10,y=145)
pbLab = Label(nhapFrame,text="Phòng ban:", font="arial 10").place(x=10,y=180)

idEntr = Entry(nhapFrame,font="arial 10", width=15)
idEntr.place(x=80,y=5)
nameEntr = Entry(nhapFrame,font="arial 10",width=30)
nameEntr.place(x=80,y=40)
dayEntr = Entry(nhapFrame,font="arial 10",width=15)
dayEntr.place(x=80,y=75)
gtEntr = Entry(nhapFrame,font="arial 10",width=15)
gtEntr.place(x=80,y=110)
phoneEntr = Entry(nhapFrame,font="arial 10",width=15)
phoneEntr.place(x=80,y=145)
pbEntr = Entry(nhapFrame,font="arial 10",width=15)
pbEntr.place(x=80,y=180)

addBut = Button(nhapFrame, text="Thêm",  font="arial 10", width=10,command=addNV)
addBut.place(x=320, y=10)
delBut = Button(nhapFrame, text="Xóa",  font="arial 10", width=10,command=delNV)
delBut.place(x= 430, y=10)
changeBut = Button(nhapFrame, text="Sửa",  font="arial 10", width=10,command=changeNV)
changeBut.place(x=320, y=45)
findBut = Button(nhapFrame, text="Tìm Kiếm",  font="arial 10", width=10,command=findNV)
findBut.place(x=430,y=45)
excelBut = Button(nhapFrame, text="Xuất DL",  font="arial 10", width=10,command=xuatDL)
excelBut.place(x=320,y=80)
clearBut = Button(nhapFrame, text="Clear",  font="arial 10", width=10,command=clearNV)
clearBut.place(x=430, y=80)

locLab = Label(nhapFrame, text="Lọc thông tin",  font="arial 10").place(x=380,y=115)

lcBut = Button(nhapFrame, text="Lao Công",  font="arial 10", width=10,command=lcShow)
lcBut.place(x=320, y=145)
bvBut = Button(nhapFrame, text="Bảo Vệ",  font="arial 10", width=10,command=bvShow)
bvBut.place(x=430, y=145)
gvBut = Button(nhapFrame, text="Giáo Viên",  font="arial 10", width=10, command=gvShow)
gvBut.place(x=320, y=180)
gvcnBut = Button(nhapFrame, text="GVCN",  font="arial 10", width=10,command=gvcnShow)
gvcnBut.place(x=430, y=180)
gvbmBut = Button(nhapFrame, text="GVBM",  font="arial 10", width=10,command=gvbmShow)
gvbmBut.place(x=320, y=215)
ldBut = Button(nhapFrame, text="Lãnh Đạo",  font="arial 10", width=10,command=ldShow)
ldBut.place(x=430, y=215)

#Frame Phòng ban
maPBlab = Label(phongbanFrame,text="Mã PB:", font="arial 10").place(x=50,y=20)
tenPBlab = Label(phongbanFrame,text="Tên PB:", font="arial 10").place(x=50,y=60)

maPBentr = Entry(phongbanFrame,font="arial 10", width=10)
maPBentr.place(x=150,y=20)
tenPBentr = Entry(phongbanFrame,font="arial 10", width=15)
tenPBentr.place(x=150,y=60)

aPBbut = Button(phongbanFrame,text="Thêm",font="arial 10",width=10,command=addPB)
aPBbut.place(x=220,y=100)
xPBbut = Button(phongbanFrame,text="Xóa",font="arial 10",width=10,command=xoaPB)
xPBbut.place(x=220,y=145)
sPBbut = Button(phongbanFrame,text="Sửa",font="arial 10",width=10,command=suaPB)
sPBbut.place(x=220,y=190)

pbTree = ttk.Treeview(phongbanFrame,columns=(1,2),show="headings")
pbTree.heading(1,text="MaPB")
pbTree.column(1,width=50)
pbTree.heading(2,text="TenPB")
pbTree.column(2,width=150)
#load db
for i in rows:
    pbTree.insert('','end',iid=i[0],values=i)
    
pbTree.place(x=10,y=110,width=200,height=100)

##########################################

nvTree =ttk.Treeview(window,columns=(1,2,3,4,5,6),show="headings")
nvTree.heading(1,text="MaNV")
nvTree.column(1,width="50")
nvTree.heading(2,text="HoTen")
nvTree.column(2,width="150")
nvTree.heading(3,text="NgaySinh")
nvTree.column(3,width="150")
nvTree.heading(4,text="GioiTinh")
nvTree.column(4,width="70")
nvTree.heading(5,text="SDT")
nvTree.column(5,width="150")
nvTree.heading(6,text="TenPB")
nvTree.column(6,width="100")
nvTree.place(x=20,y=320, width=700,height=250)

qlTM = Button(window,text="QL Tổ Môn",font="aral 15", width=15,command=lambda: switch_windowTM(window))
qlTM.place(x=720,y=320)
qlLH = Button(window,text="QL Lớp Học",font="aral 15", width=15,command=lambda: switch_windowLH(window))
qlLH.place(x=720,y=420)
exitBut = Button(window,text="Thoát",font="aral 15", width=10,command=window.destroy)
for i in rows2:
    nvTree.insert('','end',iid=i[0],values=i)
    
exitBut.place(x=720,y=520)

############################## QL Tổ Môn ###########################

window2 = tk.Toplevel()
window2.withdraw()
window2.geometry("700x500")
window2.title("Quản lý tổ môn")
window2.resizable(width=False, height=False) #lock win size

########Load table
query3="select * from tomon"
q_show3=db.cursor()
q_show3.execute(query3)
rows3 = q_show3.fetchall()

########

######### Xử lý button

def addTM():
    query="INSERT INTO tomon VALUES (%s, %s, %s, %s);"
    val = (maGVEntr.get(),cmEntr.get(),cvEntr.get(),maTTEntr.get())
    q_add=db.cursor()
    q_add.execute(query,val)
    db.commit()
    
    for i in tmTree.get_children():
        tmTree.delete(i)
    
    query2="select * from tomon"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        tmTree.insert('','end',iid=i[0],values=i)
    tmTree.place(x=100,y=250, width=500,height=200)
    
    maGVEntr.delete(0,'end')
    cmEntr.delete(0,'end')
    cvEntr.delete(0,'end')
    maTTEntr.delete(0,'end')

def delTM():
    selected = tmTree.selection()[0]
    query = "delete from tomon where magv=%s"
    data =(selected,)
    q_del = db.cursor()
    q_del.execute(query,data)
    db.commit()
    tmTree.delete(selected)
    
def changeTM():
    query="update tomon set chuyenmon=%s,chucvu=%s,matt=%s where magv=%s;"
    val = (cmEntr.get(),cvEntr.get(),maTTEntr.get(),maGVEntr.get())
    q_add=db.cursor()
    q_add.execute(query,val)
    db.commit()
    
    for i in tmTree.get_children():
        tmTree.delete(i)
    
    query2="select * from tomon"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        tmTree.insert('','end',iid=i[0],values=i)
    tmTree.place(x=100,y=250, width=500,height=200)

def findTM():
    for i in tmTree.get_children():
        tmTree.delete(i)   
    query2="select * from tomon where chuyenmon like '%"+cmEntr.get()+"%'"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        tmTree.insert('','end',iid=i[0],values=i)
    tmTree.place(x=100,y=250, width=500,height=200)
    
    maGVEntr.delete(0,'end')
    cmEntr.delete(0,'end')
    cvEntr.delete(0,'end')
    maTTEntr.delete(0,'end')
    
def switch_windowMain(old_window):
  old_window.withdraw()
  window.deiconify()

#########


nhapFrame = LabelFrame(window2,text="Nhập thông tin",width=600,height=200)
nhapFrame.place(x=50,y=40)

lab = Label(window2,text="QUẢN LÝ TỔ MÔN", font="arial 25").pack()
#Frame thông tin tổ môn
maGVLab = Label(nhapFrame,text="Mã GV:", font="arial 10").place(x=10,y=5)
cmLab = Label(nhapFrame,text="Chuyên môn:", font="arial 10").place(x=10,y=40)
cvLab = Label(nhapFrame,text="Chức vụ:", font="arial 10").place(x=10,y=75)
maTTLab = Label(nhapFrame,text="Mã Tổ trưởng:", font="arial 10").place(x=10,y=110)

maGVEntr = Entry(nhapFrame,font="arial 10", width=15)
maGVEntr.place(x=100,y=5)
cmEntr = Entry(nhapFrame,font="arial 10",width=20)
cmEntr.place(x=100,y=40)
cvEntr = Entry(nhapFrame,font="arial 10",width=20)
cvEntr.place(x=100,y=75)
maTTEntr = Entry(nhapFrame,font="arial 10",width=15)
maTTEntr.place(x=100,y=110)

addBut = Button(nhapFrame, text="Thêm",  font="arial 10", width=10,command=addTM)
addBut.place(x=320, y=10)
delBut = Button(nhapFrame, text="Xóa",  font="arial 10", width=10, command=delTM)
delBut.place(x= 470, y=10)
changeBut = Button(nhapFrame, text="Sửa",  font="arial 10", width=10,command=changeTM)
changeBut.place(x=320, y=75)
findBut = Button(nhapFrame, text="Tìm Kiếm",  font="arial 10", width=10,command=findTM)
findBut.place(x=470,y=75)
backBut = Button(nhapFrame, text="Quay Lại",  font="arial 10", width=10,command=lambda: switch_windowMain(window2))
backBut.place(x=390,y=140)

##########################################
tmTree =ttk.Treeview(window2,columns=(1,2,3,4),show="headings")
tmTree.heading(1,text="MaGV")
tmTree.column(1,width="50")
tmTree.heading(2,text="Chuyên Môn")
tmTree.column(2,width="150")
tmTree.heading(3,text="Chức vụ")
tmTree.column(3,width="150")
tmTree.heading(4,text="Mã Tổ Trưởng")
tmTree.column(4,width="70")

tmTree.place(x=100,y=250, width=500,height=200)
for i in rows3:
    tmTree.insert('','end',iid=i[0],values=i)




################################################################

############################## QL Lớp học ###########################

window3 = tk.Toplevel()
window3.withdraw()
window3.geometry("700x500")
window3.title("Quản lý lớp học")
window3.resizable(width=False, height=False) #lock win size

###########Load table
query4="select * from lophoc"
q_show4=db.cursor()
q_show4.execute(query4)
rows4 = q_show4.fetchall()

###########

###########Xử lý button Lớp học
def addLH():
    query="INSERT INTO lophoc VALUES (%s, %s, %s, %s, %s, %s, %s);"
    val = (malopEntr.get(),tenlopEntr.get(),ssEntr.get(),gvcnEntr.get(),toanEntr.get(),lyEntr.get(),hoaEntr.get())
    q_add=db.cursor()
    q_add.execute(query,val)
    db.commit()
    
    for i in lhTree.get_children():
        lhTree.delete(i)
    
    query2="select * from lophoc"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        lhTree.insert('','end',iid=i[0],values=i)
    lhTree.place(x=50,y=250, width=500,height=230)
    
    malopEntr.delete(0,'end')
    tenlopEntr.delete(0,'end')
    ssEntr.delete(0,'end')
    gvcnEntr.delete(0,'end')
    toanEntr.delete(0,'end')
    lyEntr.delete(0,'end')
    hoaEntr.delete(0,'end')

def delLH():
    selected = lhTree.selection()[0]
    query = "delete from lophoc where mal=%s"
    data =(selected,)
    q_del = db.cursor()
    q_del.execute(query,data)
    db.commit()
    lhTree.delete(selected) 
    
def changeLH():
    query="update lophoc set tenl=%s,siso=%s,gvcn=%s,gvt=%s,gvl=%s,gvh=%s where mal=%s;"
    val = (tenlopEntr.get(),ssEntr.get(),gvcnEntr.get(),toanEntr.get(),lyEntr.get(),hoaEntr.get(),malopEntr.get())
    q_add=db.cursor()
    q_add.execute(query,val)
    db.commit()
    
    for i in lhTree.get_children():
        lhTree.delete(i)
    
    query2="select * from lophoc"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        lhTree.insert('','end',iid=i[0],values=i)
    lhTree.place(x=50,y=250, width=500,height=230)
    
def findLH():
    for i in lhTree.get_children():
        lhTree.delete(i)   
    query2="select * from lophoc where tenl like '%"+tenlopEntr.get()+"%'"
    q_show=db.cursor()
    q_show.execute(query2)
    rows = q_show.fetchall()
    
    for i in rows:
        lhTree.insert('','end',iid=i[0],values=i)
    lhTree.place(x=50,y=250, width=500,height=230)
    
    malopEntr.delete(0,'end')
    tenlopEntr.delete(0,'end')
    ssEntr.delete(0,'end')
    gvcnEntr.delete(0,'end')
    toanEntr.delete(0,'end')
    lyEntr.delete(0,'end')
    hoaEntr.delete(0,'end')

###########

nhapFrame = LabelFrame(window3,text="Nhập thông tin",width=600,height=200)
nhapFrame.place(x=50,y=40)

lab = Label(window3,text="QUẢN LÝ LỚP HỌC", font="arial 25").pack()
#Frame thông tin tổ môn
malopLab = Label(nhapFrame,text="Mã Lớp:", font="arial 10").place(x=10,y=5)
tenlopLab = Label(nhapFrame,text="Tên Lớp:", font="arial 10").place(x=10,y=40)
ssLab = Label(nhapFrame,text="Sỉ số", font="arial 10").place(x=10,y=75)
gvcnLab = Label(nhapFrame,text="GVCN:", font="arial 10").place(x=10,y=110)
toanLap = Label(nhapFrame,text="GV Toán:", font="arial 10").place(x=250,y=5)
lyLap = Label(nhapFrame,text="GV Lý:", font="arial 10").place(x=250,y=55)
hoaLap = Label(nhapFrame,text="GV Hóa:", font="arial 10").place(x=250,y=105)

malopEntr = Entry(nhapFrame,font="arial 10", width=15)
malopEntr.place(x=100,y=5)
tenlopEntr = Entry(nhapFrame,font="arial 10",width=15)
tenlopEntr.place(x=100,y=40)
ssEntr = Entry(nhapFrame,font="arial 10",width=15)
ssEntr.place(x=100,y=75)
gvcnEntr = Entry(nhapFrame,font="arial 10",width=15)
gvcnEntr.place(x=100,y=110)
toanEntr = Entry(nhapFrame,font="arial 10",width=15)
toanEntr.place(x=320,y=5)
lyEntr = Entry(nhapFrame,font="arial 10",width=15)
lyEntr.place(x=320,y=55)
hoaEntr = Entry(nhapFrame,font="arial 10",width=15)
hoaEntr.place(x=320,y=105)

addBut = Button(nhapFrame, text="Thêm",  font="arial 10", width=10,command=addLH)
addBut.place(x=470, y=5)
delBut = Button(nhapFrame, text="Xóa",  font="arial 10", width=10,command=delLH)
delBut.place(x= 470, y=50)
changeBut = Button(nhapFrame, text="Sửa",  font="arial 10", width=10,command=changeLH)
changeBut.place(x=470, y=95)
findBut = Button(nhapFrame, text="Tìm Kiếm",  font="arial 10", width=10,command=findLH)
findBut.place(x=470,y=140)

##########################################

backBut = Button(window3, text="Quay Lại",  font="arial 15", width=10,command=lambda: switch_windowMain(window3))
backBut.place(x=570,y=400)

lhTree =ttk.Treeview(window3,columns=(1,2,3,4,5,6,7),show="headings")
lhTree.heading(1,text="Mã Lớp")
lhTree.column(1,width="70")
lhTree.heading(2,text="Tên Lớp")
lhTree.column(2,width="70")
lhTree.heading(3,text="Sỉ Số")
lhTree.column(3,width="70")
lhTree.heading(4,text="GVCN")
lhTree.column(4,width="70")
lhTree.heading(5,text="GV Toán")
lhTree.column(5,width="70")
lhTree.heading(6,text="GV Lý")
lhTree.column(6,width="70")
lhTree.heading(7,text="GV Hóa")
lhTree.column(7,width="70")
lhTree.place(x=50,y=250, width=500,height=230)
for i in rows4:
    lhTree.insert('','end',iid=i[0],values=i)



################################################################

# Thực thi chương trình
window4.mainloop()

