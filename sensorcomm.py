import sys, serial, struct, binascii

ino = serial.Serial("/dev/ttyACM0", 19200)
ino.readline()

while True:
    b64 = ino.readline()
    try:
        data = binascii.a2b_base64(b64)
    
        # checksum
        cksum = sum(data[:-1]) % 256

        print("Digital", end=" ")
        byte0mask = (0b00000000, 0b00000000, 0b00000100, 0b00000010, 0b00000001)
        for i in range(2,5):
            print(str(i) + ": " + str(data[0] &  byte0mask[i] == byte0mask[i]).ljust(5), end =" ")

        for i in range(8):
            print(str(5 + i) + ": " + str(data[1] >> (7 - i)  & 1 == 1).ljust(5), end=" ")
    
        print("")
        print("Analog ", end=" ")
    
        other_data = struct.unpack(">6hc", data[2:])
        for i in range(6):
            print(str (i) + ": " + str(other_data[i]).zfill(4), end=" ")
        
        real_cksum = int.from_bytes(other_data[6], "big")
        
        print("cksum " + hex(cksum)[2:].ljust(2) + ((" should be " + hex(real_cksum)[2:].ljust(2)) if cksum != real_cksum else ""))
    except binascii.Error:
        print("Read error, retrying", file=sys.stderr)
