# -*- coding: utf-8 -*-
# author: wujishanxia 2017.4.9
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
                    send_bytes=send_all(remote,self.encrypt(data))
                    if send_bytes<len(data):
                        raise Exception('failed to send all data')
                if remote in r:
                    data=remote.recv(4096)
                    if len(data)<=0:
                        break
                    send_bytes=send_all(sock,self.decrypt(data))
                    if send_bytes<len(data):
                        raise Exception('failed to send all data')
                    #print data
        finally:
            sock.close()
            remote.close()
    def handle(self):
        try:
            sock=self.connection
            #print self.client_address
            sock.recv(262)
            sock.send('\x05\x00')
            data=self.rfile.read(4)
            addr_type=ord(data[3])
            addr_to_send=data[3]
            if addr_type==1:
                addr_ip=self.rfile.read(4)
                addr=socket.inet_ntoa(self.rfile.read(4))
                addr_to_send+=addr_ip
            elif addr_type==3:
                fqdn_len=self.rfile.read(1)
                addr=self.rfile.read(ord(fqdn_len))
                print "domain",addr
                addr_to_send+=fqdn_len+addr
            addr_port=self.rfile.read(2)
            addr_to_send+=addr_port
            port=struct.unpack('>H',addr_port)
            try:
                reply='\x05\x00\x00\x01'
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #remote.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                remote.connect((config['server'],config['port']))
                self.send_encrypt_data(remote,addr_to_send)
                peer=remote.getpeername()
                reply+=socket.inet_aton(peer[0])+struct.pack('>H',peer[1])
                self.wfile.write(reply)
            except socket.error, e:
                print e
            self.handle_tcp(sock,remote)
        except socket.error, e:
            print e
    def encrypt(self,data):
        return data.translate(encrypt_table)
    def decrypt(self,data):
        return data.translate(decrypt_table)
    def send_encrypt_data(self,sock,data):
        sock.send(self.encrypt(data))

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
        'server':'23.83.247.108',
        'port':1088
    }
    encrypt_table=''.join(get_table(config['password']))
    decrypt_table=string.maketrans(encrypt_table,string.maketrans('',''))
    server=Server(('',1080),Handler)
    server.serve_forever()