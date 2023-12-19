import json
import asyncio
import aiofiles

from usersData import UsersData


class Users_json_manager:
    def __init__(self):
        self.file_path = "users_data.json"
        self.lock = asyncio.Lock()

    async def update_users(self):
        new_users_data = UsersData().usersData
        if new_users_data:
            await self.update_data(users_new_data=new_users_data)

    async def update_data(self, users_new_data):
        async with self.lock:
            async with aiofiles.open(self.file_path, "w") as json_file:
                await json_file.write(json.dumps(users_new_data, indent=4))

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
