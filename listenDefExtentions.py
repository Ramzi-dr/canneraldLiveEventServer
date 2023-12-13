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


def add_door_instance(door_id, users_data, doors_data):
    global doors_instances
    thread_id = threading.current_thread().ident
    doors_instances[(thread_id, door_id)] = doors_instances.get(
        (thread_id, door_id), create_observer(users_data, doors_data)
    )


def create_observer(users_data, doors_data):
    access_manager = AccessManager(
        doors_instances, delete_door_instance, users_data, doors_data
    )
    if access_manager is None:
        return None
    return Observer(access_manager)


async def handle_door(door_id, data, users_data, doors_data):
    if door_id is not None and data is not None and users_data and doors_data:
        try:
            add_door_instance(
                door_id=door_id,
                users_data=users_data,
                doors_data=doors_data,
            )

            observer = doors_instances.get((threading.current_thread().ident, door_id))
            if observer is None:
                observer = create_observer(users_data=users_data, doors_data=doors_data)
                doors_instances[(threading.current_thread().ident, door_id)] = observer
            if observer:
                await observer.observer(data)

        except Exception as e:
            send_email(
                subject= "exception in listenDefExtentions.py at handle_door", 
                message=f'''error : {e}  \n users_data :{users_data} \n doors_data :{doors_data} \n
                data :{data}\n
                door_id:{door_id} '''
            )
