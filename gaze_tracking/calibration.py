from __future__ import division
import cv2
from .pupil import Pupil


class Calibration(object):
    """
    Denne klasse kalibrerer pupil detection algoritmen,
    ved at finde de bedste binarization threshold værdier,
    for den givne person og kamera.
    """

    # Definerer en masse variabler
    def __init__(self):
        self.nb_frames = 20
        self.thresholds_left = []
        self.thresholds_right = []

    def is_complete(self):
        """Returnerer True hvis kalibrationen er færdiggjort"""
        return len(self.thresholds_left) >= self.nb_frames and len(self.thresholds_right) >= self.nb_frames

    def threshold(self, side):
        """Returnerer treshold værdierne for det givne øje.
        Argument:
            side: Indikerer hvorvidt det er venstre øje (0) eller om det er højre øje (1)
        """

        # Venstre øje
        if side == 0:
            # Returnerer summen af venstre threshold og deler det med længden af listen for venstre threshold
            return int(sum(self.thresholds_left) / len(self.thresholds_left))

        # Højre øje
        elif side == 1:
            return int(sum(self.thresholds_right) / len(self.thresholds_right))

    @staticmethod
    def iris_size(frame):
        """Returnerer procendelen af plads som irisen er af øjet.

        Argument:
            frame (numpy.ndarray): Binarized iris frame
        """

        frame = frame[5:-5, 5:-5]
        height, width = frame.shape[:2]
        # Antal af pixels
        nb_pixels = height * width
        # Antal af sorte pixels
        nb_blacks = nb_pixels - cv2.countNonZero(frame)
        return nb_blacks / nb_pixels

    @staticmethod
    def find_best_threshold(eye_frame):
        """Udregner den optimale treshold for at binarize billedet til det givne øje.
        Argument:
            eye_frame (numpy.ndarray): Frame of the eye to be analyzed
        """
        average_iris_size = 0.48
        trials = {}

        for threshold in range(5, 100, 5):
            # Definerer iris_frame til at være funktionen kørt med de to parameter.
            iris_frame = Pupil.image_processing(eye_frame, threshold)
            # Finder størrelsen af irisen ud fra iris_frame og gemmer det i en liste
            trials[threshold] = Calibration.iris_size(iris_frame)

        # Gemmer det bedste threshhold i den liste med færrest elementer.
        # Gemmer iris størrelsen ved at tage den absolutte værdi af p[1]- gennemsnitlige iris størrelse, 0.48.
        # key er et keyword, dermed at den kører i listen p og sorterer i den liste ud fra absolutte værdi af p[1] og average iris size.
        best_threshold, iris_size = min(trials.items(), key=(lambda p: abs(p[1] - average_iris_size)))
        # Returnerer bedste threshold
        return best_threshold

    def evaluate(self, eye_frame, side):
        """Optimerer på kalibrationen ved at tage det givne billede i overvejlse.

        Arguments:
            eye_frame (numpy.ndarray): Frame of the eye
            side: Indicates whether it's the left eye (0) or the right eye (1)
        """
        # gemmer threshold i en variabel der definerer threshhold ud fra det givne eye_frame man levere.
        threshold = self.find_best_threshold(eye_frame)
        # Venstre øje
        if side == 0:
            self.thresholds_left.append(threshold)
        # Højre øje
        elif side == 1:
            self.thresholds_right.append(threshold)
