import json
import requests
from payloadCollection import PayloadCollection


class DoorsData:

    # Class-level variable to hold the common url
    common_url = PayloadCollection.glutzRpcServerUrl

    def __init__(self):
        self.headers = PayloadCollection.headers
        self.url = DoorsData.common_url
        self.doorsData = self.getDoorsPropertyData()
    

    @classmethod
    def update_common_url(cls, new_url):
        cls.common_url = new_url

    def getAccessPointsWithTwoFactorAuthenticationId(self):
        accessPointIdList = []
        try:
            response = requests.get(
                url=self.url,
                headers=self.headers,
                verify=True,
                data=PayloadCollection.accessPointPropertyData,
            )
            results = json.loads(response.text)["result"]
            for result in results:
                for key, value in result.items():
                    if {key: value} == {
                        "propertyId": PayloadCollection.towFactorAuthenticationId
                    }:
                        for key, value in result.items():
                            if {key: value} == {"value": True} or {key: value} == {
                                "value": "1"
                            }:
                                baseId = result["baseId"]
                                accessPointIdList.append(baseId)
            return accessPointIdList
        except Exception as e:
            print(f'exception in requeset: {e}')
            return
            

    def getDoorsPropertyData(self):
        accessPointIdList = self.getAccessPointsWithTwoFactorAuthenticationId()
        try:
            response = requests.get(
                url=self.url,
                headers=self.headers,
                verify=True,
                data=PayloadCollection.devices,
            )

            results = json.loads(response.text)["result"]
            accessPointDevices = {}
            for result in results:
                for accessPointId in accessPointIdList:
                    if result["accessPointId"] == accessPointId:
                        list_of_dicts = [result]
                        for item in list_of_dicts:
                            access_point_id = item["accessPointId"]
                            device_type = item["deviceType"]
                            device_id = item["deviceid"]
                            if device_type == 103:
                                accessPointDevices.setdefault(
                                    access_point_id, {}
                                ).setdefault("IO_Module", []).append(device_id)
                            if device_type == 80:
                                accessPointDevices.setdefault(
                                    access_point_id, {}
                                ).setdefault("IO_Extender", []).append(device_id)
                            elif device_type == 101 or device_type == 102:
                                accessPointDevices.setdefault(
                                    access_point_id, {}
                                ).setdefault("E_Reader", []).append(device_id)

            return accessPointDevices
        except Exception as e:
            print(f'exeption in request:{e}')
            return
