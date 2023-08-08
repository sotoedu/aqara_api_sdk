Aqara Developer Platform is an open cooperation platform of Lumi United Technology Co.,Ltd for IoT software and hardware products.

# Getting Started
https://developer.aqara.com/

## Step 1: install package

```bash
# pip install
$ mkdir project
$ cd project
$ python -m venv venv
$ source venv/bin/activate
$ mkdir myapp
$ cd myapp
$ pip install git+https://github.com/sotoedu/aqara_api_sdk.git

```

## Step 2: create app.py


```bash
# create app.py
$ touch app.py
$ nano app.py
```

def auth()
```bash
# def auth()

def auth():
    try: 
        client = AqaraClient(api_key='iloveiot!')
        print('auth payload : ' , request)
        APPID = request.json.get('data1')
        APPKEY = request.json.get('data2')
        KEYID = request.json.get('data3')
        email = request.json.get('data4')

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
