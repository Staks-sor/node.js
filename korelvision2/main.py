import sys
from streamlit import cli as stcli
import folium
from streamlit_folium import folium_static
import tempfile
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import time
import os
import json
import torch
import cv2
from stqdm import stqdm
import tkinter as tk
from tkinter import filedialog


@st.cache()
def load_model(path='models/best.pt'):
    detection_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    return detection_model


def detect_image(image, model):
    pred = model(image)
    pred_df = pred.pandas().xyxy[0].sort_values('confidence', ascending=False)
    pred_image = pred.render()[0]
    if pred_df.shape[0] > 0:
        if pred_df.confidence.iloc[0] > 0.5:
            return pred_image, pred_df.name.iloc[0]
        else:
            return pred_image, 'Авария'
    else:
        return image, 'нет аварии'




def process_video(cap, model, save=True, path_to_save='temp.mp4'):
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    stframe = st.empty()
    preds = []
    if save:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(path_to_save, fourcc, 25.0, (frame_width, frame_height))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame, pred = detect_image(frame, model)
        # st.write(pred)
        if pred != 'авария' and pred != 'нет аварии':
            if save:
                out.write(frame)
            stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            preds.append(pred)
        elif pred == 'нет аварии':
            preds.append(pred)
    cap.release()
    if save:
        out.release()
    if len(preds) > 0:
        return pd.DataFrame(preds).reset_index().groupby(0).count().sort_values('index').index[-1]
    else:
        return 'нет аварии'


def main():
    st.title('Обработка видео на наличие аварий')

    model = load_model('best.pt')

    data_type = st.radio(
        "Выберите тип данных",
        ('Директория с видео', 'Видео'))

    if data_type == 'Директория с фото':

        st.header('Обработка директории с фотографиями')
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)

        st.write('Выберите папку с фотографиями:')
        clicked = st.button('Выбор папки')

        if clicked:
            # Создать папки, в которых будут лежать обработанные фотографии

            dirname = st.text_input('Выбранная папка:', filedialog.askdirectory(master=root))
            # directory = "ProcessedImages"
            path = './ProcessedVideos'  # os.path.join(dirname, directory)
            try:
                os.mkdir(path)
            except:
                st.write('WARNING: Папка ProcessedVideos уже существует.')

            for i in ['Auto', 'Person', 'spectransport']:
                os.mkdir(os.path.join(path, i))
            # Загрузка модели
            labels = {}
            for img_path in stqdm([dirname + '\\' + x for x in os.listdir(dirname)]):
                try:
                    image = np.array(Image.open(img_path))
                    image, prediction = detect_image(image, model)
                except:
                    continue

                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                labels[img_path.split('\\')[-1]] = [prediction]

                with open('labels.json', 'w') as outfile:
                    json.dump(labels, outfile)

                for i, p in zip(
                        ['Автомобиль', 'Человек', 'Спец транспорт'],
                        ['Auto', 'Person', 'spectransport']):
                    if prediction == i:
                        path_init = os.path.join(path, p)
                        path_to_save = os.path.join(path_init, img_path.split('\\')[-1])
                        cv2.imwrite(path_to_save, np.array(image))
                        break

            st.write('Фотографии обработаны')





    elif data_type == 'Директория с видео':
        st.header('Обработка директории с видео')
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)

        st.write('Выберите папку с видео:')
        clicked = st.button('Выбор папки')

        if clicked:
            # Создать папки, в которых будут лежать обработанные фотографии

            dirname = st.text_input('Выбранная папка:', filedialog.askdirectory(master=root))
            # directory = "ProcessedImages"
            path = './ProcessedVideos'  # os.path.join(dirname, directory)
            try:
                os.mkdir(path)
            except:
                st.write('WARNING: Папка ProcessedVideos уже существует.')

            labels_video = {}
            for video_path in stqdm([dirname + '\\' + x for x in os.listdir(dirname)]):
                cap = cv2.VideoCapture(video_path)

                prediction = process_video(cap, model, save=True, path_to_save='./ProcessedVideos/' + video_path.split('\\')[-1].split('.')[0] + '.mp4')
                st.write(prediction)

                labels_video[video_path.split('\\')[-1]] = [prediction]

                with open('labels_video.json', 'w') as outfile:
                    json.dump(labels_video, outfile)

            st.write('Видео обработаны')




    elif data_type == 'Видео':
        st.header('Обработка видео')
        file = st.file_uploader('Загрузите видео')
        if file:
            st.header('Результаты распознавания')
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(file.read())
            cap = cv2.VideoCapture(tfile.name)
            pred = process_video(cap, model)
            massagedown = st.text('Видео обработано')
            st.metric('Вид', pred)
            if massagedown:
                # Создать папки, в которых будут лежать обработанные фотографии

                dirname = st.text_input('Выбранная папка:', filedialog.askdirectory(master=root))
                # directory = "ProcessedImages"
                path = './ProcessedVideos'  # os.path.join(dirname, directory)
                try:
                    os.mkdir(path)
                except:
                    st.write('WARNING: Папка ProcessedVideos уже существует.')

                labels_video = {}
                for video_path in stqdm([dirname + '\\' + x for x in os.listdir(dirname)]):
                    cap = cv2.VideoCapture(video_path)

                    prediction = process_video(cap, model, save=True, path_to_save='./ProcessedVideos/' +
                                                                                   video_path.split('\\')[-1].split(
                                                                                       '.')[0] + '.mp4')
                    st.write(prediction)

                    labels_video[video_path.split('\\')[-1]] = [prediction]

                    with open('labels_video.json', 'w') as outfile:
                        json.dump(labels_video, outfile)




if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
