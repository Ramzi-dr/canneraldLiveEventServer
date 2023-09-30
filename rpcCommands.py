import requests
import json
import sys
from payloadCollection import PayloadCollection

url = PayloadCollection.glutzRpcServerUrl


def update_rpcUrl(new_url):
    global url
    url = new_url


def get_userLabel(user_id):
    try:
        response = requests.get(
            url=url,
            headers=PayloadCollection.headers,
            verify=True,
            data=PayloadCollection.userGroupRelations,
        )
        results = json.loads(response.text)["result"]
        for result in results:
            for key, value in result.items():
                if value == user_id:
                    user_label = result["label"]
                    return user_label
    except Exception as e:
        print(f"exeption in requeset: {e}")
        return


def get_userIdByMedia_info(publicMediaLabel):
    try:
        response = requests.get(
            url=url,
            headers=PayloadCollection.headers,
            verify=True,
            data=PayloadCollection.media,
        )

        results = json.loads(response.text)["result"]
        for result in results:
            for key, value in result.items():
                if value == publicMediaLabel:
                    user_id = result["userId"]
                    return user_id
    except Exception as e:
        print(f"exeption in requeset: {e}")
        return


def get_doorLabel(accessPointId):
    try:
        response = requests.get(
            url=url,
            headers=PayloadCollection.headers,
            verify=True,
            data=PayloadCollection.accessPoints,
        )
        results = json.loads(response.text)["result"]
        for result in results:
            for key, value in result.items():
                if value == accessPointId:
                    doorLabel = result["label"]
                    return doorLabel
    except Exception as e:
        print(f"exeption in requeset: {e}")
        return


def get_accessPointIdByReaderId_info(deviceId):
    try:
        response = requests.get(
            url=url,
            headers=PayloadCollection.headers,
            verify=True,
            data=PayloadCollection.devices,
        )
        results = json.loads(response.text)["result"]
        for result in results:
            for key, value in result.items():
                if value == deviceId:
                    accessPointId = result["accessPointId"]
                    return accessPointId
    except Exception as e:
        print(f"exeption in requeset: {e}")
        return


def activateReader_Output(readerId, outputNum):
    try:
        response = requests.get(
            url=url,
            headers=PayloadCollection.headers,
            verify=True,
            data=PayloadCollection.activate_output(
                deviceId=readerId, outputNum=outputNum, action=1
            ),
        )
    except Exception as e:
        print(f"Error: rpcCommands.py/ activateReader_Output: {e}")
        return


def openDoor_short(deviceId, outputNum):
    try:
        response = requests.get(
            url=url,
            headers=PayloadCollection.headers,
            verify=True,
            data=PayloadCollection.activate_output(
                deviceId=deviceId, outputNum=outputNum, action=1
            ),
        )
    except Exception as e:
        print(f"Error: rpcCommands.py/ openDoor_short: {e}")
        return


def openOrClose_door(deviceId, outputNum, is_Extender):
    from inputsState import getInputsState

    print("here")

    def relayToggle():
        openAction = 4
        closeAction = 16
        action = None
        if not is_Extender:
            if (
                getInputsState(deviceId=deviceId) == 1
                or getInputsState(deviceId=deviceId) == 3
            ):
                # state 2 = relay1 is active /state 2 = relay2 is active / state 3 = relay1 and 2 are active
                action = closeAction
                print("🚪 the door will be closed! 👍")
            elif (
                getInputsState(deviceId=deviceId) == 0
                or getInputsState(deviceId=deviceId) == 2
            ):
                action = openAction
                print("🚪 the door will stay open 👍")
            return action
        if is_Extender:
            if getInputsState(deviceId=deviceId) in (
                2,
                3,
                7,
                15,
                31,
                63,
                127,
                255,
                195,
                67,
                131,
                194,
                66,
                130,
            ):
                action = closeAction
                print("🚪 the door will be closed! 👍")
            elif getInputsState(deviceId=deviceId) in (
                0,
                1,
                4,
                8,
                16,
                32,
                64,
                128,
                65,
                129,
                192,
            ):
                action = openAction
                print("🚪 the door will stay open 👍")

            return action

    try:
        response = requests.get(
            url=url,
            headers=PayloadCollection.headers,
            verify=True,
            data=PayloadCollection.activate_output(
                deviceId=deviceId,
                outputNum=outputNum,
                action=relayToggle(),
            ),
        )
    except Exception as e:
        print(f"Error: rpcCommands.py/openOrClose_door: {e}")
        return


def Toggle_alarmSystem_output_8(deviceId, action):
    from inputsState import getInputsState

    highAction = 4
    lowAction = 16
    if getInputsState(deviceId=deviceId) in (
        128,
        255,
        195,
        131,
        129,
        194,
        130,
        192,
    ):
        try:
            response = requests.get(
                url=url,
                headers=PayloadCollection.headers,
                verify=True,
                data=PayloadCollection.activate_output(
                    deviceId=deviceId,
                    outputNum=PayloadCollection.IO_Extender_output_8_disarm,
                    action=highAction,
                ),
            )
            print("disarmed")
        except Exception as e:
            print(f"Error: Toggle_alarmSystem_output_8: {e}")
            return
    else:
        print("is already disarmed")
    if action == "low":
        try:
            response = requests.get(
                url=url,
                headers=PayloadCollection.headers,
                verify=True,
                data=PayloadCollection.activate_output(
                    deviceId=deviceId,
                    outputNum=PayloadCollection.IO_Extender_output_8_disarm,
                    action=lowAction,
                ),
            )
            print("armed")
        except Exception as e:
            print(f"Toggle_alarmSystem_output_8: {e}")
            return
    """ else:
        print("is already armed") """


def activate_panic_output_7(deviceId):
    print("we are in output7")
    try:
        response = requests.get(
            url=url,
            headers=PayloadCollection.headers,
            verify=True,
            data=PayloadCollection.activate_output(
                deviceId=deviceId,
                outputNum=PayloadCollection.IO_Extender_output_7_Panic,
                action=1,
            ),
        )
    except Exception as e:
        print(f"Error: rpcCommands.py/openOrClose_door: {e}")
        return
