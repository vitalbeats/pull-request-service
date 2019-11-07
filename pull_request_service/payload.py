from twisted.web import resource
import hmac
from hashlib import sha1
import json
from pull_request_service import webhook_token

class PayloadHandler(resource.Resource):
    isLeaf = True
    secret_path = 'config/secret/webhook'

    def __init__(self, path):
        secret_path = path

    def render_POST(self, request):
        secret = request.getHeader('X-Hub-Signature')
        event = request.getHeader('X-GitHub-Event')
        if secret:
            wht = webhook_token.WebHookToken(self.secret_path)
            content = request.content.read()
            digest = hmac.new(wht.token.encode('utf-8'), content, sha1).hexdigest()
            sig_parts = secret.split('=', 1)
            if len(sig_parts) > 1 and hmac.compare_digest(sig_parts[1], digest):
                content_as_json = json.loads(content)
                if event == 'pull_request':
                    project = content_as_json['repository']['name'].lower() + '-pr-' + str(content_as_json['number'])
                    print('Received pull request notification for ' + project + ' with action ' + content_as_json['action'])
                    return project
                return content
        request.setResponseCode(403)
        return 'Forbidden.'.encode('utf-8')
