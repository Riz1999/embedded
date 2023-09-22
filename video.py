from ultralytics import YOLO
import cv2
import numpy as np
import os
import sys
from api import process_api
# Loading YOLO models
def execute(image_path):
    # print("Executing py script")
    detect_model = YOLO("Detect-20230921T094350Z-001/Detect/best.pt")
    pattern_model = YOLO("Pattern-20230921T094355Z-001/Pattern/best.pt")
    color_model = YOLO("Color-20230921T094349Z-001/Color/best.pt")


    # test = os.path.join('.', 'test')
    # video_path = os.path.join(test, 'WhatsApp Video 2023-09-20 at 6.00.02 PM.mp4')

    # # Open the video and get video properties
    # cap = cv2.VideoCapture(video_path)
    # frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # fps = int(cap.get(cv2.CAP_PROP_FPS))
    # ret, frame = cap.read()
    # H, W, _ = frame.shape

    # # Get the user input for the second to start processing
    # desired_second = float(input("Enter the second to start processing: "))


    # start_frame = int(desired_second * fps)

    threshold = 0.5

    # image_path ="s.png"  # Replace with the path to your image
    frame = cv2.imread(image_path)

    class_names = {
        0: 'sleeve top',
        1: 'long sleeve top',
        2: 'short sleeve outwear',
        3: 'long sleeve outwear',
        4: 'vest',
        5: 'sling',
        6: 'shorts',
        7: 'trousers',
        8: 'skirt',
        9: 'short sleeve dress',
        10: 'long sleeve dress',
        11: 'vest dress',
        12: 'sling dress'
    }

    # frame_number = 0 

    # while ret:
    #     if frame_number == start_frame:
    #         results_detect = detect_model(frame)[0]

    #         for result in results_detect.boxes.data.tolist():
    #             x1, y1, x2, y2, score, class_id = result

    #             if score > threshold:
    #                 cropped_region = frame[int(y1):int(y2), int(x1):int(x2)]

    #                 pattern_results = pattern_model(cropped_region)
    #                 pattern_dict = pattern_results[0].names
    #                 pattern_probs = pattern_results[0].probs.data.tolist()
    #                 pattmax = pattern_dict[np.argmax(pattern_probs)]

    #                 color_results = color_model(cropped_region)
    #                 color_dict = color_results[0].names
    #                 color_probs = color_results[0].probs.data.tolist()
    #                 colormax = color_dict[np.argmax(color_probs)]

    #                 label = f'{pattmax} {colormax} {results_detect.names[int(class_id)].upper()} '

                
    #                 print(label)

    #     ret, frame = cap.read()
    #     frame_number += 1

    
    #     if frame_number > start_frame:
    #         break

    # cap.release()
    # cv2.destroyAllWindows()


    results_detect = detect_model(frame)[0]

    for result in results_detect.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cropped_region = frame[int(y1):int(y2), int(x1):int(x2)]

            pattern_results = pattern_model(cropped_region)
            pattern_dict = pattern_results[0].names
            pattern_probs = pattern_results[0].probs.data.tolist()
            pattmax = pattern_dict[np.argmax(pattern_probs)]

            color_results = color_model(cropped_region)
            color_dict = color_results[0].names
            color_probs = color_results[0].probs.data.tolist()
            colormax = color_dict[np.argmax(color_probs)]

            label = f'{pattmax} {colormax} {results_detect.names[int(class_id)].upper()} '

            print(label)
            result = process_api(label)
            for res in result:
                print(res['product_link'])

execute(sys.argv[1])