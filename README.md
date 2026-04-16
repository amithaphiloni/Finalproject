# Final Project - Computer Networks

A TCP-based chat application built with Python, featuring a multi-threaded server and a GUI client. This project also includes HTTP traffic simulation and packet analysis using Wireshark.

## Overview

This project demonstrates core networking concepts through two parts:

1. **HTTP Traffic Simulation** - Generating and analyzing HTTP packets using a Jupyter Notebook and CSV-based scenarios
2. **TCP Chat Application** - A real-time messaging system with a multi-threaded server and a graphical client

## Project Structure

```
Finalproject/
├── server.py                        # Multi-threaded TCP chat server
├── client.py                        # GUI chat client (Tkinter, dark mode)
├── group02_http_input.csv           # HTTP traffic simulation data
├── raw_tcp_ip_notebook_*.ipynb      # Jupyter Notebook for packet creation & analysis
└── עבודה רשתות תקשורת.docx          # Full project documentation (Hebrew)
```

## Features

### TCP Chat Server (`server.py`)
- Multi-client support using Python `threading`
- User login and session management
- Private messaging between connected users (format: `Recipient: Message`)
- Graceful disconnect handling

### GUI Chat Client (`client.py`)
- Dark mode interface built with Tkinter
- Login screen with username input
- Real-time message display with auto-scroll
- Send messages via button or Enter key
- Resizable window

### HTTP Traffic Simulation
- CSV-driven HTTP request/response scenarios (GET, POST, 200, 403)
- Jupyter Notebook for constructing raw TCP/IP packets
- Wireshark capture and analysis (documented in the Word file)

## Setup

### Prerequisites
- Python 3.8+

### Run the Chat Application

**1. Start the server:**
```bash
python server.py
```

**2. Start one or more clients (in separate terminals):**
```bash
python client.py
```

**3. Enter a username and start chatting!**

Message format: `RecipientName: Your message here`

## Technologies

- **Python** - Core language
- **Socket** - TCP networking
- **Threading** - Concurrent client handling
- **Tkinter** - GUI framework
- **Scapy** (in notebook) - Packet crafting
- **Wireshark** - Network traffic analysis

## Author

- [Amit Haphiloni](https://github.com/amithaphiloni)
