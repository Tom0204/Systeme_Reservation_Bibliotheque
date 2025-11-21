import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

clients = []

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.sendall(message)
            except Exception:
                pass

def handle_client(conn, addr):
    print(f"[+] Nouveau client connecté: {addr}")
    while True:
        try:
            msg = conn.recv(1024)
            if not msg:
                break
            texte = msg.decode()
            print(f"[{addr}] {texte}")
            broadcast(msg, conn)
        except Exception:
            break
    print(f"[-] Déconnexion: {addr}")
    clients.remove(conn)
    conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[Serveur lancé sur {HOST}:{PORT}]")
        while True:
            conn, addr = s.accept()
            clients.append(conn)
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
