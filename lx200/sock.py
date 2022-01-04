import socket
import sys

MAX_LEN = 32

class sock:
  def __init__(self, sock=None):

    self.sock = None
    self.host = ''
    self.port = ''
    self.connected = False

  def connect(self, host = '', port = ''):

    try:
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
      sys.stderr.write('Error opening host: %s, port %s - %s\n' % (host, port, str(e)))
      sys.exit(1)

    if host != '':
      self.host = host
    if port != '':
      self.port = port

    try:
      self.sock.connect((self.host, self.port))
    except socket.error as e:
      sys.stderr.write('Error opening host: %s, port %s - %s\n' % (host, port, str(e)))
      sys.exit(1)

  def close(self):
    self.sock.close()

  def send(self, msg):
    if self.connected == False:
      self.connect(self.host, self.port)
      self.connected = True

    self.sock.sendall(msg.encode('utf-8'))

  def recv(self):
    data = self.sock.recv(MAX_LEN)
    return data.decode('utf-8')
