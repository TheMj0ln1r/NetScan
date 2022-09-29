import subprocess
import re
from platform import system
import socket
from banner import *
banner()


def webip():
	print("Make sure you have an active internet connection..")
	url = input("\tEnter website url : ")
	try:
		if 	"Linux" in system():
			p = subprocess.check_output(["ping","-c","2",url])
		if "Windows" in system():
			p = subprocess.check_output(["ping","-n","2",url])
		ip = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',str(p))
		print("\tThe IP address of the "+url+" is "+ip[0])
	except subprocess.CalledProcessError:
		print("\n\tWebsite Not found..")


def pingscan():
	hip = input("Enter your IP address : ")
	start = int(input("Enter start host number : "))
	stop = int(input("Enter end host number : "))
	hip = hip.split(".")
	hip = ".".join(hip[0:3])+"."
	print("\nPerforming Pingscan please wait...\n")
	try:
		if "Linux" in system():
			livehosts = []
			for i in range(start,stop):
				ip = hip+str(i)
				p = subprocess.run(["ping","-c","1",ip],capture_output=True,text=True)
				if p.returncode == 0:
					print(ip+" is active")

		if "Windows" in system():
			livehosts = []
			for i in range(start,stop):
				ip = hip+str(i)
				p = subprocess.run(["ping","-n","1",ip],capture_output=True,text=True)
				if p.returncode == 0:
					print(ip+" is active")

	except subprocess.CalledProcessError:
		print("Something went wrong.. Check your network connection and try again..")

def tcpscan():
	hip = input("Enter your IP address : ")
	start = int(input("Enter start host number : "))
	stop = int(input("Enter end host number : "))
	hip = hip.split(".")
	hip = ".".join(hip[0:3])+"."
	print("\nPerforming TCPscan please wait...\n")
	for i in range(start,stop):
		ip = hip + str(i)
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		socket.setdefaulttimeout(1)
		out = s.connect_ex((ip,135))
		if out == 0 :
			print(ip+" is live")

def macscan():
	print("\nPerforming MAC scan..\n")
	p = subprocess.Popen(["arp","-e"],stdout = subprocess.PIPE)
	for i in p.stdout.readlines():
		if b"incomplete" not in i:
			print(i)

print("""
1> Get any websites IP address \n
2> Discover live hosts [slow scan]\n
3> Discover live hosts [Fast scan]\n
4> Discover hosts and their MAC addresses \n
0> Exit\n
""")
choice = int(input("Enter  (0/1/2/3) : "))

if choice == 1:
	webip()

elif choice == 2:
	pingscan()
elif choice == 3:
	tcpscan()
elif choice == 4:
	macscan()
elif choice == 0:
	print("Terminating....")
	exit()