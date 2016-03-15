# pifo #
A Python script to output system info for Raspberry Pi in JSON.

## Python Dependencies ##
os, platform, json, time, subprocess, psutil

## Supported OS ##
[Raspbian](http://www.raspbian.org)

## Notes ##

* Disk utilization currently supports only the root partition ( **/** )
* Temperature data is retrieved via the **vcgencmd measure_temp** command
* Voltage data is retrieved via the **vcgencmd measure_volts** command
* Processes list is retrieved via **ps axfo user,group,pcpu,pmem,etime,pid,cmd --sort pcpu,pmem**

## Frontend Example ##
A frontend (not included) example that reads JSON output from pifo.py

![Frontend Example](https://i.imgur.com/h13wKRH.png)
