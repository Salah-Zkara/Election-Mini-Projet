import random
from hashlib import md5
import pickle
from tkinter import *
from PIL import ImageTk, Image
import tkinter.messagebox

def randomPass():
	def randomString():
		letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		return ''.join(random.choice(letters) for i in range(4))
	def randomNum():
		return ''.join(str(random.randint(0,9)) for i in range(4))
	return randomString()+'@'+randomNum()

def Inscription():
	def Inscription_(Lname,Fname):
		Lname=Lname.upper()
		Fname=Fname.upper()
		All=Lname+':'+Fname+':'
		F=open('./.resources/personnes.txt','a')
		F.close()
		F=open('./.resources/personnes.txt','r')
		for line in F:
			l=line.split(':')
			if (l[0]==Lname) and (l[1]==Fname):
				F.close()
				return False
		F.close()
		F=open('./.resources/personnes.txt','a')
		F.write(All)
		F.close()
		return True
	def click():
		Lname=textentry1.get()
		Fname=textentry2.get()
		if(Inscription_(Lname,Fname)==False) :
			tkinter.messagebox.showinfo("ALERT!!","vous etes deja inscrit!")
			window2.destroy()
		else:
			F=open('./.resources/personnes.txt','r+')
			i=0
			for line in F:
				i+=1
			if(i<10) :
				code='E00'+str(i)
			elif(i<100):
				code='E0'+str(i)
			else:
				code='E'+str(i)

			paswd=randomPass()
			F.write(code+':'+ str(md5(paswd.encode()).hexdigest())+':'+'OK'+'\n')
			F.close()
			window4= Tk()
			window4.geometry("250x100")
			window4.title("INFO!!")
			window4.resizable(0,0)
			window4.configure(background=background_color)
			Label(window4,text="inscription réussie",bg=background_color).pack()
			output= Text(window4,width=25,height=10,wrap=WORD,background=background_color)
			output.pack()
			m="Login: "+code+"\nPassword: "+paswd
			output.insert(END,m)
			window2.destroy()
			#window4.iconbitmap('./.resources/Team-Male.ico')
			window4.mainloop()
	window2 =Tk()
	window2.title("Inscription")
	window2.configure(background="#32a6a8")
	window2.geometry("270x180")
	window2.resizable(0, 0)
	#window2.iconbitmap('./.resources/Team-Male.ico')
	Label(window2,text="Nom:",bg=background_color).place(x=10,y=10)
	textentry1= Entry(window2,bg="white",width=38)
	textentry1.place(x=10,y=30)
	Label(window2,text="Prenom:",bg=background_color).place(x=10,y=60)
	textentry2= Entry(window2,bg="white",width=38)
	textentry2.place(x=10,y=80)
	Button(window2,font="none 9 italic",fg="white",bg="black",text="Sign Up",command=click).place(x=190,y=120)
	window2.mainloop()

def Liste_Candidat():
	F=open('./.resources/candidats.txt','r')
	i=1
	R=""
	for line in F:
		l=line.split(':')
		l[-1]=l[-1][0:-1]
		R+=l[0]+" -->  "+l[1]+" "+l[2]+'\n'
		i+=1
	R+='C'+str(i)+" -->  blanc\n"
	tkinter.messagebox.showinfo("Liste des candidats",R)
	return i
	F.close()

def Statistiques():
	A=open('./.resources/result.bin','rb')
	mypick=pickle.Unpickler(A)
	D=mypick.load()
	A.close()
	n=0
	for k in D:
		n+=D[k]
	if(n==0) :
		n=1
	A=open('./.resources/candidats.txt','r')
	i=1
	R=""
	for lin in A:
		a=lin.split(':')
		R+=a[1]+" "+a[2][0:-1]+"  --> "+str(D['C'+str(i)])+" votes "+str(D['C'+str(i)]*100/n)+"%"+'\n'
		i+=1
	A.close()
	R+="blanc  --> "+str(D['C'+str(i)])+" votes "+str(D['C'+str(i)]*100/n)+"\n"
	tkinter.messagebox.showinfo("Statistiques",R)

