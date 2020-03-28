#!/usr/bin/env python
import serial
import csv
import threading
import os
from time import sleep


class SerialThread(threading.Thread):
    def run(self):
        read_size = 12  # arbitrary number
        with serial.Serial(com_port, 115200, timeout=None) as port:
            while True:
                if port.in_waiting > read_size:
                    with open('temp_file.txt', 'a') as temp_file:
                        temp_file.write(str(port.read(read_size)))


def parse_data(data_str: str, freq: int) -> {}:
    data_str = data_str.split(',')
    time = float(data_str[0]) / freq
    voltage = round((float(data_str[1]) / 1023 * 5) * 1000, 4)
    output = {
        'Time [s]': time,
        'V [mV]': voltage
    }
    return output


if __name__ == '__main__':
    # params
    com_port = 'COM16'
    read_size = 12  # arbitrary number
    frequency = 60  # should match that from the .ino file 

    # get file name from user
    file_name = input('Enter file name >>> ')
    file_name = 'data/'+file_name+'.csv'
    wait = input('Press <enter> to continue...')
    while wait != '':
        wait = input('Press <enter> to continue...')

    # write data from serial to temp file
    serial = SerialThread()
    serial.start()

    # parse and clean data from temp file
    while True:
        with open('temp_file.txt', 'r') as temp_file:
            chunk = temp_file.read()
        chunk = chunk.replace('b', '')
        chunk = chunk.replace("'", '')
        chunk = chunk[chunk.find('START\\r\\n')+9:]
        chunk = chunk.split('\\r\\n')
        del chunk[-1]  # last element usually cut-off

        # write data to csv file
        with open(file_name, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Time [s]', 'V [mV]'])
            for reading in chunk:
                data = parse_data(reading, frequency)
                writer.writerow([data[val] for val in data])

        os.remove('temp_file.txt')
