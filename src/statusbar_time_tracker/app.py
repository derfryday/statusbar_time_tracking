from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

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


def install() -> None:
    target_launch_agents_path: Path = Path.home() / "Library/LaunchAgents"
    logging.info("Launch agent will be installed into %s", str(target_launch_agents_path))
    file_name: str = "statusbar_time_tracking.plist"
    launch_file = target_launch_agents_path / file_name
    template_file: Path = Path(__file__).resolve().parent / "resources" / file_name
    raw_template = template_file.read_text(encoding="utf-8")

    python_path: Path = Path(__file__).resolve() / ".venv/bin/python"
    script_path: Path = Path(__file__).resolve()
    project_path: Path = script_path.parent
    raw_template = (
        raw_template
        .replace("%PYTHON_PATH%", str(python_path))
        .replace("%SCRIPT_PATH%", str(script_path))
        .replace("%PROJECT_PATH%", str(project_path))
    )
    logging.info("Installing launch agent %s", str(launch_file))
    launch_file.write_text(raw_template, encoding="utf-8")


def uninstall() -> None:
    target_launch_agents_path: Path = Path("~/Library/LaunchAgents").resolve()
    file_name: str = "statusbar_time_tracking.plist"
    launch_file = target_launch_agents_path / file_name
    logging.info("Uninstalling %s", str(launch_file))
    launch_file.unlink(missing_ok=True)


def setup() -> None:
    configure()
    install()


def main() -> None:
    config_path = Path.home() / ".config/statusbar_config.json"

    parser = ArgumentParser(description="Statusbar Time Tracker command line interface")
    parser.add_argument("--setup", dest="run_setup", action="store_true", default=False)
    parser.add_argument("--install", dest="install", action="store_true", default=False)
    parser.add_argument("--uninstall", dest="uninstall", action="store_true", default=False)
    parser.add_argument("--configure", dest="configure", action="store_true", default=False)
    parser.add_argument("--verbose", "-v", dest="verbose", action="store_true", default=False)

    args = parser.parse_args()

    if args.run_setup:
        setup()
        sys.exit(0)
    elif args.install:
        install()
        sys.exit(0)
    elif args.uninstall:
        uninstall()
        sys.exit(0)
    elif args.configure:
        configure()
        sys.exit(0)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if not config_path.exists():
        logging.error("Config file does not exist, please run setup or configuration wizard!")
        sys.exit(1)
    else:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        app = StatusBarTimeTracker(statusbar_config=config)
        app.run()
