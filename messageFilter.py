from emailManager import send_email
from inputsState import inputStateEvent
import asyncio
from doorsJsonManager import Doors_json_manager
from usersJsonManager import Users_json_manager


class MessageFilter:
    def __init__(self):
        pass


    async def handel_other_message(self, message):
        if "params" in message:
            param_message = message["params"][0]
            if param_message in (
                "Codes",
                "Media",
                "UsersGroups",
                "Rights",
                "ObservedStates",
                "UserGroupRelations",
            ):
                print(
                    f"there is a change in users  and the message is:        {param_message}"
                )
                users_json_instance = Users_json_manager()
                await users_json_instance.update_users()
            if message["params"][0] in ("AccessPointPropertyData",):
                doors_json_instance = Doors_json_manager()
                await doors_json_instance.update_doors()
                print(
                    f"there is changes in doors  and this is the message:    {message['params']}"
                )

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
            print(f"dat is list : {message}")
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
            #  print(f"Error  messageFilter.py/def get_door_id {type}")
            send_email(subject="get_door_id", message=f"error : {type}")
            return None
        # Add this method to your MessageFilter class

    # async def get_users_with_retry(self, max_retries=3):
    #     for attempt in range(max_retries):
    #         try:
    #             users_data = await self.get_users()
    #             if users_data is not None:
    #                 return users_data
    #         except Exception as e:
    #             print(f"Error getting users (attempt {attempt + 1}): {e}")
    #             await asyncio.sleep(2)  # Wait for a short duration before retrying

    #     print(f"Failed to get users after {max_retries} attempts.")
    #     return None  # or raise an exception, depending on your use case

    # async def get_doors_with_retry(self, max_retries=3):
    #     for attempt in range(max_retries):
    #         try:
    #             result = await self.get_doors()
    #             if result is not None:
    #                 return result
    #         except Exception as e:
    #             print(f"Error getting doors (attempt {attempt + 1}): {e}")
    #             await asyncio.sleep(2)  # Wait for a short duration before retrying
    #     print(f"Failed to get doors after {max_retries} attempts.")
    #     return None  # or raise an exception, depending on your use case
