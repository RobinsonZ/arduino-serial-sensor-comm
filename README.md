# arduino-serial-sensor-comm
Read sensor status from an Arduino over the serial (USB) port. A Python client is provided, but the protocol used should be able to be read in any programming language that supports numbers.

This repository contains two pieces of code: 

## Arduino server

A simple sketch to transmit the state of DIO pins 2--12 and AIO 0--5 over the serial USB connection on an Arduino Uno.
Requires [base64_arduino](https://github.com/Densaugeo/base64_arduino).

Transmits a packet roughly 114 times per second, but this can be adjusted by changing the baud rate.

### Packet format

| Type     | Description                                      | Byte # |
| -------- | ------------------------------------------------ | ------ |
| Raw bits | 5 bits of padding followed by DIOs 2-–4 in order | 0      |
| Raw bits | DIOs 5-–12 in order                              | 1      |
| `int16`  | 6 2-byte `ints` for each analog channel          | 2-–13  |
| `byte`   | Checksum                                         | 13     |


This is then Base64-encoded and a trailing newline is added. All numbers are transmitted big-endian.

## Python client

A simple Python client to read the aforementioned data packets from a serial port (the address of which can be changed by modifying line 3) and print them to the console.
