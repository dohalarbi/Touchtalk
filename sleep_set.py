
def sleep_mode_write(num):
	file=open('sleep_mode.txt', 'w')
	file.write(str(num))
	file.close()

sleep_mode_write(0)

