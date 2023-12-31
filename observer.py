from emailManager import send_email


class Observer:
    def __init__(
        self,
        access_manager=None,
    ):
        self.access_manager = access_manager

    async def other_kind_of_message(self, other_message):
        print(f"other message : {other_message}")
        for key, value in other_message.items():
            if key == "event":
                if value == "Alive":
                    return

    async def observer(self, data):
        events = data["events"][0]
        reader_bs6 = "555.865.897"
        reader_bs7 = "555.989.578"
        clean_tek_doors = [reader_bs6, reader_bs7]

        try:
            if events["event"] == "RFID Media":
                badgeId = events["publicMediaLabel"]
                reader = data["deviceid"]
                await self.access_manager.did_badge(
                    badgeId=badgeId,
                    reader=reader,
                )

            elif events["event"] == "Code":
                panic = False
                code = events["code"]
                code_reader = data["deviceid"]
                """ if "condition" in events:
                    if events["condition"] == "Triangle Button":
                        print(" Bedrohungsalarm")
                        panic = True"""
                await self.access_manager.code_is_given(
                    code=code, reader=code_reader, is_panic=panic
                    )
            else:
                for key, value in events.items():
                    if key == "condition":
                        if events["condition"] == "Falling Edge":
                            print("Falling Edge")

                        elif events["condition"] == "Rising Edge":
                            print("Rising Edge")
                    else:
                         await self.other_kind_of_message(events)
        except Exception as s:
          #  print(f"from Observer/def observer: {s} + \n events::{events}")

            send_email(
                subject="there is exception in inputState at observer.py",
                message=f"error: {s}",
            )
