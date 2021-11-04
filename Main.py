# import af forskelleige moduler vi gør brug af.
import cv2
from gaze_tracking import GazeTracking
from time import sleep
from FireBaseHelper import DB_Helper

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
sentence = []
liste = []
T = 0
# Alfabetet vi plotter til at starte med i programmet
start = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
         'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
         'u', 'v', 'w', 'x', 'y', 'z', 'æ', 'ø', 'å', '-', '←']

startstring = ""

# Laver en kolonne i databasen
DB_Helper().INSERTWL(start)
DB_Helper().INSERTDATA(startstring)
sleep(1)


def convert_to_string(l):
    string = ""

    for char in l:
        string = string + str(char)

    return string


while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""
    # Alfabet som gentagende gange slices, der er tilføjet mellemrum og slet, for at man også kan gøre de funktioner.
    alfa = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', 'æ', 'ø', 'å', '-', '←']
    # Kigger brugeren til højre, gøres følgende
    if gaze.is_right():
        # text = "Looking right"

        if T == 0:
            k = round(len(alfa) / 2)
            sentence = alfa[k:]
            #print(sentence)
            DB_Helper().INSERTWL(sentence)
            T += 1
            sleep(0.8)

        else:
            k = round(len(sentence) / 2)
            sentence = sentence[k:]
            #print(sentence)
            DB_Helper().INSERTWL(sentence)
            sleep(0.8)

    # Kigger brugeren til vesntre, gøres følgende.
    elif gaze.is_left():
        # text = "Looking left"
        if T == 0:
            k = round(len(alfa) / 2)
            sentence = alfa[:k]
            #print(sentence)
            DB_Helper().INSERTWL(sentence)
            T += 1
            sleep(0.8)

        else:
            k = round(len(sentence) / 2)
            sentence = sentence[:k]
            #print(sentence)
            DB_Helper().INSERTWL(sentence)
            sleep(0.8)

    # Er der kun et element i listen, betyder det at brugeren har indsnævret sig til det bogstav de gerne ville have.
    if len(sentence) == 1:
        # Vælger man slet, så sletter den det sidste element i listen.
        if sentence == ['←']:
            #print("Hej")
            if len(liste) > 0:
                liste.pop()
                DB_Helper().INSERTDATA(convert_to_string(liste))

        # Vælger man mellemrum, indsætter den et mellemrum.
        elif sentence == ["-"]:
            liste.append(" ")
            liste.append(sentence)
            DB_Helper().INSERTDATA(convert_to_string(liste))

        # Hvis det enten ikke er mellemrum eller slet, tager den bare bogstavet og appender til listen.
        else:
            #print("Før liste: " + str(liste))
            liste.append(sentence)
           # print("Efter liste: " + str(liste))
            DB_Helper().INSERTDATA(convert_to_string(liste))
            sleep(0.8)

        sentence = alfa
        T = 0
        DB_Helper().INSERTWL(sentence)

    if T == 0:
        text = str(alfa)
    else:
        text = str(sentence)

    font = cv2.FONT_HERSHEY_DUPLEX
    textsize = cv2.getTextSize(text, font, 1, 2)[0]

    # get coords based on boundary
    textX = (frame.shape[1] - textsize[0]) / 2
    cv2.putText(frame, text, (int(textX), 40), cv2.FONT_HERSHEY_DUPLEX, 0.5, (147, 58, 31), 2)

    # Tager koordinaterne for venstre og højre pupil og gemmer det i variabler.
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    # Plotter/printer koordinaterne for øjnene på videofeeden.
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    # Viser livevideofeed.
    cv2.imshow("Demo", frame)

    # Klikker man på ESC så lukker programmet.
    if cv2.waitKey(1) == 27:
        break
