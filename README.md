# Installation
```bash
wget "https://github.com/derfryday/statusbar_time_trackign/releases/latest/download/StatusbarTimeTracker"

./StatusbarTimeTracker --setup
```
You can put this file anywhere you want really, I'd recommend your home directory or perhaps `~/bin/`. All paths referencing the executable will be set by the executable itself upon setup.

# Updating (starting from version 0.1.4)
To update you can open the `Settings` menu option and click on `Check for Updates`. This will check for updates and change the title of the menu option to `Download Update and Restart` if there are any updates available.
Clicking on `Install Update and Restart` will download the latest version from GitHub, save it over the current binary and restart the Launch Agent.


# Configuration
config file location: `~/.config/statusbar_config.json`

Initial configuration will be handled by the setup.

You can also get to the config file via the `Open Config` button in the `Settings` menu. This will open the config file with your default editor for JSON files.

### configuration parameters:

```json
{
  "username": "c.norris", // the same username you use to log into smalltime
  "display_name": "Chuck Norris", // name as seen on the smalltime overview page
  "password_hash": "d73cbcd9234156a073afb5511f7ceb27413a0d9f", // sha1 checksum of your password
  "smalltime_index_url": "https://your-smalltime-url/index.php", // this is the URL at which you can find the index.php
  "smalltime_tracker_url": "https://your-possibly-different-smalltime-tracker-url/track_time.php" // this is the URL at which you can find the track_time.php which may be under a different URL in case you have everything apart from the tracking locked behind a VPN
}
```

# Compiling from Source
requirements:
- poetry
- Xcode (for the `make` command and clang)

```bash
git clone git@github.com:derfryday/statusbar_time_tracking.git
cd statusbar_time_tracking
make
```

# Debugging
the log file is located at `~/Library/Logs/StatusbarTimeTracker.log`

# Attribution
- credit for the coffee-break icon goes to https://www.flaticon.com/authors/uniconlabs
- credit for the warning icon goes to https://www.freepik.com
- credit for the working icon goes to https://www.flaticon.com/authors/dreamicons

# TODOs:
- [X] update README.md
- [ ] global keyboard shortcut for toggle tracking https://stackoverflow.com/questions/11347862/system-wide-shortcut-for-mac-os-x
- [X] write makefile to make building the binary easier
- [ ] cleanup code
- [X] display `Start Tracking`/`Stop Tracking` based on current state rather than `Toggle Tracking`
- [X] make enabling and disabling of the launchd daemon easier/more straight forward
- [X] make installer/setup/configuration wizard better
- [X] add option to enable/disable icon only mode for tray icon
- [X] create single binary file for use an distribution
- [ ] ~~create pipy package for easier installation~~
- [ ] ~~create launch agents instead of using a .app file that needs to be manually added.~~
