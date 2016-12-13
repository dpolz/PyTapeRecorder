import RPi.GPIO as GPIO
import threading
import os.path
import time

class usbstick():
	
	def __init__(self, path, led_pin):
		
		self.path = path
		self.led_pin = led_pin
		self.usb_busy = threading.Lock()
		
		self.watch_thread = watch(self.path, self.led_pin)
		self.watch_thread.start()
		
	def get_led_pin(self):
	
		return led_pin
	
	def ismounted(self):
		
		return self.watch_thread.ismount
	
	def waitmount(self):
		
		if (self.watch_thread.ismount):
			return
		
		else:
			print 'Massenspeichergeraet nicht gefunden'
			print 'Warte auf Massenspeichergeraet'

			# Restart after timeout 
			timestamp = time.time()
			while not (self.watch_thread.ismount):
				if ((time.time() - timestamp) > 120):
					time.sleep(5)
					print 'Timeout.'
					#reboot()
					#myexit()

			print 'Massenspeichergeraet gefunden'
			return

class watch(threading.Thread):
	
	def __init__(self, path, led_pin):
		
		threading.Thread.__init__(self)
		self.ismount = False
		self.path = path
		self.led_pin = led_pin
		GPIO.setup(self.led_pin, GPIO.OUT)
		
		
	def run(self):
		
		while True:
			if (os.path.ismount(self.path)):
				self.ismount = True
				GPIO.output(self.led_pin, GPIO.HIGH)
			else:
				self.ismount = False
				GPIO.output(self.led_pin, GPIO.LOW)

