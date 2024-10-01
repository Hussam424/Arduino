import cv2
import numpy as np
import serial  # For sending data to Arduino

# Open serial connection to Arduino (adjust port as necessary)
arduino = serial.Serial('COM3', 9600)  # Adjust to the correct port for Arduino

# OpenCV setup
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Capture frame from camera
    frame = cv2.flip(frame, 1)  # Flip frame to match real-world movements
    roi = frame[100:400, 100:400]  # Region of interest (hand detection area)
    
    # Convert to grayscale and apply Gaussian blur
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (35, 35), 0)
    
    # Threshold the image to create a binary image
    _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        # Find the largest contour (assumed to be the hand)
        contour = max(contours, key=cv2.contourArea)
        hull = cv2.convexHull(contour)
        
        # Draw the hand contour and hull
        cv2.drawContours(roi, [contour], -1, (0, 255, 0), 2)
        cv2.drawContours(roi, [hull], -1, (0, 0, 255), 2)
        
        # Count fingers based on convexity defects
        hull = cv2.convexHull(contour, returnPoints=False)
        defects = cv2.convexityDefects(contour, hull)
        if defects is not None:
            count_defects = 0
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(contour[s][0])
                end = tuple(contour[e][0])
                far = tuple(contour[f][0])
                a = np.linalg.norm(np.array(start) - np.array(end))
                b = np.linalg.norm(np.array(start) - np.array(far))
                c = np.linalg.norm(np.array(end) - np.array(far))
                angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
                
                if angle <= np.pi / 2:  # Angle less than 90 degrees, treat as a finger
                    count_defects += 1
            
            # Send the number of fingers detected to Arduino
            if count_defects == 0:
                arduino.write(b'1')  # Send '1' for 1 finger detected
            elif count_defects == 1:
                arduino.write(b'2')  # Send '2' for 2 fingers detected
            elif count_defects == 2:
                arduino.write(b'3')  # Send '3' for 3 fingers detected
            elif count_defects == 3:
                arduino.write(b'4')  # Send '4' for 4 fingers detected
            elif count_defects == 4:
                arduino.write(b'5')  # Send '5' for 5 fingers detected
    
    # Display the ROI (Region of Interest) for debugging
    cv2.imshow("Threshold", thresh)
    cv2.imshow("ROI", roi)
    
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
