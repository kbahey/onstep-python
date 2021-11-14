import socket

MAX_LEN = 32

class sock:
  def __init__(self, sock=None):

    self.sock = None
    self.host = ''
    self.port = ''

  def connect(self, host = '', port = ''):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if host != '':
      self.host = host
    if port != '':
      self.port = port

    self.sock.connect((self.host, self.port))

  def send(self, msg):
    self.connect(self.host, self.port)
    self.sock.sendall(msg.encode('utf-8'))

  def recv(self):
    data = self.sock.recv(MAX_LEN)
    return data.decode('utf-8')
