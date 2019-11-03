#!/bin/bash

PWD="$(pwd)"
cd ..
cd ..
BASE_DIR="$(pwd)"
ARDUPI_DIR="$BASE_DIR/arduPi"
ARDUPIAPI_DIR="$BASE_DIR/arduPi-api"
EXAMPLES_DIR="$BASE_DIR/examples/RS485"
LIBRARY_DIR="$BASE_DIR/libraries/arduPiRS485"

#compile arduPi
cd "$ARDUPI_DIR"
file="./arduPi.o"
if [ -e $file ]; then
  if [ "$1" == "-clean" ]; then
    echo "arduPi.o -> purged"
    rm ./arduPi.o
  else
    echo "arduPi already compiled"
  fi
else 
  if [ "$1" != "-clean" ]; then
    echo "Compiling arduPi..."
    g++ -c arduPi.cpp -o arduPi.o
  fi
fi 

#compile arduPi-api
cd "$ARDUPIAPI_DIR"
file="./arduPiUART.o"
if [ -e $file ]; then
  if [ "$1" == "-clean" ]; then
    echo "arduPiUART.o -> purged"
    rm ./arduPiUART.o
  else
	echo "arduPiUART already compiled"
  fi
else 
  if [ "$1" != "-clean" ]; then
	echo "Compiling arduPiUART..."
    g++ -c arduPiUART.cpp -o arduPiUART.o
  fi
fi 

file="./arduPiUtils.o"
if [ -e $file ]; then
  if [ "$1" == "-clean" ]; then
    echo "arduPiUtils.o -> purged"
    rm ./arduPiUtils.o
  else
	echo "arduPiUtils already compiled"
  fi
else 
  if [ "$1" != "-clean" ]; then
	echo "Compiling arduPiUtils..."
    g++ -c arduPiUtils.cpp -o arduPiUtils.o
  fi
fi 

file="./arduPiMultiprotocol.o"
if [ -e $file ]; then
  if [ "$1" == "-clean" ]; then
    echo "arduPiMultiprotocol.o -> purged"
    rm ./arduPiMultiprotocol.o
  else
	echo "arduPiMultiprotocol already compiled"
  fi
else 
  if [ "$1" != "-clean" ]; then
	echo "Compiling arduPiMultiprotocol..."
    g++ -c arduPiMultiprotocol.cpp -o arduPiMultiprotocol.o
  fi
fi 

#compile library
cd "$LIBRARY_DIR"
file="./arduPiRS485.o"
if [ -e $file ]; then
  if [ "$1" == "-clean" ]; then
    echo "arduPiRS485.o -> purged"
    rm ./arduPiRS485.o
  else
	echo "arduPiRS485 already compiled"
  fi
else 
  if [ "$1" != "-clean" ]; then
	echo "Compiling arduPiRS485..."
    g++ -c arduPiRS485.cpp \
      -I"$ARDUPIAPI_DIR" \
      -I"$ARDUPI_DIR" \
      -o arduPiRS485.o
  fi
fi 

file="./ModbusMaster485.o"
if [ -e $file ]; then
  if [ "$1" == "-clean" ]; then
    echo "ModbusMaster485.o -> purged"
    rm ./ModbusMaster485.o
  else
	echo "ModbusMaster485 already compiled"
  fi
else 
  if [ "$1" != "-clean" ]; then
	echo "Compiling ModbusMaster485..."
    g++ -c ModbusMaster485.cpp \
      -I"$ARDUPIAPI_DIR" \
      -I"$ARDUPI_DIR" \
      -o ModbusMaster485.o
  fi
fi 

file="./ModbusSlave485.o"
if [ -e $file ]; then
  if [ "$1" == "-clean" ]; then
    echo "ModbusSlave485.o -> purged"
    rm ./ModbusSlave485.o
  else
	echo "ModbusSlave485 already compiled"
  fi
else 
  if [ "$1" != "-clean" ]; then
	echo "Compiling arduPiRS485..."
    g++ -c ModbusSlave485.cpp \
      -I"$ARDUPIAPI_DIR" \
      -I"$ARDUPI_DIR" \
      -o ModbusSlave485.o
  fi
fi 


sleep 1


#compile example
cd "$EXAMPLES_DIR"
file="./$1"

if [ "$1" != "-clean" ]; then
  if [ -e $file ]; then
    if [ "$1" != "" ]; then
    echo "Compiling Example..."
       
    g++ -lrt -lpthread -lstdc++ "$1" \
      "$LIBRARY_DIR/arduPiRS485.o" \
      "$LIBRARY_DIR/ModbusMaster485.o" \
      "$LIBRARY_DIR/ModbusSlave485.o" \
      "$ARDUPIAPI_DIR/arduPiUART.o" \
      "$ARDUPIAPI_DIR/arduPiUtils.o" \
      "$ARDUPIAPI_DIR/arduPiMultiprotocol.o" \
      "$ARDUPI_DIR/arduPi.o" \
      -I"$ARDUPI_DIR" \
      -I"$ARDUPIAPI_DIR" \
      -I"$LIBRARY_DIR" \
      -o "$1_exe" 
    else
      echo "---------------HELP------------------"
      echo "Compiling: ./mak.sh filetocompile.cpp"
      echo "Cleaning:  ./mak.sh -clean"
      echo "-------------------------------------"
    fi
  else
    echo "ERROR No such file or directory: $file"
  fi
else
  echo "¡¡Spotless Kitchen!!"
fi
 
sleep 1

exit 0

