import httpx

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'


#httpclient class
class HttpClient:
    def __init__(self):
        self.session = httpx.Client(headers={'User-Agent': user_agent})
        
    #a method for get request
    def get(self, url,headers={},params={},cookies={}):
        return self.session.get(url,headers=headers,params=params,cookies=cookies,follow_redirects=True)
    
    #a post request method
    def post(self,url,data={},headers={},cookies={}):
        return self.session.post(url,data=data,headers=headers,cookies=cookies,follow_redirects=True)
        
        