import json
import requests
from emailManager import send_email
from payloadCollection import PayloadCollection

class DoorsData:
    def __init__(self):
        self.session = requests.Session()
        self.headers = PayloadCollection.headers
        self.url = PayloadCollection.glutzRpcServerUrl
        self.doorsData = self._get_doors_property_data()

    def close_session(self):
        self.session.close()

    def _make_request(self, endpoint, data):
        try:
            response = self.session.get(
                url=self.url,
                headers=self.headers,
                verify=True,
                data=data,
            )
            response.raise_for_status()  # Raise HTTPError for bad responses
            return json.loads(response.text)["result"]
        except requests.exceptions.RequestException as e:
          #  print(f"Exception in {endpoint} request: {e}")
            send_email(
                subject=f"Exception in doorsData at {endpoint}",
                message=f"Error: {e}",
            )
            return None

    def getAccessPointsWithTwoFactorAuthenticationId(self):
        accessPointIdList = []
        try:
            response = self._make_request("getAccessPointsWithTwoFactorAuthenticationId", PayloadCollection.accessPointPropertyData)
            results = response or []

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
          #  print(f"exception in requeset: {e}")
            send_email(
                subject="there is Exception in doorsData at getAccessPointsWithTwoFactorAuthenticationId ",
                message=f"error: {e}",
            )

            return[] 

    def getAccessPointsWithMasterDoorId(self):
        MasterDoorAccessPointIdList = []
        try:
            response = self._make_request("getAccessPointsWithMasterDoorId", PayloadCollection.accessPointPropertyData)
            results = response or []

            for result in results:
                for key, value in result.items():
                    if {key: value} == {"propertyId": PayloadCollection.masterDoorId}:
                        for key, value in result.items():
                            if {key: value} == {"value": True} or {key: value} == {
                                "value": "1"
                            }:
                                baseId = result["baseId"]
                                MasterDoorAccessPointIdList.append(baseId)
            return MasterDoorAccessPointIdList
        except Exception as e:
           # print(f"exception in requeset: {e}")
            send_email(
                subject="there is Exception in doorsData at getAccessPointsWithTwoFactorAuthenticationId ",
                message=f"error: {e}",
            )

            return[] 

    def getAccessPointsWithPushNotification(self):
        controlledDoorAccessPointIdList = []
        try:
            response = self._make_request("getAccessPointsWithPushNotification", PayloadCollection.accessPointPropertyData)
            results = response or []

            for result in results:
                for key, value in result.items():
                    if {key: value} == {
                        "propertyId": PayloadCollection.controlledDoorNotification
                    }:
                        for key, value in result.items():
                            if {key: value} == {"value": True} or {key: value} == {
                                "value": "1"
                            }:
                                baseId = result["baseId"]
                                controlledDoorAccessPointIdList.append(baseId)
            return controlledDoorAccessPointIdList
        except Exception as e:
          #  print(f"exception in requeset: {e}")
            send_email(
                subject="there is Exception in doorsData.py at getAccessPointsWithTwoFactorAuthenticationId ",
                message=f"error: {e}\n and controlled door access Point id list :{controlledDoorAccessPointIdList}   \ e empty list will be returned  ",
            )

            return[] 

    def _get_doors_property_data(self):
        accessPointIdList = self.getAccessPointsWithTwoFactorAuthenticationId()
        masterDoorList = self.getAccessPointsWithMasterDoorId()
        controlledDoorList = self.getAccessPointsWithPushNotification()

        try:
            response = self._make_request("getDoorsPropertyData", PayloadCollection.devices)
            results = response or []
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
                            if device_type == 101 or device_type == 102:
                                accessPointDevices.setdefault(
                                    access_point_id, {}
                                ).setdefault("E_Reader", []).append(device_id)
                            if item["accessPointId"] in controlledDoorList:
                                accessPointDevices.setdefault(
                                    access_point_id, {}
                                ).setdefault("controlledDoor", True)
                            if item["accessPointId"] not in controlledDoorList:
                                accessPointDevices.setdefault(
                                    access_point_id, {}
                                ).setdefault("controlledDoor", False)
                            if item["accessPointId"] in masterDoorList:
                                accessPointDevices.setdefault(
                                    access_point_id, {}
                                ).setdefault("masterDoor", True)
                            else:
                                accessPointDevices.setdefault(
                                    access_point_id, {}
                                ).setdefault("masterDoor", False)

            return accessPointDevices

        except Exception as e:
         #   print(f"Exception in request: {e}")
            send_email(
                subject="Exception in doorsData.py at _get_doors_property_data ",
                message=f"Error: {e}\n   and accessPointDevices :{accessPointDevices} \n def will return a empty Dic   ",
            )
            return{} 
