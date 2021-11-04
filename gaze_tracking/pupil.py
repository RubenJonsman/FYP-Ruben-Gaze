import numpy as np
import cv2


class Pupil(object):
    """
    Denne klasse detekterer iri s af et øje og estimere positionen af pupilen.
    """
    # Definerer en masse variabler
    def __init__(self, eye_frame, threshold):
        self.iris_frame = None
        self.threshold = threshold
        self.x = None
        self.y = None

        self.detect_iris(eye_frame)

    # They behave like plain functions except that you can call them from an instance or the class:
    # Staticmethods are used to group functions which have some logical connection with a class to the class.

    # Alt i alt, denne funktion bliver kørt som en helt normal funktion og ikke objektorienteret.
    # Det er simpelthen bare fordi vi ikke vidste hvor functionen ellers skulle være,
    # derfor var det bare nemmere at smide den her
    @staticmethod
    def image_processing(eye_frame, threshold):
        """Laver operationer på eye_frame for at isolere irisen.

        Arguments:
            eye_frame (numpy.ndarray): Frame containing an eye and nothing else
            threshold (int): Threshold value used to binarize the eye frame

        Returns:
            Et frame, med et element der repræsenterer irisen.
        """
        kernel = np.ones((3, 3), np.uint8)
        new_frame = cv2.bilateralFilter(eye_frame, 10, 15, 15)
        new_frame = cv2.erode(new_frame, kernel, iterations=3)
        new_frame = cv2.threshold(new_frame, threshold, 255, cv2.THRESH_BINARY)[1]

        return new_frame

    def detect_iris(self, eye_frame):
        """Detekterer irisen og estimerer positionen af irisen ved at udregne det geometriske tyngdepunkt

        Arguments:
            eye_frame (numpy.ndarray): Frame containing an eye and nothing else
        """
        # Gemmer det isolerede iris i en variabel.
        self.iris_frame = self.image_processing(eye_frame, self.threshold)
        # Finds contours in a binary image.
        contours, _ = cv2.findContours(self.iris_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
        #Sorterer contours ud fra nøglen: contourarea altså det hvor der bliver contoured.
        contours = sorted(contours, key=cv2.contourArea)

        """@brief Calculates all of the moments up to the third order of a polygon or rasterized shape."""
        # Prøver at...
        # Gemme moments for contours[-2] i en variabel.
        # Definerer x til at være int værdien af intensiteten af pixel-farverne i hvert center of mass billedet.
        # Samme med y bare med y værdier.
        try:
            moments = cv2.moments(contours[-2])
            self.x = int(moments['m10'] / moments['m00'])
            self.y = int(moments['m01'] / moments['m00'])
        except (IndexError, ZeroDivisionError):
            pass
