from flask_login import current_user
from depeche_house import app
import os
from PIL import Image
import secrets


#FUNCTION TO ADD UPDATED PICTURE TO FILEPATH
def save_profile_pic(uploaded_pic):
    #create new name for uploaded picture
    random_hex = secrets.token_hex(4)
    pic_name = str(current_user.username) + random_hex
    #extracting the file extension (jpg or png) 
    _, f_ext = os.path.splitext(uploaded_pic.filename)
    #creating the new filename with the last two variables
    pic_filename = pic_name + f_ext
    #creating the picture path for it to be saved
    picture_path = os.path.join(app.root_path, 'static/profile_pics', pic_filename)
    #USING PILLOW. define new image size
    output_size = (100, 100)
    #open the image saved as a variable
    i = Image.open(uploaded_pic)
    #convert to RGB as png does not support RGBA
    rgb_i = i.convert('RGB')
    #add the new dimension size to the image
    rgb_i.thumbnail(output_size)
    #saving changes
    rgb_i.save(picture_path)
    #returning the new picture which has now been added to the static folder 
    return pic_filename
