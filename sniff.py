from datetime import datetime
import matplotlib.pyplot as pyplot
import RPi.GPIO as GPIO


RECEIVED_SIGNAL = [[], []]      # [[time of reading], [signal reading]]
MAX_DURATION = 2                # How many seconds to read the signal
RECEIVE_PIN = 21                # The data pin of the receiver

if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)                  # Set the way we will refer to the GPIO pins
    GPIO.setup(RECEIVE_PIN, GPIO.IN)        # Set pin 21 for input (Receiver)
    cumulative_time = 0                     # Start duration at 0
    beginning_time = datetime.now()         # Set time to now

    print '**Started recording**'

    while cumulative_time < MAX_DURATION:
        time_delta = datetime.now() - beginning_time
        RECEIVED_SIGNAL[0].append(time_delta)
        RECEIVED_SIGNAL[1].append(GPIO.input(RECEIVE_PIN))
        cumulative_time = time_delta.seconds

    print '**Ended recording**'
    print len(RECEIVED_SIGNAL[0]), 'samples recorded'   # Output how many samples were recorded
    GPIO.cleanup()

    print '**Processing results**'
    for i in range(len(RECEIVED_SIGNAL[0])):
        RECEIVED_SIGNAL[0][i] = RECEIVED_SIGNAL[0][i].seconds + RECEIVED_SIGNAL[0][i].microseconds/1000000.0

    print '**Plotting results**'
    pyplot.plot(RECEIVED_SIGNAL[0], RECEIVED_SIGNAL[1])
    pyplot.axis([0, MAX_DURATION, -1, 2])
    pyplot.show()
