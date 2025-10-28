import socket

# --- Configuration ---
HOST = "0.0.0.0"      # Listen on all available network interfaces
PORT = 5000           # Pick any unused port above 1024

# --- Create a TCP/IP socket ---
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)   # Allow 1 queued connection

print(f"[SERVER] Listening on {HOST}:{PORT}...")

# --- Wait for a client to connect ---
conn, addr = server_socket.accept()
print(f"[SERVER] Connected by {addr}")

# --- Communication loop ---
while True:
    data = conn.recv(1024)              # Receive up to 1024 bytes
    if not data:                        # Client closed connection
        break
    print(f"[SERVER] Received: {data.decode()}")
    conn.sendall(b"Message received!")  # Send response

# --- Clean up ---
conn.close()
server_socket.close()
print("[SERVER] Connection closed.")
