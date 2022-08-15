# Installation
```bash

git clone git@github.com:derfryday/statusbar_time_tracking.git

cd statusbar_time_tracking

poetry build -f wheel

# outside of the poetry shell run
pip install ./dist/<name of wheel>

```
now manually add the StatusbarTimeTracker.app to your login items in the system preferences

# Usage
start by running
`statusbar_time_tracker & disown`

This should only be necessary if the time tracker crashes or if you just installed it.
I will eventually turn it into a LaunchAgent but I just couldn't get it to work for now.

# Configuration
config file location: `~/.config/statusbar_config.json`
## There are 2 ways to configure the statusbar time tracker
1. manually copy `config/statusbar_config.dist.json` to `~/.config/statusbar_config.json` and change the values according to your needs.
   1. you can get your password hash by running `unset HISTFILE; echo -n "your_password" | sha1sum | awk '{print $1}')`
2. run the setup by running `poetry run python statusbar_time_tracker_app.py --setup` and follow the wizard.

### configuration parameters:

```json
{
  "username": "c.norris", // the same username you use to log into smalltime
  "display_name": "Chuck Norris", // name as seen on the smalltime overview page
  "password_hash": "d73cbcd9234156a073afb5511f7ceb27413a0d9f", // sha1 checksum of your password
   "smalltime_index_url": "https://your-smalltime-url/index.php",
   "smalltime_tracker_url": "https://your-possibly-different-smalltime-tracker-url/track_time.php"
}
```

# Attribution
- credit for the coffee-break icon goes to https://www.flaticon.com/authors/uniconlabs
- credit for the warning icon goes to https://www.freepik.com
- credit for the working icon goes to https://www.flaticon.com/authors/dreamicons

# TODOs:
- create pipy package for easier installation
- create launch agents instead of using a .app file that needs to be manually added.