from ctypes import *
import random
import os
import cv2
import time
import darknet
import argparse
import pyrealsense2 as rs
import numpy as np
import math
from threading import Thread, enumerate
from queue import Queue

# 4 is D435i RGB
# 6 is 笔记本 RGB
def parser():
    parser = argparse.ArgumentParser(description="YOLO Stick Detection")
    parser.add_argument("--input", type=str, default=4,
                        help="video source. If empty, uses webcam 0 stream")
    parser.add_argument("--out_filename", type=str, default="",
                        help="inference video name. Not saved if empty")
    parser.add_argument("--weights", default="./backup/stick_final.weights",
                        help="yolo weights path")
    parser.add_argument("--dont_show", action='store_true',
                        help="windown inference display. For headless systems")
    parser.add_argument("--ext_output", action='store_true',
                        help="display bbox coordinates of detected objects")
    parser.add_argument("--config_file", default="./cfg/stick.cfg",
                        help="path to config file")
    parser.add_argument("--data_file", default="./cfg/stick.data",
                        help="path to data file")
    parser.add_argument("--thresh", type=float, default=.25,
                        help="remove detections with confidence below this value")
    return parser.parse_args()


def str2int(video_path):
    """
    argparse returns and string althout webcam uses int (0, 1 ...)
    Cast to int if needed
    """
    try:
        return int(video_path)
    except ValueError:
        return video_path


def check_arguments_errors(args):
    assert 0 < args.thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
    if not os.path.exists(args.config_file):
        raise(ValueError("Invalid config path {}".format(os.path.abspath(args.config_file))))
    if not os.path.exists(args.weights):
        raise(ValueError("Invalid weight path {}".format(os.path.abspath(args.weights))))
    if not os.path.exists(args.data_file):
        raise(ValueError("Invalid data file path {}".format(os.path.abspath(args.data_file))))
    if str2int(args.input) == str and not os.path.exists(args.input):
        raise(ValueError("Invalid video path {}".format(os.path.abspath(args.input))))


def model():
    pipeline = rs.pipeline()
    cfg = rs.config()
    cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    profile = pipeline.start(cfg)
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    align = rs.align(rs.stream.color)
    flag = 1
    location = []
    args = parser()
    check_arguments_errors(args)

    network, class_names, class_colors = darknet.load_network(
            args.config_file,
            args.data_file,
            args.weights,
            batch_size=1
        )
    return [pipeline,align,network, class_names, class_colors,args,profile]
   #width = darknet.network_width(network)
   #height = darknet.network_height(network)


def shibie(pipeline,align,network, class_names, class_colors,args,profile):
    width = 640
    height = 480
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
    if not aligned_frames:
        return 0
    depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()
    #Intrinsics & Extrinsics
    depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
    color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
    depth_to_color_extrin = depth_frame.profile.get_extrinsics_to(color_frame.profile)

    color_image = np.asanyarray(color_frame.get_data())

    frame_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (width, height),
                               interpolation=cv2.INTER_LINEAR)
    img_for_detect = darknet.make_image(width, height, 3)
    darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())

    arknet_image = img_for_detect
    prev_time = time.time()
    darknet_image = img_for_detect
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=args.thresh)


    fps = int(1/(time.time() - prev_time))
    print("FPS: {}".format(fps))
    darknet.print_detections(detections, args.ext_output)
    darknet.free_image(darknet_image)
    if frame_resized is not None:
        image ,location= darknet.draw_boxes(detections, frame_resized, class_colors)
        if location[3] >= 480:
            location[3] = 480
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        a=[int(location[0]*0.5+location[2]*0.5),int(location[1]*0.5+location[3]*0.5)]
        print(a)
        dist_a = depth_frame.get_distance(a[0], a[1])
        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        a_point = rs.rs2_deproject_pixel_to_point(depth_intrin, a, dist_a)
        print("距离为：",dist_a)
        cv2.imshow('Inference', image)
        key= cv2.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:
            pipeline.stop()
            cv2.destroyAllWindows()
            return 0
        return [location,dist_a]
