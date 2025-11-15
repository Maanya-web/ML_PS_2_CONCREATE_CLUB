import cv2

IMAGE_PATH = 'snapshot.png'
DISPLAY_WIDTH = 1280

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        (orig_h, orig_w) = params['original_shape']
        (disp_h, disp_w) = params['display_shape']
        
        x_scale = orig_w / disp_w
        y_scale = orig_h / disp_h
        
        orig_x = int(x * x_scale)
        orig_y = int(y * y_scale)
        
        print(f"Original 4K Coords: (x={orig_x}, y={orig_y})")

image = cv2.imread(IMAGE_PATH)
if image is None:
    print(f"Error: Could not read image at {IMAGE_PATH}")
    exit()

original_height, original_width = image.shape[:2]

display_height = int((DISPLAY_WIDTH / original_width) * original_height)

display_image = cv2.resize(image, (DISPLAY_WIDTH, display_height))

params = {
    "original_shape": (original_height, original_width),
    "display_shape": (display_height, DISPLAY_WIDTH)
}

cv2.namedWindow('Click to find coordinates (Press Q to quit)')
cv2.setMouseCallback('Click to find coordinates (Press Q to quit)', click_event, params)

print("--- Coordinate Finder Tool ---")
print(f"Original image size: {original_width}x{original_height}")
print(f"Displaying at: {DISPLAY_WIDTH}x{display_height}")
print("Click on the image to get the 4K coordinates. Press 'q' to quit.")

while True:
    cv2.imshow('Click to find coordinates (Press Q to quit)', display_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()