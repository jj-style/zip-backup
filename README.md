# zip-backup
Zip backup utility written in Python.  
  
## Usage
### Installation
- `pip install -e .`
- `$ zipy-backup`

### Manual
- Put [backupper.py](backupper.py) anywhere you like, I use `~/.local/bin`.
- Mark script as executable `sudo chmod +x ~/.local/bin/backupper.py`
- Copy/Create the configuration file in `/usr/local/etc/zipy-backup.conf`
- Call script whenever you want, in systemd unit or in crontab to backup folders and frequently/infrequently as you like

### Configuration
Example configuration file:
```conf
# default section is required
# destination should point to folder where zips are placed
[DEFAULT]
DESTINATION = ~/Backups

# optional sections for each folder to backup
# the zip's name will be the name of the section (Pictures below)
[Pictures]
SOURCE = ~/Pictures
#PASSWORD = password # this will encrypt the zip with this password (optional)
```
