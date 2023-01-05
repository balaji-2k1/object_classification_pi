from PIL import Image, ImageFont, ImageDraw 
file_path = "sample_pictures/5.jpg"
my_image = Image.open(file_path)
# my_image = Image.open("4.jpg")
# title_font = ImageFont.truetype('playfair/playfair-font.ttf', 20)


# title_font = ImageFont.truetype("arial.ttf", 50)
# title_text = "Tiger"
# tit="100%"
# image_editable = ImageDraw.Draw(my_image)
# image_editable.text((15,15), title_text, (0, 0, 0), font=title_font)
# image_editable.text((150,15), tit, (0, 0, 0), font=title_font)
# my_image.save("result_pics/result.jpg")

perc=1*100;
perc=str(perc)
perc=perc+" %"
file_path = "sample_pictures/5.jpg"
my_image = Image.open(file_path)
title_font = ImageFont.truetype( None,30)
title_text = "tress"
image_editable = ImageDraw.Draw(my_image)
image_editable.text((15,15), title_text, (0, 0, 0), font=title_font)
image_editable.text((15,50), perc, (0, 0, 0), font=title_font)
my_image.save("result_pics/result.jpg")
my_image.show("result_pics/result.jpg")