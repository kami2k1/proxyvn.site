import json
import requests
class path:
    def __init__(self , host ="https://proxyvn.site/"):
        self.host = host
        self.csrf = host+ "api/auth/csrf"
        self.login = host + "api/auth/callback/credentials"
        self.sesseion = host + "api/auth/session"
        self.my_ip = host + "quang/api/v1/users/proxies?page=1&limit=5000"
        

class PROXYVN_SITE: 
    """ bypass Kamidev """
    def __init__(self , user , password  ,token  : str = None):
        self.user = user
        self.password = password
        self.req = requests.Session()
        self.path = path()
        self.req.get(self.path.host)  # Initialize session with the host
        self.Token = ""
        self.merchantId ="e7c649f3-1c6c-4f59-a475-b8988a59efde"
        if not token:
            self.login()
        else:
            self.req.headers.update({
                    "Authorization": f"Bearer {token}"
                })
            
        self.MY_ip_static = []
        self.MY_IP_rote = []

        
    @staticmethod
    def Extreact_request(response :
         requests.Response)-> dict:
        """ Extract JSON data from response """
        try:
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
            return response.json()
        
        except : 
          raise Exception("Failed to extract JSON from response, response may not be in JSON format")
    def GETMY_IP(self):
        """ Get my IP """
        
        response = self.req.get(self.path.my_ip)
        data = self.Extreact_request(response)
        data = data.get("data", [])

        for item in data:
            id = item.get("id")
            ip= item['proxy']['ipaddress']['ip']
            user = item['proxy']['username']
            password = item['proxy']['password']
            port = item['proxy']['port']
            pro_type = item['proxy']['ipaddress']['categorytype']['slug']
            protocol = item['protocol']
            if pro_type == "static":
                self.MY_ip_static.append({
                    "id": id,
                    "ip": ip,
                    "user": user,
                    "password": password,
                    "port": port,
                    "type": pro_type,
                    "protocol": protocol
                })
            elif pro_type == "rote":
                self.MY_IP_rote.append({
                    "id": id,
                    "ip": ip,
                    "user": user,
                    "password": password,
                    "port": port,
                    "type": pro_type,
                    "protocol": protocol
                })
            
            print(f"ID: {id}, IP: {ip}, User: {user}, Password: {password}, Port: {port}, Type: {pro_type}, Protocol: {protocol}")
        return data
    
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
    

    def login(self) -> bool:
        if len(self.user) < 3 or len(self.password) < 3:
            return False

        token = self.get_csrf_token()
        print(f"CSRF Token: {token}")
        
        # Data phải được URL encode đúng cách
        prams = {
            "phone": self.user,
            "password": self.password,
            "merchantId": self.merchantId,
            "csrfToken": token,
            "callbackUrl": self.path.host 
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
                self.Token = data.get('accessToken')
                print(f"Login successful, token: {self.Token}")
                return True
            # Uncomment để in dữ liệu đăng nhập
            else:
                print("Login failed, no session data returned.")
                # raise Exception("Login failed, no session data returned. user password may be incorrect.")
           
            # data = self.Extreact_request(response)
            # print(data)
        
        return False
    def Change_IP_Proxy(self, ids , retry = 0 ):
        if retry > 3:
            print("Retry limit exceeded for Change IP Proxy")
            return 
        """ Change IP Proxy  list or single id """
        data = []
        msg = " "
        if not isinstance(ids, list ) :
            data.append(ids)
        else:
            data = ids
        for id in data:
            r = self.req.get(self.path.host + f"quang/api/v1/proxies/{id}/rotate")
            r = self.Extreact_request(r)
            
            code =  r.get("statusCode", 861)
            
            if code == 401:
                msg = f"[{id}] Change IP Proxy failed, please login again"
                print(f"[{id}] Change IP Proxy failed, please login again")
                self.login()
                print(f"[{id}] retrying Change IP Proxy")
                self.Change_IP_Proxy(id, retry + 1) # gọi dệ quy 1 lần nữa

            elif code == 400:
                print(f"[{id}] Change IP Proxy failed, invalid id")
                msg = f"[{id}] Change IP Proxy failed, invalid id"
            elif code == 861 and ("msg" in r.get("errors", {})):
                msg = f"[{id}] {r['errors']['msg']}"
                msg = f"[{id}] {r['errors']['msg']}"
            elif r['status'] == "success":
                print(f"[{id}] Change IP Proxy success")
                msg = f"[{id}] Change IP Proxy success"

                return True, msg

        return False, msg


