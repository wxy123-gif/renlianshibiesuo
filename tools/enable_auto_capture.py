from pathlib import Path
p=Path('face/python/ESP32摄像头人脸录入.py')
t=p.read_text(encoding='utf-8')
t=t.replace('auto_remaining = 0\nlast_auto = 0.0\n','auto_remaining = 20\nlast_auto = 0.0\nauto_start_at = None\n')
t=t.replace('''        if not frame_ready_announced:
            print("已收到图像，按 A 自动保存20张，或按 S 保存一张")
            frame_ready_announced = True
''','''        if not frame_ready_announced:
            print("已收到图像，3秒后自动保存20张，请缓慢左右转动头部")
            auto_start_at = time.time() + 3
            frame_ready_announced = True
''')
t=t.replace('if auto_remaining > 0 and frame is not None and now - last_auto >= 0.5:', 'if auto_remaining > 0 and frame is not None and auto_start_at is not None and now >= auto_start_at and now - last_auto >= 0.5:')
t=t.replace('''        if save_frame(frame, index):
            index += 1
            auto_remaining -= 1
        last_auto = now
''','''        if save_frame(frame, index):
            index += 1
            auto_remaining -= 1
            if auto_remaining == 0:
                print("自动保存完成，共20张。按 Q 退出。")
        last_auto = now
''')
p.write_text(t,encoding='utf-8')
print('auto capture enabled')
