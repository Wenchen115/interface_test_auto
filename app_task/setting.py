# -*- coding: utf-8 -*-
# @file: setting.py  
# @time: 2021/3/16 16:53
# @author: 岩滨
import os
from interface_test_auto.settings import BASE_DIR

EXTEND_DIR = os.path.join(BASE_DIR, "app_task", "extend")
TASK_DATA = os.path.join(EXTEND_DIR, "task_data.json")
TASK_RUN = os.path.join(EXTEND_DIR, "task_run.py")
TASK_RESULTS = os.path.join(EXTEND_DIR, "task_results.xml")