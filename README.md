# ProxyVN.site API Client

Thư viện Python để tương tác với API của ProxyVN.site - quản lý và sử dụng proxy một cách dễ dàng.

## 🚀 Tính năng

- ✅ Đăng nhập tự động với phone/password
- ✅ Lấy danh sách proxy (static/rotate)
- ✅ Đổi IP proxy
- ✅ Quản lý session tự động
- ✅ Retry mechanism khi lỗi 401
- ✅ Hỗ trợ cả HTTP và SOCKS5

## 📦 Cài đặt

```bash
pip install requests
```

## 🔧 Sử dụng cơ bản

### 1. Khởi tạo và đăng nhập

```python
from proxvn import PROXYVN_SITE

# Tạo instance với phone và password
client = PROXYVN_SITE(user="0123456789", password="your_password")

# Đăng nhập tự động được thực hiện trong __init__
print("Đăng nhập thành công!")
```

### 2. Lấy danh sách proxy

```python
# Lấy tất cả proxy của bạn
client.GETMY_IP()

# Xem proxy static
print("Proxy Static:")
for proxy in client.MY_ip_static:
    print(f"ID: {proxy['id']}")
    print(f"IP: {proxy['ip']}:{proxy['port']}")
    print(f"Auth: {proxy['user']}:{proxy['password']}")
    print(f"Protocol: {proxy['protocol']}")
    print("---")

# Xem proxy rotate
print("Proxy Rotate:")
for proxy in client.MY_IP_rote:
    print(f"ID: {proxy['id']}")
    print(f"IP: {proxy['ip']}:{proxy['port']}")
    print(f"Auth: {proxy['user']}:{proxy['password']}")
    print(f"Protocol: {proxy['protocol']}")
    print("---")
```

### 3. Đổi IP proxy

```python
# Đổi IP cho một proxy
proxy_id = "your_proxy_id"
success = client.Change_IP_Proxy(proxy_id)

if success:
    print("Đổi IP thành công!")
else:
    print("Đổi IP thất bại!")

# Đổi IP cho nhiều proxy cùng lúc
proxy_ids = ["id1", "id2", "id3"]
client.Change_IP_Proxy(proxy_ids)
```

## 📝 Ví dụ đầy đủ

```python
import json
from proxvn import PROXYVN_SITE

def main():
    # Khởi tạo client
    client = PROXYVN_SITE(
        user="0123456789", 
        password="your_password"
    )
    
    try:
        # Lấy danh sách proxy
        print("Đang lấy danh sách proxy...")
        client.GETMY_IP()
        
        # In thông tin proxy static
        if client.MY_ip_static:
            print(f"\n📍 Có {len(client.MY_ip_static)} proxy static:")
            for i, proxy in enumerate(client.MY_ip_static, 1):
                print(f"{i}. {proxy['ip']}:{proxy['port']} ({proxy['protocol']})")
        
        # In thông tin proxy rotate
        if client.MY_IP_rote:
            print(f"\n🔄 Có {len(client.MY_IP_rote)} proxy rotate:")
            for i, proxy in enumerate(client.MY_IP_rote, 1):
                print(f"{i}. {proxy['ip']}:{proxy['port']} ({proxy['protocol']})")
                
                # Đổi IP cho proxy rotate đầu tiên
                if i == 1:
                    print(f"\n🔄 Đang đổi IP cho proxy {proxy['id']}...")
                    success = client.Change_IP_Proxy(proxy['id'])
                    if success:
                        print("✅ Đổi IP thành công!")
                    else:
                        print("❌ Đổi IP thất bại!")
        
        # Lưu thông tin proxy vào file
        proxy_data = {
            "static": client.MY_ip_static,
            "rotate": client.MY_IP_rote
        }
        
        with open('my_proxies.json', 'w', encoding='utf-8') as f:
            json.dump(proxy_data, f, indent=2, ensure_ascii=False)
        
        print("\n💾 Đã lưu thông tin proxy vào my_proxies.json")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()
```

## 🛠️ API Reference

### Class: `PROXYVN_SITE`

#### Constructor
```python
PROXYVN_SITE(user: str, password: str)
```
- `user`: Số điện thoại đăng nhập
- `password`: Mật khẩu

#### Methods

##### `GETMY_IP()`
Lấy danh sách tất cả proxy của user và phân loại vào:
- `self.MY_ip_static`: List proxy static
- `self.MY_IP_rote`: List proxy rotate

##### `Change_IP_Proxy(ids, retry=0) -> bool`
Đổi IP cho proxy.
- `ids`: ID proxy (string) hoặc list ID (list)
- `retry`: Số lần retry (mặc định 0)
- Return: `True` nếu thành công, `False` nếu thất bại

##### `get_csrf_token() -> str`
Lấy CSRF token để authentication.

##### `GETTOKEN() -> dict`
Lấy session token hiện tại.

## 📋 Cấu trúc dữ liệu Proxy

Mỗi proxy có cấu trúc:

```python
{
    "id": "proxy_id",
    "ip": "192.168.1.1",
    "user": "username",
    "password": "password", 
    "port": 8080,
    "type": "static|rote",
    "protocol": "http|socks5"
}
```

## 🔍 Sử dụng proxy với requests

```python
# Lấy proxy đầu tiên
if client.MY_ip_static:
    proxy = client.MY_ip_static[0]
    
    # Cấu hình proxy cho requests
    proxies = {
        'http': f"http://{proxy['user']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}",
        'https': f"http://{proxy['user']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}"
    }
    
    # Sử dụng proxy
    import requests
    response = requests.get('https://httpbin.org/ip', proxies=proxies)
    print(response.json())
```

## ⚠️ Lưu ý

1. **Rate Limiting**: Không đổi IP quá nhanh để tránh bị limit
2. **Session**: Client tự động quản lý session và retry khi cần
3. **Error Handling**: Luôn wrap code trong try-catch
4. **Security**: Không commit file chứa username/password

## 🐛 Troubleshooting

### Lỗi đăng nhập
```
Login failed, no session data returned. user password may be incorrect.
```
- Kiểm tra lại username/password
- Đảm bảo tài khoản chưa bị khóa

### Lỗi 401 khi đổi IP
```
[proxy_id] Change IP Proxy failed, please login again
```
- Client sẽ tự động retry với login mới
- Nếu vẫn lỗi, kiểm tra tài khoản

### Lỗi 400
```
[proxy_id] Change IP Proxy failed, invalid id
```
- Kiểm tra lại proxy ID có đúng không
- Proxy có thuộc về tài khoản không

## 📄 License

MIT License

## 🤝 Contributing

Pull requests are welcome! 

---

Made with ❤️ by [kami2k1](https://github.com/kami2k1)
