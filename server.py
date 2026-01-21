import socket
import threading


class ChatServer:
    def __init__(self, ip, port):
        self.server_ip = ip
        self.server_port = port
        self.server_socket = None
        self.active_users = {}  # Dictionary: username -> socket
        self.running = True

    def start(self):
        """Initializes the server and starts listening."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.server_ip, self.server_port))
            self.server_socket.listen(5)

            print(f"--- Chat Server Running on {self.server_ip}:{self.server_port} ---")

            while self.running:
                client_sock, client_addr = self.server_socket.accept()
                # Start a thread for each new client
                threading.Thread(target=self.handle_client, args=(client_sock, client_addr)).start()

        except Exception as e:
            print(f"[Error] Server failed to start: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()

    def handle_client(self, conn, addr):
        """Handles communication with a single client."""
        print(f"[Log] New connection from: {addr}")
        current_user = None

        try:
            # Login Phase
            current_user = conn.recv(1024).decode('utf-8').strip()
            self.active_users[current_user] = conn
            print(f"[Log] User logged in: {current_user}")

            conn.send(f"Welcome {current_user}. Format: 'Recipient: Message'".encode('utf-8'))

            # Chat Loop
            while True:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break

                if ':' in data:
                    recipient, body = data.split(':', 1)
                    recipient = recipient.strip()
                    self.route_message(current_user, recipient, body, conn)
                else:
                    conn.send("[System] Invalid format.".encode('utf-8'))

        except Exception as e:
            print(f"[Log] Connection lost with {addr}: {e}")
        finally:
            self.disconnect_user(current_user, conn)

    def route_message(self, sender, recipient, body, sender_conn):
        """Logic to forward the message."""
        if recipient in self.active_users:
            try:
                target_socket = self.active_users[recipient]
                formatted_msg = f"@{sender}: {body}"
                target_socket.send(formatted_msg.encode('utf-8'))
            except:
                sender_conn.send(f"[System] Failed to send to {recipient}.".encode('utf-8'))
        else:
            sender_conn.send(f"[System] User '{recipient}' not found.".encode('utf-8'))

    def disconnect_user(self, user, conn):
        """Clean up resources when a user disconnects."""
        if user and user in self.active_users:
            del self.active_users[user]
            print(f"[Log] User {user} disconnected.")
        conn.close()


if __name__ == "__main__":
    server = ChatServer('127.0.0.1', 55555)
    server.start()