import time

from gpiozero import LED


class RadioHead:
    def __init__(self, radio, receive_timeout) -> None:
        self.radio = radio
        self.receive_timeout = receive_timeout
        self.radio.on_recv = self.on_recv

        self.rx_ctrl = LED(22)
        self.tx_ctrl = LED(23)
        self.receive_success = False

    def send_message(self, data, header_to, with_ack, header_id=0, header_flags=0):
        self.tx_ctrl.on()
        self.radio.set_mode_tx()
        if with_ack:
            result = self.radio.send(data, header_to, header_id, header_flags)
        else:
            result = self.radio.send_to_wait(data, header_to, header_flags, 3)
        self.tx_ctrl.off()
        return result

    def receive_message(self) -> bytes:
        self.rx_ctrl.on()
        self.receive_success = False
        self.radio.set_mode_rx()
        start = time.monotonic()
        timed_out = False
        while not self.receive_success and not timed_out:
            if (time.monotonic() - start) >= self.receive_timeout:
                timed_out = True
        if timed_out:
            return None
        self.rx_ctrl.off()
        return self.last_payload

    def on_recv(self, payload):
        print("Packet received!")
        self.receive_success = True
        self.last_payload = payload
