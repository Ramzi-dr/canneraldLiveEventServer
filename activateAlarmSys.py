import asyncio
import time
import threading
from rpcCommands import Toggle_alarmSystem_output_8


class ActivateAlarmSys:
    _instances = {}

    def __init__(self, deviceId) -> None:
        self.deviceId = deviceId
        self.timer_running = False
        self.timer_duration = None
        self.timer_start_time = None
        self.seconds = 5
        self.printCounter = 25

    def _start_timer(self):
        while self.timer_running:
            current_time = time.time()

            elapsed_time = current_time - self.timer_start_time
            print(
                f" Alarm for ID {self.deviceId} Will be activated in {self.printCounter}..."
            )
            self.printCounter -= 1
            if elapsed_time >= self.timer_duration:
                self.timer_running = False
                print(f"Timer for ID {self.deviceId} is out")
                asyncio.run(self.arm())
            else:
                time_to_sleep = min(1, self.timer_duration - elapsed_time)
                time.sleep(time_to_sleep)

    def activate_timer(self):
        if self.deviceId in ActivateAlarmSys._instances:
            # Timer for this ID is already running, reset it
            print(f"Resetting timer for ID {self.deviceId}")
            ActivateAlarmSys._instances[self.deviceId].timer_running = False

        # Create a new instance or update the existing one
        self.timer_duration = self.seconds
        self.timer_start_time = time.time()
        self.timer_running = True
        ActivateAlarmSys._instances[self.deviceId] = self
        print(f"Timer for ID {self.deviceId} is running now")
        # Start the timer in a separate thread
        timer_thread = threading.Thread(target=self._start_timer)
        timer_thread.start()

    async def arm(self):
        Toggle_alarmSystem_output_8(deviceId=self.deviceId, action="low")
