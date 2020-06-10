from threading import Thread
import time
from bluetooth import *

USER_MAX_CONNECT = 5

TIME_VF_THREAD = 5

server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "LampRasp",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
                    )

class connection_bluetooth(Thread):

	def __init__ (self):
		Thread.__init__(self)
	def run(self):
		while True:
			try:
				data = client_sock.recv(3)
				if len(data) == 0: break
				print "received [%s]" % data

				if data == 'oi':
					print("FUNCIONA!!!!!")
				elif data == 'kk':
					print("FUNCIONA DE MAIS MANO!!!!")
				elif data == 'qui':
					break
				else:
					print("sla")

			except IOError:
				break

			except KeyboardInterrupt:
				break
		


def main():
	
	thread_list = []
	sock_client_list = []
	try:
		while True:  

			print ("Waiting for connection on RFCOMM channel %d" % port)

			client_sock, client_info = server_sock.accept()
			
			t = connection_bluetooth()
			t.start()

			thread_list.append(t)
			sock_client_list.append(client_sock)

			for i in thread_list:
				if not(i.is_alive()):
					index = thread_list.index(i)
					thread_list.remove(i)
					del sock_client_list[index]
					print("Thread finished")

			while len(thread_list) >= USER_MAX_CONNECT:
				print ("Waiting for a connection to finish")
				for i in thread_list:
					if not(i.is_alive()):
						index = thread_list.index(i)
						thread_list.remove(i)
						del sock_client_list[index]
						print("Thread finished")
				time.sleep(TIME_VF_THREAD)


			print ("Accepted connection from ", client_info)

	except KeyboardInterrupt:
		for i in sock_client_list:
			i.close()
		server_sock.close()

if __name__ == '__main__':
    main()