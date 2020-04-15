import random
from hashlib import md5
from getpass import getpass
import pickle
import subprocess as sp

def randomPass():
	def randomString():
		letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		return ''.join(random.choice(letters) for i in range(4))
	def randomNum():
		return ''.join(str(random.randint(0,9)) for i in range(4))
	return randomString()+'@'+randomNum()

def Inscription():
	def Inscription_():
		Lname=input("Saisir votre nom: ").upper()
		Fname=input("Saisir votre prénom: ").upper()
		All=Lname+':'+Fname+':'
		F=open('personnes.txt','a')
		F.close()
		F=open('personnes.txt','r')
		for line in F:
			l=line.split(':')
			if (l[0]==Lname) and (l[1]==Fname):
				F.close()
				return False
		F.close()
		F=open('personnes.txt','a')
		F.write(All)
		F.close()
		return True
	if(Inscription_()==False) :
		print("vous etes deja inscrit.")
		return False
	F=open('personnes.txt','r+')
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
	print("inscription réussie\nVoici vos informations:\nLogin:",code,"\tPassword:",paswd)

def Liste_Candidat():
	F=open('candidats.txt','r')
	print("Liste des candidats: ")
	i=1
	for line in F:
		l=line.split(':')
		l[-1]=l[-1][0:-1]
		print(l[0],"-->",l[1],l[2])
		i+=1
	print('C'+str(i),"--> blanc\n")
	F.close()

def test_in(choice):
	c=[]
	C=open('candidats.txt','r')
	i=1
	for line in C:
		i+=1
		b=line.split(':')
		c.append(b[0])
	c.append('C'+str(i))
	C.close()
	if(choice not in c) :
		return False
	return True

def Vote():
	code=input("Saisir votre code(E...): ").upper()
	paswd=str(md5(getpass().encode()).hexdigest())
	#paswd=str(md5(input("Saisir votre Mot de Passe: ").encode()).hexdigest()) 
	F=open('personnes.txt','a')
	F.close()
	F=open('personnes.txt','r+')
	lines=""
	u=0
	for line in F:
		l=line.split(':')
		if(l[-3]==code) and (l[-2]==paswd) :
			u=1
			print("Bienvenue",l[1],l[0])
			l[-1]=l[-1][0:-1]
			if(l[-1]!='OK') :
				return False
			Liste_Candidat()
			choice=input("quelle est votre choix? ").upper()
			while(test_in(choice)!=True) :
				choice=input("le choix que vous avez entré ne correspond a aucun code des candidats veuillez rentrez votre choix! ").upper()
			sure=input("Confirmer votre choix (Y/N): ").upper()
			while(sure!='Y') :
				if(sure == 'N') :
					choice=input("quelle est votre choix? ").upper()
					while(test_in(choice)!=True) :
						choice=input("le choix que vous avez entré ne correspond a aucun code des candidats veuillez rentrez votre choix! ").upper()
					sure=input("Confirmer votre choix (Y/N): ").upper()
				else:
					sure=input("Confirmer votre choix (Y/N): ").upper()
			l[-1]='NO'
			line=':'.join(l)+'\n'
			A=open('result.bin','rb')
			mypick=pickle.Unpickler(A)
			D=mypick.load()
			A.close()
			D[choice]+=1

			A=open('result.bin','wb')
			mypick2=pickle.Pickler(A)
			mypick2.dump(D)
			A.close()
		lines=lines+line
	if(u==0) :
		print("code ou mot de passe incorrecte!")
	F.close()
	F=open('personnes.txt','w')
	F.write(lines)
	F.close()

def Statistiques():
	print("Résultat de l'élection: ")
	A=open('result.bin','rb')
	mypick=pickle.Unpickler(A)
	D=mypick.load()
	A.close()
	n=0
	for k in D:
		n+=D[k]
	if(n==0) :
		n=1
	A=open('candidats.txt','r')
	i=1
	for lin in A:
		a=lin.split(':')
		print(a[1],a[2][0:-1],"-->",D['C'+str(i)],"votes",D['C'+str(i)]*100/n,"%")
		i+=1
	A.close()
	print("blanc -->",D['C'+str(i)],"votes",D['C'+str(i)]*100/n,"\n")

def clear_():
	D=Dic_candidat()
	A=open('result.bin','wb')
	mypick2=pickle.Pickler(A)
	mypick2.dump(D)
	A.close()
	F=open('personnes.txt','r+')
	lines=""
	for line in F:
		l=line.split(':')
		l[-1]='OK'
		line=':'.join(l)+'\n'
		lines=lines+line
	F.close()
	F=open('personnes.txt','w')
	F.write(lines)
	F.close()

def Dic_candidat():
	c=[]
	C=open('candidats.txt','r')
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

def prcp():
	print("1)- Inscription\n2)- Liste codes --> candidat\n3)- Voter\n4)- Statistiques\n5)- Clear Result\n6)- Quitter")
	n=input()
	while(n!='6') :
		if(n=='1') :
			Inscription()
			input("\nappuyer sur ENTRER !!")
		elif(n=='2'):
			Liste_Candidat()
			input("\nappuyer sur ENTRER !!")
		elif(n=='3'):
			if(Vote()==False) :
				print("vous avez deja voté!!! ")
			input("\nappuyer sur ENTRER")
		elif(n=='4'):
			Statistiques()
			input("\nappuyer sur ENTRER !!")
		elif(n=='5'):
			clear_()
		else:
			print("veuillez entrer votre choix correctement !!!")
			for i in range(99999999):
				pass
		sp.call('cls',shell=True)
		print("1)- Inscription\n2)- Liste codes --> candidat\n3)- Voter\n4)- Statistiques\n5)- Clear Result\n6)- Quitter")
		n=input()

prcp()
