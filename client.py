import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024)
            if msg:
                print(f"\nMessage reçu: {msg.decode()}")
            else:
                break
        except Exception:
            break

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connecté au serveur de discussion sur {HOST}:{PORT}")
        pseudo = input("Choissisez un pseudo : ")
        s.sendall(f"[{pseudo}] a rejoint le chat".encode())
        threading.Thread(target=receive_messages, args=(s,), daemon=True).start()
        while True:
            msg = input("> ")
            if msg:
                s.sendall(f"[{pseudo}] {msg}".encode())
            else:
                break

if __name__ == "__main__":
    start_client()