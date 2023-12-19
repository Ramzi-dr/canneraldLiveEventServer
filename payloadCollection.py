import json
import os


class PayloadCollection:
    username = os.environ.get("GLUTZ_BST_USER")
    password = os.environ.get("GLUTZ_BST_PASS")
    email_user = os.environ.get("EMAIL_BST_USER")
    email_pass = os.environ.get("EMAIL_BST_PASS")
    eAccess_service_name = "eAccess.service"
    headers = {"Content-Type": "application/json"}
    demo_server = "31.24.10.138:8333"
    # werk-fraubrunnen.onlinezuko.ch
    GlutzUrl = "werk-fraubrunnen.onlinezuko.ch"
    glutzRpcServerUrl = f"http://{username}:{password}@{demo_server}/rpc/"
    backupGlutzRpcUrl = f"http://{username}:{password}@127.0.0.1:8333/rpc/"
    glutzWsServerUrl = f"ws://{username}:{password}@{demo_server}"
    backupServerPort = 8800
    backupServerIp = "192.168.1.251"
    backupServerUrl = f"ws://{backupServerIp}:{backupServerPort}"
    backupGlutzUrl = f"ws://{username}:{password}@127.0.0.1:8333"

    # towFactorAuthenticationId = "5025"  # in Glutz door Properties
    towFactorAuthenticationId = "5022"  # in Glutz door Properties
    masterDoorId = "5026"
    controlledDoorNotification = "5027"
    # masterCodeActionProfileId = "1001"  # in Glutz Codes menu profile non Default
    masterCodeActionProfileId = "1002"  # in Glutz Codes menu profile non Default
    valueLabelId = "5001"
    IO_Module_Type = 103
    E_Reader_IP55_Type = 102
    E_Reader_Type = 101
    relayShortOpenAction = 1
    relayOpenForEver = 4
    relayClose = 16

    IO_ModuleRelay_1 = 2
    IO_ModuleRelay_2 = 4
    #  IO Extender info and spec 3batteryPowered
    IO_Extender_Type = 80
    IO_Extender_output_1_openDoor = 2
    IO_Extender_output_2_openDoorIsActivate = 4
    IO_Extender_output_3_Led_masterCode = 8
    IO_Extender_output_4 = 16
    IO_Extender_output_5 = 32
    IO_Extender_output_6_Panic = (
        64  # AlarmSystem Panic activate the output for 3 Seconds
    )

    IO_Extender_output_7_PanicIsActivate = 128
    IO_Extender_output_8_disarm = 256
    IO_Extender_input_1_kurzzeitentriegelung = "Input 1"
    IO_Extender_input_2_tuerzustandVirtual = "Input 2"
    IO_Extender_input_3_tuerzustand = "Input 3"
    IO_Extender_input_6_austrittstaster = (
        "Input 6"  # activate AlarmSystem after 45 Seconds Output 8
    )
    IO_Extender_input_7_signal_EMA_virtual = (
        "Input 7"  # activate AlarmSystem after 45 Seconds Output 8
    )
    IO_Extender_input_8_ZustandEma = "Input 8"  # AlarmSystem state
    state_all_inputs_low = 0
    state_input_1_High = 1
    state_input_2_High = 2
    state_input_3_High = 4
    state_input_4_High = 8  #  clean-tek Schleuse activ
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

    def accessPointPropertyData(property):
        accessPointData = json.dumps(
            {
                "method": "eAccess.getModel",
                "params": [
                    "AccessPointPropertyData",
                    {"propertyId": property},
                    [],
                ],
                "id": 2,
                "jsonrpc": "2.0",
            }
        )
        return accessPointData

    def media(userId):
        media_data = json.dumps(
            {
                "method": "eAccess.getModel",
                "params": [
                    "Media",
                    {"userId": userId},
                    [
                        "id",
                        "userId",
                        "actionProfileId",
                        "publicMediaLabel",
                    ],
                ],
                "id": 8,
                "jsonrpc": "2.0",
            }
        )
        return media_data

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
            "params": [
                "UserPropertyData",
                {"actionProfileId": masterCodeActionProfileId},
            ],
            "id": 26,
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
