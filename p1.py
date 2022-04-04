from tkinter import *
from tkinter import messagebox,simpledialog
from os import listdir,mkdir,remove
from random import randrange
try:
	mkdir("userfiles")
except:
	pass

home=Tk()
home.configure(background="#f1f1f1")
home.title("En-De-Cryptor")
home.minsize(800,540)
home.maxsize(800,540)
home.geometry("800x540")
icon=PhotoImage(file="icon.png")
home.iconphoto(True,icon)

m=[]

def show_content(content):
	text_box.delete("1.0",END)
	text_box.insert(INSERT,content)



def encrypted(a,diff_tens,diff_ones):
    n=ord(a)
    if n<32 and n>123:
        return chr(n)
    tens=int(n//10)
    tens+=diff_tens
    if tens>12:
        tens=tens-10
    ones=int(n%10)
    check=ones
    ones*=2
    if check%2==0:
        ones%=10
        return chr(int(str(tens)+str(int(ones))))
    else:
        
        ones-=diff_ones
        ones%=10
        return chr(int(str(tens)+str(int(ones))))
    


    
def encrypt_string(string,success):
    key1=randrange(0,10)
    key2=randrange(1,8,2)    
    success(key1,key2)
    for i in string:
        yield (lambda x:encrypted(x,key1,key2))(i)




def encrypt(string,success):
   key=0
   def getkeys(key1,key2):
       nonlocal key
       key=int(str(key1)+str(key2))
       key3=randrange(2,6)
       key=str((2*key+key3)*key3)+str(key3)
       success("Successfully Encrypted\nkey has been generated: KEY is "+key+"\nIMP: Remember key to Decrypt it")
        
   encrypted_string=str().join(list(encrypt_string(string,getkeys)))
   return encrypted_string
    





def key_decode(key):
    key=str(key)
    key3=int(key[-1])
    if key3==0:
        return 0,0
   
    key12=int(key[0:-1])
    key12=int(round(key12*(1/key3)))
    key12-=key3
    key12/=2
    
    key1=int(key12//10)
    key2=int(key12%10)
    return key1,key2





def decrypted(a,diff_tens,diff_ones):
    n=ord(a)
    if n<32 and n>123:
        return chr(n)
    ones=n%10
    tens=n//10
    if ones%2==0:
        if int((ones/2))%2==0:
            ones/=2
        else:
            ones=int((10+ones)/2)
    else:
        
        ones=ones+diff_ones
        if ones<10:
            ones+=10
        if (ones/2)%2==0:
            ones=int((ones%10)/2)
        else:
            ones/=2
    tens-=diff_tens
    if tens<3:
        tens=10+tens
    return chr(int(str(int(tens))+str(int(ones))))




def decrypt_string(string,key1,key2):
	for i in string:
		yield (lambda x:decrypted(x,key1,key2))(i)




def decrypt(string,key,success,failure):
	key1,key2=key_decode(key)
	if key2==0:
		failure("Sorry, an Error has occured or Key Invalid")
		return
	decrypted_string=str().join(list(decrypt_string(string,key1,key2)))
	success("Successfully Decrypted \nIMP: wrong Key Leads to Wrong Output\nPress Ok to view.")
	return decrypted_string




def failure(data):
	#print(data)
	messagebox.showerror("Key Invalid!",data)

def success(data):
	#print(data)
	messagebox.showinfo("Success",data)





def read_from_file(filename):
	file=open(str("userfiles/"+filename+".txt"),"r")
	return file.read()



def is_file_exists(filename):
	filename=filename+".txt"
	l=listdir("userfiles")
	for i in l:
		if filename==i:
			return True
	return False


def write_to_file(content,filename):
	file=open(str("userfiles/"+filename+".txt"),"w")
	try:
		file.write(str(content))
		file.close()
	except:
		file.close()
		delete_file(filename)
		messagebox.showerror("Fail","ENCRYPTION FAILED.\n Probably because the encrypted characters are not\n SUPPORTED IN THIS PC\n please try again")



def perform_encryption():
	textval=text_box.get("1.0","end-1c")
	if textval=="":
		messagebox.showwarning("Error","Cannot encrypt an empty file")
	else:
		
		res=simpledialog.askstring("filename","Enter FILE NAME to proceed")
		


		status=True
		if res:
			if is_file_exists(res):
				status=messagebox.askyesno("Already Exists!","File "+res+" already exists. Do you want to replace it?",icon="warning")
		

			if status:
					enc_val=encrypt(str(textval),success)
					write_to_file(enc_val,res)
					listfiles()
		else:
			messagebox.showwarning("name error","File name is compulsory")



def perform_decryption():
	filename=simpledialog.askstring("File name","Enter FILE NAME to decrypt:")
	if filename:
		if is_file_exists(filename):
			userkey=simpledialog.askstring("KEY","Enter KEY:")
			if str(userkey).isdigit():
				content=read_from_file(filename)
				dec_val=decrypt(content,userkey,success,failure)
				if dec_val:
					show_content(dec_val)
					
				else:
					pass
			else:
				failure("KEY INVALID!!")
		else:
			messagebox.showwarning("Not found",str(filename)+" doesn't exist. Try again")
	else:
		messagebox.showwarning("filename","File name is compulsory")


def open_as_it_is():
	filename=simpledialog.askstring("File name","Enter FILE NAME to decrypt:")
	if filename:
		if is_file_exists(filename):
			content=read_from_file(filename)
			show_content(content)
		else:
			messagebox.showwarning("Not found",str(filename)+" doesn't exist. Try again")
	else:
		messagebox.showwarning("filename","File name is compulsory")

def delete_file(fname=False):
	filename=fname
	if not fname:
		filename=simpledialog.askstring("Delete","Enter FILE NAME to DELETE:")
	if filename:
		if is_file_exists(filename):
			x=True
			if not fname:
				x=messagebox.askyesno("Delete","Are you sure you want to delete "+filename+"?",icon="warning")
			if x:
				remove("userfiles/"+filename+".txt")
				listfiles()
			else:
				pass
		else:
			messagebox.showwarning("Not found",str(filename)+" doesn't exist. Try again")
	else:
		messagebox.showwarning("filename","File name is compulsory")





top_frame=Frame(home,borderwidth=4,relief=RIDGE)
top_frame.pack(side=TOP,fill=X)
Label(top_frame,text="En-De-Cryptor",font="comicsansms 25 bold",fg="#fefefe",bg="#232323",padx=4,pady=5,height=2).pack(side=TOP,fill=X)

side_frame=Frame(home,width=210,bg="#e5e5e5",borderwidth=2,relief=RAISED)
side_frame.pack(fill=Y,side=LEFT)

encrypt_btn=Button(side_frame,text="Encrypt",font="helvetica 16 ",bg="#4584a8",fg="white",padx=60,pady=1,command=perform_encryption)
encrypt_btn.pack(padx=10,pady=6,fill=X,side=TOP)

decrypt_btn=Button(side_frame,text="Decrypt",font="helvetica 16 ",bg="#45b864",fg="white",padx=60,pady=1,command=perform_decryption)
decrypt_btn.pack(padx=10,pady=6,fill=X)

open_btn=Button(side_frame,text="Open",font="helvetica 16 ",bg="#d5c854",fg="white",padx=60,pady=1,command=open_as_it_is)
open_btn.pack(padx=10,pady=6,fill=X)

dlt_btn=Button(side_frame,text="Delete",font="helvetica 16 ",bg="#857854",fg="white",padx=60,pady=1,command=delete_file)
dlt_btn.pack(padx=10,pady=6,fill=X)

text_box=Text(home,font="comicsansms 14")
text_box.insert(INSERT,"")
text_box.pack(expand=True,fill='both')

list_frame=Frame(side_frame,bg="#e8e8e8",borderwidth=2,relief=RIDGE)
list_frame.pack(expand=True,fill='both',side=BOTTOM,pady=10,padx=4)


Label(list_frame,text="List of Files:",font="comicsansms 14 bold",bg="#454545",fg="#fefefe").pack(fill=X,side=TOP)
def listfiles():
	global m

	while m:
		m[0].destroy()
		m.pop(0)
		
	for i in listdir("userfiles"):
		m.append(Label(list_frame,text=i,font="comicsansms 14",bg="#e8e8e8"))
	for i in m:
		i.pack(padx=2,fill=X,pady=1)
listfiles()


def on_closing():
	if messagebox.askokcancel("Quit","Do you want to quit?",icon="warning"):
		home.destroy()


home.protocol("WM_DELETE_WINDOW", on_closing)


home.mainloop()

