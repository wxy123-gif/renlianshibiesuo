from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
src = Image.open(Path('pcb_output_bluepill/FaceDoor_BluePill_PCB_Preview.png')).convert('RGB')
# Board extents in the old preview are approximately (40,37)-(1140,940).
crop = src.crop((88, 37, 1030, 941))
canvas = Image.new('RGB', (1042, 1004), 'white')
resample = Image.Resampling.LANCZOS
fit = crop.resize((942, 904), resample)
canvas.paste(fit, (50, 65))
d = ImageDraw.Draw(canvas)
try:
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 24)
except Exception:
    font = ImageFont.load_default()
d.text((50, 18), 'FaceDoor Blue Pill - 100.0 mm x 96.52 mm', fill='black', font=font)
d.rectangle((49, 64, 992, 969), outline='black', width=2)
out = Path('pcb_output_bluepill_100x100/FaceDoor_BluePill_100x100_PCB_Preview.png')
canvas.save(out, quality=95)
canvas.save('pcb_output_bluepill_100x100/FaceDoor_BluePill_100x100_PCB.pdf', 'PDF', resolution=150.0)
print(out)
