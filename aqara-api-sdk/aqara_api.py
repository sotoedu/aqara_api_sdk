'''

Aqara Developer Platform for API
==================================
Aqara Developer Platform is an open cooperation platform of Lumi United Technology Co.,Ltd for IoT software and hardware products.
https://developer.aqara.com/

'''


import requests
import json
import hashlib
import time
import logging
import traceback
import pprint

logger = logging.getLogger('aqara')

# MAINNET = 'https://open-cn.aqara.com'
MAINNET  = 'https://open-kr.aqara.com'
APIURL = MAINNET + '/v3.0/open/api'
TOKENURL = MAINNET + '/v3.0/open/access_token'
AUTHURL = MAINNET + '/v3.0/open/authorize'

class AqaraClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_id = ''
        self.api_key = ''
        self.key_id = ''
    
    def get_headers(self, accessToken, appid, appkey , keyid):
        
        logger.info('[get_headers] appid : ' + appid)
        logger.info('[get_headers] appkey : ' + appkey)
        logger.info('[get_headers] keyid : ' + keyid)

        currentUTC = str(round(time.time(), 3))
        Appid = appid
        Keyid = keyid
        AppKey = appkey
        Time = currentUTC.replace('.', '')
        Nonce = currentUTC.replace('.', '')

        headers = ''
        
        if accessToken == 'No':
            accessToken = ''
            preSign = 'Appid=' + Appid + '&' + 'Keyid=' + Keyid + '&' + 'Nonce=' + Nonce + '&' + 'Time=' + Time + AppKey

            preSign = preSign.lower()
            Sign = str(hashlib.md5(preSign.encode()).hexdigest())

            headers = {
                'Content-Type' : 'application/json',
                'Appid': Appid,
                'Keyid': Keyid,
                'Nonce': Nonce,
                'Time': Time,
                'Sign': Sign,
                'Lang': 'ko'
            }
        else:
            preSign = 'Accesstoken=' + accessToken + '&' + 'Appid=' + Appid + '&' + 'Keyid=' + Keyid + '&' + 'Nonce=' + Nonce + '&' + 'Time=' + Time + AppKey
            preSign = preSign.lower()
            Sign = str(hashlib.md5(preSign.encode()).hexdigest())

            headers = {
                'Content-Type' : 'application/json',
                'Accesstoken': accessToken,
                'Appid': Appid,
                'Keyid': Keyid,
                'Nonce': Nonce,
                'Time': Time,
                'Sign': Sign,
                'Lang': 'ko'
            }
        
        print('[get_headers] header : ', headers)

        return headers
