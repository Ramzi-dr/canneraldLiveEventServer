import asyncio
import time
from inputsState import activateReaderSignal
from messageFilter import MessageFilter
from payloadCollection import PayloadCollection
from rpcAction import RpcAction
from doorsJsonManager import Doors_json_manager
from usersJsonManager import Users_json_manager

# from rpcCommands import activate_panic_output_7


class AccessManager:
    def __init__(self, doors_instances, delete_door_instance_function):
        self.doors_instances = doors_instances
        self.delete_door_instance = delete_door_instance_function
        self.doorsData = None
        self.usersData = None
        self.reader = None
        self.is_Master = False
        self.ListOf_IO_Module = None
        self.ListOf_IO_Extender = None
        self.code = None
        self.isMasterCode = False
        self.isMasterDoor = False
        self.badgeId = None
        self.timer_running = False
        self.timer_start_time = None
        self.timer_duration = None
        self.timer_thread = None
        self.seconds = 10
        self.rpc_action = RpcAction()
        self.last_call_time = 0
        # Dictionary to store timer state for each reader
        self.active_readers = []

    async def initialize_data(self):
        if self.doorsData is None:
            doors_json_instance = Doors_json_manager()
            doors_local_data = await doors_json_instance.load_from_file()
            if doors_local_data:
                self.doorsData = doors_local_data
            else:
                await doors_json_instance.update_doors()
                self.doorsData = await doors_json_instance.load_from_file()

        if self.usersData is None:
            users_json_instance = Users_json_manager()
            users_local_data = await users_json_instance.load_from_file()
            if users_local_data:
                self.usersData = users_local_data
            else:
                await users_json_instance.update_users()
                self.usersData = await users_json_instance.load_from_file()

    async def _start_timer(self):
        while self.timer_running and self.reader in self.active_readers:
            current_time = time.time()
            elapsed_time = current_time - self.timer_start_time
            # print(f"blink blink...{self.seconds}..." + "\N{winking face}")
            self.seconds -= 1
            # if self.seconds % 3 == 0:
            # activateReaderSignal(deviceId=self.reader)
            #  print("please give ur code now")
            if elapsed_time >= self.timer_duration:
                self.timer_running = False
                #  print("sorry ur time is out")
                activateReaderSignal(deviceId=self.reader, signal=40)
                self.delete_door_instance(
                    door_id=self.reader
                )  # Call the delete_door_instance function
                self.seconds = 10
                self.active_readers.remove(self.reader)  #
            else:
                time_to_sleep = min(1, self.timer_duration - elapsed_time)
                await asyncio.sleep(time_to_sleep)

    async def did_badge(self, badgeId, reader):
        await self.initialize_data()
        # activateReaderSignal(deviceId=self.reader, signal=45)
        print(f"doors data : {self.doorsData}")
        print(f"users data : {self.usersData}")
        global user_did_badge
        user_did_badge = True
        print("user did badge")
        self.badgeId = badgeId
        self.reader = reader
        self.isMasterDoor = await self.is_master_door(reader=reader)

        if await self.reader_exist(reader=reader):
            if await self.door_have_outputDevice(reader=reader):
                if self.reader in self.active_readers:
                    # Timer is already running, so reset it
                    # print("timer is running and is reset")
                    self.timer_running = False
                    self.active_readers.remove(self.reader)
                    await asyncio.sleep(1)
                self.active_readers.append(self.reader)
                self.seconds = 10
                self.timer_duration = self.seconds
                self.timer_start_time = time.time()
                self.timer_running = True
                # print("timer is running now")
                # Add the reader to active readers
                await asyncio.gather(self._start_timer())
        else:
            self.delete_door_instance(door_id=self.reader)

    async def code_is_given(self, code, reader, is_panic):
        self.code = code
        print("code is given")
        if not self.timer_running:
            # print("u have to use ur badge first")
            return
        if self.timer_running:
            # The second method is called while the timer is still running
            if self.reader == reader:
                if self.same_CodeAndBadge_user():
                    self.timer_running = False
                    self.code = code
                    #  print("timer is stopped")

                    await self.give_access(door_id=reader)
                    # if is_panic:
                    #     print(is_panic)
                    #     if self.ListOf_IO_Extender is not None:
                    #         print(self.ListOf_IO_Extender)
                    #         activate_panic_output_7(deviceId=self.ListOf_IO_Extender[0])

    async def door_have_outputDevice(self, reader):
        haveOutputDevice = False
        for doorId, doorDevices in self.doorsData.items():
            if reader in doorDevices["E_Reader"]:
                for key, value in doorDevices.items():
                    if key == "IO_Module":
                        if value:
                            haveOutputDevice = True
                            self.ListOf_IO_Module = value

                    if key == "IO_Extender":
                        if value:
                            haveOutputDevice = True
                            self.ListOf_IO_Extender = value

        return haveOutputDevice

    async def is_master_door(self, reader):
        is_master_door = False
        for key, value in self.doorsData.items():
            if "E_Reader" in value:
                if reader in value["E_Reader"]:
                    if "Permanent open (Dauerauf)" in value:
                        is_master_door = value["Permanent open (Dauerauf)"]
                        print(f"door is Master: {is_master_door}")
        return is_master_door

    async def reader_exist(self, reader):
        deviceId_found = False
        for key, value in self.doorsData.items():
            for device, deviceId in value.items():
                if device == "E_Reader":
                    for my_id in deviceId:
                        if my_id == reader:
                            deviceId_found = True
        return deviceId_found

    def same_CodeAndBadge_user(self):
        is_theSameUser = False
        for user in self.usersData:
            for badge in user["media"]:
                if badge == self.badgeId:
                    for user_code in user["code"]:
                        if user_code == self.code:
                            is_theSameUser = True
                    for user_code in user["MasterCode"]:
                        if user_code == self.code:
                            is_theSameUser = True
                            self.isMasterCode = True
                    return is_theSameUser

    async def give_access(self, door_id):
        self.delete_door_instance(
            door_id=door_id
        )  # Call the delete_door_instance function
        if self.ListOf_IO_Extender is not None:
            if self.isMasterCode and self.isMasterDoor:
                self.rpc_action.disarm_and_openDoor(
                    IO_Device=self.ListOf_IO_Extender[0],
                    master_modus=True,
                    outputNum=PayloadCollection.IO_Extender_output_1_openDoor,
                    is_Extender=True,
                )
            else:
                self.rpc_action.disarm_and_openDoor(
                    IO_Device=self.ListOf_IO_Extender[0],
                    outputNum=PayloadCollection.IO_Extender_output_1_openDoor,
                    is_Extender=True,
                )
        if self.ListOf_IO_Extender is None and self.ListOf_IO_Module is not None:
            if self.isMasterCode and self.isMasterDoor:
                self.rpc_action.disarm_and_openDoor(
                    IO_Device=self.ListOf_IO_Module[0],
                    master_modus=True,
                    outputNum=PayloadCollection.IO_ModuleRelay_1,
                    is_Extender=False,
                )
            else:
                self.rpc_action.disarm_and_openDoor(
                    IO_Device=self.ListOf_IO_Module[0],
                    outputNum=PayloadCollection.IO_ModuleRelay_1,
                    is_Extender=False,
                )
