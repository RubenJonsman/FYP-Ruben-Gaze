from __future__ import division
import os
import cv2
import dlib
from .eye import Eye
from .calibration import Calibration


class GazeTracking(object):
    """
    Denne klasse tracker brugeres gaze.
    Den vidergiver brugbar information såsom positionen af øjene og
    pupilerne og tillader at vide om øjnene er lukkede eller åbne.
    Den kan derudover også tjekke om man kigger til henholdvist højre og venstre.
    """

    def __init__(self):
        self.frame = None
        self.eye_left = None
        self.eye_right = None
        self.calibration = Calibration()

        # _face_detector bruges til at finde ansigtet.
        self._face_detector = dlib.get_frontal_face_detector()

        # _predictor bruges til at finde ansigts landmarks af et givnet ansigt.
        cwd = os.path.abspath(os.path.dirname(__file__))
        # Definerer pathen for vores pre-weighted algoritmen
        model_path = os.path.abspath(os.path.join(cwd, "trained_models/shape_predictor_68_face_landmarks.dat"))
        # Siger at den skal predicte ud fra algoriten definerert ovenover.
        self._predictor = dlib.shape_predictor(model_path)

    # "The main purpose of any decorator is to change your class methods or
    # attributes in such a way so that the user of your class no need to make
    # any change in their code."
    @property
    def pupils_located(self):
        """Tjekker at pupilen er blevet lokaliseret"""
        # Prøver at tage int værdierne af de forskellige pupil koordinater
        try:
            int(self.eye_left.pupil.x)
            int(self.eye_left.pupil.y)
            int(self.eye_right.pupil.x)
            int(self.eye_right.pupil.y)
            return True
        except Exception:
            return False

    def _analyze(self):
        """Detekterer ansigtet og initializer "Eye objects" """
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_detector(frame)

        # Prøver at tage landmarksne af frame og faces[0]
        try:
            landmarks = self._predictor(frame, faces[0])
            # Gemmer derefter venstre øje som
            #             original_frame, landmarks, side, calibration):
            self.eye_left = Eye(frame, landmarks, 0, self.calibration)
            self.eye_right = Eye(frame, landmarks, 1, self.calibration)
        # Hvis der kommer en fejl, sætter den øjnene til at være None
        except IndexError:
            self.eye_left = None
            self.eye_right = None

    def refresh(self, frame):
        """Refresher framet og analyserer det.

        Arguments:
            frame (numpy.ndarray): The frame to analyze
        """
        self.frame = frame
        self._analyze()

    def pupil_left_coords(self):
        """Returnerer koordinaterne for venstre pupil"""
        # Tjekker først om venstre pupil er fundet
        if self.pupils_located:
            # Sætter derefter x-koordinatet til at være Orego's x-værdi + intensiteten af farverne
            x = self.eye_left.origin[0] + self.eye_left.pupil.x
            y = self.eye_left.origin[1] + self.eye_left.pupil.y
            return (x, y)

    def pupil_right_coords(self):
        """Returnerer koordinaterne for højre pupil"""
        # Tjekker først om højre pupil er fundet
        if self.pupils_located:
            x = self.eye_right.origin[0] + self.eye_right.pupil.x
            y = self.eye_right.origin[1] + self.eye_right.pupil.y
            return (x, y)

    def horizontal_ratio(self):
        """Returnerer et tal mellem 0.0 og 1.0 der indikerer den horisontale retning for gaze.
        Den ekstreme højre er 0.0, centrum bør være 0.5 og ekstreme venstre er 1.0"""

        # Tjekker om pupilerne er lokaliseret.
        if self.pupils_located:
            # Definerer venstre pupil ved at tage x / centrum af venstre øje x-værdi * 2 - 10
            pupil_left = self.eye_left.pupil.x / (self.eye_left.center[0] * 2 - 10)
            # Definerer højre pupil ved at tage x / centrum af højre øje * 2 - 10
            pupil_right = self.eye_right.pupil.x / (self.eye_right.center[0] * 2 - 10)
            # Returnerer (venstre + højre) / 2. På denne måde vil man altid få en
            # værdi mellem 0 og 1 der bestemmer hvor hen øjet kigger.
            return (pupil_left + pupil_right) / 2

    def vertical_ratio(self):

        """Returnerer et tal mellem 0.0 og 1.0 der indikerer den
        vertikale retning af gaze. Den ekstreme top er 0.0,
        centrum er 0.5 og ekstremt bund er 1.0"""
        # Tjekker om pupilerne er fundet
        if self.pupils_located:
            pupil_left = self.eye_left.pupil.y / (self.eye_left.center[1] * 2 - 10)
            pupil_right = self.eye_right.pupil.y / (self.eye_right.center[1] * 2 - 10)
            return (pupil_left + pupil_right) / 2

    def is_right(self):
        """Returnerer True hvis brugeren kigger til højre"""
        if self.pupils_located:
            # Hvis den horizontale_ratio er mindre
            # eller lig 0.4, kigger personen til højre.
            # Denne værdi kan ændres, afhængigt af kamera, bruger osv..
            # Den er tilpasset til Rubens computer og Ruben der bruger programmet. D
            # Dette vil betyde at det meget vel ikke vil virke på andre computere,
            # Dog er sandsynligheden for at det virker på andre mennesker,
            # der gør brug af Rubens computer stor
            return self.horizontal_ratio() <= 0.40

    def is_left(self):
        """Returnerer True hvis brugeren kigger til venstre"""
        if self.pupils_located:
            # Samme som ovenstående funktion
            return self.horizontal_ratio() >= 0.80

    def is_center(self):
        """Returnerer True hvis brugeren kigger i midten"""
        if self.pupils_located:
            # Hvis brugeren ikke kigger til venstre, eller ikke
            # kigger til højre, vil personen kigge i midten.
            return self.is_right() is not True and \
                   self.is_left() is not True

    def is_blinking(self):
        """Returnerer sandt, hvis brugere lukker sine øjne."""
        if self.pupils_located:
            # Definerer blinking_ratio som blinking ratioen af venstre og højre lagt sammen delt med 2.
            blinking_ratio = (self.eye_left.blinking + self.eye_right.blinking) / 2
            # Hvis blinking ratio er større end 5, betyder det at personen blinker.
            return blinking_ratio > 5

    def annotated_frame(self):
        """Returnerer main frame med pupiler optegnet"""
        # Kopierer framet
        frame = self.frame.copy()

        # Tjekker om pupilerne er fundet
        if self.pupils_located:
            """Sætter en masse punkter i øjet, og tegner derefter 4 linjer der til sidst bliver til et kryds."""
            color = (0, 255, 0)
            x_left, y_left = self.pupil_left_coords()
            x_right, y_right = self.pupil_right_coords()
            cv2.line(frame, (x_left - 5, y_left), (x_left + 5, y_left), color)
            cv2.line(frame, (x_left, y_left - 5), (x_left, y_left + 5), color)
            cv2.line(frame, (x_right - 5, y_right), (x_right + 5, y_right), color)
            cv2.line(frame, (x_right, y_right - 5), (x_right, y_right + 5), color)

        return frame
