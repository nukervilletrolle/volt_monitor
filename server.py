#!/usr/bin/python
import web
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cStringIO
import os
import datetime
import locale

urls = (
     "/", "index",
     "/test", "index2"
)

class index2:
	def GET(self):
	    data = open("voltage.txt","r")
	    file_array = data.readlines()[-9001:-1]
	    last_data = file_array[-1]
	    if last_data[0] != "0":	
                #gather plot data
                i = 1
                plotarray = []
                tdata = []
                len_data = len(file_array)
                while i < len_data:
                    voltage = int(last_data[0:4])
                    voltage = voltage - 1
                    voltage = float(voltage * 5)
                    voltage = voltage * 0.00303969
                    plot_point = voltage
                    plotarray.append(voltage)
                    k = 0
                    last_data_new = []
		    if last_data[3] != "\t":
			path = 1
                    	while k < 29:
                        	if k != 13:
                            		last_data_new.append(last_data[k])
                        	else:
                            		if last_data[k] == " ":
                                		last_data_new.append("0")
                            		else:
                                		last_data_new.append(last_data[k])
                        	k += 1
			last_data_2 = ''.join(last_data_new[9:29])
		    if last_data[4] != "\t":
			path = 2
			while k < 28:
				if k != 12:
					last_data_new.append(last_data[k])
				else:
					if last_data[k] == " ":
						last_data_new.append("0")
					else:
						last_data_new.append(last_data[k])
				k += 1
                    	last_data_2 = ''.join(last_data_new[8:28])
                    date_time = datetime.datetime.strptime(last_data_2,'%b %d %H:%M:%S %Y') #.strftime('%d%H%M')
                    tdata.append(date_time)
                    i += 1
                    j = len_data - i
                    last_data = file_array[-j]
	    else:
		voltage = 0
	    data.close()

	    matplotlib.rcParams['axes.unicode_minus'] = False
	    fig, ax = plt.subplots()
	    ax.plot(tdata, plotarray, 'o')
	    plt.gcf().autofmt_xdate()
	    fig.set_size_inches(14,7)
	    ax.set_title('Voltage')
	    ax.grid(True)
	    ax.set_ylim(9, 15)
	    format = "png"
	    sio = cStringIO.StringIO()
	    plt.savefig("ploot.png")
            return open("ploot.png","rb").read()

class index:
	def GET(self):
		data = open("voltage.txt","r")
		last_line = data.readlines()[-1]
		if last_line[0] != "0":
			voltage = int(last_line[0:4])
			voltage = voltage - 1
                        voltage = float(voltage * 5)
                        voltage = voltage * 0.00303969
		else:
			voltage = 0
		data.close()
 		return voltage

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
