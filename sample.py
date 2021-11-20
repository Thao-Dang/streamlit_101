from numpy.core.fromnumeric import shape
import streamlit as st
import pandas as pd
import numpy as np
import cv2
import tensorflow as tf

model = tf.keras.models.load_model('model\my_model_checkpoint.h5')
model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
money_type = ['1000', '10000', '100000', '2000', '20000', '200000', '5000', '50000', '500000']
  

menu = ['home', 'about me', 'read data', 'camera', 'predict money']
choice = st.sidebar.selectbox('Menu', menu)
if choice == 'home':
    st.write('Hello')
    st.header('First webapp')
    st.image('media\dog-beach-lifesaver.png')
    col1, col2 = st.columns(2)
    with col1:
        dog_name = st.text_input('What is your dog name?')
        st.write('Your dog name:', dog_name)
    with col2:
        age = st.slider('Dog age:', min_value=1, max_value=20)
        st.write('Your dog age:', age)
elif choice == 'read data':
    df = pd.read_csv('media\AB_NYC_2019.csv')
    st.dataframe(df)
elif choice == 'about me':
    fileup = st.file_uploader('upload file', type = ['jpg', 'png', 'jpeg'])
    st.image(fileup)

elif choice == 'predict money':
    image_upload = st.file_uploader('upload file', type = ['jpg', 'png', 'jpeg'])
    if image_upload != None:
        image_np = np.asarray(bytearray(image_upload.read()),dtype = np.uint8)
        img = cv2.imdecode(image_np,1)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224,224))
        img = np.expand_dims(img, axis=0)
        prediction = model.predict(img)
        index = np.argmax(prediction[0])
        money = money_type[index]
        st.image(image_upload)
        st.write('This is:', money)
        
        



elif choice == 'camera':
    cam = cv2.VideoCapture(0) # device 0. If not work, try with 1 or 2

    if not cam.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame, 1)
        
        cv2.imshow('My App!', frame)

        key = cv2.waitKey(1) & 0xFF
        if key==ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()
    
