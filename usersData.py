import json
import requests
from payloadCollection import PayloadCollection


class UsersData:
    # Class-level variable to hold the common url
    common_url = PayloadCollection.glutzRpcServerUrl

    def __init__(self):
        self.headers = PayloadCollection.headers
        self.url = UsersData.common_url
        self.codeList = self.getUserCode()
        self.mediaList = self.getMedia()
        self.masterUserList = self.getMasterUser()
        self.usersData = self.getUserData()

    @classmethod
    def update_common_url(cls, new_url):
        cls.common_url = new_url

    def getMedia(self):
        try:
            response = requests.get(
                url=self.url,
                headers=self.headers,
                verify=True,
                data=PayloadCollection.media,
            )

            return json.loads(response.text)["result"]
        except Exception as e:
            print(f"exeption in requeset: {e}")
            return

    def getUserCode(self):
        url = self.url

        try:
            response = requests.get(
                url=url, headers=self.headers, verify=True, data=PayloadCollection.code
            )
            return json.loads(response.text)["result"]
        except Exception as e:
            print(f"exeption in requeset: {e}")
            return

    def getMasterUser(self):
        try:
            response = requests.get(
                url=self.url,
                headers=self.headers,
                verify=True,
                data=PayloadCollection.master,
            )

            return json.loads(response.text)["result"]
        except Exception as e:
            print(f"exeption in requeset: {e}")
            return

    def getUserData(self):
        # Creating a dictionary to store the user information temporarily
        user_info_dict = {}

        # Adding codes to the user_info_dict
        for item in self.codeList:
            userId = item["userId"]
            code = item["code"]
            if userId not in user_info_dict:
                user_info_dict[userId] = {
                    "userId": userId,
                    "media": [],
                    "code": [],
                    "MasterCode": [],
                }
            if item["actionProfileId"] != PayloadCollection.masterCodeActionProfileId:
                user_info_dict[userId]["code"].append(code)
            if item["actionProfileId"] == PayloadCollection.masterCodeActionProfileId:
                user_info_dict[userId]["MasterCode"].append(code)

        # Adding media to the user_info_dict
        for item in self.mediaList:
            userId = item["userId"]
            media = item["publicMediaLabel"]
            if userId not in user_info_dict:
                user_info_dict[userId] = {
                    "userId": userId,
                    "media": [],
                    "code": [],
                    "MasterCode": False,
                }
            user_info_dict[userId]["media"].append(media)

        # # Adding Master to the user_info_dict
        # for item in self.codeList:
        #     # print(item)
        #     userId = item["userId"]
        #     Master = item["actionProfileId"]
        #     if userId not in user_info_dict:
        #         user_info_dict[userId] = {
        #             "userId": userId,
        #             "media": [],
        #             "code": [],
        #             "Master": Master,
        #         }
        #     user_info_dict[userId]["Master"] = Master

        # Converting the user_info_dict values to a list

        usersList = list(user_info_dict.values())
        usersData = []
        for user in usersList:
            if len(user["media"]) > 0 and len(user["code"]) > 0:
                usersData.append(user)

        return usersData
