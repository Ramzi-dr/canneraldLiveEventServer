#!/usr/bin/env python
import asyncio
import threading
import websockets.exceptions
from websockets import connect
from usersData import UsersData
from doorsData import DoorsData
from inputsState import update_rpcUrl as update_rpcUrl2
from payloadCollection import *
from listenDefExtentions import *
from messageFilter import MessageFilter
from startStopGlutz import *
from rpcCommands import update_rpcUrl as update_rpcUrl1

main_server_online = True
backup_wSserver_online = True
servers_num = 2
counter_backupWs = 0
message_sent = 0
run = True


async def listen(url, serverInfo):
    global main_server_online
    global run

    while run:
        try:

            async with connect(url) as websocket:
                if url == PayloadCollection.glutzWsServerUrl:
                    main_server_online = True
                    if servers_num == 3 and main_server_online:
                       
                        run = False
                        await determine_main(True)
                        print('we are going out')
                        break
                    if servers_num == 2:
                        await websocket.send(json.dumps(PayloadCollection.message))
                        while run:
                            
                            message = json.loads(await websocket.recv())
                            print(message)
                            message_filter = MessageFilter()
                            data = message_filter.messageFilter(message=message)
                            door = message_filter.get_door_id(message=message)
                            if door is not None:
                                if door not in doors_instances:
                                    asyncio.create_task(handle_door(door, data))
                                else:
                                    observer = doors_instances.get(
                                        (threading.current_thread().ident, door)
                                    )
                                    await observer.observer(data)
                            if not run:
                                print('going out')

                if url == PayloadCollection.backupGlutzUrl:
                    if servers_num == 3 and not main_server_online:
                        print(f'glutz main backup is online {serverInfo}')
                        await websocket.send(json.dumps(PayloadCollection.message))
                        while not main_server_online:
                            message = json.loads(await websocket.recv())
                            print(message)
                            message_filter = MessageFilter()
                            data = message_filter.messageFilter(message=message)
                            door = message_filter.get_door_id(message=message)
                            if door is not None:
                                if door not in doors_instances:
                                    asyncio.create_task(handle_door(door, data))
                                else:
                                    observer = doors_instances.get(
                                        (threading.current_thread().ident, door)
                                    )
                                    await observer.observer(data)

                elif url == PayloadCollection.backupWsServerUrl:
                    print(f'websocket backup is online {serverInfo}')
                    await websocket.send(json.dumps("hoi from Cannerald Event Server"))
                    while run:
                        json.loads(await websocket.recv())

        except (ConnectionRefusedError, websockets.exceptions.ConnectionClosedOK,
                websockets.exceptions.ConnectionClosedError,
                OSError, asyncio.exceptions.TimeoutError, websockets.ConnectionClosed, Exception) as e:

            if url == PayloadCollection.glutzWsServerUrl and servers_num == 2:
                main_server_online = False
                await determine_main(False)
                break
            if url == PayloadCollection.backupGlutzUrl and main_server_online:
                run = False
                await determine_main(True)
                break
            if url == PayloadCollection.backupWsServerUrl:
                await asyncio.sleep(3)
                print(f'the back WS Server is down: {serverInfo}')
                return


async def main_with_2_servers():
    await asyncio.sleep(1)
    global servers_num
    servers_num = 2
    try:
        await asyncio.gather(
            listen(
                url=PayloadCollection.glutzWsServerUrl, serverInfo=PayloadCollection.GlutzUrl
            ),
            listen(
                url=PayloadCollection.backupWsServerUrl, serverInfo=PayloadCollection.backupWsServerIp
            ),
        )
    except KeyboardInterrupt:
        print("Server shutting down...")
    except Exception as e:
        print(f"An error occurred: {e}")
        sendMail_afterException(serverInfo='async def main_with_2_servers():', exception=f"General Error {e}")


async def main_with_3_servers():
    global servers_num
    servers_num = 3
    try:
        await asyncio.gather(
            listen(
                url=PayloadCollection.glutzWsServerUrl, serverInfo=PayloadCollection.GlutzUrl
            ),
            listen(
                url=PayloadCollection.backupWsServerUrl, serverInfo=PayloadCollection.backupWsServerIp
            ),
            listen(
                url=PayloadCollection.backupGlutzUrl, serverInfo='local Glutz Server'
            ),
        )
    except KeyboardInterrupt:
        print("Server shutting down...")
    except Exception as e:
        print(f"An error occurred: {e}")
        sendMail_afterException(serverInfo='async def main_with_3_servers():', exception=f"General Error {e}")


async def determine_main(mainGlutz_online):
    await asyncio.sleep(2)
    if mainGlutz_online:
        print("using main_with_2_servers()")
        print('the back glutz server is not running ')
       # stop_service(PayloadCollection.eAccess_service_name)
       # update_rpcUrl1(new_url=PayloadCollection.glutzRpcServerUrl)
       ### update_rpcUrl2(new_url=PayloadCollection.glutzRpcServerUrl)
        #UsersData.update_common_url(new_url=PayloadCollection.glutzRpcServerUrl)
        #DoorsData.update_common_url(new_url=PayloadCollection.glutzRpcServerUrl)
        await main_with_2_servers()

    else:
        print("using main_with_3_servers()")
        ##start_service(PayloadCollection.eAccess_service_name)
        #update_rpcUrl1(new_url=PayloadCollection.backupGlutzRpcUrl)
        #update_rpcUrl2(new_url=PayloadCollection.backupGlutzRpcUrl)
        ##UsersData.update_common_url(new_url=PayloadCollection.backupGlutzRpcUrl)
        #DoorsData.update_common_url(new_url=PayloadCollection.backupGlutzRpcUrl)
        await main_with_3_servers()


if __name__ == "__main__":
    asyncio.run(determine_main(True))
