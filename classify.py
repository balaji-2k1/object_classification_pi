# OBJECT DETECTION


# Importing required Libraries tflite will only work on embedded pi not on laptop
from tflite_runtime.interpreter import Interpreter
import numpy as np
from PIL import Image, ImageFont, ImageDraw 
import time
import cv2

model_path = "model_files/mobilenet_v1_1.0_224_quant.tflite" 

# Optional models
#model_path = "model_files/mobilenet_v2_1.0_224_quant.tflite" 
#model_path = "model_files/inception_v1_224_quant.tflite" 
label_path = "model_files/labels.txt"

### Create interpreter for the specified model
interpreter = Interpreter(model_path=model_path)

### Read the label file and load all the values in an array
with open(label_path, 'r') as f:
    labels = list(map(str.strip, f.readlines()))



#print(labels)
print('\n Printing value of label at index 126:',labels[126])



### Obtain input and output details of the model.
print("\n--------Input Details of Model-------------------\n")
input_details = interpreter.get_input_details()
print(input_details)

print("\n--------Output Details of Model-------------------\n")
output_details = interpreter.get_output_details()
print(output_details)

print("\n\n")


### Obtain input size of image from input details of the model
input_shape = input_details[0]['shape']
print("shape of input: ",input_shape)
size = input_shape[1:3]
print("size of input image should be: ", size) 

print("\n--------Preprocess Image-------------------\n")

# Capturing image using mobile from IP Webcam
url = "http://192.168.43.1:8080/video"
cp = cv2.VideoCapture(url)
while(True):
    camera, frame = cp.read()
    if frame is not None:
        cv2.imshow("Frame", frame)
    q = cv2.waitKey(1)
    if q==ord("q"):
        break
cv2.destroyAllWindows()


### Fetch image & preprocess it to match the input requirements of the model
file_path = "sample_pictures/5.jpg"
img = Image.open(file_path).convert('RGB')
img = img.resize(size)
img = np.array(img)
print('value of pixel 145x223: ',img[145][223])
processed_image = np.expand_dims(img, axis=0)# Add a batch dimension
print('value of pixel 145x223:',processed_image[0][145][223])



### Now allocate tensors so that we can use the set_tensor() method to feed the processed_image
interpreter.allocate_tensors()


#print(input_details[0]['index']) ;a random image label name
interpreter.set_tensor(input_details[0]['index'], processed_image)

print("\n--------Performing Inference-------------------\n")
t1=time.time()
interpreter.invoke()
t2=time.time()
time_taken=(t2-t1)*1000 #milliseconds
print("time taken for Inference: ",str(time_taken), "ms")



### Obtain results 
predictions = interpreter.get_tensor(output_details[0]['index'])[0]

print("\n--------Processing the output-------------------\n")
print("length of array: ", len(predictions),"\n")
s=""
for i in range(len(predictions)):
    if(predictions[i]>0):
        #s = s + str(i) + "(" + str(predictions[i]) + ")"
        print("predictions["+str(i)+"]: ",predictions[i])

print("\n--------Top 5 indices (sorted)-------------------\n")
top_k = 5
top_k_indices = np.argsort(predictions)[::-1][0:top_k]
print("Sorted array of top indices:",top_k_indices)

print("\n--------scores and labels associated to top indices----------\n")
for i in range(top_k):
    score=predictions[top_k_indices[i]]/255.0
    lbl=labels[top_k_indices[i]]
    print(lbl, "=", score)


print("\n--------score and label of best match----------\n")

index_max_score=top_k_indices[0]
max_score=score=predictions[index_max_score]/255.0
max_label=labels[index_max_score]

#Get the possible closest match and its accuracy
print(max_label,": ",max_score)

perc=max_score*100
perc=float(perc)
perc=str(perc)+" %"

#Keep a track of detected image in a folder 
my_image = Image.open(file_path)
title_font = ImageFont.truetype("arial.ttf", 30)
image_editable = ImageDraw.Draw(my_image)
image_editable.text((15,15), max_label, (0, 0, 0), font=title_font)
image_editable.text((15,50), perc, (0, 0, 0), font=title_font)
my_image.save("result_pics/result.jpg")
my_image.show("result_pics/result.jpg")
