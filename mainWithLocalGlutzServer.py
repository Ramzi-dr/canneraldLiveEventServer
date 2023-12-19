#!/usr/bin/env python
import asyncio

import websockets.exceptions
from websockets import connect

from listenDefExtentions import *
from messageFilter import MessageFilter
from payloadCollection import *

glutz_server_online = False
backup_server_online = False
local_Database_server_online = False
servers_num = 2
run = True

user_did_badge = False


async def message_generator(websocket):
    global run
    while run:
        message = json.loads(await websocket.recv())
        print(message)

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
            async with connect(url, timeout=60) as websocket:
                if url == PayloadCollection.glutzWsServerUrl:
                    glutz_server_online = True
                    await asyncio.sleep(3)
                    await MessageFilter().update_users()
                    await MessageFilter().update_doors()
                    if servers_num == 3 and glutz_server_online:
                        print(
                            f"from ( if servers_num == 3 and main_server_online:)glutz server is: {glutz_server_online}"
                            f" online servers number :{servers_num}"
                        )

                        await determine_main(True)

                    if servers_num == 2:
                        await websocket.send(json.dumps(PayloadCollection.message))
                        await message_generator(websocket=websocket)
                if url == PayloadCollection.backupGlutzUrl:
                    if servers_num == 3 and not glutz_server_online:
                        print(f"glutz main backup is online {serverInfo}")
                        await websocket.send(json.dumps(PayloadCollection.message))
                        while not glutz_server_online:
                            await message_generator(websocket)

                elif url == PayloadCollection.backupWsServerUrl:
                    print(f"websocket backup is online {serverInfo}")
                    await websocket.send(json.dumps("hoi from Cannerald Event Server"))
                    send_email(subject="the backup Server is online ", message="")
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
                print(f"Connection to {url} refused. Server may be offline.")

            await asyncio.sleep(2)
            if url == PayloadCollection.glutzWsServerUrl and servers_num == 2:
                print("glutz server is Offline")
                print(f"exception main.py line 94 in glutz server : {e}")
                await asyncio.sleep(60)
                send_email(
                    subject="there is Exception in main at main_with_2_servers ",
                    message=f"error: {e}",
                )

                glutz_server_online = False
                await determine_main(False)

            if url == PayloadCollection.backupGlutzUrl and glutz_server_online:
                break

            if url == PayloadCollection.backupWsServerUrl:
                await asyncio.sleep(60)
                print(f"the back WS Server with IP : {serverInfo} is Down")
                send_email(
                    subject="there is Exception in main at main_with_2_servers ",
                    message=f"error: {e}",
                )
                break
            if (
                str(e) == "no close frame received or sent"
                and url == PayloadCollection.glutzWsServerUrl
            ):
                glutz_server_online = False
                await asyncio.sleep(5)
                await determine_main(False)
            else:
                print(f"Error to  debug in main : {e}")
                send_email(
                    subject="there is Exception in main at Listen Def ",
                    message=f"error: {e}",
                )


async def main_with_2_servers():
    global servers_num
    servers_num = 2
    try:
        await asyncio.gather(
            listen(
                url=PayloadCollection.glutzWsServerUrl,
                serverInfo=PayloadCollection.GlutzUrl,
            ),
            # connect to the backup server websocket
            # listen(
            #     url=PayloadCollection.backupWsServerUrl,
            #     serverInfo=PayloadCollection.backupWsServerIp,
            # ),
        )
    except KeyboardInterrupt:
        print("Server shutting down...")
    except Exception as e:
        print(f"An error occurred: {e}")
        # send_email(
        #     subject="there is Exception in main at main_with_2_servers ",
        #     message=f"error: {e}",
        # )


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
        print(f"exeption in main : {e}")
        # send_email(
        #     subject="there is Exception in main at main_with_3_servers ",
        #     message=f"error: {e}",
        # )


async def determine_main(online):
    global run
    # await MessageFilter().get_users()  this be  activated when the local glutz data server is online -configurate
    # await MessageFilter().get_doors()  this be  activated when the local glutz data server is online- configurate
    run = False
    await asyncio.sleep(1)
    run = True
    if online:
        # stop_service(PayloadCollection.eAccess_service_name)
        # update_rpcUrl1(new_url=PayloadCollection.glutzRpcServerUrl)
        # update_rpcUrl2(new_url=PayloadCollection.glutzRpcServerUrl)
        # UsersData.update_common_url(new_url=PayloadCollection.glutzRpcServerUrl)
        # DoorsData.update_common_url(new_url=PayloadCollection.glutzRpcServerUrl)
        await main_with_2_servers()

    else:
        # start_service(PayloadCollection.eAccess_service_name)
        # update_rpcUrl1(new_url=PayloadCollection.backupGlutzRpcUrl)
        # update_rpcUrl2(new_url=PayloadCollection.backupGlutzRpcUrl)
        # UsersData.update_common_url(new_url=PayloadCollection.backupGlutzRpcUrl)
        # DoorsData.update_common_url(new_url=PayloadCollection.backupGlutzRpcUrl)
        await main_with_3_servers()


if __name__ == "__main__":
    asyncio.run(determine_main(True))
