from paste.deploy import loadapp
from eventlet import wsgi
import eventlet
import sys

sys.path.insert(0,'../')


if __name__ == '__main__':

    wsgi_app = loadapp('config:' +  '/home/ubuntu/cloud/r4capi/web.ini')
    wsgi.server(eventlet.listen(('', 8090)),wsgi_app)
