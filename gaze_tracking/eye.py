import math
import numpy as np
import cv2
from .pupil import Pupil



class Eye():
    """
    Denne klasse laver et nyt frame til at isolere øjet og initialise pupil detection
    """

    LEFT_EYE_POINTS = [36, 37, 38, 39, 40, 41]
    RIGHT_EYE_POINTS = [42, 43, 44, 45, 46, 47]

    def __init__(self, original_frame, landmarks, side, calibration):
        self.frame = None
        self.origin = None
        self.center = None
        self.pupil = None

        self._analyze(original_frame, landmarks, side, calibration)

    @staticmethod
    def _middle_point(p1, p2):
        """Returnerer midtpunktet (x,y) mellem to punkter.

        Arguments:
            p1 (dlib.point): First point
            p2 (dlib.point): Second point
        """
        # Tager x-værdien for p1 og p2 plusser dem og deler med 2. Tager også int værdien
        x = int((p1.x + p2.x) / 2)
        # Gør det samme bare med y.
        y = int((p1.y + p2.y) / 2)
        return (x, y)

    def _isolate(self, frame, landmarks, points):
        """Isolerer et øje, for at have et frame uden andre dele af ansigtet.
        Arguments:
            frame (numpy.ndarray): Frame containing the face
            landmarks (dlib.full_object_detection): Facial landmarks for the face region
            points (list): Points of an eye (from the 68 Multi-PIE landmarks)
        """
        # Region = er et np array for de forskellige landmarks for x og y koordinaterne lagt sammen i et array.
        region = np.array([(landmarks.part(point).x, landmarks.part(point).y) for point in points])
        # Kopierer arrayet og sætter det hele til typen int32
        region = region.astype(np.int32)


        # Laver en mask for kun at få øjet.
        height, width = frame.shape[:2]
        # Laver masken til et black frame, hvilket bør gøre at alt er ca samme farve og man sorterer dermed alle uønskede farver fra billedet.
        black_frame = np.zeros((height, width), np.uint8)
        mask = np.full((height, width), 255, np.uint8)
        cv2.fillPoly(mask, [region], (0, 0, 0))
        eye = cv2.bitwise_not(black_frame, frame.copy(), mask=mask)

        # Cropper listen for regionen med et margin
        margin = 5
        min_x = np.min(region[:, 0]) - margin
        max_x = np.max(region[:, 0]) + margin
        min_y = np.min(region[:, 1]) - margin
        max_y = np.max(region[:, 1]) + margin

        # Definerer et nyt frame ud fra minimum og maximum af x og y-værdier
        self.frame = eye[min_y:max_y, min_x:max_x]
        # Sætter Orego til minx og miny
        self.origin = (min_x, min_y)
        # Højden og bredden defineret...
        height, width = self.frame.shape[:2]
        # og centrum defineret
        self.center = (width / 2, height / 2)

    def _blinking_ratio(self, landmarks, points):
        """Udregner et forhold der indikerer hvorvidt øjet er lukket eller ej.
        Det er divisionen af bredden af øjet med højden.

        Arguments:
            landmarks (dlib.full_object_detection): Facial landmarks for the face region
            points (list): Points of an eye (from the 68 Multi-PIE landmarks)

        Returns:
            The computed ratio
        """
        # Definerer venstre, højre, top og bund, ved at tage de forskellige landmark points og tage indeksværdier for dem.
        left = (landmarks.part(points[0]).x, landmarks.part(points[0]).y)
        right = (landmarks.part(points[3]).x, landmarks.part(points[3]).y)
        top = self._middle_point(landmarks.part(points[1]), landmarks.part(points[2]))
        bottom = self._middle_point(landmarks.part(points[5]), landmarks.part(points[4]))

        # Definerer øje-bredden ved at tage hypotenusen ud fra venstre[0]-højre[0] og venstre[1] - højre[1]
        eye_width = math.hypot((left[0] - right[0]), (left[1] - right[1]))
        # Gør det samme bare med top og bund.
        eye_height = math.hypot((top[0] - bottom[0]), (top[1] - bottom[1]))

        # Prøver at definerer ratio, vil den kun kunne gøre hvis den har været succesfuld med ovenstående.
        # Hvis den ikke er succesfuld, sætter den bare ratio til er være None.
        try:
            ratio = eye_width / eye_height
        except ZeroDivisionError:
            ratio = None

        return ratio

    def _analyze(self, original_frame, landmarks, side, calibration):
        """Detekterer og isolerer øjet i et nyt frame og sender data til kalibrationen og initialiser pupil som et objekt.

        Arguments:
            original_frame (numpy.ndarray): Frame passed by the user
            landmarks (dlib.full_object_detection): Facial landmarks for the face region
            side: Indicates whether it's the left eye (0) or the right eye (1)
            calibration (calibration.Calibration): Manages the binarization threshold value
        """
        # Venstre øje
        if side == 0:
            points = self.LEFT_EYE_POINTS
        # Højre øje
        elif side == 1:
            points = self.RIGHT_EYE_POINTS
        else:
            return

        # Definerer blinking ratio af landmarks og points som blinking,
        self.blinking = self._blinking_ratio(landmarks, points)
        #Isolerer derefter ud fra oprindelige frame, landmarks og points
        self._isolate(original_frame, landmarks, points)

        # Hvis kalibrationen ikke er færdig kører den det her
        if not calibration.is_complete():
            # Optimerer på kalibrationen ved at tage det givne billede i overvejlse.
            # ud fra det givne frame og siden.
            calibration.evaluate(self.frame, side)

        # threshold er nu thresholdet af siden
        threshold = calibration.threshold(side)
        # Pupilen er nu funktionen pupil kørt med parameteren frame og threshold
        self.pupil = Pupil(self.frame, threshold)
