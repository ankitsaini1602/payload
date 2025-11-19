#!/usr/bin/env python3
import socket
import sys
import threading
import time

def receive_messages(sock):
    """Receive and display messages from server"""
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                print("\n[*] Connection closed by server")
                break
            print(data.decode('utf-8'), end='')
        except:
            break

def start_client(server_ip, server_port=4444):
    """Connect to the VPS server"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print(f"[*] Connecting to {server_ip}:{server_port}...")
        client.connect((server_ip, server_port))
        print("[+] Connected to server!")
        print("[*] Type your commands (use 'exit' or 'quit' to disconnect)\n")
        # Handle authentication
auth_prompt = client.recv(1024).decode('utf-8')
if "password" in auth_prompt.lower():
    password = input(auth_prompt)
    client.send(f"{password}\n".encode('utf-8'))
    auth_result = client.recv(1024).decode('utf-8')
    print(auth_result, end='')
    if "failed" in auth_result.lower():
        client.close()
        return
        # Start thread for receiving messages
        receiver = threading.Thread(target=receive_messages, args=(client,))
        receiver.daemon = True
        receiver.start()
        
        # Main loop for sending commands
        while True:
            try:
                command = input()
                client.send(f"{command}\n".encode('utf-8'))
                
                if command.lower() in ['exit', 'quit']:
                    time.sleep(0.5)
                    break
                    
            except KeyboardInterrupt:
                print("\n[*] Disconnecting...")
                client.send(b"exit\n")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                break
                
    except ConnectionRefusedError:
        print("[-] Connection refused. Make sure the server is running.")
    except Exception as e:
        print(f"Connection error: {str(e)}")
    finally:
        client.close()
        print("[-] Disconnected")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 local_client.py <SERVER_IP> [PORT]")
        print("Example: python3 local_client.py 192.168.1.100 4444")
        sys.exit(1)
    
    SERVER_IP = sys.argv[1]
    PORT = 4444
    
    if len(sys.argv) > 2:
        try:
            PORT = int(sys.argv[2])
        except ValueError:
            print("Invalid port number. Using default port 4444")
    
    start_client(SERVER_IP, PORT)
