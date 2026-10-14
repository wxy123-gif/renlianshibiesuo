from PIL import Image
from pathlib import Path
src=Image.open(r'D:\QQ\消息\1730735716\FileRecv\MobileFile\1790453211255.jpg').convert('RGB')
img=src.crop((550,500,1080,1650)).resize((1060,2300),Image.Resampling.LANCZOS)
out=Path('_eda_work/cam_front_crop.png'); img.save(out); print(out.resolve())