def Vote():
	radio_var=StringVar()
	def click1():
		code=textentry1.get().upper()
		paswd=str(md5(textentry2.get().upper().encode()).hexdigest())
		window3.destroy()
		F=open('./.resources/personnes.txt','a')
		F.close()
		F=open('./.resources/personnes.txt','r+')
		lines=""
		u=0
		for line in F:
			l=line.split(':')
			if(l[-3]==code) and (l[-2]==paswd) :
				u=1
				tkinter.messagebox.showinfo("INFO","Bienvenue "+l[1]+" "+l[0])
				l[-1]=l[-1][0:-1]
				if(l[-1]!='OK') :
					tkinter.messagebox.showinfo("ALERT!!","vous avez deja voté!!! ")
					return False
				l[-1]='NO'
				line=':'.join(l)+'\n'
				def click2():
					window5.destroy()
					A=open('./.resources/result.bin','rb')
					mypick=pickle.Unpickler(A)
					D=mypick.load()
					A.close()
					choice=v.get()
					D[choice]+=1
					A=open('./.resources/result.bin','wb')
					mypick2=pickle.Pickler(A)
					mypick2.dump(D)
					A.close()
					tkinter.messagebox.showinfo("ALERT!!","Merci pour votre vote!")
					q=open('./.resources/personnes.txt','w')
					q.write(lines)
					q.close()
			lines=lines+line
		if(u==0) :
			tkinter.messagebox.showinfo("ALERT!!","code ou mot de passe incorrecte!")
			return False
		n=Liste_Candidat()
		window5 = Tk()
		window5.resizable(0, 0)
		window5.title("Vote")
		#window5.iconbitmap('./.resources/vote.ico')
		window5.configure(background=background_color)
		#window5.geometry("225x200")
		Label(window5,text="veuillez votez pour votre candidat",bg=background_color).pack()
		values={}
		for i in range(1,n+1):
			C='C'+str(i)
			values[C]=C

		v = StringVar(window5, "1") 
		for (text, value) in values.items(): 
		    Radiobutton(window5,bg=background_color, text = text, variable = v, value = value).pack(side = TOP, ipady = 5) 
		Button(window5,font="none 9 italic",fg="white",bg="black",text="VOTE",command=click2).pack()
		F.close()
		window5.mainloop()

	window3 = Tk()
	window3.resizable(0, 0)
	window3.title("Login")
	#window3.iconbitmap('./.resources/Team-Male.ico')
	window3.configure(background=background_color)
	window3.geometry("225x150")
	Label(window3,text="Saisir votre code(E...):",bg=background_color).place(x=20,y=10)
	textentry1= Entry(window3,bg="white",width=30)
	textentry1.place(x=20,y=30)
	Label(window3,text="Password:",bg=background_color).place(x=20,y=60)
	textentry2= Entry(window3,show='*',bg="white",width=30)
	textentry2.place(x=20,y=80)
	Button(window3,font="none 9 italic",fg="white",bg="black",text="Submit",command=click1).place(x=90,y=120)
	window3.mainloop()

def Dic_candidat():
	c=[]
	C=open('./.resources/candidats.txt','r')
	i=1
	for line in C:
		i+=1
		b=line.split(':')
		c.append(b[0])
	c.append('C'+str(i))
	C.close()
	D={}
	for e in c:
		D[e]=0
	return D

def clear_():
	D=Dic_candidat()
	A=open('./.resources/result.bin','wb')
	mypick2=pickle.Pickler(A)
	mypick2.dump(D)
	A.close()
	F=open('./.resources/personnes.txt','r+')
	lines=""
	for line in F:
		l=line.split(':')
		l[-1]='OK'
		line=':'.join(l)+'\n'
		lines=lines+line
	F.close()
	F=open('./.resources/personnes.txt','w')
	F.write(lines)
	F.close()
	tkinter.messagebox.showinfo("ALERT!!","Les résultats sont mis à zéro.\ntous les membres puissent voter à nouveau!!")

def load():
	D=Dic_candidat()
	A=open('./.resources/result.bin','rb')
	mypick=pickle.Unpickler(A)
	D1=mypick.load()
	A.close()
	D.update(D1)
	A=open('./.resources/result.bin','wb')
	mypick2=pickle.Pickler(A)
	mypick2.dump(D)
	A.close()

def prcp_gui(background_color):
	load()
	#window.resizable(0, 0)
	Button(window,font=button_font,fg="white",bg=button_color,width=20,text="Inscription",command=Inscription).place(x=20,y=170)
	Button(window,font=button_font,fg="white",bg=button_color,width=20,text="Liste codes --> candidat",command=Liste_Candidat).place(x=420,y=170)
	Button(window,font=button_font,fg="white",bg=button_color,width=20,text="Voter",command=Vote).place(x=20,y=220)
	Button(window,font=button_font,fg="white",bg=button_color,width=20,text="Statistiques",command=Statistiques).place(x=420,y=225)
	Button(window,font=button_font,fg="white",bg=button_color,width=20,text="Clear Result",command=clear_).place(x=220,y=280)

background_color="#32a6a8"
button_color="#576161"
button_font="none 12 bold"
window = Tk()
window.geometry("653x350")
window.title("Election 2020 by ZKARA(©)")
window.configure(background=background_color)
#window.iconbitmap('./.resources/vote.ico')
imge=Image.open("./.resources/Team Male.png")
photo=ImageTk.PhotoImage(imge)
lab=Label(image=photo,bg=background_color)
lab.place(x=272,y=20)
prcp_gui(background_color)
window.mainloop()
