# -*- coding: utf-8 -*-
"""
用户数据存储与方案归档引擎 (JSON Persistence Engine)
特点：
1. 自动保存与自动载入：任何数值修改、锁定状态、身份、目标存储、性别均静默自动写入 user_data.json。
2. 启动时自动恢复用户最后一次的所有状态，无需手动载入。
3. 全面涵盖网购、宠物、旅游、数码、美妆、女生生理期、男生仪容等全维分类。
"""

import os
import json
from datetime import datetime

DEFAULT_DATA = {
    "version": "2.0",
    "last_modified": "",
    "active_profile": {
        "gender": "female",
        "theme": "pink",
        "identity": "职场新人（1-3年）",
        "income": "4200",
        "debt": "0",
        "target_surplus": "500",
        "social_mode": "单位代缴",
        "social_base": "3800",
        "tax_deduction": "0",
        "expenses": {
            "food": {"amount": "900", "is_locked": False, "name": "餐饮伙食"},
            "housing": {"amount": "1050", "is_locked": False, "name": "住房房租"},
            "transport": {"amount": "150", "is_locked": False, "name": "交通通勤"},
            "phone": {"amount": "60", "is_locked": False, "name": "通讯网络"},
            "health": {"amount": "40", "is_locked": False, "name": "医疗健康"},
            "period": {"amount": "60", "is_locked": False, "name": "生理护理"},
            "shop": {"amount": "280", "is_locked": False, "name": "网购消费"},
            "pet": {"amount": "120", "is_locked": False, "name": "宠物养护"},
            "travel": {"amount": "150", "is_locked": False, "name": "旅游出行"},
            "beauty": {"amount": "160", "is_locked": False, "name": "美妆护肤"},
            "clothes": {"amount": "180", "is_locked": False, "name": "穿搭鞋包"},
            "digital": {"amount": "100", "is_locked": False, "name": "数码科技"},
            "drink": {"amount": "80", "is_locked": False, "name": "茶饮轻食"},
            "sport": {"amount": "60", "is_locked": False, "name": "运动健身"},
            "fun": {"amount": "120", "is_locked": False, "name": "聚会社交"},
            "study": {"amount": "80", "is_locked": False, "name": "自我提升"},
            "insurance": {"amount": "0", "is_locked": False, "name": "商业防线"},
            "other": {"amount": "60", "is_locked": False, "name": "机动备用"}
        },
        "custom_items": []
    }
}

def get_storage_path():
    """获取数据保存路径（支持移动端沙盒与桌面运行）"""
    try:
        from kivy.app import App
        app = App.get_running_app()
        if app and hasattr(app, 'user_data_dir') and app.user_data_dir:
            p = os.path.join(app.user_data_dir, "user_data.json")
            return p
    except Exception:
        pass
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "user_data.json")

def load_user_data():
    """自动加载用户数据，不存在时初始化默认配置"""
    path = get_storage_path()
    if not os.path.exists(path):
        save_user_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "active_profile" not in data:
                data["active_profile"] = DEFAULT_DATA["active_profile"]
            return data
    except Exception as e:
        print(f"[Storage] 读取失败，使用默认配置: {e}")
        return DEFAULT_DATA.copy()

def save_user_data(data):
    """自动保存数据至本地 user_data.json 文件"""
    path = get_storage_path()
    data["last_modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        local_p = os.path.join(base_dir, "user_data.json")
        if path != local_p:
            try:
                with open(local_p, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception:
                pass
        return True
    except Exception as e:
        print(f"[Storage] 自动保存失败: {e}")
        return False
