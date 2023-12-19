import json
import asyncio
import aiofiles

from doorsData import DoorsData


class Doors_json_manager:
    def __init__(self):
        self.file_path = "doors_data.json"
        self.lock = asyncio.Lock()

    async def update_doors(self):
        doors_json_instance = Doors_json_manager()
        new_doors_data = DoorsData().doorsData
        if new_doors_data:
            await self.check_changes(new_data=new_doors_data)

    async def update_data(self, doors_new_data):
        async with self.lock:
            async with aiofiles.open(self.file_path, "w") as json_file:
                await json_file.write(json.dumps(doors_new_data, indent=4))

    async def load_from_file(self):
        async with self.lock:
            try:
                async with aiofiles.open(self.file_path, "r") as json_file:
                    content = await json_file.read()
                    if not content.strip():
                        return {}
                    return json.loads(content)
            except FileNotFoundError:
                # Create an empty file if it doesn't exist
                async with aiofiles.open(self.file_path, "w") as json_file:
                    await json_file.write("{}")
                return {}

    async def check_changes(self, new_data):
        try:
            old_data = await self.load_from_file()
            if old_data and new_data:
                keys_only_in_old_data = set(old_data.keys()) & set(new_data.keys())
                keys_only_in_new_data = set(new_data.keys()) & set(old_data.keys())
                print(f"keys only in old data :  {keys_only_in_old_data}")
                print(f"keys only in new data :  {keys_only_in_new_data}")
                common_keys = set(old_data.keys()) & set(new_data.keys())
                value_changes = {}
                for key in common_keys:
                    if (
                        key in old_data
                        and key in new_data
                        and old_data[key] != new_data[key]
                    ):
                        if isinstance(old_data[key], bool) and isinstance(
                            new_data[key], bool
                        ):
                            value_changes[key] = {
                                "old_value": old_data[key],
                                "new_value": new_data[key],
                            }
                print(f"value change :    {value_changes}")
            await self.update_data(new_data)
        except Exception as e:
            print(f"exception in check changes : {e}")
