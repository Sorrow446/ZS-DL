# ZS-DL
CLI Zippyshare downloader written in Python. JS execution, Selenium and BSoup-**FREE**. 


**People have been seen selling my tools. DO NOT buy them. My tools are free and always will be.**

![](https://orion.feralhosting.com/sorrow/share/ZS-DL.png)

# Usage
Download two files to default directory:    
`ZS-DL.py -u https://www1.zippyshare.com/v/00000000/file.html https://www1.zippyshare.com/v/00000000/file.html`

Download from text file to "G:\ZS-DL downloads" with HTTPS proxy:   
`ZS-DL.py -u G:\links.txt -o "G:\ZS-DL downloads" -p 0.0.0.0:8080`

```
 _____ _____     ____  __
|__   |   __|___|    \|  |
|   __|__   |___|  |  |  |__
|_____|_____|   |____/|_____|

usage: zs-dl.py [-h] -u URLS [URLS ...] [-o OUTPUT_PATH] [-ov] [-p PROXY]

optional arguments:
  -h, --help            show this help message and exit
  -u URLS [URLS ...], --urls URLS [URLS ...]
                        URLs separated by a space or an abs path to a txt
                        file.
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        Abs output directory.
  -ov, --overwrite      Overwrite file if already exists.
  -p PROXY, --proxy PROXY
                        HTTPS only. <IP>:<port>.
```
