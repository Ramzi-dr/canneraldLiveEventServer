import json
import requests
from emailManager import send_email
from payloadCollection import PayloadCollection

class RpcCommands:
    def __init__(self):
        self.url = PayloadCollection.glutzRpcServerUrl
        self.headers = PayloadCollection.headers
        self.session = requests.Session()

    def make_rpc_request(self, data):
        try:
            response = self.session.get(
                url=self.url,
                headers=self.headers,
                verify=True,
                data=data,
            )
            response.raise_for_status()
            return json.loads(response.text)["result"]
        except Exception as e:
            send_email(
                subject="Exception in rpcCommands.py  make_rpc_request()",
                message=f"Error: {e}",
            )
            pass

    def get_userLabel(self, user_id):
        data = PayloadCollection.userGroupRelations
        try:
            results = self.make_rpc_request(data) or []
            for result in results:
                for key, value in result.items():
                    if value == user_id:
                        user_label = result["label"]
                        return user_label
        except Exception as e:
            send_email(
                subject="Exception in rpcCommands at get_user_label()",
                message=f"Error: {e}",
            )
            pass
    def get_userIdByMedia_info(self,publicMediaLabel):
        data = PayloadCollection.media
        try:
            results = self.make_rpc_request(data) or []
            for result in results:
                for key, value in result.items():
                    if value == publicMediaLabel:
                        user_id = result["userId"]
                        return user_id
        except Exception as e:
            send_email(
                subject="there is exception in rpcCommands at get_userIdByMedia_info()",
                message=f"error: {e}",
            )
            pass


    def get_doorLabel(self, accessPointId):
        data=PayloadCollection.accessPoints
        try:
            results = self.make_rpc_request(data) or []
            for result in results:
                for key, value in result.items():
                    if value == accessPointId:
                        doorLabel = result["label"]
                        return doorLabel
        except Exception as e:
            send_email(
                subject="there is exception in rpcCommands at get_doorLabel()",
                message=f"error: {e}",
            )

            pass


    def get_accessPointIdByReaderId_info(self, publicMediaLabel):
        data = PayloadCollection.media
        try:
            results = self.make_rpc_request(data) or []
            for result in results:
                for key, value in result.items():
                    if value == publicMediaLabel:
                        user_id = result["userId"]
                        return user_id
        except Exception as e:
            send_email(
                subject="Exception in rpcCommands at get_accessPointIdByReaderId_info()",
                message=f"Error: {e}",
            )
            pass

    def get_doorlabel(self, accessPointId):
        data = PayloadCollection.accessPoints
        try:
            results = self.make_rpc_request(data) or []
            for result in results:
                for key, value in result.items():
                    if value == accessPointId:
                        door_label = result["label"]
                        return door_label
        except Exception as e:
            send_email(
                subject="Exception in rpcCommands at get_door_label()",
                message=f"Error: {e}",
            )
            pass

    def get_access_PointIdByReaderId_info(self, deviceId):
        data = PayloadCollection.devices
        try:
            results = self.make_rpc_request(data) or []
            for result in results:
                for key, value in result.items():
                    if value == deviceId:
                        accessPointId = result["accessPointId"]
                        return accessPointId
        except Exception as e:
            send_email(
                subject="Exception in rpcCommands at get_access_point_id_by_reader_id_info()",
                message=f"Error: {e}",
            )
            pass

    def activateReader_output(self, readerId, outputNum):
        data = PayloadCollection.activate_output(deviceId=readerId, outputNum=outputNum, action=1)
        try:
            self.make_rpc_request(data)
        except Exception as e:
            send_email(
                subject="Exception in rpcCommands at activate_reader_output",
                message=f"Error: {e}",
            )
            pass

    def openDoor_short(self, deviceId, outputNum):
        data = PayloadCollection.activate_output(deviceId=deviceId, outputNum=outputNum, action=1)
        try:
            self.make_rpc_request(data)
        except Exception as e:
            send_email(
                subject="Exception in rpcCommands at open_door_short()",
                message=f"Error: {e}",
            )
            pass

    def openOrClose_door(self, deviceId, outputNum, is_Extender):
        from inputsState import getInputsState

        def relay_toggle():
            open_action = 4
            close_action = 16
            action = None

            if is_Extender:
              #  print(f"InputState : {getInputsState(deviceId=deviceId)}")
                if getInputsState(deviceId=deviceId) in (
                    0, 3, 4, 7, 15, 31, 63, 127, 255, 195, 67, 131, 194, 66, 130,
                ):
                    action = close_action
                elif getInputsState(deviceId=deviceId) in (
                    1, 2, 6, 8, 16, 32, 64, 128, 65, 129, 192,
                ):
                    action = open_action

                return action

            if not is_Extender:
                if (
                    getInputsState(deviceId=deviceId) == 1
                    or getInputsState(deviceId=deviceId) == 3
                ):
                    action = close_action
                elif (
                    getInputsState(deviceId=deviceId) == 0
                    or getInputsState(deviceId=deviceId) == 2
                ):
                    action = open_action
                return action

        try:
            action = relay_toggle()
            output_list = [
                outputNum,
                PayloadCollection.IO_Extender_output_3_Led_masterCode,
                PayloadCollection.IO_Extender_output_2_openDoorIsActivate,
            ]

            for outputNum in output_list:
                data = PayloadCollection.activate_output(
                    deviceId=deviceId, outputNum=outputNum, action=action
                )
                self.make_rpc_request(data)
        except Exception as e:
            send_email(
                subject="Exception in rpcCommands at open_or_close_door",
                message=f"Error: {e}",
            )
            pass

    def get_rpc_info(self):
        data = PayloadCollection.userGroupRelations
        try:
            results = self.make_rpc_request(data) or []
        except Exception as e:
            send_email(
                subject="Exception in rpcCommands at get_rpc_info",
                message=f"Error: {e}",
            )
            pass

    def Toggle_alarmSystem_output_8(deviceId, action):
        pass
        # from inputsState import getInputsState

        # highAction = 4
        # lowAction = 16
        # if getInputsState(deviceId=deviceId) in (
        #     128,
        #     255,
        #     195,
        #     131,
        #     129,
        #     194,
        #     130,
        #     192,
        # ):
        #     try:
        #         requests.get(
        #             url=url,
        #             headers=PayloadCollection.headers,
        #             verify=True,
        #             data=PayloadCollection.activate_output(
        #                 deviceId=deviceId,
        #                 outputNum=PayloadCollection.IO_Extender_output_8_disarm,
        #                 action=highAction,
        #             ),
        #         )
        #         print("disarmed")
        #     except Exception as e:
        #         print(f"Error: Toggle_alarmSystem_output_8: {e}")
        #         send_email(
        #             subject="there is exception in rpcCommands at Toggle_alarmSystem_output_8",
        #             message=f"error: {e}",
        #         )
        #         pass
        # else:
        #     print("is already disarmed")
        # if action == "low":
        #     try:
        #         requests.get(
        #             url=url,
        #             headers=PayloadCollection.headers,
        #             verify=True,
        #             data=PayloadCollection.activate_output(
        #                 deviceId=deviceId,
        #                 outputNum=PayloadCollection.IO_Extender_output_8_disarm,
        #                 action=lowAction,
        #             ),
        #         )
        #         print("armed")
        #     except Exception as e:
        #         print(f"Toggle_alarmSystem_output_8: {e}")
        #         send_email(
        #             subject="there is exception in rpcCommands at Toggle_alarmSystem_output_8"
        #             "   where action == low",
        #             message=f"error: {e}",
        #         )
        #         pass


    def activate_panic_output_7(deviceId):
        pass
        # try:
        #     requests.get(
        #         url=url,
        #         headers=PayloadCollection.headers,
        #         verify=True,
        #         data=PayloadCollection.activate_output(
        #             deviceId=deviceId,
        #             outputNum=PayloadCollection.IO_Extender_output_6_Panic,
        #             action=1,
        #         ),
        #     )
        # except Exception as e:
        #     print(f"Error: rpcCommands.py/openOrClose_door: {e}")
        #     send_email(
        #         subject="there is exception in rpcCommands at activate_panic_output_7",
        #         message=f"error: {e}",
        #     )
        #     pass
