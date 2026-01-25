import numpy as np

def denoise(csi_matrix: np.ndarray) -> np.ndarray:
    """
    Applies basic noise reduction to the CSI matrix.
    Args:
        csi_matrix: Complex CSI data
    Returns:
        Denoised CSI data
    """
    # Simple magnitude filtering for MVP - could use butterworth etc.
    # Here we just return as is or apply a slight threshold clip for the mock
    return csi_matrix

def extract_features(csi_frame) -> np.ndarray:
    """
    Extracts relevant features from a CSIFrame for the model.
    Typically extracts Amplitude and Phase.
    """
    data = csi_frame.data
    
    # Calculate Amplitude
    amplitude = np.abs(data)
    
    # Calculate Phase
    phase = np.angle(data)
    
    # Phase Sanitization (Remove random phase offsets)
    # Simple linear fit removal for mock purposes
    for i in range(phase.shape[1]):
        unwrapped_phase = np.unwrap(phase[:, i])
        # Fit linear trend to remove (CFO/SFO proxy)
        x = np.arange(len(unwrapped_phase))
        z = np.polyfit(x, unwrapped_phase, 1)
        p = np.poly1d(z)
        phase[:, i] = unwrapped_phase - p(x)
        
    # Combine flattened features
    return np.concatenate([amplitude.flatten(), phase.flatten()])
