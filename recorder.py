import subprocess
import os.path
import shutil
import sys
import RPi.GPIO as GPIO
import key
import usbstick

def shutdown():
	
	command = "/usr/bin/sudo /sbin/shutdown -h now"
	import subprocess
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]
	print output

def reboot():
	
	command = "/usr/bin/sudo /sbin/shutdown -r now"
	import subprocess
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]
	print output

def myexit():
	
	print 'Programm wird beendet'
	GPIO.cleanup()
	shutdown()

try:
	# Define storage
	path_tmp = '/ram/'
	path = '/mnt/usb/'
	prefix = 'Titel'
	extension = '.mp3'
	
	# Configure GPIOs
	GPIO.setmode(GPIO.BOARD)
	button_shutdown = key.key(7)
	button_record = key.key(11)
	GPIO.setup(12, GPIO.OUT)
	GPIO.setup(15, GPIO.OUT)
	GPIO.output(12, GPIO.HIGH)
	
	# Start thread to detect external memory
	usb = usbstick.usbstick(path, 13)
		
	# Configure volume
	#m = alsaaudio.Mixer('Mic', 0, 1)
	#m.setvolume(100, 0, 'capture')
	
	# Only run until shutdown button gets pressed
	while not (button_shutdown.pressed()):
		
		# Only record if record button is pressed and memory is mounted
		if (button_record.pressed()):

			# Wait for external memory
			usb.waitmount()			
						
			# Find next file name
			i = 0
			filename = ''
			while (True):
				i += 1
				filename = path + prefix + format(i, '03') + extension
				if not (os.path.exists(filename)):
					break
			filename_tmp = path_tmp + prefix + format(i, '03') + extension
			print 'Neue Aufnahme wird gespeichert unter ' + filename
			
			# Record sound
			GPIO.output(15, GPIO.HIGH)
			command_arecord = "sudo arecord -D sysdefault:CARD=Device -f S16_LE --rate=44100 --channels=1 --buffer-size=88200"
			command_arecord_stop = "sudo pkill arecord"
			command_lame = "sudo lame -b 320 - " + filename_tmp
			process_arecord = subprocess.Popen(command_arecord.split(), stdout=subprocess.PIPE)
			process_lame = subprocess.Popen(command_lame.split(), stdin=process_arecord.stdout, stdout=subprocess.PIPE)
			while (button_record.pressed()):
				pass
			
			# Stop record and save
			process_arecord = subprocess.Popen(command_arecord_stop.split(), stdout=subprocess.PIPE)
			process_lame.wait()
			GPIO.output(15, GPIO.LOW)
			GPIO.output(12, GPIO.LOW)
			usb.waitmount()
			shutil.copy(filename_tmp, filename)
			os.remove(filename_tmp)
			GPIO.output(12, GPIO.HIGH)
			print 'Aufnahme beendet\n'
	
	myexit()

except KeyboardInterrupt:
	
	print 'Programm wird beendet'
	GPIO.cleanup()

