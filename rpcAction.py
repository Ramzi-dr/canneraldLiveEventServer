from rpcCommands import RpcCommands


class RpcAction:
    def __init__(self):
        self.rpc_command = RpcCommands()

    def disarm_and_openDoor(
        self,
        IO_Device,
        outputNum,
        is_Extender=None,
        master_modus=False,
    ):
        if is_Extender:
            from inputsState import getInputsState

            extender_inputs_state = getInputsState(deviceId=IO_Device)
            # check_list_state = [
            #     2,
            #     3,
            #     7,
            #     15,
            #     31,
            #     63,
            #     127,
            #     255,
            #     195,
            #     67,
            #     131,
            #     194,
            #     66,
            #     130,
            # ]
            # if extender_inputs_state not in check_list_state:
            # Toggle_alarmSystem_output_8(deviceId=IO_Device, action="high")
            # check if clean-tek input is deactivate before openig the door  input 4
            if extender_inputs_state not in (8, 15, 31, 63, 127, 255):
                if master_modus:
                    self.rpc_command.openOrClose_door(
                        deviceId=IO_Device, outputNum=outputNum, is_Extender=is_Extender
                    )

                else:
                    self.rpc_command.openDoor_short(
                        deviceId=IO_Device, outputNum=outputNum
                    )
                #  print("door is open for user ")
        # if is IO_MOdule ?
        if not is_Extender:
            if master_modus:
                self.rpc_command.openOrClose_door(
                    deviceId=IO_Device, outputNum=outputNum, is_Extender=is_Extender
                )

            else:
                self.rpc_command.openDoor_short(deviceId=IO_Device, outputNum=outputNum)
            #  print("door is open for user ")
