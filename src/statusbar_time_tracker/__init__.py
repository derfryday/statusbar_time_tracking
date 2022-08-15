from __future__ import annotations

import logging

from rumps import App
from rumps import MenuItem
from rumps import clicked
from rumps import timer

import webbrowser

from statusbar_time_tracker.Enum import WorkState
from statusbar_time_tracker.Util import Util


class StatusBarTimeTracker(App):
    def __init__(self, statusbar_config: dict[str, str]) -> None:
        super(StatusBarTimeTracker, self).__init__("Statusbar Time Tracker", quit_button=MenuItem("Quit", key="q"))
        self.menu = ["Toggle tracking", "Open Smalltime"]
        self.title = WorkState.pause
        self.icon = Util.get_icon_path(self.title)
        self.config = statusbar_config

    def get_own_state(self) -> WorkState:
        for user in Util.get_users(index_url=self.config["smalltime_index_url"]):
            if user[0] == self.config["display_name"]:
                logging.debug("matched user: %s", user)
                return user[1]
        logging.error("Could not match %s against any user from smalltime!", self.config["display_name"])
        return WorkState.error

    def toggle_state(self):
        own_state: WorkState = self.get_own_state()
        if own_state == WorkState.pause:
            self.title = WorkState.work
        elif own_state == WorkState.work:
            self.title = WorkState.pause
        else:
            self.title = WorkState.error
        self.icon = Util.get_icon_path(self.title)

    @clicked("Toggle tracking")
    def toggle_tracking(self, _):
        Util.toggle_smalltime_tracking(
            username=self.config["username"],
            password_hash=self.config["password_hash"],
            tracker_url=self.config["smalltime_tracker_url"]
        )
        self.toggle_state()

    @clicked("Open Smalltime")
    def open_smalltime(self, _):
        webbrowser.open(url=self.config["smalltime_index_url"])

    @timer(5)
    def check_status(self, _):
        self.title = self.get_own_state()
        self.icon = Util.get_icon_path(self.title)
