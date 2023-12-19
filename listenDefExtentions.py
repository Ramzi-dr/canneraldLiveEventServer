import threading
from accessManager import AccessManager
from emailManager import send_email
from observer import Observer

doors_instances = {}


def delete_door_instance(door_id):
    global doors_instances
    thread_id = threading.current_thread().ident
    if (thread_id, door_id) in doors_instances:
        del doors_instances[(thread_id, door_id)]


def add_door_instance(door_id):
    print("in try")
    global doors_instances
    thread_id = threading.current_thread().ident
    doors_instances[(thread_id, door_id)] = doors_instances.get(
        (thread_id, door_id), create_observer()
    )


def create_observer():
    access_manager = AccessManager(doors_instances, delete_door_instance)
    if access_manager is None:
        return None
    return Observer(access_manager)


async def handle_door(door_id, data):
    if door_id is not None and data:
        try:
            add_door_instance(
                door_id=door_id,
            )

            observer = doors_instances.get((threading.current_thread().ident, door_id))
            if observer is None:
                observer = create_observer()
                doors_instances[(threading.current_thread().ident, door_id)] = observer
            if observer:
                await observer.observer(data)

        except Exception as e:
            print(e)
            '''send_email(
                subject="exception in listenDef Extentions.py at handle_door",
                message=f"""error : {e}  \n
                data :{data}\n
                door_id:{door_id} """,
            )'''
