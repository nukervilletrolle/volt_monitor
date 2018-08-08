#!/usr/bin/python
import web
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cStringIO
import os

#plt.show()

urls = (
     "/", "index",
     "/test", "index2","/static/(.*)","images"
)

class images:
        def GET(self,name):
            ext = name.split(".")[-1]
            
            cType = {
                "png":"images/png",
                "jpg":"images/jpg"}
            
            web.header("Content-Type", cType[ext])
            return open('images/%s'%name,"rb").read()

class index2:
	def GET(self):
	    data = open("voltage.txt","r")
	    last_line = data.readlines()[5000:5300]
	    last_data = last_line[-1]
	    if last_data[0] != "0":
		voltage = int(last_data[0:3])
		voltage = voltage - 1
                voltage = float(voltage * 5)
                voltage = voltage / 1023
                voltage = voltage * (16/5)
                voltage = voltage * 0.9165
                #gather plot data
                i = 1
                plotarray = []
                tdata = []
                len_data = len(last_line)
                while i < len_data:
                    #j = (5760 - i)
                    plot_point = last_line[i]
                    plotarray.append(plot_point[0:3])
                    tdata.append(i)
                    i += 1
	    else:
		voltage = 0
	    data.close()

	    matplotlib.rcParams['axes.unicode_minus'] = False
	    fig, ax = plt.subplots()
	    ax.plot(tdata, plotarray, 'o')
	    ax.set_title('Syed Awad hair plot')
	    ax.set_xlim(0, 300)
	    ax.set_ylim(0, 1400)
	    format = "png"
	    sio = cStringIO.StringIO()
	    plt.savefig("ploot.png")
		
	    cType = {
                "png":"images/png",
                "jpg":"images/jpg"}
            
            #web.header("Content-Type", cType[png])
            return open("ploot.png","rb").read()

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
