from flask import Flask ,jsonify , request
import proxvn
import json
app = Flask(__name__)
TOKEN = {}
import threading
TToken_lock = threading.Lock()
req = {
  "status":102,
  "proxyhttp": "",
   "msg": ""
}

@app.route("/quang3")
def quang3():
  rq = req.copy()
  token = request.args.get('token', "")
  user = request.args.get('user', "")
  password = request.args.get('password', "")
  id = request.args.get('id', "")
  if (len(token)  <  6)  and (  len ( user) < 3 and len(password)  < 3):
    rq['msg'] = "Invalid user or password  token "
    return jsonify(rq)
  key = f"{user}:{password}"
  if not token:
    
    with TToken_lock:
      if key in TOKEN:
        token = TOKEN[key]
        #print(f"Using existing token for {key}: {token}")

  User = proxvn.PROXYVN_SITE(user, password, token)
  data = User.GETMY_IP()

#   with open("data.json", "a") as f:
#     f.write(json.dumps(data))
  for item in data:
    _id = item.get("id")
    if int(_id) == int(id):
      #print(f"Changing IP for ID: {_id}")
      ok, msg = User.Change_IP_Proxy(_id)
      
      ip= item['proxy']['ipaddress']['ip']
      user = item['proxy']['username']
      password = item['proxy']['password']
      port = item['proxy']['port']
      pro_type = item['proxy']['ipaddress']['categorytype']['slug']
      protocol = item['protocol']

      code = 100 if ok else 101
      
      rq.update({
          "status": code,
          "msg": msg,
          "proxyhttp": f"{ip}:{port}:{user}:{password}",
          "user": user,
          "password": password,
          "port": port,
          "type": pro_type,
          "protocol": protocol,

          "ip": ip,
          "token": User.Token
        })
      #print(f"ID: {_id}, IP: {ip}, User: {user}, Password: {password}, Port: {port}, Type: {pro_type}, Protocol: {protocol}")
      break
  with TToken_lock:
    #print(f"Updating token for {key}: {User.Token}")
    TOKEN[key] =  User.Token

  return jsonify(rq)
# app.run(debug=True, host="0.0.0.0", port=5000)

