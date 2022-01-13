import imageio

reader = imageio.get_reader('C:/Users/stass/OneDrive/Desktop/Онлайн этап/13.mp4')

for frame_number, im in enumerate(reader):
    # im is numpy array
    if frame_number % 10 == 0:
        imageio.imwrite(f'frame_{frame_number}.jpg', im)