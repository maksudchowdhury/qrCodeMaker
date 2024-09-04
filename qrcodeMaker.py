
import qrcode
import PIL
from PIL import Image, ImageDraw
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer,VerticalBarsDrawer,SquareModuleDrawer
from  qrcode.image.styles.colormasks import SolidFillColorMask


def makeQR(id):
  base_url="https://link.freightageglobal.com/fgl"+id

  #Custom function for eye styling. These create the eye masks

  def style_inner_eyes(img):
    img_size = img.size[0]
    eye_size = 70 #default
    quiet_zone = 40 #default
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((60, 60, 90, 90), fill=255) #top left eye
    draw.rectangle((img_size-90, 60, img_size-60, 90), fill=255) #top right eye
    draw.rectangle((60, img_size-90, 90, img_size-60), fill=255) #bottom left eye
    return mask

  def style_outer_eyes(img):
    img_size = img.size[0]
    eye_size = 70 #default
    quiet_zone = 40 #default
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((40, 40, 110, 110), fill=255) #top left eye
    draw.rectangle((img_size-110, 40, img_size-40, 110), fill=255) #top right eye
    draw.rectangle((40, img_size-110, 110, img_size-40), fill=255) #bottom left eye
    draw.rectangle((60, 60, 90, 90), fill=0) #top left eye
    draw.rectangle((img_size-90, 60, img_size-60, 90), fill=0) #top right eye
    draw.rectangle((60, img_size-90, 90, img_size-60), fill=0) #bottom left eye 
    return mask



  if not hasattr(PIL.Image, 'Resampling'):
    PIL.Image.Resampling = PIL.Image
  # Now PIL.Image.Resampling.BICUBIC is always recognized.


  qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)



  qr.add_data(base_url)

  qr_inner_eyes_img = qr.make_image(image_factory=StyledPilImage,
                              eye_drawer=RoundedModuleDrawer(radius_ratio=1),
                              color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(228, 1, 18)))

  qr_outer_eyes_img = qr.make_image(image_factory=StyledPilImage,
                              eye_drawer=RoundedModuleDrawer(),
                              color_mask=SolidFillColorMask(front_color=(0, 0, 0)))                            

  qr_img = qr.make_image(image_factory=StyledPilImage,
                        module_drawer=RoundedModuleDrawer(),embeded_image_path="./assets/fgl_logo_qr.png")



  inner_eye_mask = style_inner_eyes(qr_img)
  outer_eye_mask = style_outer_eyes(qr_img)
  intermediate_img = Image.composite(qr_inner_eyes_img, qr_img, inner_eye_mask)
  final_image = Image.composite(qr_outer_eyes_img, intermediate_img, outer_eye_mask)
  filepath="generated_qr/fgl"+id+".png"
  final_image.save(filepath)
  final_image