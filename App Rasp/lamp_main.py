import threading
import time
from bluetooth import *
import select

USER_MAX_CONNECT = 5

TIME_VF_THREAD = 5

TIME_OUT_SOCK = 7200

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

def connection_bluetooth(client_sock):

	client_sock.setblocking(0)

	while True:
		data = ""
		try:
			ready = select.select([client_sock], [], [], TIME_OUT_SOCK)
			if ready[0]:
				data = client_sock.recv(3)
			if len(data) == 0:
				client_sock.close()
				break
			print "received [%s]" % data
			if data == 'oi':
				print("call function here")
			elif data == 'qui':
				client_sock.close()
				break
			else:
				print("MSG ERROR!")

		except IOError:
			client_sock.close()
			break

		except KeyboardInterrupt:
			client_sock.close()
			break



def main():
	
	thread_list = []
	sock_client_list = []
	try:
		while True:  

			print ("Waiting for connection on RFCOMM channel %d" % port)

			client_sock, client_info = server_sock.accept()
			t = threading.Thread(target=connection_bluetooth, args=(client_sock,))
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
		
		for i in thread_list:
			if not(i.is_alive()):
				index = thread_list.index(i)
				thread_list.remove(i)
				del sock_client_list[index]
				print("Thread finished")

		for i in sock_client_list:
			i.close()
		server_sock.close()

if __name__ == '__main__':
    main()