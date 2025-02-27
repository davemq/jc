[Home](https://kellyjonbrazil.github.io/jc/)
<a id="jc.parsers.ini"></a>

# jc.parsers.ini

jc - JSON Convert `INI` file parser

Parses standard `INI` files and files containing simple key/value pairs.

- Delimiter can be `=` or `:`. Missing values are supported.
- Comment prefix can be `#` or `;`. Comments must be on their own line.
- If duplicate keys are found, only the last value will be used.

> Note: Values starting and ending with double or single quotation marks
> will have the marks removed. If you would like to keep the quotation
> marks, use the `-r` command-line argument or the `raw=True` argument in
> `parse()`.

Usage (cli):

    $ cat foo.ini | jc --ini

Usage (module):

    import jc
    result = jc.parse('ini', ini_file_output)

Schema:

ini or key/value document converted to a dictionary - see the configparser
standard library documentation for more details.

    {
      "key1":       string,
      "key2":       string
    }

Examples:

    $ cat example.ini
    [DEFAULT]
    ServerAliveInterval = 45
    Compression = yes
    CompressionLevel = 9
    ForwardX11 = yes

    [bitbucket.org]
    User = hg

    [topsecret.server.com]
    Port = 50022
    ForwardX11 = no

    $ cat example.ini | jc --ini -p
    {
      "bitbucket.org": {
        "ServerAliveInterval": "45",
        "Compression": "yes",
        "CompressionLevel": "9",
        "ForwardX11": "yes",
        "User": "hg"
      },
      "topsecret.server.com": {
        "ServerAliveInterval": "45",
        "Compression": "yes",
        "CompressionLevel": "9",
        "ForwardX11": "no",
        "Port": "50022"
      }
    }

<a id="jc.parsers.ini.parse"></a>

### parse

```python
def parse(data, raw=False, quiet=False)
```

Main text parsing function

Parameters:

    data:        (string)  text data to parse
    raw:         (boolean) unprocessed output if True
    quiet:       (boolean) suppress warning messages if True

Returns:

    Dictionary representing the ini file

### Parser Information
Compatibility:  linux, darwin, cygwin, win32, aix, freebsd

Version 1.8 by Kelly Brazil (kellyjonbrazil@gmail.com)
