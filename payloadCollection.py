import json
import os


class PayloadCollection:
    username = os.environ.get("GLUTZ_BST_USER")
    password = os.environ.get("GLUTZ_BST_PASS")
    eAccess_service_name = "eAccess.service"
    headers = {"Content-Type": "application/json"}
    GlutzUrl = "31.24.10.138"
    glutzRpcServerUrl = f"http://{username}:{password}@{GlutzUrl}:8333/rpc/"
    backupGlutzRpcUrl = f"http://{username}:{password}@127.0.0.1:8333/rpc/"
    glutzWsServerUrl = f"ws://{username}:{password}@{GlutzUrl}:8333"
    backupWsServerPort = 8800
    backupWsServerIp = "192.168.1.251"
    backupWsServerUrl = f"ws://{backupWsServerIp}:{backupWsServerPort}"
    backupGlutzUrl = f"ws://{username}:{password}@127.0.0.1:8333"
    towFactorAuthenticationId = "5022"  # in Glutz door Properties
    IO_Module_Type = 103
    E_Reader_IP55_Type = 102
    E_Reader_Type = 101
    relayShortOpenAction = 1
    relayOpenForEver = 4
    relayClose = 16

    IO_ModuleRelay_1 = 2
    IO_ModuleRelay_2 = 4
    #  IO Extender info and spec 3'batteryPowered'
    IO_Extender_Type = 80
    IO_Extender_output_1_openDoor = 2
    IO_Extender_output_2 = 4
    IO_Extender_output_3 = 8
    IO_Extender_output_4 = 16
    IO_Extender_output_5 = 32
    IO_Extender_output_6 = 64
    IO_Extender_output_7_Panic = (
        128  # AlarmSystem Panic activate the output for 3 Seconds
    )
    IO_Extender_output_8_disarm = 256
    IO_Extender_input_1_kurzzeitentriegelung = "Input 1"
    IO_Extender_input_2_türzustand = "Input 2"
    IO_Extender_input_7_austrittstaster = (
        "Input 7"  # activate AlarmSystem after 45 Seconds Output 8
    )
    IO_Extender_input_8_ZustandEma = "Input 8"  # AlarmSystem state
    state_input_1_High = 1
    state_input_2_High = 2
    state_input_3_High = 4
    state_input_4_High = 8
    state_input_5_High = 16
    state_input_6_High = 32
    state_input_7_High = 64
    state_input_8_High = 128
    state_input_1_2_High = 3
    state_input_1_2_3_High = 7
    state_input_1_2_3_4_High = 15
    state_input_1_2_3_4_5_High = 31
    state_input_1_2_3_4_5_6_High = 63
    state_input_1_2_3_4_5_6_7_High = 127
    state_input_1_2_3_4_5_6_7_8_High = 255
    state_input_1_2_7_8_High = 195
    state_input_1_2_7_High = 67
    state_input_1_2_8_High = 131
    state_input_1_7_High = 65
    state_input_1_8_High = 129
    state_input_2_7_8_High = 194
    state_input_2_7_High = 66
    state_input_2_8_High = 130
    state_input_7_8_High = 192

    masterCodeActionProfileId = "1002"  # in Glutz Codes menu profile non Default
    message = {
        "method": "registerObserver",
        "params": [
            [
                "UsersGroups",
                "UserGroupRelations",
                "Codes",
                "Media",
                "Devices",
                "AccessPoints",
                "AuthorizationPoints",
                "AuthorizationPointRelations",
                "DeviceEvents",
                "Rights",
                "ObservedStates",
                "TimeProfiles",
                "TimeSlots",
                "DeviceStatus",
                "RouteTree",
                "Properties",
                "PropertyValueSpecs",
                "DevicePropertyData",
                "DeviceStaticPropertyData",
                "SystemPropertyData",
                "AccessPointPropertyData",
                "UserPropertyData",
                "HolidayCalendars",
                "Holidays",
                "DeviceUpdates",
                "EventLog",
                "CustomProperties",
                "Logins",
                "ActionProfiles",
                "PermissionProfiles",
                "Permissions",
                "Subsystems",
                "CustomFilesTree",
            ]
        ],
        "jsonrpc": "2.0",
    }
    userGroupRelations = json.dumps(
        {
            "method": "eAccess.getModel",
            "params": ["UsersGroups", {}, ["id", "subsystemId", "label", "class"]],
            "id": 9,
            "jsonrpc": "2.0",
        }
    )

    @staticmethod
    def activate_output(deviceId, outputNum, action):
        payload = json.dumps(
            {
                "method": "eAccess.deviceOperation",
                "params": [
                    "OpenDoor",
                    {
                        "deviceid": deviceId,
                        "action": action,
                        "outputs": outputNum,
                        "hasMotor": "false",
                    },
                ],
                "id": 61,
                "jsonrpc": "2.0",
            }
        )
        return payload

    getAuthorizationPointProperty = json.dumps(
        {
            "method": "eAccess.getAuthorizationPointProperty",
            "params": [
                "propertyName",
                {},
                [],
            ],
            "id": 16,
            "jsonrpc": "2.0",
        }
    )

    devices = json.dumps(
        {
            "method": "eAccess.getModel",
            "params": [
                "Devices",
                {},
                ["id", "label", "deviceid", "deviceType", "accessPointId", "roles"],
            ],
            "id": 8,
            "jsonrpc": "2.0",
        }
    )
    accessPointPropertyData = json.dumps(
        {
            "method": "eAccess.getModel",
            "params": ["AccessPointPropertyData", {}, []],
            "id": 2,
            "jsonrpc": "2.0",
        }
    )
    accessPoints = json.dumps(
        {
            "method": "eAccess.getModel",
            "params": ["AccessPoints", {}, ["id", "label", "function"]],
            "id": 8,
            "jsonrpc": "2.0",
        }
    )
    media = json.dumps(
        {
            "method": "eAccess.getModel",
            "params": [
                "Media",
                {},
                [
                    "id",
                    "userId",
                    "actionProfileId",
                    "uid",
                    "publicMediaLabel",
                    "description",
                    "validFrom",
                    "validTo",
                    "mediumType",
                    "technicalMediaId",
                ],
            ],
            "id": 8,
            "jsonrpc": "2.0",
        }
    )
    code = json.dumps(
        {
            "method": "eAccess.getModel",
            "params": [
                "Codes",
                {},
                [
                    "id",
                    "userId",
                    "actionProfileId",
                    "code",
                    "description",
                    "validFrom",
                    "validTo",
                ],
            ],
            "id": 9,
            "jsonrpc": "2.0",
        }
    )

    master = json.dumps(
        {
            "method": "eAccess.getModel",
            "params": ["UserPropertyData", {}],
            "id": 26,
            "jsonrpc": "2.0",
        }
    )

    @staticmethod
    def getAccessPoint():
        payload = json.dumps(
            {
                "method": "eAccess.getModel",
                "params": [
                    "Rights",
                    {},
                    [
                        "id",
                        "userId",
                        "authorizationPointId",
                        "timeProfileId",
                        "validFrom",
                        "validTo",
                        "actions",
                        "options",
                    ],
                ],
                "id": 4,
                "jsonrpc": "2.0",
            }
        )
        return payload
