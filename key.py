import RPi.GPIO as GPIO
import time

class key:
	
	def __init__(self, pin):
		
		self.pin = pin
		GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		self.timestamp = time.time()
		self.new_state = self.l2bool(GPIO.input(self.pin))
		self.old_state = self.new_state
		self.no_edge_detected = False
		GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.cb_edge)
	
	def l2bool(self, level):
	
		if (level == GPIO.LOW):
			return True
		else:
			return False
	
	def get_pin(self):
		
		return self.pin
	
	def pressed(self):
		
		if (self.no_edge_detected):
			return self.old_state
			
		else:
			if ((time.time() - self.timestamp) > 0.3):
				self.old_state = self.new_state
				self.no_edge_detected = True
				return self.old_state
		
		return self.old_state
	
	def cb_edge(self, channel):
		
		temp = self.l2bool(GPIO.input(self.pin))
		if (temp != self.new_state):
			self.new_state = temp
			self.timestamp = time.time()
			self.no_edge_detected = False
