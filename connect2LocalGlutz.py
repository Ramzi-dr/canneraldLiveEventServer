import asyncio
import threading

import websockets.exceptions
from websockets import connect

from accessManager import AccessManager
from emailManager import send_email
from messageFilter import MessageFilter
from observer import *
from payloadCollection import *

# Define the global variable 'doors_instances' at the module level
doors_instances = {}


def delete_door_instance(door_id):
    global doors_instances
    thread_id = threading.current_thread().ident
    if (thread_id, door_id) in doors_instances:
        del doors_instances[(thread_id, door_id)]
        print(f"Threading stopped for door instance. {door_id}")


def add_door_instance(door_id):
    global doors_instances
    thread_id = threading.current_thread().ident
    doors_instances[(thread_id, door_id)] = doors_instances.get(
        (thread_id, door_id), create_observer()
    )


def create_observer():
    access_manager = AccessManager(
        doors_instances, delete_door_instance
    )  # Pass the doors_instances and delete_door_instance function
    if access_manager is None:
        print("Access manager is None in create_observer()")
        return None
    return Observer(access_manager)


async def handle_door(door_id, data):
    add_door_instance(door_id=door_id)

    observer = doors_instances.get((threading.current_thread().ident, door_id))
    if observer is None:
        observer = create_observer()
        doors_instances[(threading.current_thread().ident, door_id)] = observer

    # The observer object might be None if `create_observer()` returns None.
    if observer:
        await observer.observer(data)
    else:
        print(f"Observer is None for door_id: {door_id}")


glutzServe_isOffline = True


def update_GlutzServerState(is_offline):
    global glutzServe_isOffline
    glutzServe_isOffline = is_offline


async def listen():
    counter = 0
    connected = False
    url = PayloadCollection.backupGlutzUrl
    while glutzServe_isOffline:
        print(f"insinde the while : {glutzServe_isOffline}")
        try:
            async with connect(url) as websocket:
                await websocket.send(json.dumps(PayloadCollection.message))
                print("Connected to Glutz Server")
                counter = 0
                connected = True
                while True:
                    message = json.loads(await websocket.recv())
                    print(f"message listen() in connect2LocalGlutz: {message}")
                    message_filter = MessageFilter()
                    data = message_filter.messageFilter(message=message)
                    door = message_filter.get_door_id(data=message)

                    if door is not None:
                        if door not in doors_instances:
                            # Start a new thread or process to handle the new door_id
                            asyncio.create_task(handle_door(door, data))
                        else:
                            observer = doors_instances.get(
                                (threading.current_thread().ident, door)
                            )
                            await observer.observer(data)
                        # ... Continue processing existing door_ids ...
        except ConnectionRefusedError:
            print(f"Hoi We don't have a connection. Please control the Server: {url} .")
            await asyncio.sleep(1)

            counter += 1

            if counter == 50 or counter == 500 or counter == 5000:
                exceptionMessage = "ConnectionRefusedError"
                send_email(
                    subject="there is Exception in connect2LocalGlutz at Listen Def  ",
                    message=f"error: {exceptionMessage}",
                )

        except (
            websockets.exceptions.ConnectionClosedOK,
            websockets.exceptions.ConnectionClosedError,
        ):
            print(f"Hoi We lost connection. Please control the Internet. {url}")
            await asyncio.sleep(1)
            print(f"I am trying to reconnect for the {counter} time to: {url} .")
            if counter == 50 or counter == 500 or counter == 500:
                exceptionMessage = (
                    "websockets.exceptions.ConnectionClosedOK-ConnectionClosedError,"
                )
                send_email(
                    subject="there is Exception in connect2LocalGlutz at Listen Def  ",
                    message=f"error: {exceptionMessage}",
                )

        except OSError:
            await asyncio.sleep(1)
            print(
                f"Server: {url} is down. There is no connection, and I will try to reconnect for the {counter} time."
            )
            counter += 1
            if counter == 50 or counter == 500 or counter == 5000:
                exceptionMessage = "OsError"
                send_email(
                    subject="there is Exception in connect2LocalGlutz at Listen Def  ",
                    message=f"error: {exceptionMessage}",
                )

        except asyncio.exceptions.TimeoutError:
            await asyncio.sleep(1)
            counter += 1
            if counter == 50 or counter == 500 or counter == 5000:
                exceptionMessage = "asyncio.exceptions.TimeoutError,"
                send_email(
                    subject="there is Exception in connect2LocalGlutz at Listen Def  ",
                    message=f"error: {exceptionMessage}",
                )

        except Exception as e:
            print(f"exeptoioon : {e}")
            # sendMail_afterException(serverInfo=serverInfo, exeption=e)

        except websockets.ConnectionClosed:
            print("except websockets.ConnectionClosed:")
            counter += 1
            if counter == 50 or counter == 500 or counter == 5000:
                exceptionMessage = "asyncio.exceptions.TimeoutError,"
                send_email(
                    subject="there is Exception in connect2LocalGlutz at Listen Def  ",
                    message=f"error: {exceptionMessage}",
                )

            continue
        connected = False


async def main():
    try:
        await asyncio.gather(
            listen(),
        )
    except KeyboardInterrupt:
        print("Server shutting down...")
    except Exception as e:
        print(f"An error occurred: {e}")
        send_email(
            subject="there is Exception in connect2LocalGlutz at Listen Def  ",
            message=f"error: {e}",
        )


# if __name__ == "__main__":
# asyncio.run(main())
