# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import socket
import json

PORT = 1234

def command(cmd):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = json.dumps(cmd).encode("utf-8")
    dest = ("localhost", PORT)
    s.sendto(payload, dest)

class ActionStop(Action):

    def name(self) -> Text:
        return "action_stop"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cmd = ["stop"]
        command(cmd)

        return []
    
class ActionPause(Action):

    def name(self) -> Text:
        return "action_pause"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cmd = ["pause"]
        command(cmd)

        return []

class ActionResume(Action):

    def name(self) -> Text:
        return "action_resume"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cmd = ["resume"]
        command(cmd)

        return []

class ActionPlay(Action):

    def name(self) -> Text:
        return "action_play"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        title = tracker.get_slot("title")
        cmd = ["play", title]
        command(cmd)

        return []