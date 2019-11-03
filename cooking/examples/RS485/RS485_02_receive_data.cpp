/*   
 *  This sketch shows how to receive data through RS-485 standard. 
 *  This standard defines the electrical characteristics of drivers
 *  and receivers for use in digital systems. It does not specify
 *  or recommend any communications protocol. For a complete 
 *  communication protocol, please see the Modbus examples. 
 *   
 *  Copyright (C) 2014 Libelium Comunicaciones Distribuidas S.L. 
 *  http://www.libelium.com 
 *   
 *  This program is free software: you can redistribute it and/or modify 
 *  it under the terms of the GNU General Public License as published by 
 *  the Free Software Foundation, either version 2 of the License, or 
 *  (at your option) any later version. 
 *   
 *  This program is distributed in the hope that it will be useful, 
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of 
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
 *  GNU General Public License for more details. 
 *   
 *  You should have received a copy of the GNU General Public License 
 *  along with this program. If not, see <http://www.gnu.org/licenses/>. 
 *   
 *  Version:          0.2
 *  Implementation:   Ahmad Saad, Ruben Martin
 */

// Include always this library when you are using the RS-485 functions
#include "arduPiRS485.h"
#include "arduPi.h"

// Create an instance
RS485 myDevice = RS485();

void setup() { 
  // Initializes the serial for viewing data in the serial monitor 
  Serial.begin(115200);
  delay(100);

  // Initializes the module and assigns the SPI
  if ( myDevice.begin() == 0)
     printf("RS-485 module started successfully\n");
  else
     printf("RS-485 did not initialize correctly\n");

  // Configure the baud rate of the module
  myDevice.baudRateConfig(9600);
  // Configure the parity bit as disabled 
  myDevice.parityBit(DISABLE);
  // Use one stop bit configuration 
  myDevice.stopBitConfig(1);  
  // Print hello message
  printf("This is RS-485 communication receive data example.\n");
}


void loop() {     
  // If data in response buffer
  if (myDevice.available()) 
  {
    while (myDevice.available()) 
    {
      // Read one byte from the buffer 
      char data = myDevice.read();
      // Print data received in the serial monitor
      printf("%c",data);   
      delay(1);         
    }
  }   
  delay(10);
}

int main (){
	setup();
	while(1){
		loop();
	}
	return (0);
}

