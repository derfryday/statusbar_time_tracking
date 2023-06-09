from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from rumps import App
from rumps import MenuItem
from rumps import timer
import rumps

from statusbar_time_tracker.Agent import LaunchAgent
from statusbar_time_tracker.Updater import Updater

rumps.debug_mode(True)
from importlib import metadata

import webbrowser

from statusbar_time_tracker.Enum import WorkState
from statusbar_time_tracker.Util import Util


class StatusBarTimeTracker(App):
    def __init__(self, config_path: Path) -> None:
        super(StatusBarTimeTracker, self).__init__("Statusbar Time Tracker", quit_button=MenuItem("Quit", key="q"))

        self.config_path = config_path
        self.config = json.loads(config_path.read_text(encoding="utf-8"))
        self.state: WorkState = WorkState.error
        self.title = "starting..."
        self.icon = Util.get_icon_path(self.state)

        self.toggle_button: MenuItem = MenuItem("Toggle Tracking", callback=self.toggle_tracking)

        self.menu = [
            self.toggle_button,
            MenuItem("Open Smalltime", callback=self.open_smalltime),
            None,
            ["Settings", [
                MenuItem("Reload Config", callback=self.reload_config),
                MenuItem("Open Config", callback=self.open_config),
                MenuItem("Toggle Icon Only", callback=self.toggle_icon_only),
                MenuItem("Check for Updates", callback=self.check_for_updates)
                        ],
            ],
            None,
            f"version: {metadata.version(__package__ or __name__)}",
            None
        ]

    @staticmethod
    def check_for_updates(menu_item: MenuItem):
        logging.info("Checking for updates...")

        if menu_item.title == "Check for Updates":
            if Updater.update_available():
                logging.info("Updates found!")
                menu_item.title = "Install Update and Restart"
        elif menu_item.title == "Install Update and Restart":
            Updater.update()

    def open_config(self, _):
        os.system(f"open {str(self.config_path)}")

    def update_config(self):
        self.config_path.write_text(json.dumps(self.config))

    def toggle_icon_only(self, _):
        self.config["icon_only"] = not self.config["icon_only"]
        self.update_config()
        self.update_title()

    def update_title(self) -> None:
        if self.config.get("icon_only", False) is False:
            self.title = self.state
        else:
            self.title = ""

    def update_toggle_icon_title(self):
        if self.state == WorkState.pause:
            self.toggle_button.title = "Start Tracking"
        elif self.state == WorkState.work:
            self.toggle_button.title = "Stop Tracking"

    def update_icon(self) -> None:
        self.icon = Util.get_icon_path(self.state)

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
            self.state = WorkState.work

        elif own_state == WorkState.work:
            self.state = WorkState.pause
        else:
            self.state = WorkState.error

        self.update_icon()
        self.update_title()
        self.update_toggle_icon_title()

    def toggle_tracking(self, _):
        Util.toggle_smalltime_tracking(
            username=self.config["username"],
            password_hash=self.config["password_hash"],
            tracker_url=self.config["smalltime_tracker_url"]
        )
        self.toggle_state()

    def open_smalltime(self, _):
        webbrowser.open(url=self.config["smalltime_index_url"])

    def reload_config(self, _):
        self.config = json.loads(self.config_path.read_text(encoding="utf-8"))

    @timer(5)
    def check_status(self, _):
        new_state: WorkState = self.get_own_state()
        if new_state != self.state:
            self.state = new_state
            self.update_icon()
            self.update_title()
            self.update_toggle_icon_title()
