Aqara Developer Platform is an open cooperation platform of Lumi United Technology Co.,Ltd for IoT software and hardware products.

# Getting Started
https://developer.aqara.com/

## Step 0: prepare venv

```bash
# create venv
mkdir project
cd project
python -m venv venv
source venv/bin/activate
mkdir myapp
cd myapp

```

## Step 1: install package

```bash
# pip install
pip install git+https://github.com/sotoedu/aqara_api_sdk.git

```

## Step 2: create app.py


```bash
# create app.py
nano app.py
```

def auth()
```bash
# app.py
from aqara import AqaraClient
import traceback
import json

APPID  = 'data1'
APPKEY = 'data2'
KEYID  = 'data3'

def auth(email):
    try: 
        client = AqaraClient(api_key='iloveiot!')
        print('auth payload : ' , request)

        # email  = 'data4'

        payload = {
            'appid': APPID,
            'appkey': APPKEY , 
            'keyid': KEYID ,
            'email': email
        }

        response_data = client.get_auth(payload)

        response = {
            'message': 'success',
            'result': response_data
        }
        
        return jsonify(response)
    
    except Exception as error:
        print('[error] : ' , error)
        print("[auth] traceback : ", traceback.format_exc())

```

def token()
```bash
# app.py
from aqara import AqaraClient
import traceback
import json

APPID  = 'data1'
APPKEY = 'data2'
KEYID  = 'data3'

def token(authCode, email):
    try: 

        client = AqaraClient(api_key='iloveiot!')
        
        # authCode = 'data4'
        # email  = 'data5'

        # POST 요청
        payload = {
            'authCode': authCode,                
            'appid': APPID,
            'appkey': APPKEY , 
            'keyid': KEYID ,
            'email': email
        }

        response_data , response_msg = client.get_token(payload)

        response = {
            'message': 'success',
            'token': response_data,
            'response' : response_msg
        }
        
        return jsonify(response)
    
    except Exception as error:
        print('error : ' , error)

```

def position()
```bash
# app.py
from aqara import AqaraClient
import traceback
import json

APPID  = 'data1'
APPKEY = 'data2'
KEYID  = 'data3'

def position(token):
    try: 

        client = AqaraClient(api_key='iloveiot!')

        # token  = 'data4'

        # POST 요청
        payload = {
            'token': token,                
            'appid': APPID,
            'appkey': APPKEY , 
            'keyid': KEYID 
        }

        all_position_value, positionResponse, all_device_list = client.get_position(payload)
        print('[position] all_device_list : ' , all_device_list)

        response = {
            'message': 'success',
            'postion': all_position_value,
            'roomList': positionResponse,
            'deviceList': all_device_list
        }
        
        return jsonify(response)
    
    except Exception as error:
        print('[position] error : ' , error)

```

def status()
```bash
# app.py
from aqara import AqaraClient
import traceback
import json

APPID  = 'data1'
APPKEY = 'data2'
KEYID  = 'data3'

def status(model, token):
    try: 

        client = AqaraClient(api_key='iloveiot!')

        # model  = 'data4'
        # token  = 'data5'

        # POST 요청
        payload = {
            'model': model,                
            'token': token,
            'appid': APPID,
            'appkey': APPKEY , 
            'keyid': KEYID 
        }

        response_data , response_msg = client.get_resource(payload)

        response = {
            'message': 'success',
            'result': response_data,
            'response' : response_msg
        }
        
        return jsonify(response)
    
    except Exception as error:
        print('error : ' , error)

```

def write()
```bash
# app.py
from aqara import AqaraClient
import traceback
import json

APPID  = 'data1'
APPKEY = 'data2'
KEYID  = 'data3'

def write(did, resid, control, token):
    try: 

        client = AqaraClient(api_key='iloveiot!')
        
        # did     = 'data4'
        # resid   = 'data5'
        # control = 'data6'   # 'on' or 'off'
        # token   = 'data7'

        # POST 요청
        payload = {                          
            'appid': APPID,
            'appkey': APPKEY , 
            'keyid': KEYID ,
            'did': did,  
            'resid': resid,  
            'control': control,  
            'token': token
        }

        response_msg = client.write_resource(payload)

        response = {
            'message': 'success',
            'response' : response_msg
        }
        
        return jsonify(response)
    
    except Exception as error:
        print('error : ' , error)

```

def read()
```bash
# app.py
from aqara import AqaraClient
import traceback
import json

APPID  = 'data1'
APPKEY = 'data2'
KEYID  = 'data3'

def read(did,resid,token):
    try: 

        client = AqaraClient(api_key='iloveiot!')
        
        # did    = 'data4'
        # resid  = 'data5'
        # token  = 'data6'

        # POST 요청
        payload = {                          
            'appid': APPID,
            'appkey': APPKEY , 
            'keyid': KEYID ,
            'did': did,  
            'resid': resid,  
            'token': token
        }

        response_msg = client.read_resource(payload)

        response = {
            'message': 'success',
            # 'result': response_data,
            'response' : response_msg
        }
        
        return jsonify(response)
    
    except Exception as error:
        print('error : ' , error)

```

def history()
```bash
# app.py
from aqara import AqaraClient
import traceback
import json

APPID  = 'data1'
APPKEY = 'data2'
KEYID  = 'data3'

def history(did,resid,token):
    try: 

        client = AqaraClient(api_key='iloveiot!')

        # did    = 'data4'
        # resid  = 'data5'
        # token  = 'data6'

        # POST 요청
        payload = {                         
            'appid': APPID,
            'appkey': APPKEY , 
            'keyid': KEYID ,
            'did': did,   
            'resid': resid,   
            'token': token
        }

        response_msg = client.get_history(payload)

        response = {
            'message': 'success',
            # 'result': response_data,
            'response' : response_msg
        }
        
        return jsonify(response)
    
    except Exception as error:
        print('error : ' , error)

```

## Congratulations! :tada:

You've successfully run and modified your Project. :partying_face:

### Now what?

- If you want to add ... , check out the [Developer guide](https://developer.aqara.com).


# Troubleshooting

If you can't get this to work, see the [Troubleshooting](https://developer.aqara.com) page.

# Learn More

To learn more about React Native, take a look at the following resources:

- [Developer API Website](https://developer.aqara.com) - learn more about Aqara API.
- [Getting Started](https://opendoc.aqara.cn/en) - Getting Started.
- [Learn the Basics](https://opendoc.aqara.cn/en) - Learn the Basics.
