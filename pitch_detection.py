import copy
from os import close
import numpy as np
import scipy.fftpack

# General settings that can be changed by the user
SAMPLE_FREQ = 36000  # sample frequency in Hz
WINDOW_SIZE = 12000  # window size of the DFT in samples
NUM_HPS = 5  # max number of harmonic product spectrums
POWER_THRESH = 1e-4
CONCERT_PITCH = 440  # defining a1
ALL_NOTES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

HANN_WINDOW = np.hanning(WINDOW_SIZE)

""" 
def find_pitch(in_data):
    hann_samples = in_data * HANN_WINDOW
    magnitude_spec = abs(scipy.fftpack.fft(hann_samples)[:len(hann_samples) // 2])

    # interpolate spectrum
    mag_spec_ipol = np.interp(np.arange(0, len(magnitude_spec), 1 / NUM_HPS), np.arange(0, len(magnitude_spec)),
                              magnitude_spec)
    mag_spec_ipol = mag_spec_ipol / np.linalg.norm(mag_spec_ipol, ord=2)  # normalize it

    hps_spec = copy.deepcopy(mag_spec_ipol)

    for i in range(NUM_HPS):
        tmp_hps_spec = np.multiply(hps_spec[:int(np.ceil(len(mag_spec_ipol) / (i + 1)))], mag_spec_ipol[::(i + 1)])
        if not any(tmp_hps_spec):
            break
        hps_spec = tmp_hps_spec

    max_ind = np.argmax(hps_spec)
    max_freq = max_ind * (SAMPLE_FREQ / WINDOW_SIZE) / NUM_HPS

    i = int(np.round(np.log2(max_freq / CONCERT_PITCH) * 12))
    closest_note = ALL_NOTES[i % 12] + str(4 + (i + 9) // 12)
    closest_pitch = CONCERT_PITCH * 2 ** (i / 12)

    return max_freq, round(closest_pitch), closest_note 
"""


def find_pitches(in_data):
    pitches = []
    for i in range(len(in_data) // WINDOW_SIZE):
        window_samples = in_data[i * WINDOW_SIZE:(i + 1) * WINDOW_SIZE]
        signal_power = (np.linalg.norm(window_samples, ord=2) ** 2) / len(window_samples)
        if signal_power < POWER_THRESH:
            #print('입력없음')
            continue
        hann_samples = window_samples * HANN_WINDOW
        magnitude_spec = abs(scipy.fftpack.fft(hann_samples)[:len(hann_samples) // 2])

        # interpolate spectrum
        mag_spec_ipol = np.interp(np.arange(0, len(magnitude_spec), 1 / NUM_HPS), np.arange(0, len(magnitude_spec)),
                                  magnitude_spec)
        mag_spec_ipol = mag_spec_ipol / np.linalg.norm(mag_spec_ipol, ord=2)  # normalize it

        hps_spec = copy.deepcopy(mag_spec_ipol)

        for i in range(NUM_HPS):
            tmp_hps_spec = np.multiply(hps_spec[:int(np.ceil(len(mag_spec_ipol) / (i + 1)))],
                                       mag_spec_ipol[::(i + 1)])
            if not any(tmp_hps_spec):
                break
            hps_spec = tmp_hps_spec

        max_ind = np.argmax(hps_spec)
        max_freq = max_ind * (SAMPLE_FREQ / WINDOW_SIZE) / NUM_HPS

        i = int(np.round(np.log2(max_freq / CONCERT_PITCH + 1e-8) * 12))
        closest_note = ALL_NOTES[i % 12] + str(4 + (i + 9) // 12)
        closest_pitch = CONCERT_PITCH * 2 ** (i / 12)

        pitches.append(round(closest_pitch))  # pitch 데이터 저장

        #print('{}Hz'.format(max_freq), '{}Hz'.format(round(closest_pitch)), closest_note)
    return pitches