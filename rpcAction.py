from rpcCommands import *


class RpcAction:
    def __init__(self):
        pass

    def disarm_and_openDoor(
        self,
        IO_Module,
        outputNum,
        is_Extender=None,
        activationModus=None,
    ):
        if is_Extender:
            from inputsState import getInputsState

            doorState = getInputsState(deviceId=IO_Module)
            if doorState not in (
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
                Toggle_alarmSystem_output_8(deviceId=IO_Module, action="high")

            if activationModus == "keep_it_open/close_it":
                openOrClose_door(
                    deviceId=IO_Module, outputNum=outputNum, is_Extender=is_Extender
                )

            else:
                openDoor_short(deviceId=IO_Module, outputNum=outputNum)
                print("door is open for user ")
        else:
            if activationModus == "keep_it_open/close_it":
                openOrClose_door(
                    deviceId=IO_Module, outputNum=outputNum, is_Extender=is_Extender
                )

            else:
                openDoor_short(deviceId=IO_Module, outputNum=outputNum)
                print("door is open for user ")
