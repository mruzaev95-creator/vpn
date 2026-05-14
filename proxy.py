import socket, threading

def handle(c):
    try:
        d = c.recv(4096)
        if not d: c.close(); return
        l = d.split(b'\r\n')[0].decode()
        if l.startswith('CONNECT'):
            h, p = l.split()[1].split(':')
            r = socket.create_connection((h, int(p)), 15)
            c.send(b'HTTP/1.1 200 Connection Established\r\n\r\n')
            def f(a,b):
                try:
                    while True:
                        x = a.recv(8192)
                        if not x: break
                        b.sendall(x)
                except: pass
            t1 = threading.Thread(target=f, args=(c, r)); t1.daemon = True
            t2 = threading.Thread(target=f, args=(r, c)); t2.daemon = True
            t1.start(); t2.start(); t1.join(); t2.join()
        else:
            c.send(b'HTTP/1.1 200 OK\r\n\r\nProxy OK'); c.close()
    except: pass

s = socket.socket(); s.setsockopt(1, 2, 1); s.bind(('0.0.0.0', 10000)); s.listen(20)
print("Proxy on port 10000")
while True:
    c, a = s.accept()
    threading.Thread(target=handle, args=(c,)).start()