/******************************************************************************
spitest.cpp
Raspberry Pi Data Read
Stephen Nawrocki>
12/17/2017

This example makes use of the Wiring Pi library, which streamlines the interface
to the the I/O pins on the Raspberry Pi, providing an API that is similar to the
Arduino.  You can learn about installing Wiring Pi here:
http://wiringpi.com/download-and-install/

The wiringPi SPI API is documented here:
https://projects.drogon.net/raspberry-pi/wiringpi/spi-library/

The init call returns a standard file descriptor.  More detailed configuration
of the interface can be performed using ioctl calls on that descriptor.
See the wiringPi SPI implementation (wiringPi/wiringPiSPI.c) for some examples.
Parameters configurable with ioctl are documented here:
http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/tree/Documentation/spi/spidev

Hardware connections:
The board was connected as follows:
(Raspberry Pi)(Serial 7 Segment)
GND  -> GND
3.3V -> Vcc
CE1  -> SS (Shift Select)
SCK  -> SCK 
MOSI -> SDI
MISO -> SDO

To build this file, I use the command:
>  g++ spiread.cpp -lwiringPi

Then to run it, first the spi kernel module needs to be loaded.  This can be 
done using the GPIO utility.
> gpio load spi
> ./a.out

Distributed as-is; no warranty is given.
******************************************************************************/

#include <iostream>
#include <errno.h>
#include <wiringPiSPI.h>
#include <unistd.h>
#include <fstream>
#include <sstream>
#include <string>
#include <stdio.h>
#include <time.h>

int readvoltage();
std::string getTime();
std::string InttoStr(int);

using namespace std;

// channel is the wiringPi name for the chip select (or chip enable) pin.
// Set this to 0 or 1, depending on how it's connected.
static const int CHANNEL = 1;

int main()
{
   int voltavg;
    
   // Configure the interface.
   // CHANNEL insicates chip select,
   wiringPiSPISetup(CHANNEL, 125000);
    
   while(1)
   {
      voltavg = readvoltage();
      ofstream out("/home/pi/voltage.txt", std::ios_base::app);
      out << InttoStr(voltavg) << "	" << getTime();
      out.close();
   }
}

std::string InttoStr(int in)
{
	ostringstream convert;
    string Result;
	convert << in;
	Result = convert.str();
	return Result;
}
	
std::string getTime()
{
	time_t rawtime;
	struct tm * timeinfo;
	time(&rawtime);
	timeinfo = localtime(&rawtime);
	return asctime(timeinfo);
}

int readvoltage()
{
   int fd, result;
   long voltage;
   long avg[4];
   unsigned char buffer[3];

   buffer[0] = 0x76;
   wiringPiSPIDataRW(CHANNEL, buffer, 1);

   for(int i = 0; i <= 3; i++)
   {
	while(buffer[0] != 0xEF)
	{
		buffer[0] = 0xAB;
		buffer[1] = i;
      		result = wiringPiSPIDataRW(CHANNEL, buffer, 1);
	}
	if(buffer[0] == 0xEF)
	{
      		wiringPiSPIDataRW(CHANNEL, buffer, 1);
		voltage = buffer[0];
      		wiringPiSPIDataRW(CHANNEL, buffer, 1);
		voltage = voltage + (buffer[0] << 8);
		if(voltage < 1024)
		{
			avg[i] = voltage;
		}
      		sleep(3);
	}
   }
    voltage = avg[1] + avg[2] + avg[3];
    voltage = voltage/3;
}
