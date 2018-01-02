#!/usr/bin/python
import web

urls = (
     '/', 'index'
)

class index:
	def GET(self):
		data = open("voltage.txt","r")
		last_line = data.readlines()[-1]
		if last_line[0] != "0":
			voltage = int(last_line[0:3])
			voltage = voltage - 1
                        voltage = float(voltage * 5)
                        voltage = voltage / 1023
                        voltage = voltage * (16/5)
                        voltage = voltage * 0.9165
		else:
			voltage = 0
		data.close()
		return voltage

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
