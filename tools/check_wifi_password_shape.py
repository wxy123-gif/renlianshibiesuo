import ast, re
from pathlib import Path
text=Path('face/esp32-cam/camera.py').read_text(encoding='utf-8')
pw=ast.literal_eval(re.search(r'^WIFI_PASSWORD\s*=\s*(.+)$',text,re.M).group(1))
print('password_length=',len(pw))
print('has_non_ascii=',any(ord(c)>127 for c in pw))
print('has_leading_or_trailing_space=',pw!=pw.strip())
print('contains_quote=',('"' in pw or "'" in pw))
