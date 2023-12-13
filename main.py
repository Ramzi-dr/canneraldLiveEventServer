#!/usr/bin/env python
import asyncio
import json
import threading
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from websockets import connect

from listenDefExtentions import *
from messageFilter import MessageFilter
from payloadCollection import *

glutz_server_online = False
backup_server_online = False
user_did_badge = False

async def message_generator(websocket):
    
    while True:
        try:
            message = json.loads(await websocket.recv())
           # print(message)
            message_filter = MessageFilter()
            data = await message_filter.messageFilter(message=message)
            door = await message_filter.get_door_id(data=data)
            
            if door is not None:
                if door not in doors_instances:
                    asyncio.create_task(
                        handle_door(
                            door,
                            data,
                            users_data=   message_filter.users_data,
                            doors_data=   message_filter.doors_data,
                        )
                    )
                elif not user_did_badge:
                    observer = doors_instances.get((threading.current_thread().ident, door))
                    await observer.observer(data)
        except (ConnectionClosedOK, ConnectionClosedError) as e:
            print(f"Connection closed unexpectedly: {e}")
            break
        except Exception as e:
            print(f"Error in message_generator: {e}")

async def connect_to_server(url, serverInfo):
    while True:
        try:
            async with connect(url, timeout=60) as websocket:
                print(f"Connected to {serverInfo}")
                if url == PayloadCollection.glutzWsServerUrl:
                    await asyncio.sleep(1)
                    await MessageFilter().get_users()
                    await MessageFilter().get_doors()
                    await websocket.send(json.dumps(PayloadCollection.message))
                    await message_generator(websocket=websocket)
                elif url == PayloadCollection.backupServerUrl:
                    print(f"websocket backup is online {serverInfo}")
                    await websocket.send(json.dumps("hoi from Cannerald Event Server"))
                    send_email(subject="the backup Server is online ", message="")
                    json.loads(await websocket.recv())
        except (ConnectionRefusedError, asyncio.TimeoutError, Exception) as e:
            if url =='await message_filter.get_doors_with_retry()':
                pass
        await asyncio.sleep(2)

async def main_with_2_servers():
    global servers_num
    servers_num = 2
    try:
        # Start both connections in parallel
        await asyncio.gather(
            connect_to_server(
                url=PayloadCollection.glutzWsServerUrl,
                serverInfo=PayloadCollection.GlutzUrl,
            ),
            connect_to_server(
                
                url=PayloadCollection.backupServerUrl,
                serverInfo=PayloadCollection.backupServerIp,
            ),
        )
    except KeyboardInterrupt:
        print("Server shutting down...")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main_with_2_servers())
