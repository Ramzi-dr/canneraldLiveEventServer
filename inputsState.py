import jsonrpclib
#from activateAlarmSys import ActivateAlarmSys
from emailManager import send_email
from payloadCollection import PayloadCollection
from rpcAction import RpcAction
from rpcCommands import RpcCommands

url = PayloadCollection.glutzRpcServerUrl


# def update_rpcUrl(new_url):
#     global url
#     url = new_url


async def inputStateEvent(deviceId, inputNum, inputState):
    rpcAction = RpcAction()
  #  print(f"inputNum : {inputNum}")
 #   print(f"inputState: {inputState}")
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
        inputNum == PayloadCollection.IO_Extender_input_6_austrittstaster
        and inputState == 0
    ):
        RpcCommands().openDoor_short(
            deviceId=deviceId,
            outputNum=PayloadCollection.IO_Extender_output_1_openDoor,
        )
        # activateAlarmSys = ActivateAlarmSys(deviceId=deviceId)
        # activateAlarmSys.activate_timer()


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
        send_email(
            subject="there is exception in inputState at getInputsState",
            message=f"error: {e}",
        )
        print(f"Error: inputsState/ getInputsState= {e}")


def activateReaderSignal(deviceId):
    try:
        server = jsonrpclib.Server(url)
        server.eAccess.deviceOperation(
            "Signal", {"deviceid": deviceId, "signallingid": 30, "Buzzer": "4"}
        )

    except Exception as e:
        send_email(
            subject="there is exception in inputState at activateReaderSIgnal",
            message=f"error: {e}",
        )
        print(f"Error: inputState.py/activateReaderSignal={e}")
