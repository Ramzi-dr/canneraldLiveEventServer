from inputsState import inputStateEvent
from usersData import UsersData
from doorsData import DoorsData


class MessageFilter:
    users_data = []
    doors_data = []

    def __init__(self):
        pass

    async def get_users(self):
        new_users_data = UsersData().usersData
        if new_users_data != MessageFilter.users_data:
            MessageFilter.users_data = new_users_data

    async def get_doors(self):
        new_doors_data = DoorsData().doorsData
        if new_doors_data != MessageFilter.doors_data:
            MessageFilter.doors_data = new_doors_data

    async def handel_other_message(self, message):
        if "params" in message:
            if message["params"][0] in (
                "AccessPointPropertyData",
                "codes",
                "Media",
                "UsersGroups",
                "Rights",
            ):
                await self.get_doors()
                await self.get_users()

    async def condition_handler(self, condition):
        deviceId = None
        inputState = None
        inputNum = None
        if "deviceid" in condition:
            deviceId = condition["deviceid"]
            if "events" in condition:
                if "condition" in condition["events"][0]:
                    if condition["events"][0]["condition"] == "Rising Edge":
                        inputState = 1
                        inputNum = condition["events"][0]["event"]
                        if all(
                            var is not None for var in (deviceId, inputState, inputNum)
                        ):
                            await inputStateEvent(
                                deviceId=deviceId,
                                inputNum=inputNum,
                                inputState=inputState,
                            )
                            return None

                    if condition["events"][0]["condition"] == "Falling Edge":
                        inputState = 0
                        inputNum = condition["events"][0]["event"]
                        if all(
                            var is not None for var in (deviceId, inputState, inputNum)
                        ):
                            await inputStateEvent(
                                deviceId=deviceId,
                                inputNum=inputNum,
                                inputState=inputState,
                            )
                        return None
                    else:
                        return condition

    async def messageFilter(self, message):
        data = None
        if type(message) is dict:
            for key, value in message.items():
                if key == "params":
                    if value[0] == "ObservedStates":
                        data = value[1]["data"]
                        if "events" in data:
                            if "code" in data["events"][0]:
                                return data
                            if "batteryPowered" in data["events"][0]:
                                return None
                            if "condition" in data["events"][0]:
                                return await self.condition_handler(condition=data)
                        elif "modified" in data:
                            return None
                        else:
                            return data
                    else:
                        await self.handel_other_message(message=message)
        elif type(message) is list:
            if message[0] == "ObservedStates":
                data = message[1]["data"]

            return data

    async def get_door_id(self, data):
        try:
            if data is not None:
                for key, value in data.items():
                    if key == "deviceid":
                        return data["deviceid"]
                    elif key == "modified":
                        return None
        except TypeError as type:
            print(f"Error  messageFilter.py/def get_door_id {type}")
            return None
