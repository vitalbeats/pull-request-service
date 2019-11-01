class WebHookToken():
    token = ''
    
    def __init__(self, path):
        with open(path,'r') as f:
            self.token = f.read().replace('\n', '')
