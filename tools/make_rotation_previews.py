from PIL import Image
img=Image.open('face/python/img/user.1.1.jpg')
img.rotate(-90, expand=True).save('_eda_work/face_cw.jpg')
img.rotate(90, expand=True).save('_eda_work/face_ccw.jpg')
print('saved')
