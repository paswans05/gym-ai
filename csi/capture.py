import time
import random
import numpy as np
from dataclasses import dataclass
from typing import Optional

@dataclass
class CSIFrame:
    timestamp: float
    data: np.ndarray  # Shape: (subcarriers, antennas)
    rssi: float

class CSICapturer:
    """
    Handles capturing of Channel State Information (CSI) from Wi-Fi interfaces.
    Currently supports a Mock mode for development.
    """
    def __init__(self, interface: str = "mock", mock: bool = True):
        self.interface = interface
        self.mock = mock
        print(f"[CSI] Initialized capturer on {interface} (Mock={mock})")

    def get_frame(self) -> CSIFrame:
        """
        Retrieves the next CSI frame.
        """
        if self.mock:
            return self._generate_mock_frame()
        else:
            raise NotImplementedError("Real hardware capture not implemented in this MVP.")

    def _generate_mock_frame(self) -> CSIFrame:
        """
        Generates a synthetic CSI frame simulating human presence.
        Returns:
            CSIFrame: 30 subcarriers x 3 antennas (Complex numbers)
        """
        # Simulate ~30 subcarriers, 3 Rx antennas
        # Using complex numbers for Amplitude + Phase
        # Adding some random fluctuation to simulate movement noise
        subcarriers = 30
        antennas = 3
        
        # Base signal
        real_part = np.random.normal(0, 1, size=(subcarriers, antennas))
        imag_part = np.random.normal(0, 1, size=(subcarriers, antennas))
        csi_data = real_part + 1j * imag_part
        
        # RSSI typically around -40 to -70 dBm
        rssi = -50.0 + random.uniform(-5, 5)

        return CSIFrame(
            timestamp=time.time(),
            data=csi_data,
            rssi=rssi
        )
