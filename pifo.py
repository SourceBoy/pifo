#!/usr/bin/env python

import os
import platform
import json
import time
import subprocess
import psutil

#from collections import namedtuple
#CPUSpeed = namedtuple('CPUSpeed', 'min max current')

P = psutil.Process

memory = psutil.virtual_memory()

root_partition = '/'
disk_root = psutil.disk_usage(root_partition)

net_traffics = []
net_connected = []
net_listening = []

for interface, iface in psutil.net_io_counters(True).items():

	if interface != 'lo':
		net_traffics.append({
			'interface': interface,
			'sent': iface.bytes_sent,
			'received': iface.bytes_recv
		})

for connection in psutil.net_connections('inet4'):

	laddr = connection.laddr
	raddr = connection.raddr
	pname = P(connection.pid).name()

	if connection.status == 'ESTABLISHED':
		net_connected.append({
			'local': {'ip': laddr[0], 'port': laddr[1]},
			'remote': {'ip': raddr[0], 'port': raddr[1]},
			'pname': pname
		})

	elif connection.status == 'LISTEN':
		net_listening.append({
			'ip': laddr[0], 'port': laddr[1],
			'pname': pname
		})

output = {

	'memory': {
		'total': memory.total,
		'available': memory.available,
		'percent': memory.percent
	},

	'disk': {
		'partition': root_partition,
		'total': disk_root.total,
		'used': disk_root.used,
		'free': disk_root.free,
		'percent': disk_root.percent
	},

	'net': {
		'traffics': net_traffics,
		'connected': net_connected,
		'listening': net_listening
	},

	'uptime': time.time() - psutil.boot_time(), # Float seconds

	'processes': subprocess.check_output(['ps', 'axfo', 'user,group,pcpu,pmem,etime,pid,cmd', '--sort', 'pcpu,pmem']),

	'cpu': {
		#'percent': psutil.cpu_percent(10),
		'type': platform.machine(),
		'loadavg': os.getloadavg(), # List of floats
		'temperature': subprocess.check_output(['vcgencmd', 'measure_temp'])[5:9], # Celsius
		'voltage': subprocess.check_output(['vcgencmd', 'measure_volts'])[5:9], # V
		'speed': {
			'min': int(open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq', 'r').read()) / 1000, # MHz
			'max': int(open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq', 'r').read()) / 1000, # MHz
			'current': int(open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq', 'r').read()) / 1000 #MHz
		}
	},

}

#print(json.dumps(output, indent = 4, separators = (',', ': '))) # Pretty print
print(json.dumps(output)) # Machine print
