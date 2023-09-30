#!/usr/bin/env python
import asyncio
import threading
import websockets.exceptions
from websockets import connect
from doorsData import DoorsData

from inputsState import update_rpcUrl as update_rpcUrl2
from payloadCollection import *
from listenDefExtentions import *
from listenDefExtentions import *
from messageFilter import MessageFilter
from startStopGlutz import *
from rpcCommands import update_rpcUrl as update_rpcUrl1
import json

from usersData import UsersData

glutz_server_online = False
backup_server_online = False
local_Database_server_online = False
servers_num = 2
run = True


user_did_badge = False

async def send_pingToBackupServer(websocket,connected):
    is_connected = connected
    while(is_connected):
        try:
            await websocket.send(json.dumps("ping"))
            await asyncio.sleep(5)
        except Exception as e:
            print(f'exception from sendPin in main.py {e}')
            is_connected = False
    
    
async def message_generator(websocket):
    global run

    while run:
        message = json.loads(await websocket.recv())

        message_filter = MessageFilter()
        data = await message_filter.messageFilter(message=message)
        door = await message_filter.get_door_id(data=data)

        if door is not None:
            if door not in doors_instances:
                asyncio.create_task(
                    handle_door(
                        door,
                        data,
                        users_data=message_filter.users_data,
                        doors_data=message_filter.doors_data,
                    )
                )
            elif not user_did_badge:
                observer = doors_instances.get((threading.current_thread().ident, door))
                await observer.observer(data)


async def listen(url, serverInfo):
    global glutz_server_online
    global backup_server_online
    global local_Database_server_online
    global run

    while run:
        try:
            async with connect(url) as websocket:
                if url == PayloadCollection.glutzWsServerUrl:
                    glutz_server_online = True
                    if servers_num == 3 and glutz_server_online:
                        print(
                            f"from ( if servers_num == 3 and main_server_online:)glutz server is: {glutz_server_online}online servers number :{servers_num}  "
                        )
                        await determine_main(True)

                    if servers_num == 2:
                        await websocket.send(json.dumps(PayloadCollection.message))
                        await message_generator(websocket=websocket)

                if url == PayloadCollection.backupGlutzUrl:
                    if servers_num == 3 and not glutz_server_online:
                        print(f"glutz main backup is online {serverInfo}")
                        await websocket.send(json.dumps(PayloadCollection.message))
                        await message_generator(websocket)

                elif url == PayloadCollection.backupWsServerUrl:
                    print(f"websocket backup is online {serverInfo}")
                    await send_pingToBackupServer(websocket=websocket,connected=True)
                    while run:
                        json.loads(await websocket.recv())

        except (
            ConnectionRefusedError,
            websockets.exceptions.ConnectionClosedOK,
            websockets.exceptions.ConnectionClosedError,
            OSError,
            asyncio.exceptions.TimeoutError,
            websockets.ConnectionClosed,
            Exception,
        ) as e:
            if isinstance(e, ConnectionRefusedError):
                print(f'Connection to {url} refused Server may be offline')
            else:
                
                print(f"Error to debug : {e}")
               
            await asyncio.sleep(2)
            if url == PayloadCollection.glutzWsServerUrl and servers_num == 2:
                print("glutz server is Offline")

                main_server_online = False
                await determine_main(False)

            if url == PayloadCollection.backupGlutzUrl and glutz_server_online:
                print(
                    "from exception url url == PayloadCollection.backupGlutzUrl and glutz_server_online:"
                )
                return

            if url == PayloadCollection.backupWsServerUrl:
                await send_pingToBackupServer(websocket=url,connected=False)
                await asyncio.sleep(10)
                print(f"the back WS Server is down: {serverInfo}")
                
                continue
            print(f"exception in here : {e}")
            print(type(e))
            print(url)
            if (
                str(e) == "no close frame received or sent"
                and url == PayloadCollection.glutzWsServerUrl
            ):
                print("he")

                main_server_online = False
                await asyncio.sleep(5)
                await determine_main(False)


async def main_with_2_servers():
    global servers_num
    servers_num = 2
    try:
        await asyncio.gather(
            listen(
                url=PayloadCollection.glutzWsServerUrl,
                serverInfo=PayloadCollection.GlutzUrl,
            ),
            listen(
                url=PayloadCollection.backupWsServerUrl,
                serverInfo=PayloadCollection.backupWsServerIp,
            ),
        )
    except KeyboardInterrupt:
        print("Server shutting down...")
    except Exception as e:
        print(f"An error occurred: {e}")
        sendMail_afterException(
            serverInfo="async def main_with_2_servers():",
            exception=f"General Error {e}",
        )


async def main_with_3_servers():
    global servers_num
    servers_num = 3
    try:
        await asyncio.gather(
            listen(
                url=PayloadCollection.glutzWsServerUrl,
                serverInfo=PayloadCollection.GlutzUrl,
            ),
            listen(
                url=PayloadCollection.backupWsServerUrl,
                serverInfo=PayloadCollection.backupWsServerIp,
            ),
            listen(
                url=PayloadCollection.backupGlutzUrl, serverInfo="local Glutz Server"
            ),
        )
    except KeyboardInterrupt:
        print("Server shutting down...")
    except Exception as e:
        print(f"An error occurred: {e}")
        sendMail_afterException(
            serverInfo="async def main_with_3_servers():",
            exception=f"General Error {e}",
        )


async def determine_main(online):
    global run
    await MessageFilter().get_users()
    await MessageFilter().get_doors()
    run = False
    await asyncio.sleep(1)
    run = True
    if online:
        print("using main_with_2_servers()")
        print("the back glutz server is not running ")
        stop_service(PayloadCollection.eAccess_service_name)
        update_rpcUrl1(new_url=PayloadCollection.glutzRpcServerUrl)
        update_rpcUrl2(new_url=PayloadCollection.glutzRpcServerUrl)
        UsersData.update_common_url(new_url=PayloadCollection.glutzRpcServerUrl)
        DoorsData.update_common_url(new_url=PayloadCollection.glutzRpcServerUrl)
        await main_with_2_servers()

    else:
        print("using main_with_3_servers()")
        start_service(PayloadCollection.eAccess_service_name)
        update_rpcUrl1(new_url=PayloadCollection.backupGlutzRpcUrl)
        update_rpcUrl2(new_url=PayloadCollection.backupGlutzRpcUrl)
        UsersData.update_common_url(new_url=PayloadCollection.backupGlutzRpcUrl)
        DoorsData.update_common_url(new_url=PayloadCollection.backupGlutzRpcUrl)
        await main_with_3_servers()


if __name__ == "__main__":
    asyncio.run(determine_main(True))
