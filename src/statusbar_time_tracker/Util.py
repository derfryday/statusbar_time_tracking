import logging
import subprocess
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from statusbar_time_tracker import LaunchAgent
from statusbar_time_tracker.Enum import WorkState
from statusbar_time_tracker.Updater import Updater

import urllib3

urllib3.disable_warnings()


class Util:
    @staticmethod
    def get_users(index_url: str) -> list[tuple[str, WorkState]]:
        enriched_users: list[tuple[str, WorkState]] = []

        status_response = requests.get(index_url, verify=False, timeout=1)
        response_content = status_response.content
        if status_response.status_code == 200:
            soup = BeautifulSoup(response_content, "html.parser")
            raw_users = soup.find_all("td", {"class": "alert"})
            for user in raw_users:
                raw_user_state = user.__dict__["attrs"]["class"][1]
                clean_username = str(user.__dict__["next_element"]).strip()
                user_state = WorkState.error
                if raw_user_state == "alert-success":
                    user_state = WorkState.work
                elif raw_user_state == "alert-error":
                    user_state = WorkState.pause

                user_tuple = (clean_username, user_state)
                enriched_users.append(user_tuple)
        else:
            logging.error(
                "Could not get users from smalltime! Statuscode: %s\nContent:\n%s",
                status_response.status_code,
                response_content
            )
        return enriched_users

    @staticmethod
    def toggle_smalltime_tracking(username: str, password_hash: str, tracker_url: str) -> None:
        args = {
            "name": username,
            "secret": password_hash
        }
        response = requests.get(url=tracker_url, params=args, timeout=60)
        if response.status_code != 200:
            logging.error(
                "Could not toggle tracking state for user \"%s\"! Statuscode: %s\nContent:\n%s",
                username,
                response.status_code,
                response.content
            )

    @staticmethod
    def get_icon_path(work_state: WorkState) -> str:
        base_path = Path(__file__).resolve().parent / "resources"
        icon_map: dict[WorkState, str] = {
            WorkState.work: f"{base_path}/working.png",
            WorkState.pause: f"{base_path}/coffee-break.png",
            WorkState.error: f"{base_path}/warning.png"
        }

        return icon_map[work_state]

    @staticmethod
    def update_and_restart() -> None:
        Updater.update()
        LaunchAgent.restart_launchd_agent()

