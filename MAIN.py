import grain_extract
def hi(rice_type):
    img = 'image/uploaded_img/input_image.jpg'
    fd = grain_extract.grain_extract(img, rice_type)
    return fd
