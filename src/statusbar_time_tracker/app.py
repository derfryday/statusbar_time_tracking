from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

from statusbar_time_tracker.agent import LaunchAgent

from statusbar_time_tracker import StatusBarTimeTracker
from argparse import ArgumentParser
import hashlib


def configure() -> None:
    username: str = input("username: ")
    display_name: str = input("display name (as shown on smalltime overview): ")
    password: str = input("password: ")
    smalltime_index_url: str = input("smalltime index url: ")
    smalltime_tracker_url: str = input("smalltime tracker url: ")
    new_config: dict[str, str | int] = {
        "username": username,
        "display_name": display_name,
        "password_hash": hashlib.sha1(password.encode("utf-8")).hexdigest(),
        "smalltime_index_url": smalltime_index_url,
        "smalltime_tracker_url": smalltime_tracker_url
    }
    config_dir_path = Path.home() / ".config"
    new_config_file = config_dir_path / "statusbar_config.json"
    new_config_file.write_text(json.dumps(new_config), encoding="utf-8")


def setup() -> None:
    configure()
    LaunchAgent.create_launchd_file()


def main() -> None:
    parser = ArgumentParser(description="Statusbar Time Tracker command line interface")
    parser.add_argument("--setup", dest="run_setup", action="store_true", default=False)
    parser.add_argument("--install", dest="install", action="store_true", default=False)
    parser.add_argument("--uninstall", dest="uninstall", action="store_true", default=False)
    parser.add_argument("--configure", dest="configure", action="store_true", default=False)
    parser.add_argument("--log-level", dest="log_level", choices=["debug", "info", "warning", "error"], default="info")

    args = parser.parse_args()

    log_file: Path = Path.home() / "Library/Logs/StatusbarTimeTracker.log"

    logging.basicConfig(filename=str(log_file), level=getattr(logging, args.log_level.upper()))
    logging.getLogger().addHandler(logging.StreamHandler())
    config_path = Path.home() / ".config/statusbar_config.json"

    if args.run_setup:
        logging.info("Starting Setup wizard...")
        setup()
        sys.exit(0)
    elif args.install:
        LaunchAgent.create_launchd_file()
        LaunchAgent.enable_launchd_service()
        LaunchAgent.start_launchd_agent()
        sys.exit(0)
    elif args.uninstall:
        LaunchAgent.disable_launchd_service()
        LaunchAgent.delete_launchd_file()
        sys.exit(0)
    elif args.configure:
        configure()
        sys.exit(0)

    if not config_path.exists():
        logging.error("Config file does not exist, please run setup or configuration wizard!")
        sys.exit(1)
    else:
        app: StatusBarTimeTracker = StatusBarTimeTracker(config_path=config_path)
        logging.info("Starting StatusbarTimeTracker...")
        app.run()


if __name__ == "__main__":
    main()
