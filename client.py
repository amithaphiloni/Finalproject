import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# --- Design Constants (Dark Mode Theme) ---
DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#BB86FC'
WHITE = 'white'
FONT = ("Helvetica", 12)
BUTTON_FONT = ("Helvetica", 10, "bold")
SMALL_FONT = ("Helvetica", 10)


class GUIChatClient:
    def __init__(self, master):
        self.root = master
        self.root.title("Python Chat Messenger")
        self.root.geometry("600x550")  # הגדלנו קצת את הגובה ההתחלתי
        self.root.resizable(True, True)  # תיקון 1: מאפשר לשנות גודל חלון עם העכבר

        # Network variables
        self.client_socket = None
        self.username = ""
        self.target_ip = '127.0.0.1'
        self.target_port = 55555

        # --- Login Frame ---
        self.login_frame = tk.Frame(self.root, bg=DARK_GREY)
        self.login_frame.pack(fill="both", expand=True)

        tk.Label(self.login_frame, text="Welcome to Chat", font=("Helvetica", 24, "bold"), bg=DARK_GREY,
                 fg=OCEAN_BLUE).pack(pady=50)

        tk.Label(self.login_frame, text="Enter Username:", font=FONT, bg=DARK_GREY, fg=WHITE).pack(pady=5)
        self.username_entry = tk.Entry(self.login_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, insertbackground='white')
        self.username_entry.pack(pady=5, ipadx=50, ipady=5)

        connect_btn = tk.Button(self.login_frame, text="Connect", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=DARK_GREY,
                                command=self.connect_to_server)
        connect_btn.pack(pady=20, ipadx=20)

        # --- Chat Frame (Hidden initially) ---
        self.chat_frame = tk.Frame(self.root, bg=DARK_GREY)

        # Input Area (Pinned to bottom)
        input_frame = tk.Frame(self.chat_frame, bg=DARK_GREY)
        input_frame.pack(side=tk.BOTTOM, fill="x", padx=10, pady=10)

        tk.Label(input_frame, text="Format: 'Name: Message'", font=SMALL_FONT, bg=DARK_GREY, fg="gray").pack(anchor="w")

        self.msg_entry = tk.Entry(input_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, insertbackground='white')
        self.msg_entry.pack(side="left", fill="x", expand=True, ipady=5)
        self.msg_entry.bind("<Return>", self.send_message)

        send_btn = tk.Button(input_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=DARK_GREY,
                             command=self.send_message)
        send_btn.pack(side="right", padx=5, ipadx=10)

        # Message Display Area (Fills the rest)
        self.chat_area = scrolledtext.ScrolledText(self.chat_frame, bg=MEDIUM_GREY, fg=WHITE, font=FONT,
                                                   state='disabled')
        self.chat_area.pack(side=tk.TOP, padx=10, pady=10, fill="both", expand=True)

        # Handle window closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def connect_to_server(self):
        """Attempts to establish a connection to the server."""
        user = self.username_entry.get()
        if not user:
            messagebox.showerror("Error", "Please enter a username")
            return

        self.username = user

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.target_ip, self.target_port))

            self.client_socket.send(self.username.encode('utf-8'))

            self.login_frame.pack_forget()
            self.chat_frame.pack(fill="both", expand=True)

            self.add_message(f"[System] Connected as {self.username}")
            threading.Thread(target=self.listen_for_messages, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server:\n{e}")

    def listen_for_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.add_message(message)
                else:
                    break
            except:
                break
        self.add_message("[System] Disconnected from server.")
        if self.client_socket:
            self.client_socket.close()

    def send_message(self, event=None):
        msg = self.msg_entry.get()
        if msg:
            try:
                self.client_socket.send(msg.encode('utf-8'))
                self.msg_entry.delete(0, tk.END)
            except Exception as e:
                self.add_message(f"[Error] Failed to send: {e}")

    def add_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.see(tk.END)
        self.chat_area.config(state='disabled')

    def on_closing(self):
        if self.client_socket:
            self.client_socket.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GUIChatClient(root)
    root.mainloop()