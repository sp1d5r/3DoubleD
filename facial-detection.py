# pip install opencv-python
# install opencv "pip install opencv-python"
import cv2

# distance from camera to object(face) measured
# centimeter
Known_distance = 76.2

# width of face in the real world or Object Plane
# centimeter
Known_width = 14.3

# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# defining the fonts
fonts = cv2.FONT_HERSHEY_SIMPLEX

# face detector object
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


def face_data(image):
    face_width = 0  # making face width to zero

    # converting color image to gray scale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detecting face in the image
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)

    # looping through the faces detect in the
    # image getting coordinates x, y ,
    # width and height
    for (x, y, h, w) in faces:
        # draw the rectangle on the face
        cv2.rectangle(image, (x, y), (x + w, y + h), GREEN, 2)

        # getting face width in the pixels
        face_width = w

    # return the face width in pixel
    return face_width


# Calculate the focal length
def calc_focal_length(measured_distance, real_width, width_in_ref):
    # finding the focal length
    focal_length = (width_in_ref * measured_distance) / real_width
    return focal_length


# distance finder
def distance_finder(focal_Length, real_face_width, face_width_in_frame):
    distance = (real_face_width * focal_Length) / face_width_in_frame

    # return the distance
    return distance


# reading reference_image from directory
ref_image = cv2.imread("/Users/elijahahmad/PycharmProjects/Facial-Distance-Detection/ref-image.png")

# find the face width(pixels) in the reference_image
ref_image_face_width = face_data(ref_image)

# get the focal by calling "Focal_Length_Finder"
# face width in reference(pixels),
# Known_distance(centimeters),
# known_width(centimeters)
focal_length_found = calc_focal_length(
    Known_distance, Known_width, ref_image_face_width)

# initialize the camera object so that we
# can get frame from it
cap = cv2.VideoCapture(0)

# looping through frame, incoming from
# camera/video
while True:

    # reading the frame from camera
    _, frame = cap.read()

    # calling face_data function to find
    # the width of face(pixels) in the frame
    face_width_in_frame = face_data(frame)

    # check if the face is zero then not
    # find the distance
    if face_width_in_frame != 0:
        # finding the distance by calling function
        # Distance finder function need
        # these arguments the Focal_Length,
        # Known_width(centimeters),
        # and Known_distance(centimeters)
        Distance = distance_finder(focal_length_found, Known_width, face_width_in_frame) #Distance_finder(Focal_length_found, Known_width, face_width_in_frame)

        # draw line as background of text
        cv2.line(frame, (30, 30), (230, 30), RED, 32)
        cv2.line(frame, (30, 30), (230, 30), BLACK, 28)

        # Drawing Text on the screen
        cv2.putText(
            frame, f"Distance: {round(Distance, 2)} CM", (30, 35),
            fonts, 0.6, RED, 2)

    # show the frame on the screen
    cv2.imshow("frame", frame)

    # quit the program if you press 'q' on keyboard
    if cv2.waitKey(1) == ord("q"):
        break

# closing the camera
cap.release()

# closing the windows that are opened
cv2.destroyAllWindows()