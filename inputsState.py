import jsonrpclib
import asyncio
from emailManager import sendGmail_ramziVersion
from payloadCollection import PayloadCollection
from rpcAction import RpcAction
from activateAlarmSys import ActivateAlarmSys


url = PayloadCollection.glutzRpcServerUrl


def update_rpcUrl(new_url):
    global url
    url = new_url


async def inputStateEvent(deviceId, inputNum, inputState):
    rpcAction = RpcAction()
    if (
        inputNum == PayloadCollection.IO_Extender_input_1_kurzzeitentriegelung
        and inputState == 1
    ):
        rpcAction.disarm_and_openDoor(
            IO_Module=deviceId,
            outputNum=PayloadCollection.IO_Extender_output_1_openDoor,
            is_Extender=True,
        )
    if (
        inputNum == PayloadCollection.IO_Extender_input_7_austrittstaster
        and inputState == 0
    ):
        activateAlarmSys = ActivateAlarmSys(deviceId=deviceId)
        activateAlarmSys.activate_timer()


def getInputsState(
    deviceId,
):
    try:
        server = jsonrpclib.Server(url)
        output = server.eAccess.getModel("AccessPointLocations")

        eAccess = server.eAccess.deviceOperation(
            "TestInputState",
            {
                "deviceid": deviceId,
            },
        )
        state = eAccess["state"]

        return state
    except Exception as e:
        sendMail_afterException(exception=e)
        print(f"Error: inputsState/ getInputsState= {e}")


def activateReaderSignal(deviceId):
    try:
        server = jsonrpclib.Server(url)
        signal = server.eAccess.deviceOperation(
            "Signal", {"deviceid": deviceId, "signallingid": 30, "Buzzer": "4"}
        )

    except Exception as e:
        print(f"Error: inputState.py/activateReaderSignal={e}")


def sendMail_afterException(exception):
    try:
        sendGmail_ramziVersion(
            f"Error in inputsState file \nError: {exception}",
            subject="hallo from  event server .",
        )
    except Exception as e:
        print(f"Error: inputState.py/ sendMail_afterEception:{e}")
        pass
