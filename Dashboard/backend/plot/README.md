# Lane Annotation Tool – Step-by-Step Instructions

This guide will help you run a script that :
- Loads the first frame of a video
- Allows you to click 4 points to define each lane
- Prompts you to name each lane
- Saves all annotated lanes to a `predefined_lanes.json` file

---

## Prerequisites

Make sure you have openCV installed

```bash
pip install opencv-python
```

---

## Step 1: Prepare Your Video

Place your video file in the same directory as the script (or note its full path).

Replace the placeholder in the script:

```python
video_path = "your_video.mp4"
```

With your actual video file name, e.g.:

```python
video_path = "traffic_footage.mp4"
```

---

##  Step 2: Understand the Workflow

- You'll click **4 points** for each lane.
- After 4 clicks, the program will prompt you in the terminal to name the lane.
- You can repeat this to define as many lanes as you need.
- When you're done, press the **`s` key** to save and exit.

---

## Step 3: Running the Script

Use Python to run the script:

```bash
python manual_plot.py
```

---

## Step 4: Annotate the Lanes

- A window will open showing the **first frame** of your video.
- Click **4 points** to define the shape of the first lane.
- In the terminal, type a name when prompted (e.g., "Left Lane").
- The lane will be saved, and you can start defining the next one.
- Repeat this for all lanes you want to define.

---

## Step 5: Save the lane coordinates

- Once you're done annotating, press the **`s` key** in the image window.
- The program will:
  - Discard any incomplete lane (less than 4 points)
  - Save the result to a file called `predefined_lanes.json`

---

## Output Format Example

```json
{
    "lanes": [
        {
            "id": "lane_1",
            "name": "Left Lane",
            "points": [
                [300, 400],
                [300, 350],
                [440, 350],
                [440, 400]
            ]
        },
        {
            "id": "lane_2",
            "name": "Right Lane",
            "points": [
                [480, 400],
                [480, 350],
                [650, 350],
                [650, 400]
            ]
        }
    ]
}
```

---

After this move the ```predefeined_lanes.json``` into the src directory to use the lane coordinates for the traffic analysis.


