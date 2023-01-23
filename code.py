import time
import board
import busio
import digitalio
import adafruit_rfm9x

# set the time interval (seconds) for sending packets
transmit_interval = 10

RADIO_FREQ_MHZ = 868.0
CS = digitalio.DigitalInOut(board.GP21)
RESET = digitalio.DigitalInOut(board.GP20)
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)

# Initialze RFM radio with a more conservative baudrate
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=1000000)

# You can however adjust the transmit power (in dB).  The default is 13 dB but
# high power radios like the RFM95 can go up to 23 dB:
rfm9x.tx_power = 5


# initialize counter
counter = 0
# send a broadcast mesage
rfm9x.send(bytes("message number {}".format(counter), "UTF-8"))

# Wait to receive packets.
print("Waiting for packets...")
# initialize flag and timer
send_reading = False
time_now = time.monotonic()
while True:
    # Look for a new packet - wait up to 5 seconds:
    packet = rfm9x.receive(timeout=5.0)
    # If no packet was received during the timeout then None is returned.
    if packet is not None:
        # Received a packet!
        # Print out the raw bytes of the packet:
        print("Received (raw bytes): {0}".format(packet))
        # send reading after any packet received
    if time.monotonic() - time_now > transmit_interval:
        # reset timeer
        time_now = time.monotonic()
        # clear flag to send data
        send_reading = False
        counter = counter + 1
        rfm9x.send(bytes("message number {}".format(counter), "UTF-8"))

