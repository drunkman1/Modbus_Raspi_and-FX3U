
from cv2 import threshold
from openvino.inference_engine import IENetwork, IECore
import cv2 as cv
import numpy as np
import time

device ="MYRIAD"
xml = 'model/saved_model.xml'
bin = 'model/saved_model.bin'
ie = IECore()
#network = ie.read_network(xml, bin)
net = ie.read_network(xml,bin)
img_info_input_blob = None
feed_dict = {}
labels ="model/labels.txt"
video = "video/cars.mp4"
threshold = 0.6
print(net.inputs)
is_async_mode = False
for blob_name in net.inputs:
    if len(net.inputs[blob_name].shape) == 4:
        input_blob = blob_name
        print('input_blob:', input_blob)
    elif len(net.inputs[blob_name].shape) == 2:
        img_info_input_blob = blob_name
        print('img_info_input_blob:', img_info_input_blob)
    else:
        raise RuntimeError("Unsupported {}D input layer '{}'. Only 2D and 4D input layers are supported"
                            .format(len(net.inputs[blob_name].shape), blob_name))
        
assert len(net.outputs) == 1, "Demo supports only single output topologies"
out_blob = next(iter(net.outputs))
exec_net = ie.load_network(network=net, num_requests=2, device_name=device)
n, c, h, w = net.inputs[input_blob].shape
#print('info_blob:', img_info_input_blob)

cap = cv.VideoCapture(0)
with open(labels, 'r') as f:
    labels_map = [x.strip() for x in f]
if not cap.isOpened():
    print("Meo the tim dc camera")
    exit()
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        frame_h, frame_w = frame.shape[:2]
    else: 
        print('Meo nhan dc frame. End')
        break
    t1 = time.time()
    in_frame = cv.resize(frame, (w, h))
    in_frame = in_frame.transpose((2, 0, 1))  # Change data layout from HWC to CHW
    in_frame = in_frame.reshape((n, c, h, w))
    feed_dict[input_blob] = in_frame
    exec_net.start_async(request_id=0, inputs=feed_dict)
    if exec_net.requests[0].wait(-1) == 0:
        t2 = time.time()
        det_time = t2 -t1

        # Parse detection results of the current request
        res = exec_net.requests[0].outputs[out_blob]
        for obj in res[0][0]:
            # Draw only objects when probability more than specified threshold
            if obj[2] > threshold:
                xmin = int(obj[3] * frame_w)
                ymin = int(obj[4] * frame_h)
                xmax = int(obj[5] * frame_w)
                ymax = int(obj[6] * frame_h)
                class_id = int(obj[1])
                # Draw box and label\class_id
                color = (min(class_id * 12.5, 255), min(class_id * 7, 255), min(class_id * 5, 255))
                cv.rectangle(frame, (xmin, ymin), (xmax, ymax), (0,255,255), 2)
                
        inf_time_message = "Fps: N\A " if is_async_mode else \
                "Fps: {}".format(int(det_time * 1000)) 
        cv.rectangle(frame, (10,20),(130,55),(0,0,0),-1)

        cv.putText(frame, inf_time_message, (15, 45), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255,255), 2)
    cv.imshow("ObDetec", frame)
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()

'''
import cv2 as cv
import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
'''