import json
import requests
from emailManager import send_email
from payloadCollection import PayloadCollection

class UsersData:
    def __init__(self):
        self.session = requests.Session()
        self.headers = PayloadCollection.headers
        self.url = PayloadCollection.glutzRpcServerUrl
        self.codeList = self._get_user_code()
        self.mediaList = self._get_media()
        self.masterUserList = self._get_master_user()
        self.usersData = self._get_user_data()

    def close_session(self):
        self.session.close()

    def _make_request(self, endpoint, data):
        try:
            response = self.session.get(
                url=self.url,
                headers=self.headers,
                verify=True,
                data=data,
            )
            response.raise_for_status()  # Raise HTTPError for bad responses
            return json.loads(response.text)["result"]
        except requests.exceptions.RequestException as e:
          #  print(f"Exception in {endpoint} request: {e}")
            send_email(
                subject=f"Exception in usersData at {endpoint}",
                message=f"Error: {e}",
            )
            return None

    def _get_media(self):
        return self._make_request("getMedia", PayloadCollection.media)

    def _get_user_code(self):
        return self._make_request("getUserCode", PayloadCollection.code)

    def _get_master_user(self):
        return self._make_request("getMasterUser", PayloadCollection.master)

    def _get_user_data(self):
        user_info_dict = {}

        for item in self.codeList:
            userId = item["userId"]
            code = item["code"]
            if userId not in user_info_dict:
                user_info_dict[userId] = {"userId": userId, "media": [], "code": [], "MasterCode": []}
            if item["actionProfileId"] != PayloadCollection.masterCodeActionProfileId:
                user_info_dict[userId]["code"].append(code)
            if item["actionProfileId"] == PayloadCollection.masterCodeActionProfileId:
                user_info_dict[userId]["MasterCode"].append(code)

        for item in self.mediaList:
            userId = item["userId"]
            media = item["publicMediaLabel"]
            if userId not in user_info_dict:
                user_info_dict[userId] = {"userId": userId, "media": [], "code": [], "MasterCode": False}
            user_info_dict[userId]["media"].append(media)

        usersList = [user for user in user_info_dict.values() if len(user["media"]) > 0 and len(user["code"]) > 0]
        return usersList