#
# 
#     
    def get_authorize_code(self, payload):

        appid = payload.get('appid')
        appkey = payload.get('appkey')
        keyid = payload.get('keyid')
        email = payload.get('email')

        print('[get_authorize_code] Payload appid : ', appid)

        accessToken = 'No'

        headers = self.get_headers(accessToken, appid, appkey , keyid)

        payload = {
            'intent': 'config.auth.getAuthCode',
            'data': {
                'account': email,
                'accountType': 0,
                'accessTokenValidity': '1y'
            }
        }

        payload = json.dumps(payload) 

        try:
            
            response = requests.post(APIURL, headers=headers, data=payload)            
            response = json.loads(response.text)
            print('[get_authorize_code] send email : ', response)
            logger.info('[get_authorize_code] send email : ' , response)
            return response

        except Exception as error:
            logger.info('[get_authorize_code] Exception : ' + traceback.format_exc())
            print('[get_authorize_code] Exception : ', traceback.format_exc())
            return 'get_authorize_code'
    
    def get_access_token(self, payload):
        
        appid = payload.get('appid')
        appkey = payload.get('appkey')
        keyid = payload.get('keyid')
        email = payload.get('email')
        authCode = payload.get('authCode')

        accessToken = 'No'

        headers = self.get_headers(accessToken, appid, appkey , keyid)
        payload = {
            "intent": "config.auth.getToken",
            "data": {
                "authCode": authCode,
                "account": email,
                "accountType": 0
            }
        }
        
        try:
            response = requests.post(APIURL, headers=headers, json=payload)
            response = json.loads(response.text)
            print('[get_access_token] response : ', response)
            accessToken = response['result']['accessToken']
            print('[get_access_token] acess_token for get_token is : ', accessToken)
            return accessToken, response

        except Exception as error:
            logger.info('[get_access_token] Exception : ' + traceback.format_exc())
            print('[get_access_token] Exception : ', traceback.format_exc())
            return 'get_access_token'
    
    def get_position_info(self, payload):
        
        accessToken = payload.get('token')
        appid = payload.get('appid')
        appkey = payload.get('appkey')
        keyid = payload.get('keyid')

        response = ''
        all_position_value = []
        all_device_list = []        

        headers = self.get_headers(accessToken, appid, appkey , keyid)
        tempPayload = {
            "intent": "query.position.info",
            "data": {
                "pageNum": 1,
                "pageSize": 200
            }
        }
        
        try:
            response = requests.post(APIURL, headers=headers, json=tempPayload)

            positionResponse = json.loads(response.text)
            logger.info("response : " + str(positionResponse))
            print("[get_position_info] positionResponse : " , positionResponse ) 
            resultValue = positionResponse['result']['data']
            print("[get_position_info] resultValue : " , resultValue ) 
            # logger.info("resultValue : " + positionResponse[0]['positionId'])

            for dataSet in resultValue:
                logger.info("dataSet : " + str(dataSet))
                temp = {'positionName': dataSet['positionName'], 'positionId': dataSet['positionId']}
                all_position_value.append(temp)

            logger.info("positionId : " + str(all_position_value))
            print("[get_position_info] all_position_value : " , all_position_value ) 
            print("## all_position_value is : ")
            pprint.pprint(all_position_value)
            # pprint.pprint(response)

            if all_position_value :

                for dataSet in all_position_value:
                    responseList = self.aiot_device_list(dataSet['positionId'] , payload)
                    all_device_list.append(responseList)

            print("[get_position_info] all_device_list : ", all_device_list)
            return all_position_value, positionResponse, all_device_list
        
        except Exception as error:
            logger.info('[get_position_info] Exception : ' + traceback.format_exc())
            print('[get_position_info] Exception : ', traceback.format_exc())
            return 'get_position_info'
    
    def aiot_device_list(self, positionId, payload):
        try:
            print("[aiot_device_list].. ")
            accessToken = payload.get('token')
            appid = payload.get('appid')
            appkey = payload.get('appkey')
            keyid = payload.get('keyid')

            all_dev_list_value = []
            # result_value = ''

            headers = self.get_headers(accessToken, appid, appkey , keyid)
         
            print("[aiot_device_list] data['positionId'] : ", positionId)

            tempPayload = {
                "intent": "query.device.info",
                "data": {
                    "positionId": positionId ,
                    "pageNum": 1,
                    "pageSize": 200
                }
            }

            payload = str(json.dumps(tempPayload))
            response = requests.post(APIURL, headers=headers, data=payload)
            response = json.loads(response.text)
            logger.info("response : " + str(response))
            print("[aiot_device_list] response : ", response)
            resultValue = response['result']['data']

            print("[aiot_device_list] resultValue : ", resultValue)

            for dataSet in resultValue:
                logger.info("dataSet : " + str(dataSet))
                temp = {'deviceName': dataSet['deviceName'], 'state': dataSet['state'] , 'model': dataSet['model'] , 'did': dataSet['did'] }
                all_dev_list_value.append(temp)
                # result = get_device_info(result_value)

            return all_dev_list_value
        
        except Exception as error:
            logger.info('[aiot_device_list] Exception : ' + traceback.format_exc())
            print('[aiot_device_list] Exception : ', traceback.format_exc())
            return 'aiot_device_list'
    
    def query_resource_info(self, payload):
        try:
            print("[query_resource_info].. ")
            model = payload.get('model')
            accessToken = payload.get('token')
            appid = payload.get('appid')
            appkey = payload.get('appkey')
            keyid = payload.get('keyid')

            model_info_value = []            

            headers = self.get_headers(accessToken, appid, appkey , keyid)
         
            print("[query_resource_info] model : ", model)

            tempPayload = {
                "intent": "query.resource.info",
                "data": {
                    "model": model 
                }
            }

            payload = str(json.dumps(tempPayload))
            response = requests.post(APIURL, headers=headers, data=payload)
            response = json.loads(response.text)
            logger.info("response : " + str(response))
            print("[query_resource_info] response : ", response)
            resultValue = response['result']

            print("[query_resource_info] resultValue : ", resultValue)

            for dataSet in resultValue:
                logger.info("dataSet : " + str(dataSet))
                temp = {'name': dataSet['name'], 'resourceId': dataSet['resourceId'] , 'access': dataSet['access'] , 'description': dataSet['description'] }
                model_info_value.append(temp)

            return model_info_value , response
        
        except Exception as error:
            logger.info('[query_resource_info] Exception : ' + traceback.format_exc())
            print('[query_resource_info] Exception : ', traceback.format_exc())
            return 'query_resource_info'
    
    def write_resource_device(self, payload):
        try:
            print("[write_resource_device].. ")
            appid = payload.get('appid')
            appkey = payload.get('appkey')
            keyid = payload.get('keyid')
            did = payload.get('did')
            resid = payload.get('resid')
            control = payload.get('control')
            accessToken = payload.get('token')
            
            value = 1 if control == 'on' else 0

            headers = self.get_headers(accessToken, appid, appkey , keyid)
         
            print("[write_resource_device] did : ", did)

            tempPayload = {
                "intent": "write.resource.device",
                "data": [
                    {
                        "subjectId": did ,
                        "resources": [
                            {
                            "resourceId": resid ,
                            "value": value
                            }
                        ]
                    }
                ]
            }

            payload = str(json.dumps(tempPayload))
            response = requests.post(APIURL, headers=headers, data=payload)
            response = json.loads(response.text)
            logger.info("response : " + str(response))
            print("[write_resource_device] response : ", response)

            return response
        
        except Exception as error:
            logger.info('[write_resource_device] Exception : ' + traceback.format_exc())
            print('[write_resource_device] Exception : ', traceback.format_exc())
            return 'write_resource_device'
    
    def query_resource_value(self, payload):
        try:
            print("[query_resource_value].. ")
            appid = payload.get('appid')
            appkey = payload.get('appkey')
            keyid = payload.get('keyid')
            did = payload.get('did')
            resid = payload.get('resid')
            accessToken = payload.get('token')
            
            resid = [s.strip() for s in resid.split(",")]

            headers = self.get_headers(accessToken, appid, appkey , keyid)
         
            tempPayload = {
                "intent": "query.resource.value",
                "data": {
                    "resources": [ 
                    {
                        "subjectId": did ,
                        "resourceIds": 
                            resid                        
                    }
                    ]
                }
            }

            print("[query_resource_value] tempPayload : ", tempPayload)

            payload = str(json.dumps(tempPayload))
            response = requests.post(APIURL, headers=headers, data=payload)
            response = json.loads(response.text)
            logger.info("response : " + str(response))
            print("[query_resource_value] response : ", response)
            # resultValue = response['result']

            return response
        
        except Exception as error:
            logger.info('[query_resource_value] Exception : ' + traceback.format_exc())
            print('[query_resource_value] Exception : ', traceback.format_exc())
            return 'query_resource_value'
        
    def fetch_resource_history(self, payload):
        try:
            print("[fetch_resource_history].. ")
            appid = payload.get('appid')
            appkey = payload.get('appkey')
            keyid = payload.get('keyid')
            did = payload.get('did')
            resid = payload.get('resid')
            accessToken = payload.get('token')

            headers = self.get_headers(accessToken, appid, appkey , keyid)
         
            print("[fetch_resource_history] did : ", did)
            currentUTC = str(round(time.time(),3) - 86400 * 30 )  # 86400 = 24H : 60s * 60m * 24h
            tTime = currentUTC.replace('.','')

            tempPayload = {
                "intent": "fetch.resource.history",
                "data": {
                    "subjectId": did ,
                    "resourceIds": [
                        resid
                    ],   
                    "startTime": tTime                     
                }                
            }

            payload = str(json.dumps(tempPayload))
            response = requests.post(APIURL, headers=headers, data=payload)
            response = json.loads(response.text)
            logger.info("response : " + str(response))
            print("[fetch_resource_history] response : ", response)
            return response
        
        except Exception as error:
            logger.info('[fetch_resource_history] Exception : ' + traceback.format_exc())
            print('[fetch_resource_history] Exception : ', traceback.format_exc())
            return 'fetch_resource_history'
    
    def get_auth(self, payload):
        print('[get_auth] Payload Parameters : ', payload)
        
        try:
            authorizeCode = self.get_authorize_code(payload)
            return authorizeCode  # 응답 객체 반환
        except Exception as error:
            logger.info('[get_auth] Exception : ' + traceback.format_exc())
            print('[get_auth] Exception : ', traceback.format_exc())
            return 'get_auth'
        
    def get_token(self, payload):
        print('[get_token] Payload Parameters : ', payload)
        
        try:
            accessToken , response = self.get_access_token(payload)

            return accessToken , response # 응답 객체 반환
        except Exception as error:
            logger.info('[get_token] Exception : ' + traceback.format_exc())
            print('[get_token] Exception : ', traceback.format_exc())
            return 'get_token'
    
    def get_position(self, payload):
        print('[get_position] Payload Parameters : ', payload)
        
        try:
            all_position_value, positionResponse, all_device_list = self.get_position_info(payload)

            return all_position_value, positionResponse, all_device_list # 응답 객체 반환
        except Exception as error:
            logger.info('[get_position] Exception : ' + traceback.format_exc())
            print('[get_position] Exception : ', traceback.format_exc())
            return 'get_position'
    
    def get_resource(self, payload):
        print('[get_resource] Payload Parameters : ', payload)
        
        try:
            device_resource_value, resourceResponse = self.query_resource_info(payload)

            return device_resource_value, resourceResponse  # 응답 객체 반환
        except Exception as error:
            logger.info('[get_resource] Exception : ' + traceback.format_exc())
            print('[get_resource] Exception : ', traceback.format_exc())
            return 'get_resource'
    
    def write_resource(self, payload):
        print('[write_resource] Payload Parameters : ', payload)
        
        try:
            resourceResponse = self.write_resource_device(payload)

            return resourceResponse  # 응답 객체 반환
        except Exception as error:
            logger.info('[write_resource] Exception : ' + traceback.format_exc())
            print('[write_resource] Exception : ', traceback.format_exc())
            return 'write_resource'
    
    def read_resource(self, payload):
        print('[write_resource] Payload Parameters : ', payload)
        
        try:
            resourceResponse = self.query_resource_value(payload)

            return resourceResponse  # 응답 객체 반환
        except Exception as error:
            logger.info('[read_resource] Exception : ' + traceback.format_exc())
            print('[read_resource] Exception : ', traceback.format_exc())
            return 'read_resource'
    
    def get_history(self, payload):
        print('[get_history] Payload Parameters : ', payload)
        
        try:
            resourceResponse = self.fetch_resource_history(payload)

            return resourceResponse  # 응답 객체 반환
        except Exception as error:
            logger.info('[get_history] Exception : ' + traceback.format_exc())
            print('[get_history] Exception : ', traceback.format_exc())
            return 'get_history'

    

