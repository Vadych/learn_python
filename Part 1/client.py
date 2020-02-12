
import time
import socket

class ClientError (Exception):
    pass

class Client:
    def __init__(self,addr,port,timeout=None):
        self.addr = addr
        self.port=port
        self.timeout=timeout
    
    def put(self,key,val,timestamp=0):
        if not timestamp:
            timestamp=str(int(time.time()))
        with socket.create_connection((self.addr,self.port), self.timeout) as sock:
            try:
                sock.sendall ("put {0} {1} {2}\n".format(key,val,timestamp).encode('utf-8'))
                ans=sock.recv(1024).decode('utf-8')
            except socket.error:
                raise ClientError()


            if not ans.startswith("ok\n\n"):
                raise ClientError()

          
                
    def get (self, key):
        with socket.create_connection((self.addr,self.port), self.timeout) as sock:
            try:
                sock.sendall ("get {0}\n".format(key).encode('utf-8'))
                ans=sock.recv(1024).decode('utf-8')
            except socket.error:
                raise ClientError()

            if not ans.startswith('ok\n'):
                raise ClientError()

        return parse_answer(ans)

    def echo(self):
        with socket.create_connection((self.addr,self.port), self.timeout) as sock:
            try:
                while True:
                    str=input('комманда ')
                    sock.sendall (str.encode('utf-8'))
                    print(sock.recv(1024))
            except socket.error:
                raise ClientError()

def parse_answer(answer):
    parse_ans={}
    if not answer.startswith('ok\n\n'):
        for metric in answer[3:-1].splitlines():
            key,val, time_stamp=metric.split(' ')
            val=float(val)
            time_stamp=int(time_stamp)
            if key in parse_ans:
                parse_ans[key].append((time_stamp,val))
            else:
                parse_ans[key]=[(time_stamp,val)]
        for k in parse_ans:
            parse_ans[k]=sorted(parse_ans[k], key=lambda x:x[0])
    return parse_ans

if __name__ == '__main__':
    c=Client("127.0.0.1",8888)
    c.put('k1',0.25,1)
    c.put ('k1', 2.45,2)
    c.put('k1',3.54,4)
    c.put('k1',5.6,3)
    c.put('k2',1.4,4)
    c.put('k2',2, 5)
    c.put('k2',3,5)

    c.echo()