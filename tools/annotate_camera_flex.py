from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

src = Image.open(r'D:\QQ\消息\1730735716\FileRecv\MobileFile\1790453222315.jpg').convert('RGB')
# Crop the camera and connector area, then enlarge for clarity.
img = src.crop((0, 650, 760, 1600)).resize((1140, 1425), Image.Resampling.LANCZOS)
d = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 42)
    small = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 34)
except Exception:
    font = ImageFont.load_default()
    small = font

# Approximate positions after crop and resize.
flex_box = (120, 330, 500, 760)
seat_box = (200, 560, 500, 920)
d.ellipse(flex_box, outline=(255, 0, 0), width=10)
d.rectangle(seat_box, outline=(0, 255, 255), width=8)
d.line((700, 230, 490, 390), fill=(255, 0, 0), width=8)
d.polygon([(490,390),(530,370),(515,420)], fill=(255,0,0))
d.line((720, 1050, 500, 810), fill=(0,255,255), width=8)
d.polygon([(500,810),(540,835),(490,855)], fill=(0,255,255))
d.text((680, 170), '这是摄像头排线/FPC软排线', fill=(255,0,0), font=font)
d.text((700, 1010), '这是白色摄像头卡座', fill=(0,180,180), font=small)
out = Path('_eda_work/camera_flex_annotated.png')
img.save(out)
print(out.resolve())
