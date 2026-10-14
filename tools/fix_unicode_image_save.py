from pathlib import Path
p=Path('face/python/ESP32摄像头人脸录入.py')
t=p.read_text(encoding='utf-8')
old='''    ok = cv2.imwrite(path, frame)
    if ok:
        print("已保存：", filename)
    else:
        print("保存失败：", filename)
    return ok
'''
new='''    try:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        Image.fromarray(rgb).save(path, quality=95)
        print("已保存：", filename)
        return True
    except Exception as exc:
        print("保存失败：", filename, exc)
        return False
'''
if old not in t:
    raise SystemExit('save_frame block not found')
t=t.replace(old,new)
t=t.replace('show_preview = True\n','show_preview = True\nframe_ready_announced = False\n')
t=t.replace('''        if auto_remaining <= 0:
            print("已收到图像，按 A 自动保存20张，或按 S 保存一张")
''','''        if not frame_ready_announced:
            print("已收到图像，按 A 自动保存20张，或按 S 保存一张")
            frame_ready_announced = True
''')
p.write_text(t,encoding='utf-8')
print('unicode save fix applied')
