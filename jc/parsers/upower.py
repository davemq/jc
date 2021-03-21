"""jc - JSON CLI output utility `upower` command output parser

Usage (cli):

    $ upower -d | jc --upower

    or

    $ jc upower -d

Usage (module):

    import jc.parsers.upower
    result = jc.parsers.upower.parse(upower_command_output)

Compatibility:

    'linux'

Examples:

    $ upower -i /org/freedesktop/UPower/devices/battery | jc --upower -p
    [
      {
        "native_path": "/sys/devices/LNXSYSTM:00/device:00/PNP0C0A:00/power_supply/BAT0",
        "vendor": "NOTEBOOK",
        "model": "BAT",
        "serial": "0001",
        "power_supply": true,
        "updated": "Thu Feb 9 18:42:15 2012",
        "has_history": true,
        "has_statistics": true,
        "detail": {
          "type": "battery",
          "present": true,
          "rechargeable": true,
          "state": "charging",
          "energy": 22.3998,
          "energy_empty": 0.0,
          "energy_full": 52.6473,
          "energy_full_design": 62.16,
          "energy_rate": 31.6905,
          "voltage": 12.191,
          "time_to_full": 57.3,
          "percentage": 42.5469,
          "capacity": 84.6964,
          "technology": "lithium-ion",
          "energy_unit": "Wh",
          "energy_empty_unit": "Wh",
          "energy_full_unit": "Wh",
          "energy_full_design_unit": "Wh",
          "energy_rate_unit": "W",
          "voltage_unit": "V",
          "time_to_full_unit": "minutes"
        },
        "history_charge": [
          {
            "time": 1328809335,
            "percent_charged": 42.547,
            "status": "charging"
          },
          {
            "time": 1328809305,
            "percent_charged": 42.02,
            "status": "charging"
          }
        ],
        "history_rate": [
          {
            "time": 1328809335,
            "percent_charged": 31.691,
            "status": "charging"
          }
        ],
        "updated_epoch": 1328841735,
        "updated_seconds_ago": 1
      }
    ]

    $ upower -i /org/freedesktop/UPower/devices/battery | jc --upower -p -r
    [
      {
        "native_path": "/sys/devices/LNXSYSTM:00/device:00/PNP0C0A:00/power_supply/BAT0",
        "vendor": "NOTEBOOK",
        "model": "BAT",
        "serial": "0001",
        "power_supply": "yes",
        "updated": "Thu Feb  9 18:42:15 2012 (1 seconds ago)",
        "has_history": "yes",
        "has_statistics": "yes",
        "detail": {
          "type": "battery",
          "present": "yes",
          "rechargeable": "yes",
          "state": "charging",
          "energy": "22.3998 Wh",
          "energy_empty": "0 Wh",
          "energy_full": "52.6473 Wh",
          "energy_full_design": "62.16 Wh",
          "energy_rate": "31.6905 W",
          "voltage": "12.191 V",
          "time_to_full": "57.3 minutes",
          "percentage": "42.5469%",
          "capacity": "84.6964%",
          "technology": "lithium-ion"
        },
        "history_charge": [
          {
            "time": "1328809335",
            "percent_charged": "42.547",
            "status": "charging"
          },
          {
            "time": "1328809305",
            "percent_charged": "42.020",
            "status": "charging"
          }
        ],
        "history_rate": [
          {
            "time": "1328809335",
            "percent_charged": "31.691",
            "status": "charging"
          }
        ]
      }
    ]
"""
import locale
from datetime import datetime, timezone
import jc.utils


