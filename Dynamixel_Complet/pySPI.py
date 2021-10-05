import spi

spi = SPI("/dev/spidev1.0")

spi.mode = SPI.MODE_0

spi.bits_per_word = 8
spi.speed = 500000

received = spi.transfer([0x11, 0x22, 0xFF])

spi.write([0x12, 0x34, 0xAB, 0xCD])

received = spi.read(14)