from structlog import get_logger
import time
from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection, CrcCalculator
from sensirion_driver_adapters.i2c_adapter.i2c_channel import I2cChannel
from sensirion_i2c_sht4x.device import Sht4xDevice

def main():
    logger = get_logger()

    logger.info("starting worker")
    with LinuxI2cTransceiver("") as i2c_transceiver:
        channel = I2cChannel(
            I2cConnection(i2c_transceiver),
            slave_address=0x44,
            crc=CrcCalculator(8, 0x31, 0xFF, 0x0),
        )

        sensor = Sht4xDevice(channel)
        try:
            sensor.soft_reset()
            time.sleep(0.01)
        except Exception as e:
            logger.error(f"error: {e}")
            time.sleep(1)
        while True:
            try:
                time.sleep(0.02)
                (temperature, humidity) = sensor.measure_high_precision()
                logger.info(f"temperature: {temperature}, humidity: {humidity}")
            except Exception as e:
                logger.error(f"error: {e}")
                time.sleep(1)


if __name__ == "__main__":
    main()
