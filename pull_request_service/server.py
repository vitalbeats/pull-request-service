from twisted.web import server, resource
from twisted.internet import reactor
from pull_request_service import payload

def main():
    s = server.Site(payload.PayloadHandler('config/secret/webhook'))
    reactor.listenTCP(8080, s)
    reactor.run()
