from twisted.web import resource
from twisted.python import log
import hmac
from hashlib import sha1
import json
from pull_request_service import webhook_token
from pull_request_service import project

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
                projects = project.ProjectList()
                if event == 'pull_request' and content_as_json['action'] == 'closed':
                    log.msg('Received a pull request closed payload.')
                    project_name = content_as_json['repository']['name'].lower() + '-pr-' + str(content_as_json['number'])
                    projects.delete(project_name)
                    log.msg('Successfully handled project delete for ' + project_name)
                    return project_name.encode('utf-8')
                return content
        request.setResponseCode(403)
        return 'Forbidden.'.encode('utf-8')
