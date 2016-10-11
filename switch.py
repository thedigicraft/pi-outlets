import time
import sys
import RPi.GPIO as GPIO

switch_on = '01101111101101111111111111111'  # Code for ON state
switch_off = '101011111011011111111111111'   # Code for OFF state

short_delay = 0.00039                   # Length of a short
long_delay = 0.00130                    # Length of a long
extended_delay = 0.0136                 # Length of the delay between blocks

NUM_ATTEMPTS = 50                       # How many blocks to send

TRANSMIT_PIN = 16                       # Pin assigned to the transmitter
LED_SHORT_PIN = 19                      # Pin assigned to the Blue LED
LED_LONG_PIN = 13                       # Pin assigned to the Yellow LED

GPIO.setmode(GPIO.BCM)                  # Set the way we will refer to the GPIO pins
GPIO.setup(LED_LONG_PIN,GPIO.OUT)       # Set pin 13 for output (Yellow LED)
GPIO.setup(LED_SHORT_PIN,GPIO.OUT)      # Set pin 19 for output (Blue LED)
GPIO.setup(TRANSMIT_PIN, GPIO.OUT)      # Set pin 16 for output (Transmitter)

def transmit_code(code):

    for t in range(NUM_ATTEMPTS):
        for i in code:
            if i == '1':

                # Short send | 1:
                GPIO.output(TRANSMIT_PIN, 1)                # Send high to the transmitter
                GPIO.output(LED_SHORT_PIN,GPIO.HIGH)        # Turn ON the Blue LED (a 1 has Started)
                time.sleep(short_delay)                     # Keep sending for the length of a short period

                # Pause before next send:
                GPIO.output(TRANSMIT_PIN, 0)                # Send low to the transmitter
                GPIO.output(LED_SHORT_PIN,GPIO.LOW)         # Turn OFF the Blue LED (a 1 has Finished)
                time.sleep(long_delay)                      # Send low for period of long delay before next send

            elif i == '0':

                # Long send | 0:
                GPIO.output(TRANSMIT_PIN, 1)                # Send high to the transmitter
                GPIO.output(LED_LONG_PIN,GPIO.HIGH)         # Turn ON the Yellow LED (a 0 has Started)
                time.sleep(long_delay)                      # Keep sending for the length of a long period

                # Pause before next send:
                GPIO.output(LED_LONG_PIN,GPIO.LOW)          # Send low to the transmitter
                GPIO.output(TRANSMIT_PIN, 0)                # Turn OFF the Yellow LED (a 0 has Finished)
                time.sleep(short_delay)                     # Send low for period of short delay before next send

            else:
                continue

        GPIO.output(TRANSMIT_PIN, 0)                        # Send low for extended period
        GPIO.output(LED_SHORT_PIN,GPIO.LOW)                 # Ensure Blue LED is off
        GPIO.output(LED_LONG_PIN,GPIO.LOW)                  # Ensure Yellow LED is off
        time.sleep(extended_delay)                          # Pause before sending next block

    GPIO.cleanup()

if __name__ == '__main__':
    for argument in sys.argv[1:]:
        exec('transmit_code(' + str(argument) + ')')
