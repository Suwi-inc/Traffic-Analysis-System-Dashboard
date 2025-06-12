import cv2
import json

lanes = []
current_points = []
lane_count = 0

def click_event(event, x, y, flags, param):
    global current_points, lane_count, lanes, frame_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        current_points.append([x, y])
        cv2.circle(frame_copy, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Select Lanes", frame_copy)

        if len(current_points) == 4:
            lane_count += 1
            lane_id = f"lane_{lane_count}"
            lane_name = input(f"Enter name for {lane_id}: ")
            lane_data = {
                "id": lane_id,
                "name": lane_name,
                "points": current_points.copy()
            }
            lanes.append(lane_data)
            current_points = []
            print(f"{lane_id} saved.\nYou can now define the next lane...")

video_path = "multi_lane_sd.mp4" 
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

ret, frame = cap.read()
cap.release()

if not ret:
    print("Error: Could not read the first frame.")
    exit()

frame_copy = frame.copy()
cv2.imshow("Select Lanes", frame_copy)
cv2.setMouseCallback("Select Lanes", click_event)

print("Click 4 points to define a lane. After 4 points, you will be prompted to name the lane.")
print("Press 's' to save and exit.")

# Wait for 's' key to finish input
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        if current_points:
            print("You have an incomplete lane with fewer than 4 points. Discarding it.")
        break

cv2.destroyAllWindows()

# Save to JSON
output = {"lanes": lanes}
with open("predefined_lanes.json", "w") as f:
    json.dump(output, f, indent=4)

print("Lanes saved to predefined_lanes.json")
