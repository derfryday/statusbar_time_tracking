#!/usr/bin/env bash

FILE_NAME="de.derfryday.statusbar-time-tracker"
PROJECT_DIR="$(dirname $0)"
VERSION=$(/usr/bin/sed -nr "s#version = \"([0-9\.]+)\"#\1#p" "${PROJECT_DIR}/pyproject.toml")

# shellcheck disable=SC2164
cd "$PROJECT_DIR"

function create_launch_agent() {
    echo "creating launch agent file..."
    /usr/bin/sed -e "s#PATH_TO_STATUSBAR_EXECUTABLE#$(which statusbar_time_tracker)#g" "${PROJECT_DIR}/${FILE_NAME}.dist.plist" > "${PROJECT_DIR}/${FILE_NAME}.plist"
}

function install_launch_agent() {
    LAUNCH_AGENTS_DIRECTORY="$HOME/Library/LaunchAgents"

    echo "installing launch agent file..."
    test -d "$LAUNCH_AGENTS_DIRECTORY" || mkdir -p "$LAUNCH_AGENTS_DIRECTORY"
    mv "${PROJECT_DIR}/${FILE_NAME}.plist" "${LAUNCH_AGENTS_DIRECTORY}/" && \
    echo "loading launch agent file..." && \
    launchctl load -w "${LAUNCH_AGENTS_DIRECTORY}/${FILE_NAME}.plist" && \
    echo "enabling launch agent..." && \
    launchctl enable "gui/${UID}/${FILE_NAME}" && \
    echo "starting launch agent" && \
    launchctl start "$FILE_NAME"
}

function build_wheel() {
    poetry build -f wheel
}

function install_pip_package() {
    WHEEL_FILE="${PROJECT_DIR}/dist/statusbar_time_tracker-${VERSION}-py3-none-any.whl"
    if [ -f "$WHEEL_FILE" ]; then
        pip install "$WHEEL_FILE"
    else
        >&2 echo "Could not find wheel file for current package version!"
        exit 1
    fi
}

function help() {
    echo "./$(basename $0) --install-agent"
    echo -e "\tcreates and installs the launch agent"
    echo ""
    echo "./$(basename $0) --install-package"
    echo -e "\tbuilds and install the python package"
    echo ""
    echo "./$(basename $0) --install"
    echo -e "\tcreates and installs both the launch agent and python package"
    echo ""
    echo "./$(basename $0) --help"
    echo -e "\tprints this help"
}

case $1 in
    --install-agent)
        create_launch_agent
        install_launch_agent
        exit 0
    ;;    
    --install-package)
        build_wheel
        install_pip_package
        exit 0
    ;;
    --install)
        create_launch_agent
        install_launch_agent
        build_wheel
        install_pip_package
        exit 0
    ;;
    --help)
        help
        exit 0
    ;;
esac 
help