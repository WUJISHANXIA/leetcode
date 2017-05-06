import socket, sys, select, SocketServer, struct, time
class ThreadingTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
class Socks5Server(SocketServer.StreamRequestHandler):
    passdct = {"123":"456"};
    iplist = ['127.0.0.1'];
    def handle_tcp(self, sock, remote):
        fdset = [sock, remote]
        while True:
            r, w, e = select.select(fdset, [], [])
            if sock in r:
                if remote.send(sock.recv(4096)) <= 0: break
            if remote in r:
                if sock.send(remote.recv(4096)) <= 0: break

    def auth_user_pass(self, user, passwd):
        dic = self.__class__.passdct
        return dic.has_key(user) and passwd == self.__class__.passdct[user];


    def handle(self):
        try:
            print 'socks connection from ', self.client_address, self.__class__.iplist
            sock = self.connection
            # 1. Version
            data = sock.recv(262) # no auth, \x05\x01\x00
                                  # user/passwd auth, \x05\x03\x00\x03\x02


            if self.client_address[0] in self.__class__.iplist:
                reply = b"\x05\x00"   # no auth and ok
            else:
                reply = b"\x05\xff"

            if len(data) == 5:
                sock.send(b"\x05\x02");
                # 2. append user/passwd
                data = self.rfile.read(2)
                username = self.rfile.read(ord(data[1]))
                passwd = self.rfile.read(ord(sock.recv(1)[0]))
                # auth it
                if self.auth_user_pass(username, passwd):
                    reply = b"\x01\x00"
                else:
                    reply = b"\x01\x01"

            sock.send(reply)

            # 3. Request
            data = self.rfile.read(4)
            mode = ord(data[1])
            addrtype = ord(data[3])
            if addrtype == 1:       # IPv4
                addr = socket.inet_ntoa(self.rfile.read(4))
            elif addrtype == 3:     # Domain name
                addr = self.rfile.read(ord(sock.recv(1)[0]))

            port = struct.unpack('>H', self.rfile.read(2))
            reply = b"\x05\x00\x00\x01"
            try:
                if mode == 1:  # 1. Tcp connect
                    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    remote.connect((addr, port[0]))
                    print 'Tcp connect to', addr, port[0]
                else:
                    reply = b"\x05\x07\x00\x01" # Command not supported
                local = remote.getpeername()
                print "reply addr:", local
                reply += socket.inet_aton(local[0]) + struct.pack(">H", local[1])
                sys.stdout.flush()

            except socket.error:
                print 'socket error'
                # Connection refused
                reply = '\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00'
            sock.send(reply)
            # 4. Transfering
            if reply[1] == '\x00':  # Success
                if mode == 1:    # 1. Tcp connect
                    self.handle_tcp(sock, remote)
        except socket.error:
            print 'socket error'

def main():
    server = ThreadingTCPServer(('', 1080), Socks5Server)
    server.serve_forever()
if __name__ == '__main__':
    main()