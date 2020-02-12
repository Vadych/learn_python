import asyncio


class ClientServerProtocol(asyncio.Protocol):
    data={}
    def connection_made(self, transport):
        self.transport = transport

    @classmethod
    def set_data(cls,key,value,timestamp):
        if not key in cls.data:
            cls.data[key]=[]
        for i in range(len(cls.data[key])):
            if cls.data[key][i][0]==timestamp:
                del cls.data[key][i]
                break
        cls.data[key].append((timestamp,value))
        cls.data[key]=sorted(cls.data[key],key=lambda x:x[0])

    @classmethod
    def get_data(cls,key):
        ans="ok\n"
        key=key[:-1]
        if key=="*":
            for k in cls.data:
                ans +=cls.key_to_str(k)
        elif key in cls.data:
            ans+=cls.key_to_str(key)
        ans+='\n'
        return ans

    @classmethod
    def key_to_str(cls,key):
        key_str=''
        for metr in cls.data[key]:
            key_str+="{0} {1} {2}\n".format(key, metr[1],metr[0])
        return key_str

    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())

def process_data(str):
    ans=com_serv=param=''
    try:
        com_serv,param=str.split(maxsplit=1)
    except ValueError:
        ans = "error\nwrong command\n\n"

    if com_serv=="put":
        try:
            key, value,t=param.split()
            value=float(value)
            t=int(t)
            ans="ok\n\n"
            ClientServerProtocol.set_data(key,value,t)
        except (TypeError, ValueError):
            ans="error\nwrong type\n\n"
    elif com_serv=='get':
        if not param:
            ans="error\nwrong command\n\n"
        ans=ClientServerProtocol.get_data(param)
    else:
        ans="error\nwrong command\n\n"

    return ans

def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
        )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("прерывание")
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
    pass

if __name__ == '__main__':
        run_server('127.0.0.1',8888)