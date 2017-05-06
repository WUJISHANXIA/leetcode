# -*- coding:utf-8 -*-
# author : wujishanxia 2017.4.9
import socket,struct
import select,string,hashlib
def send_all(sock, data):
    bytes_sent = 0
    while True:
        r = sock.send(data[bytes_sent:])
        if r < 0:
            return r
        bytes_sent += r
        if bytes_sent == len(data):
            return bytes_sent
from SocketServer import TCPServer,ThreadingMixIn,StreamRequestHandler
class Server(ThreadingMixIn,TCPServer):
    pass
class Handler(StreamRequestHandler):
    def handle_tcp(self,sock,remote):
        try:
            fdset=[sock,remote]
            while True:
                r, w, e = select.select(fdset, [], [])
                if sock in r:
                    data=sock.recv(4096)
                    if len(data)<=0:
                        break
                    send_bytes=send_all(remote,self.decrypt(data))
                    if send_bytes<len(data):
                        raise Exception('failed to send all data')
                if remote in r:
                    data=remote.recv(4096)
                    if len(data)<=0:
                        break
                    send_bytes=send_all(sock,self.encrypt(data))
                    if send_bytes<len(data):
                        raise Exception('failed to send all data')
                    #print data
        finally:
            sock.close()
            remote.close()
    def encrypt(self,data):
        return data.translate(encrypt_table)
    def decrypt(self,data):
        return data.translate(decrypt_table)
    def send_encrypt_data(self,sock,data):
        sock.send(self.encrypt(data))
    def handle(self):
        try:
            sock=self.connection
            #print sock.getpeername()
            addr_type=ord(self.decrypt(self.rfile.read(1)))
            if addr_type==1:
                addr=self.decrypt(self.rfile.read(4))
                addr_ip=socket.inet_ntoa(addr)
            elif addr_type==3:
                fqdn_len=self.decrypt(self.rfile.read(1))
                addr=self.decrypt(self.rfile.read(ord(fqdn_len)))
            addr_port=self.decrypt(self.rfile.read(2))
            port=struct.unpack('>H',addr_port)
            try:
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #remote.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                remote.connect((addr,port[0]))
            except socket.error, e:
                print e
            self.handle_tcp(sock,remote)
        except socket.error, e:
            print e
def get_table(key):
    m=hashlib.md5()
    m.update(key)
    s=m.digest()
    (a,b)=struct.unpack('<QQ',s)
    table = [c for c in string.maketrans('', '')]
    for i in xrange(1, 1024):
        table.sort(lambda x, y: int(a % (ord(x) + i) - a % (ord(y) + i)))
    return table
if __name__=='__main__':
    config={
        'password':'Root@123',
        'server':'127.0.0.1',
        'port':1088
    }
    encrypt_table=''.join(get_table(config['password']))
    decrypt_table=string.maketrans(encrypt_table,string.maketrans('',''))
    server=Server(('',config['port']),Handler)
    server.serve_forever()