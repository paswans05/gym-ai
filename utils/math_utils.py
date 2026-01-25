import numpy as np
from typing import Tuple, List

def calculate_angle(a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]) -> float:
    """
    Calculates the angle at point b formed by points a, b, and c.

    Args:
        a: Coordinates of point a (x, y).
        b: Coordinates of point b (x, y) - the vertex.
        c: Coordinates of point c (x, y).

    Returns:
        float: Angle in degrees.
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))

    return np.degrees(angle)

def smooth_signal(data: List[float], window_size: int = 5) -> List[float]:
    """
    Applies a simple moving average to smooth the signal.

    Args:
        data: List of numerical values.
        window_size: Size of the smoothing window.

    Returns:
        List[float]: Smoothed data.
    """
    if len(data) < window_size:
        return data
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid').tolist()

def normalize_keypoints(keypoints: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Normalizes keypoints to be relative to the hip center or bounding box.
    For this MVP, we'll assume input is already in a consistent coordinate space (0-1),
    but this is a placeholder for future normalization.
    """
    return keypoints
