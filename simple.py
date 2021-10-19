from buildhat import Motor
motor_a = Motor('A')

while True:
	print("Position: ", motor_a.get_aposition())
