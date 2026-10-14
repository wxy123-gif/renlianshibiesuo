# -*- coding: utf-8 -*-
import os
import runpy
base = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(base, "ESP32-cam摄像头识别.py"), run_name="__main__")