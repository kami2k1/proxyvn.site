import json
import requests
class path:
    def __init__(self , host ="https://proxyvn.site/"):
        self.host = host
        self.csrf = host+ "api/auth/csrf"
        self.login = host + "api/auth/callback/credentials"
        self.sesseion = host + "api/auth/session"

class PROXYVN_SITE: 
    """ bypass Kamidev """
    def __init__(self , user , password):
        self.user = user
        self.password = password
        self.req = requests.Session()
        self.path = path()
        self.req.get(self.path.host)  # Initialize session with the host
        self.merchantId ="e7c649f3-1c6c-4f59-a475-b8988a59efde"

        self.token = None
    @staticmethod
    def Extreact_request(response :
         requests.Response)-> dict:
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def get_csrf_token(self)-> str:
        response = self.req.get(self.path.csrf)
        data = self.Extreact_request(response)
        token = data.get('csrfToken', "")
        if not token:
            raise Exception("CSRF token not found in response")

        return token 
    def GETTOKEN(self):
        response = self.req.get(self.path.sesseion)
        data = self.Extreact_request(response)
       
        return data
    

    def login(self):
        token = self.get_csrf_token()
        print(f"CSRF Token: {token}")
        
        # Data phải được URL encode đúng cách
        prams = {
            "phone": self.user,
            "password": self.password,
            "merchantId": self.merchantId,
            "csrfToken": token,
            "callbackUrl": self.path.host + "lich-su-doi-proxy"  
        }
        
     
        self.req.headers.update({
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://proxyvn.site",
            "referer": "https://proxyvn.site/lich-su-doi-proxy",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "x-auth-return-redirect": "1"
        })
        
       
        response = self.req.post(self.path.login, data=prams, allow_redirects=True)

        
        # Uncomment để xử lý response
        if response.status_code == 200:
            data = self.GETTOKEN()
            if data:
                self.req.headers.update({
                    "Authorization": f"Bearer {data.get('accessToken')}"
                })
            # Uncomment để in dữ liệu đăng nhập
            else:
                print("Login failed, no session data returned.")
                raise Exception("Login failed, no session data returned. user password may be incorrect.")
           
            # data = self.Extreact_request(response)
            # print(data)
        
        return response
    def Changer_IP_PROXY()




