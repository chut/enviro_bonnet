from aiy.enviro import EnviroKit
from aiy.cloudiot import CloudIot
from luma.core.render import canvas
from PIL import ImageDraw
from time import sleep
import time
import datetime
import subprocess

import argparse


def update_display(display, msg):
    with canvas(display) as draw:
        draw.text((0, 5), msg, fill='white')

def _none_to_nan(val):
    return float('nan') if val is None else val

def main():
    # Pull arguments from command line.
    parser = argparse.ArgumentParser(description='Enviro Kit Demo')
    parser.add_argument('--display_duration',
                        help='Measurement display duration (seconds)', type=int,
                        default=5)
    parser.add_argument('--upload_delay', help='Cloud upload delay (seconds)',
                        type=int, default=300)
    parser.add_argument('--cloud_config', help='Cloud IoT config file', default='my_config.ini')
    parser.add_argument('--print_output', help='Print output to the command line', nargs='?', const=1, type=int, default=0)
    args = parser.parse_args()

    #Get the IP of the Pi
    IP = subprocess.check_output(["hostname", "-I"]).split()[0].decode('ascii')
    # Create instances of EnviroKit and Cloud IoT.
    enviro = EnviroKit()
    with CloudIot(args.cloud_config) as cloud:
        # Indefinitely update display and upload to cloud.
        read_count = 0
        trigger_send_timer = True
        if args.print_output:
             print_output = True
        else:
             print_output = False
        sensors = {}
        while True:
            if trigger_send_timer:
               start_time = datetime.datetime.now()
               trigger_send_timer = False
            # First gather data
            msg = 'IP: %s\n' % _none_to_nan(IP)
            ts = time.time()
            sensors['timestamp'] = ts
            sensors['temperature'] = enviro.temperature
            sensors['ambient_light'] = enviro.ambient_light
            sensors['pressure'] = enviro.pressure
            #sensors['humidity'] = enviro.humidity
            #Display the data on the OLED
            msg += 'Temp: %.2f C' % _none_to_nan(sensors['temperature'])
            #msg += 'Hum: %.2f %%' % _none_to_nan(sensors['humidity'])
            update_display(enviro.display, msg)
            if print_output:
               print(msg)
            sleep(args.display_duration)
            # After the display_duration in seconds, switch to light and pressure.
            msg = 'Light: %.2f lux\n' % _none_to_nan(sensors['ambient_light'])
            msg += 'Pressure: %.2f kPa' % _none_to_nan(sensors['pressure'])
            update_display(enviro.display, msg)
            if print_output:
                print(msg)
            sleep(args.display_duration)

            # If time has elapsed, attempt cloud upload.
            time_now = datetime.datetime.now()
            delta = time_now - start_time
            if print_output:
                print ('delta %i' % delta.seconds)
            if  delta.seconds > args.upload_delay:
                trigger_send_timer = True
                if cloud.enabled():
                    cloud.publish_message(sensors)
                    if print_output:
                        print('\nMessage sent to Cloud')
                        print (sensors)
                else:
                    if print_output:
                        print ('Cloud is not enabled\nNo message sent')
            else:
               if print_output:
                    print("Delaying upload")

if __name__ == '__main__':
    main()
