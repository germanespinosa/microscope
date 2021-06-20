import cv2
import screeninfo
from time import sleep

def query_maximum_resolution(cap):
    current_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    current_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  10000)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)
    max_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    max_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  current_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, current_height)
    return max_width, max_height

zoom_value = 50
# function that handles the trackbar
def zoom(val):
    global zoom_value
    # check if the value of the slider
    zoom_value = val

flipped = False

def get_zoomed(img, zoom , size):
    height, width = img.shape[0:2]
    cheight, cwidth = int(height-(height*zoom/100/2)), int(width-(width*zoom/100/2))
    cy, cx = int((height-cheight)/2), int((width-cwidth)/2)
    cox = 0 if cx+offset[0] < 0 else width - cwidth if cx+offset[0] > width - cwidth else cx+offset[0]
    coy = 0 if cy+offset[1] < 0 else height - cheight if cx+offset[1] > height - cheight else cy+offset[1]
    if flipped:
        cropped = img[coy:coy+cheight, cox+cwidth:cox:-1]
    else:
        cropped = img[coy:coy + cheight, cox:cox + cwidth]
    return cv2.resize(cropped, size)

is_moving = False
moved = False
anchor = (0,0)
offset = (0,0)
def process_click(event, x, y,flags, params):
    global is_moving
    global moved
    global flipped
    global anchor
    global offset
    if event == cv2.EVENT_LBUTTONUP:
        is_moving = False
        if not moved:
            print("flipping")
            flipped = not flipped
    elif event == cv2.EVENT_LBUTTONDOWN:
        anchor = (x, y)
        is_moving = True
        moved = False
    else:
        if is_moving:
            moved = True
            offset = (offset[0] + x - anchor[0], offset[1] + y - anchor[1])
            anchor = (x, y)
    print(offset)

screen = screeninfo.get_monitors()[1]
cap = cv2.VideoCapture(0)
sleep(.5)

current_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
current_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print (current_width, current_height)
#Check whether user selected camera is opened successfully.

if not (cap.isOpened()):
    print("Could not open video device")


width, height = screen.width, screen.height

cv2.namedWindow("preview", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.moveWindow("preview", screen.x - 1, screen.y - 1)
cv2.createTrackbar("Zoom", 'preview', 50, 100, zoom)
cv2.setMouseCallback('preview', process_click)

while (True):
    ret, frame = cap.read()
    resized = get_zoomed(frame, zoom_value, (width, height))
    cv2.imshow("preview", resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break