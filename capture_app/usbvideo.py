import sys
import struct
import time
import usb.core
import usb.util




def usb_take_photo(size):
    dev = usb.core.find(idVendor=0x14B4, idProduct=0x1004)
    if dev is None:
        raise ValueError('Device is not found')
    # device is found :-)
    start_time = time.time()
    databin = dev.read(0x86,size)
    stop_time = time.time()
    times = stop_time - start_time
    speed = size / times / 1024 / 1024
    print("read time = %s speed = %s Mbyte/s" % (times, speed))
    print("finish")
    return databin



def parser_frame(vin):
    i = 0
    vin_len = len(vin)
    table = []
    while i < vin_len - 4:
        if vin[i] == 0xff:
            if vin[i + 1] == 0x00:
                if vin[i + 2] == 0x00:
                    if vin[i + 3] == 0x80:      #Even,Active,SAV
                        table.append(['EAS', i])
                    elif vin[i + 3] == 0x9d:     #Even, Active,EAV
                        table.append(['EAE', i])
                    elif vin[i + 3] == 0xab:     #Even,Blank, SAV
                        table.append(['EBS', i])
                    elif vin[i + 3] == 0xb6:     #Even, Blank, EAV
                        table.append(['EBE', i])
                    elif vin[i + 3] == 0xc7:     #Odd, Active, SAV
                        table.append(['OAS', i])
                    elif vin[i + 3] == 0xda:     #Odd, Active, EAV
                        table.append(['OAE', i])
                    elif vin[i + 3] == 0xec:     #Odd, Blank, SAV
                        table.append(['OBS', i])
                    elif vin[i + 3] == 0xf1:     #Odd, Blank, EAV
                        table.append(['OBE', i])
                    else:
                        print("a strange word found!")
        i = i + 1


    table_len = len(table)
    i = 0

    even_segment = []
    odd_segment = []
    while i < len(table) - 1:
        if table[i][0] == 'EAS':
            if table[i+1][0] == 'EAE':
                even_segment.append([table[i][1],table[i+1][1]])

        if table[i][0] == 'OAS':
            if table[i+1][0] == 'OAE':
                odd_segment.append([table[i][1],table[i+1][1]])
        i = i + 1

    print("even_segment len = %d" % len(even_segment))
    print(even_segment)
    print("\n\n\n\n\n\n\n")
    print("odd_segment = %d" % len(odd_segment))
    print(odd_segment)


    size = min(len(even_segment), len(odd_segment))

    video = []
    i = 0
    while i < size:
        video.append(vin[even_segment[i][0] + 4 : even_segment[i][1] ])
        video.append(vin[odd_segment[i][0] + 4 : odd_segment[i][1] ])
        i = i + 1
    save_data_file(video, sys.argv[1] + "_image" + ".raw")



def save_data_file( din, filename ):
    outfile = open(filename, 'wb')
    for dat in din:
        outfile.write(dat)
    outfile.close()



def main():
    if len(sys.argv) < 1:
        print("Usage: frame.py  input_filename")
        exit(0)
    f = open(sys.argv[1], "rb")
    datain = f.read()
    f.close()
    parser_frame(datain)


if __name__ == '__main__':
    main()