class info():
    version = '1.0'
    description = 'upower command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['upower']
    timezone_support = True


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data with the following schema:

        [
          {
            "type":                         string,
            "device_name":                  string,
            "native_path":                  string,
            "power_supply":                 boolean,
            "updated":                      string,
            "updated_epoch":                integer,      # as UTC. Works best with C locale. null if conversion fails
            "updated_seconds_ago":          integer,
            "has_history":                  boolean,
            "has_statistics":               boolean,
            "detail": {
              "type":                       string,
              "warning_level":              string,        # null if none
              "online":                     boolean,
              "icon_name":                  string
              "present":                    boolean,
              "rechargeable":               boolean,
              "state":                      string,
              "energy":                     float,
              "energy_unit":                string,
              "energy_empty":               float,
              "energy_empty_unit":          string,
              "energy_full":                float,
              "energy_full_unit":           string,
              "energy_full_design":         float,
              "energy_full_design_unit":    string,
              "energy_rate":                float,
              "energy_rate_unit":           string,
              "voltage":                    float,
              "voltage_unit":               string,
              "time_to_full":               float,
              "time_to_full_unit":          string,
              "percentage":                 float,
              "capacity":                   float,
              "technology":                 string
            },
            "history_charge": [
              {
                "time":                     integer,
                "percent_charged":          float,
                "status":                   string
              }
            ],
            "history_rate":[
              {
                "time":                     integer,
                "percent_charged":          float,
                "status":                   string
              }
            ],
            "daemon_version":               string,
            "on_battery":                   boolean,
            "lid_is_closed":                boolean,
            "lid_is_present":               boolean,
            "critical_action":              string
          }
        ]
    """
    for entry in proc_data:
        # time conversions
        if 'updated' in entry:
            updated_list = entry['updated'].replace('(', '').replace(')', '').split()
            entry['updated'] = ' '.join(updated_list[:-3])

            # try C locale. If that fails, try current locale. If that fails, give up
            entry['updated_epoch'] = None
            try:
                locale.setlocale(locale.LC_TIME, None)
                entry['updated_epoch'] = int(datetime.strptime(entry['updated'], '%c').astimezone(tz=timezone.utc).strftime('%s'))
            except Exception:
                try:
                    locale.setlocale(locale.LC_TIME, '')
                    entry['updated_epoch'] = int(datetime.strptime(entry['updated'], '%c').astimezone(tz=timezone.utc).strftime('%s'))

                except Exception:
                    pass
                finally:
                    locale.setlocale(locale.LC_TIME, None)
            finally:
                locale.setlocale(locale.LC_TIME, None)

            entry['updated_seconds_ago'] = int(updated_list[-3])

        # top level boolean conversions
        bool_list = ['power_supply', 'has_history', 'has_statistics', 'on_battery', 'lid_is_closed', 'lid_is_present']
        for key in entry:
            if key in bool_list:
                if entry[key].lower() == 'yes':
                    entry[key] = True
                else:
                    entry[key] = False

        # detail level boolean conversions
        bool_list = ['online', 'present', 'rechargeable']
        if 'detail' in entry:
            for key in entry['detail']:
                if key in bool_list:
                    if entry['detail'][key].lower() == 'yes':
                        entry['detail'][key] = True
                    else:
                        entry['detail'][key] = False

        # detail level convert warning to null if value is none
        if 'detail' in entry:
            if 'warning_level' in entry['detail']:
                if entry['detail']['warning_level'] == 'none':
                    entry['detail']['warning_level'] = None

        # detail level convert energy readings to float and add unit keys
        if 'detail' in entry:
            add_items = []
            for key, value in entry['detail'].items():
                if value and isinstance(value, str):
                    if len(value.split()) == 2 and value.split()[0].replace('.', '').isnumeric():
                        entry['detail'][key] = float(value.split()[0])
                        add_items.append({
                            key + '_unit': value.split()[1]
                        })

            if add_items:
                for item in add_items:
                    for key, value in item.items():
                        entry['detail'][key] = value

        # detail level fix percentages
        if 'detail' in entry:
            for key, value in entry['detail'].items():
                if value and isinstance(value, str):
                    if value[-1] == '%':
                        entry['detail'][key] = float(value[:-1])

        # detail level fix quoted values
        if 'detail' in entry:
            for key, value in entry['detail'].items():
                if value and isinstance(value, str):
                    if value.startswith("'") and value.endswith("'"):
                        entry['detail'][key] = value[1:-1]

        # history_charge and history_rate level convert floats and ints
        histories = []

        if 'history_charge' in entry:
            histories.append('history_charge')
        if 'history_rate' in entry:
            histories.append('history_rate')

        if histories:
            for history_obj_list in histories:
                new_history_list = []
                for history_obj in entry[history_obj_list]:
                    new_history_obj = {}
                    for key, value in history_obj.items():
                        if key == 'time':
                            new_history_obj[key] = int(value)
                        elif key == 'percent_charged':
                            new_history_obj[key] = float(value)
                        else:
                            new_history_obj[key] = value

                    new_history_list.append(new_history_obj)

                entry[history_obj_list] = new_history_list

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []
    device_obj = {}
    device_name = None
    history_key = ''
    history_list = []
    history_list_obj = {}

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            if line.startswith('Device:') or line.startswith('Daemon:'):
                if device_obj:
                    raw_output.append(device_obj)
                    device_obj = {}

                if line.startswith('Device:'):
                    device_name = line.split(':', maxsplit=1)[1].strip()
                    device_obj = {
                        'type': 'Device',
                        "device_name": device_name
                    }

                elif line.startswith('Daemon:'):
                    device_obj = {
                        'type': 'Daemon'
                    }

                continue

            # history detail lines
            if line.startswith('    ') and ':' not in line:
                line_list = line.strip().split()
                history_list_obj = {
                    'time': line_list[0],
                    'percent_charged': line_list[1],
                    'status': line_list[2]
                }
                history_list.append(history_list_obj)
                device_obj[history_key] = history_list
                continue

            # general detail lines
            if line.startswith('    ') and ':' in line:
                key = line.split(':', maxsplit=1)[0].strip().lower().replace('-', '_').replace(' ', '_').replace('(', '').replace(')', '')
                val = line.split(':', maxsplit=1)[1].strip()
                device_obj['detail'][key] = val
                continue

            # history detail lines are a special case of detail lines
            # set the history detail key
            if line.startswith('  History (charge):') or line.startswith('  History (rate):'):
                if line.startswith('  History (charge):'):
                    history_key = 'history_charge'
                elif line.startswith('  History (rate):'):
                    history_key = 'history_rate'

                device_obj[history_key] = {}
                history_list = []
                continue

            # top level lines
            if line.startswith('  ') and ':' in line:
                key = line.split(':', maxsplit=1)[0].strip().lower().replace('-', '_').replace(' ', '_').replace('(', '').replace(')', '')
                val = line.split(':', maxsplit=1)[1].strip()
                device_obj[key] = val
                continue

            # set the general detail object
            if line.startswith('  ') and ':' not in line:
                detail_type = line.strip()
                device_obj['detail'] = {
                    'type': detail_type
                }
                continue

    if device_obj:
        raw_output.append(device_obj)

    if raw:
        return raw_output
    else:
        return process(raw_output)
