# IntelliDirb
Exploring Intelligent Web Directory Enumeration

# Usage

```commandline
██╗███╗░░██╗████████╗███████╗██╗░░░░░██╗░░░░░██╗██████╗░██╗██████╗░██████╗░
██║████╗░██║╚══██╔══╝██╔════╝██║░░░░░██║░░░░░██║██╔══██╗██║██╔══██╗██╔══██╗
██║██╔██╗██║░░░██║░░░█████╗░░██║░░░░░██║░░░░░██║██║░░██║██║██████╔╝██████╦╝
██║██║╚████║░░░██║░░░██╔══╝░░██║░░░░░██║░░░░░██║██║░░██║██║██╔══██╗██╔══██╗
██║██║░╚███║░░░██║░░░███████╗███████╗███████╗██║██████╔╝██║██║░░██║██████╦╝
╚═╝╚═╝░░╚══╝░░░╚═╝░░░╚══════╝╚══════╝╚══════╝╚═╝╚═════╝░╚═╝╚═╝░░╚═╝╚═════╝░

Error: the following arguments are required: target, -w

usage: intellidirb.py [-h] -w WORDLIST [-m {dict,content,service,script,all}] [-x EXTENSIONS]
                      [-o OUT_FILE] [-t THREADS] [-l {DEBUG,INFO,ERROR,CRITICAL}] [--no_colors]
                      [--no_recurse] [--exclude EXCLUDED_DIRS]
                      target

positional arguments:
  target                Target IP and port to enumeration.

options:
  -h, --help            show this help message and exit
  -w WORDLIST           Wordlist file.
  -m {dict,content,service,script,all}
                        Choose the fuzzing mode.
  -x EXTENSIONS         Extensions to test for each word.
  -o OUT_FILE           Output file.
  -t THREADS            The number of threads to use (default=10).
  -l {DEBUG,INFO,ERROR,CRITICAL}
                        Log level for printed messages (default=INFO).
  --no_colors           Don't print colors to the console.
  --no_recurse          Don't attempt to recurse into directories.
  --exclude EXCLUDED_DIRS
                        Directories to exclude during recursion.
```

# Examples

```commandline
python .\intellidirb.py -w ..\wordlist.txt -m all -x html,txt,php -t 4 http://192.168.56.101:85 -l INFO

██╗███╗░░██╗████████╗███████╗██╗░░░░░██╗░░░░░██╗██████╗░██╗██████╗░██████╗░
██║████╗░██║╚══██╔══╝██╔════╝██║░░░░░██║░░░░░██║██╔══██╗██║██╔══██╗██╔══██╗
██║██╔██╗██║░░░██║░░░█████╗░░██║░░░░░██║░░░░░██║██║░░██║██║██████╔╝██████╦╝
██║██║╚████║░░░██║░░░██╔══╝░░██║░░░░░██║░░░░░██║██║░░██║██║██╔══██╗██╔══██╗
██║██║░╚███║░░░██║░░░███████╗███████╗███████╗██║██████╔╝██║██║░░██║██████╦╝
╚═╝╚═╝░░╚══╝░░░╚═╝░░░╚══════╝╚══════╝╚══════╝╚═╝╚═════╝░╚═╝╚═╝░░╚═╝╚═════╝░

[INFO] Loaded wordlist file with 1829 words.
[INFO] Beginning enumeration...
200    Dict     160l   10250c   http://192.168.56.101:85/
[INFO] Identified service nginx from response.
200    Href     84l    5127c    http://192.168.56.101:85/style.css
[INFO] Sent 1000 requests.
[INFO] Sent 2000 requests.
200    Dict     160l   10250c   http://192.168.56.101:85/index.html
200    Dict     46l    88024c   http://192.168.56.101:85/script.js
[INFO] Sent 3000 requests.
[INFO] Sent 4000 requests.
[INFO] Sent 5000 requests.
[INFO] Sent 6000 requests.

==== Summary ====
Finished enumerating in 62.49 seconds.
Totals: 4 / 6907

Breakdown by request origin:
- Dict:    3 / 6857
- Href:    1 / 1
- Service: 0 / 44
- Script:  0 / 5
```