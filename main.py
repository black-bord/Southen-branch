# -*- coding: utf-8 -*-
"""
个人智能财务精算大屏 v14.0 Pro · 全维场景化餐饮规划与深度理财诊断简报版
核心特性：
1. 场景化餐饮与聚餐智能精算器：
   - 完美适配现实生活：支持不吃早饭（快捷一键设为0）、工作日吃早餐、全月早餐设定。
   - 细化工作餐、日常晚餐、外出社交大餐（每月聚餐次数 × 人均金额）、下午茶奶茶咖啡与夜宵。
   - 提供 4 大高频场景一键预设：【不吃早餐/常规打工】【自律下厨节俭】【美食探店聚餐】【大学生食堂】。
2. 深度财务健康诊断简报：
   - S/A/B/C 四级财务健康综合评级与现金流抗风险评估。
   - 国际 50/30/20 三阶防线架构分层比对（刚需生存层、生活品质层、成长储备层）。
   - 针对餐饮占比、网购消费、宠物养护、旅游出行的个性化智能诊断指引。
   - 修正金额负号显示规范（-￥120 元），层级鲜明。
3. 全维生活画像全选（网购提权、宠物、旅游、数码、美妆、女生生理期、男生仪容）。
4. 五险一金三段胶囊按钮【单位代缴】【灵活就业】【无社保】。
5. 100% 实心 ModalCard 弹窗，杜绝任何透明透底穿透。
6. 随改随存、自动记忆恢复于 user_data.json。
"""

import os
import sys
import json
from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.core.clipboard import Clipboard
from kivy.utils import platform
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle

# 导入用户数据持久化模块
try:
    from . import storage
except Exception:
    import storage

# 模拟手机竖屏分辨率（电脑预览时）
if platform not in ("android", "ios"):
    Window.size = (400, 840)

# ==================== 全局中文字体注册 ====================
def setup_global_font():
    # 1. Windows 系统原生字库（优先规避非 ASCII 路径导致的 SDL2 C 层编码问题）
    if sys.platform == "win32":
        for p in [
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/msyh.ttf",
            "C:/Windows/Fonts/simhei.ttf",
        ]:
            if os.path.exists(p):
                try:
                    LabelBase.register(DEFAULT_FONT, p)
                    LabelBase.register("AppFont", p)
                    return p
                except Exception:
                    pass

    # 2. 本地捆绑 font.ttf
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_font = os.path.join(base_dir, "font.ttf")
    if os.path.exists(local_font):
        safe_font = local_font
        try:
            local_font.encode('ascii')
        except UnicodeEncodeError:
            import tempfile, shutil
            temp_path = os.path.join(tempfile.gettempdir(), "app_kivy_font.ttf")
            try:
                if not os.path.exists(temp_path) or os.path.getsize(temp_path) != os.path.getsize(local_font):
                    shutil.copyfile(local_font, temp_path)
                safe_font = temp_path
            except Exception:
                safe_font = local_font

        try:
            LabelBase.register(DEFAULT_FONT, safe_font)
            LabelBase.register("AppFont", safe_font)
            return safe_font
        except Exception:
            pass

    # 3. 安卓与 Linux 常见中文字体
    for p in [
        "/system/fonts/NotoSansSC-Regular.otf",
        "/system/fonts/NotoSansCJK-Regular.ttc",
        "/system/fonts/DroidSansFallback.ttf",
    ]:
        if os.path.exists(p):
            try:
                LabelBase.register(DEFAULT_FONT, p)
                LabelBase.register("AppFont", p)
                return p
            except Exception:
                pass
    return "Roboto"

FONT_PATH = setup_global_font()

# ==================== 多重主题调色系统 ====================
THEMES = {
    "light": {
        "name": "晴空",
        "bg_root": (0.95, 0.97, 1.0, 1.0),
        "bg_card": (1.0, 1.0, 1.0, 1.0),
        "bg_display": (0.88, 0.93, 1.0, 1.0),
        "bg_input": (0.94, 0.97, 1.0, 1.0),
        "bg_header": (0.12, 0.36, 0.86, 1.0),
        "text_header": (1.0, 1.0, 1.0, 1.0),
        "text_primary": (0.09, 0.14, 0.24, 1.0),
        "text_input": (0.09, 0.14, 0.24, 1.0),
        "text_secondary": (0.42, 0.50, 0.62, 1.0),
        "accent": (0.14, 0.42, 0.95, 1.0),
        "accent_male": (0.14, 0.42, 0.95, 1.0),
        "accent_female": (0.92, 0.35, 0.55, 1.0),
        "accent_surplus": (0.04, 0.66, 0.42, 1.0),
        "accent_red": (0.92, 0.25, 0.25, 1.0),
        "track_color": (0.85, 0.90, 0.96, 0.55),
        "btn_plan_bg": (0.14, 0.42, 0.95, 1.0),
        "btn_plan_fg": (1.0, 1.0, 1.0, 1.0),
        "btn_tool_bg": (0.92, 0.95, 1.0, 1.0),
        "btn_tool_fg": (0.14, 0.42, 0.95, 1.0),
        "btn_secondary_bg": (0.88, 0.92, 0.98, 1.0),
        "btn_secondary_fg": (0.09, 0.14, 0.24, 1.0),
        "btn_report_bg": (0.12, 0.36, 0.86, 1.0),
        "btn_report_fg": (1.0, 1.0, 1.0, 1.0),
        "chart_income": (0.12, 0.36, 0.86, 1.0),
        "chart_need": (0.16, 0.58, 0.82, 1.0),
        "chart_want": (0.42, 0.38, 0.80, 1.0),
        "chart_surplus": (0.06, 0.68, 0.45, 1.0),
    },
    "pink": {
        "name": "樱粉",
        "bg_root": (0.99, 0.95, 0.97, 1.0),
        "bg_card": (1.0, 1.0, 1.0, 1.0),
        "bg_display": (1.0, 0.92, 0.95, 1.0),
        "bg_input": (0.99, 0.95, 0.97, 1.0),
        "bg_header": (0.95, 0.42, 0.60, 1.0),
        "text_header": (1.0, 1.0, 1.0, 1.0),
        "text_primary": (0.35, 0.14, 0.22, 1.0),
        "text_input": (0.35, 0.14, 0.22, 1.0),
        "text_secondary": (0.65, 0.44, 0.52, 1.0),
        "accent": (0.95, 0.40, 0.58, 1.0),
        "accent_male": (0.35, 0.50, 0.72, 1.0),
        "accent_female": (0.95, 0.40, 0.58, 1.0),
        "accent_surplus": (0.90, 0.25, 0.46, 1.0),
        "accent_red": (0.95, 0.20, 0.30, 1.0),
        "track_color": (0.96, 0.88, 0.92, 0.50),
        "btn_plan_bg": (0.95, 0.40, 0.58, 1.0),
        "btn_plan_fg": (1.0, 1.0, 1.0, 1.0),
        "btn_tool_bg": (0.99, 0.92, 0.95, 1.0),
        "btn_tool_fg": (0.92, 0.32, 0.52, 1.0),
        "btn_secondary_bg": (0.96, 0.88, 0.92, 1.0),
        "btn_secondary_fg": (0.35, 0.14, 0.22, 1.0),
        "btn_report_bg": (0.95, 0.40, 0.58, 1.0),
        "btn_report_fg": (1.0, 1.0, 1.0, 1.0),
        "chart_income": (0.82, 0.28, 0.48, 1.0),
        "chart_need": (0.94, 0.46, 0.58, 1.0),
        "chart_want": (0.96, 0.65, 0.74, 1.0),
        "chart_surplus": (0.88, 0.30, 0.50, 1.0),
    },
    "warm": {
        "name": "护眼",
        "bg_root": (0.97, 0.95, 0.89, 1.0),
        "bg_card": (0.99, 0.98, 0.94, 1.0),
        "bg_display": (0.93, 0.90, 0.81, 1.0),
        "bg_input": (0.92, 0.88, 0.79, 1.0),
        "bg_header": (0.46, 0.30, 0.16, 1.0),
        "text_header": (1.0, 0.98, 0.92, 1.0),
        "text_primary": (0.24, 0.17, 0.10, 1.0),
        "text_input": (0.24, 0.17, 0.10, 1.0),
        "text_secondary": (0.48, 0.39, 0.28, 1.0),
        "accent": (0.68, 0.40, 0.15, 1.0),
        "accent_male": (0.32, 0.46, 0.66, 1.0),
        "accent_female": (0.78, 0.32, 0.42, 1.0),
        "accent_surplus": (0.22, 0.56, 0.30, 1.0),
        "accent_red": (0.85, 0.30, 0.20, 1.0),
        "track_color": (0.86, 0.82, 0.72, 0.55),
        "btn_plan_bg": (0.68, 0.40, 0.15, 1.0),
        "btn_plan_fg": (1.0, 1.0, 1.0, 1.0),
        "btn_tool_bg": (0.92, 0.88, 0.79, 1.0),
        "btn_tool_fg": (0.46, 0.30, 0.16, 1.0),
        "btn_secondary_bg": (0.88, 0.83, 0.73, 1.0),
        "btn_secondary_fg": (0.24, 0.17, 0.10, 1.0),
        "btn_report_bg": (0.68, 0.40, 0.15, 1.0),
        "btn_report_fg": (1.0, 1.0, 1.0, 1.0),
        "chart_income": (0.46, 0.30, 0.16, 1.0),
        "chart_need": (0.62, 0.42, 0.22, 1.0),
        "chart_want": (0.78, 0.56, 0.32, 1.0),
        "chart_surplus": (0.25, 0.55, 0.32, 1.0),
    },
    "dark": {
        "name": "曜石",
        "bg_root": (0.07, 0.09, 0.14, 1.0),
        "bg_card": (0.12, 0.16, 0.24, 1.0),
        "bg_display": (0.16, 0.22, 0.32, 1.0),
        "bg_input": (0.18, 0.24, 0.35, 1.0),
        "bg_header": (0.08, 0.11, 0.17, 1.0),
        "text_header": (0.94, 0.96, 1.0, 1.0),
        "text_primary": (0.94, 0.96, 0.98, 1.0),
        "text_input": (0.94, 0.96, 0.98, 1.0),
        "text_secondary": (0.60, 0.68, 0.78, 1.0),
        "accent": (0.28, 0.58, 0.98, 1.0),
        "accent_male": (0.30, 0.62, 0.98, 1.0),
        "accent_female": (0.96, 0.42, 0.62, 1.0),
        "accent_surplus": (0.10, 0.82, 0.56, 1.0),
        "accent_red": (0.95, 0.35, 0.35, 1.0),
        "track_color": (0.22, 0.28, 0.40, 0.40),
        "btn_plan_bg": (0.28, 0.58, 0.98, 1.0),
        "btn_plan_fg": (1.0, 1.0, 1.0, 1.0),
        "btn_tool_bg": (0.18, 0.24, 0.35, 1.0),
        "btn_tool_fg": (0.85, 0.90, 0.98, 1.0),
        "btn_secondary_bg": (0.20, 0.26, 0.36, 1.0),
        "btn_secondary_fg": (0.94, 0.96, 0.98, 1.0),
        "btn_report_bg": (0.28, 0.58, 0.98, 1.0),
        "btn_report_fg": (1.0, 1.0, 1.0, 1.0),
        "chart_income": (0.28, 0.58, 0.98, 1.0),
        "chart_need": (0.15, 0.72, 0.85, 1.0),
        "chart_want": (0.65, 0.40, 0.92, 1.0),
        "chart_surplus": (0.10, 0.82, 0.56, 1.0),
    }
}

# ==================== 现代微交互组件 ====================
class ModernButton(Button):
    def __init__(self, bg_color=(0.14, 0.42, 0.95, 1), radius=16, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.bg_color = list(bg_color)
        self.radius = dp(radius)
        if FONT_PATH and FONT_PATH != "Roboto":
            self.font_name = FONT_PATH
        with self.canvas.before:
            self.c_color = Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
        self.bind(pos=self._update_geom, size=self._update_geom)

    def _update_geom(self, *a):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def set_bg_color(self, color):
        self.bg_color = list(color)
        self.c_color.rgba = self.bg_color

    def set_style(self, bg_color, text_color=None):
        self.set_bg_color(bg_color)
        if text_color is not None:
            self.color = text_color

    def on_press(self):
        self.c_color.rgba = [min(1.0, c * 1.15) for c in self.bg_color[:3]] + [self.bg_color[3]]

    def on_release(self):
        self.c_color.rgba = self.bg_color


class LockBadgeButton(ModernButton):
    def __init__(self, **kwargs):
        kwargs.setdefault('text', '未锁')
        kwargs.setdefault('font_size', dp(10))
        kwargs.setdefault('radius', 12)
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('size', (dp(44), dp(24)))
        kwargs.setdefault('bg_color', (1.0, 0.92, 0.95, 1))
        super().__init__(**kwargs)
        self.is_locked = False
        self.bind(on_press=self.toggle_lock)

    def toggle_lock(self, *a):
        self.set_locked(not self.is_locked)
        app = App.get_running_app()
        if app:
            app.refresh_preview()
            app.auto_save_profile()

    def set_locked(self, locked):
        self.is_locked = bool(locked)
        self.refresh_state()

    def refresh_state(self, theme_dict=None):
        app = App.get_running_app()
        t = theme_dict or (THEMES.get(app.current_theme_key, THEMES["pink"]) if app else THEMES["pink"])
        t_name = t.get("name", "")
        if t_name in ("护眼", "暖阳"):
            if self.is_locked:
                self.text = "已锁"
                self.set_style(t["accent"], (1, 1, 1, 1))
                self.bold = True
            else:
                self.text = "未锁"
                self.set_style((0.92, 0.88, 0.79, 1.0), (0.46, 0.30, 0.16, 1.0))
                self.bold = False
        elif t_name == "曜石":
            if self.is_locked:
                self.text = "已锁"
                self.set_style(t["accent"], (1, 1, 1, 1))
                self.bold = True
            else:
                self.text = "未锁"
                self.set_style((0.18, 0.24, 0.35, 1.0), t["text_secondary"])
                self.bold = False
        elif t_name == "樱粉":
            if self.is_locked:
                self.text = "已锁"
                self.set_style(t["accent_female"], (1, 1, 1, 1))
                self.bold = True
            else:
                self.text = "未锁"
                self.set_style((1.0, 0.92, 0.95, 1.0), (0.92, 0.38, 0.58, 1.0))
                self.bold = False
        else: # 晴空 / light
            if self.is_locked:
                self.text = "已锁"
                self.set_style(t["accent"], (1, 1, 1, 1))
                self.bold = True
            else:
                self.text = "未锁"
                self.set_style((0.90, 0.94, 1.0, 1.0), (0.14, 0.42, 0.95, 1.0))
                self.bold = False


class RoundedInput(TextInput):
    """现代全圆角输入框：剔除安卓生硬方框黑线，自带圆角防溢底衬与对比度前景色保真"""
    def __init__(self, bg_color=(0.94, 0.97, 1.0, 1.0), radius=10, **kwargs):
        kwargs.setdefault('multiline', False)
        kwargs.setdefault('background_color', (0, 0, 0, 0))
        kwargs.setdefault('background_normal', '')
        kwargs.setdefault('background_active', '')
        if 'foreground_color' not in kwargs:
            kwargs['foreground_color'] = (0.09, 0.14, 0.24, 1.0)
        if 'cursor_color' not in kwargs:
            kwargs['cursor_color'] = kwargs['foreground_color']
        if FONT_PATH and FONT_PATH != "Roboto":
            kwargs.setdefault('font_name', FONT_PATH)
        super().__init__(**kwargs)
        self.bg_color = list(bg_color)
        self.radius = dp(radius)
        with self.canvas.before:
            self.c_bg = Color(*self.bg_color)
            self.rect_bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
            # 必须在 canvas.before 末尾显式绑定并恢复 foreground_color，确保 text 绘制时颜色不被背景色覆盖
            self.c_fg = Color(*self.foreground_color)
        self.bind(pos=self._update_geom, size=self._update_geom)
        self.bind(foreground_color=self._update_fg)

    def _update_geom(self, *a):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size

    def _update_fg(self, *a):
        if hasattr(self, 'c_fg'):
            self.c_fg.rgba = self.foreground_color

    def set_theme_input(self, bg_color, text_color=None):
        self.bg_color = list(bg_color)
        self.c_bg.rgba = self.bg_color
        if text_color is not None:
            self.foreground_color = text_color
            self.cursor_color = text_color
            if hasattr(self, 'c_fg'):
                self.c_fg.rgba = text_color


class SoftCard(BoxLayout):
    def __init__(self, bg_color=(1, 1, 1, 1), radius=14, auto_height=True, padding=dp(10), spacing=dp(6), **kwargs):
        super().__init__(**kwargs)
        self.padding = padding
        self.spacing = spacing
        self.orientation = "vertical"
        self.auto_height = auto_height
        if auto_height:
            self.size_hint_y = None
            self.bind(minimum_height=self.setter('height'))
        self.bg_color = list(bg_color)
        self.radius = dp(radius)
        with self.canvas.before:
            self.c_bg = Color(*self.bg_color)
            self.rect_bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size

    def set_theme_bg(self, bg_color):
        self.bg_color = list(bg_color)
        self.c_bg.rgba = self.bg_color


class ModalCard(BoxLayout):
    """实心不透明弹窗卡片：彻底根治背景透明、文字重叠穿透 Bug"""
    def __init__(self, bg_color=(1, 1, 1, 1), radius=16, padding=dp(16), spacing=dp(10), **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = padding
        self.spacing = spacing
        self.bg_color = list(bg_color)
        self.radius = dp(radius)
        with self.canvas.before:
            self.c_bg = Color(*self.bg_color)
            self.rect_bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
        self.bind(pos=self._update_geom, size=self._update_geom)

    def _update_geom(self, *a):
        self.rect_bg.pos = self.pos
        self.rect_bg.size = self.size


class DynamicLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault('halign', 'left')
        kwargs.setdefault('valign', 'top')
        if FONT_PATH and FONT_PATH != "Roboto":
            kwargs.setdefault('font_name', FONT_PATH)
        super().__init__(**kwargs)
        self.size_hint_x = 1
        self.size_hint_y = None
        self.bind(width=self._update_text_size)
        self.bind(texture_size=self._update_height)

    def _update_text_size(self, *args):
        self.text_size = (max(dp(50), self.width - dp(6)), None)

    def _update_height(self, *args):
        self.height = max(dp(22), self.texture_size[1] + dp(8))


def fmt(v):
    return f"{v:,.0f}"

# ==================== 女生专属模型 (包含生理护理与理发美发，贴合女性真实生活消费) ====================
FEMALE_ESSENTIAL = [
    ("food",      "餐饮伙食", 0.15, 0.30, "日常三餐、外卖、工作餐、日常食材采购"),
    ("housing",   "住房房租", 0.15, 0.30, "房租、水电燃气、物业、宿舍学费"),
    ("transport", "交通通勤", 0.03, 0.08, "地铁、公交、日常打车与出行"),
    ("phone",     "通讯网络", 0.01, 0.04, "手机话费、宽带网络套餐"),
    ("health",    "医疗健康", 0.01, 0.05, "常备药品、体检调理、门诊"),
    ("period",    "生理护理", 0.01, 0.04, "卫生巾/棉条、暖宫贴、经期调理专属"),
    ("hair",      "理发美发", 0.01, 0.05, "剪发打理、洗吹护理、发型造型与烫染折算"),
]

FEMALE_LIFESTYLE = [
    ("beauty",    "护肤美妆", 0.03, 0.12, "水乳精华、防晒彩妆、日常护肤"),
    ("clothes",   "穿搭鞋包", 0.04, 0.14, "应季衣物、穿搭配饰、鞋袜包包"),
    ("shop",      "网购百货", 0.03, 0.10, "日用百货、家居好物、高频网购"),
    ("drink",     "茶饮甜品", 0.01, 0.05, "奶茶果茶、咖啡轻食、下午茶烘焙"),
    ("fun",       "社交聚会", 0.02, 0.08, "闺蜜聚餐、周末探店、消遣娱乐"),
    ("travel",    "旅游度假", 0.02, 0.10, "假日出行、周边短途游、拍照打卡"),
    ("pet",       "萌宠生活", 0.00, 0.08, "猫狗主粮、宠物零食、驱虫护理"),
    ("digital",   "数码配件", 0.01, 0.05, "手机耳机、充电配件、小数码周边"),
    ("study",     "自我提升", 0.02, 0.08, "书籍充电、技能考证、兴趣培训"),
    ("other",     "机动备用", 0.01, 0.06, "临时突发、人情随礼、备用金"),
]

# ==================== 男生专属模型 (聚焦数码科技、电竞、运动、修容与社交) ====================
MALE_ESSENTIAL = [
    ("food",      "餐饮伙食", 0.18, 0.32, "日常三餐、工作餐、日常食材采购"),
    ("housing",   "住房房租", 0.15, 0.30, "房租、水电煤气、合租单间与物业"),
    ("transport", "交通通勤", 0.03, 0.08, "地铁、公交、日常通勤打车、加油"),
    ("phone",     "通讯网络", 0.01, 0.04, "手机话费、宽带网络套餐"),
    ("health",    "医疗健康", 0.01, 0.05, "常备药品、体检、跌打损伤"),
    ("groom",     "理发修容", 0.01, 0.04, "理发洗剪吹、剃须修容、男士洁面防晒"),
]

MALE_LIFESTYLE = [
    ("digital",   "数码科技", 0.04, 0.15, "电脑硬件、数码科技、外设键鼠、手机数码"),
    ("game",      "游戏电竞", 0.02, 0.08, "Steam/主机游戏、游戏氪金、影音会员"),
    ("sport",     "运动健身", 0.02, 0.08, "打球运动、运动球鞋、健身房打卡"),
    ("fun",       "聚会社交", 0.02, 0.09, "朋友聚餐、消遣宵夜、烟酒应酬"),
    ("clothes",   "穿搭鞋服", 0.03, 0.10, "运动鞋服、日常穿搭、手表配饰"),
    ("shop",      "网购日常", 0.02, 0.08, "日常日用百货、消耗品采购"),
    ("travel",    "旅游户外", 0.02, 0.10, "自驾露营、周末徒步、节假日出游"),
    ("pet",       "萌宠相伴", 0.00, 0.08, "宠物主粮、日常护理与猫狗用品"),
    ("study",     "自我提升", 0.02, 0.08, "专业书籍、技术考证、充电培训"),
    ("other",     "机动备用", 0.01, 0.06, "机动开销、临时应急、人情礼金"),
]

# 身份预设基准 (男女两套科学基准，杜绝任何默认超支赤字)
IDENTITY_PRESETS = {
    "全日制大学生": {
        "income": "1800", "social_mode": "无社保", "social_base": "0", "target_surplus": "200",
        "female_defaults": {
            "food": "800", "housing": "0", "transport": "40", "phone": "30", "health": "15",
            "period": "40", "hair": "30", "beauty": "80", "clothes": "100", "shop": "80",
            "drink": "50", "fun": "60", "travel": "50", "pet": "0", "digital": "50",
            "study": "60", "other": "40"
        },
        "male_defaults": {
            "food": "850", "housing": "0", "transport": "40", "phone": "30", "health": "15",
            "groom": "30", "digital": "80", "game": "60", "sport": "60", "fun": "80",
            "clothes": "80", "shop": "60", "travel": "50", "pet": "0", "study": "60", "other": "40"
        }
    },
    "职场新人（1-3年）": {
        "income": "4200", "social_mode": "单位代缴", "social_base": "3800", "target_surplus": "500",
        "female_defaults": {
            "food": "950", "housing": "950", "transport": "120", "phone": "50", "health": "30",
            "period": "50", "hair": "80", "beauty": "150", "clothes": "180", "shop": "150",
            "drink": "80", "fun": "120", "travel": "100", "pet": "0", "digital": "60",
            "study": "80", "other": "60"
        },
        "male_defaults": {
            "food": "1000", "housing": "950", "transport": "120", "phone": "50", "health": "30",
            "groom": "50", "digital": "150", "game": "100", "sport": "80", "fun": "150",
            "clothes": "150", "shop": "100", "travel": "100", "pet": "0", "study": "80", "other": "60"
        }
    },
    "自由职业/灵活就业": {
        "income": "6000", "social_mode": "灵活就业", "social_base": "4200", "target_surplus": "800",
        "female_defaults": {
            "food": "1200", "housing": "1300", "transport": "150", "phone": "60", "health": "50",
            "period": "60", "hair": "120", "beauty": "250", "clothes": "280", "shop": "220",
            "drink": "100", "fun": "160", "travel": "180", "pet": "0", "digital": "100",
            "study": "100", "other": "80"
        },
        "male_defaults": {
            "food": "1300", "housing": "1300", "transport": "150", "phone": "60", "health": "50",
            "groom": "80", "digital": "250", "game": "150", "sport": "120", "fun": "200",
            "clothes": "220", "shop": "150", "travel": "180", "pet": "0", "study": "100", "other": "80"
        }
    },
    "职场工薪（3-5年）": {
        "income": "8500", "social_mode": "单位代缴", "social_base": "6000", "target_surplus": "1500",
        "female_defaults": {
            "food": "1500", "housing": "1600", "transport": "220", "phone": "80", "health": "80",
            "period": "80", "hair": "180", "beauty": "400", "clothes": "450", "shop": "350",
            "drink": "150", "fun": "250", "travel": "300", "pet": "100", "digital": "150",
            "study": "150", "other": "120"
        },
        "male_defaults": {
            "food": "1600", "housing": "1600", "transport": "250", "phone": "80", "health": "80",
            "groom": "100", "digital": "400", "game": "200", "sport": "180", "fun": "350",
            "clothes": "350", "shop": "200", "travel": "300", "pet": "100", "study": "150", "other": "120"
        }
    },
    "高薪骨干（1.5万+）": {
        "income": "16000", "social_mode": "单位代缴", "social_base": "12000", "target_surplus": "3500",
        "female_defaults": {
            "food": "2200", "housing": "2800", "transport": "400", "phone": "120", "health": "150",
            "period": "120", "hair": "300", "beauty": "800", "clothes": "900", "shop": "700",
            "drink": "250", "fun": "500", "travel": "600", "pet": "200", "digital": "300",
            "study": "300", "other": "200"
        },
        "male_defaults": {
            "food": "2400", "housing": "2800", "transport": "500", "phone": "120", "health": "150",
            "groom": "200", "digital": "800", "game": "400", "sport": "350", "fun": "700",
            "clothes": "600", "shop": "400", "travel": "600", "pet": "200", "study": "300", "other": "200"
        }
    }
}

STUDENT_LOCKED_KEYS = ["housing"]

# 社保费率
SOCIAL_RATES = {
    "单位代缴": {
        "pension_p": 0.08, "medical_p": 0.02, "unemp_p": 0.005, "fund_p": 0.07,
        "pension_e": 0.16, "medical_e": 0.09, "unemp_e": 0.005, "injury_e": 0.004, "birth_e": 0.008, "fund_e": 0.07,
    },
    "灵活就业": {"pension_p": 0.20, "medical_p": 0.08, "unemp_p": 0.0, "fund_p": 0.0, "total_e": 0.0},
    "无社保": {"pension_p": 0.0, "medical_p": 0.0, "unemp_p": 0.0, "fund_p": 0.0, "total_e": 0.0}
}

TAX_BRACKETS = [
    (3000, 0.03, 0),
    (12000, 0.10, 210),
    (25000, 0.20, 1410),
    (35000, 0.25, 2660),
    (55000, 0.30, 4410),
    (80000, 0.35, 7160),
    (float('inf'), 0.45, 15160),
]

def compute_tax(taxable):
    if taxable <= 0:
        return 0.0
    for limit, rate, quick_sub in TAX_BRACKETS:
        if taxable <= limit:
            return max(0.0, taxable * rate - quick_sub)
    return 0.0

# ==================== 极简收支四柱流向图 ====================
class MiniCashflowWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(120)
        self.spacing = dp(4)

        self.bars_box = BoxLayout(orientation="horizontal", spacing=dp(8), size_hint=(1, 1))
        self.add_widget(self.bars_box)

        self.cols_def = ["到手", "刚需", "弹性", "结余"]
        self.col_widgets = []
        for name in self.cols_def:
            c_box = BoxLayout(orientation="vertical", spacing=dp(1), size_hint=(1, 1))
            lbl_top = Label(text="￥0\n0%", font_size=dp(10), bold=True, size_hint_y=None, height=dp(28))
            if FONT_PATH and FONT_PATH != "Roboto":
                lbl_top.font_name = FONT_PATH
            
            wgt_bar = Widget(size_hint=(1, 1))
            with wgt_bar.canvas:
                c_track = Color(0.85, 0.90, 0.96, 0.40)
                rect_track = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(3), dp(3), 0, 0])
                c_inst = Color(0.14, 0.42, 0.95, 1)
                rect_inst = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(3), dp(3), 0, 0])

            lbl_bot = Label(text=name, font_size=dp(11), bold=True, size_hint_y=None, height=dp(18))
            if FONT_PATH and FONT_PATH != "Roboto":
                lbl_bot.font_name = FONT_PATH
            c_box.add_widget(lbl_top)
            c_box.add_widget(wgt_bar)
            c_box.add_widget(lbl_bot)
            self.bars_box.add_widget(c_box)

            col_data = {
                "name": name, "lbl_top": lbl_top,
                "wgt_bar": wgt_bar, "c_track": c_track, "rect_track": rect_track,
                "c_inst": c_inst, "rect_inst": rect_inst, "lbl_bot": lbl_bot
            }
            self.col_widgets.append(col_data)
            wgt_bar.bind(pos=lambda *a: self.redraw(), size=lambda *a: self.redraw())

        self.data = {"takehome": 1, "essential": 0, "flexible": 0, "surplus": 0}
        self.current_theme = THEMES["light"]

    def update_data(self, takehome, essential, flexible, surplus, theme):
        self.data = {
            "takehome": takehome, "essential": essential,
            "flexible": flexible, "surplus": surplus
        }
        self.current_theme = theme
        self.redraw()

    def redraw(self, *args):
        takehome = max(1.0, self.data.get("takehome", 1.0))
        surplus_val = self.data.get("surplus", 0)
        values = [
            self.data.get("takehome", 0),
            self.data.get("essential", 0),
            self.data.get("flexible", 0),
            max(0, surplus_val)
        ]
        max_val = max(values + [1.0])
        t = self.current_theme
        txt_p = t["text_primary"]
        txt_s = t["text_secondary"]

        palette = [
            t.get("chart_income", t["accent"]),
            t.get("chart_need", (0.16, 0.58, 0.82, 1.0)),
            t.get("chart_want", (0.42, 0.38, 0.80, 1.0)),
            t.get("chart_surplus", t["accent_surplus"]) if surplus_val >= 0 else t["accent_red"]
        ]

        for col_data, val, col_color in zip(self.col_widgets, values, palette):
            pct = (val / takehome * 100) if takehome > 0 else 0
            if col_data["name"] == "结余" and surplus_val < 0:
                col_data["lbl_top"].text = f"-￥{fmt(-surplus_val)}\n赤字"
                col_data["lbl_top"].color = t["accent_red"]
            else:
                col_data["lbl_top"].text = f"￥{fmt(val)}\n{pct:.0f}%"
                col_data["lbl_top"].color = txt_p
            col_data["lbl_bot"].color = txt_s

            wb = col_data["wgt_bar"]
            if wb.height > 0 and wb.width > 0:
                bw = min(dp(28), max(dp(10), wb.width * 0.62))
                bx = wb.x + (wb.width - bw) / 2
                by = wb.y

                col_data["rect_track"].pos = (bx, by)
                col_data["rect_track"].size = (bw, wb.height)
                col_data["c_track"].rgba = t.get("track_color", (0.85, 0.90, 0.96, 0.45))

                bh = (val / max_val) * wb.height if max_val > 0 else dp(4)
                bh = max(dp(4), min(wb.height, bh))
                col_data["rect_inst"].pos = (bx, by)
                col_data["rect_inst"].size = (bw, bh)
                col_data["c_inst"].rgba = col_color


# ==================== 主应用程序 ====================
class FinancePlannerApp(App):
    def build(self):
        self.title = "个人财务规划"
        self.current_theme_key = "pink"
        self.current_gender = "female"
        self.custom_items = []
        self.expense_widgets = []
        self.active_identity = "职场新人（1-3年）"
        self.active_tab_idx = 0
        self.is_initializing = True

        # 读取持久化 JSON 数据
        self.user_data = storage.load_user_data()

        # 根布局
        self.root_layout = BoxLayout(orientation='vertical')
        with self.root_layout.canvas.before:
            self.root_bg_color = Color(*THEMES[self.current_theme_key]["bg_root"])
            self.root_bg_rect = RoundedRectangle(pos=(0, 0), size=Window.size)
        self.root_layout.bind(pos=lambda *a: self._update_root_bg(), size=lambda *a: self._update_root_bg())

        # 1. 顶部 Header 现代扁平导航条
        self.header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(46), padding=[dp(14), dp(4)])
        with self.header.canvas.before:
            self.header_bg_color = Color(*THEMES[self.current_theme_key]["bg_header"])
            self.header_bg_rect = RoundedRectangle(pos=(0, 0), size=(Window.width, dp(46)))
        self.header.bind(pos=lambda *a: self._update_header_bg(), size=lambda *a: self._update_header_bg())

        self.lbl_app_title = Label(text="个人财务规划", font_size=dp(16), bold=True,
                                   color=THEMES[self.current_theme_key]["text_header"], halign='center', valign='middle')
        self.lbl_app_title.bind(size=self.lbl_app_title.setter('text_size'))
        self.header.add_widget(self.lbl_app_title)
        self.root_layout.add_widget(self.header)

        # 2. 中间可滚动主体
        self.scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.scroll_content = BoxLayout(orientation='vertical', size_hint_y=None, padding=dp(10), spacing=dp(8))
        self.scroll_content.bind(minimum_height=self.scroll_content.setter('height'))
        self.scroll.add_widget(self.scroll_content)
        self.root_layout.add_widget(self.scroll)

        # 3. 底部现代分栏导航栏 (分三栏置底：收支算盘 / 开销细目 / 规划工具)
        self.tab_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50),
                                 padding=[dp(10), dp(6)], spacing=dp(8))
        with self.tab_bar.canvas.before:
            self.tab_bar_bg_color = Color(*THEMES[self.current_theme_key]["bg_card"])
            self.tab_bar_bg_rect = RoundedRectangle(pos=(0, 0), size=(Window.width, dp(50)), radius=[dp(14), dp(14), 0, 0])
        self.tab_bar.bind(pos=lambda *a: self._update_tab_bar_bg(), size=lambda *a: self._update_tab_bar_bg())

        self.btn_tab_overview = ModernButton(text="收支算盘", font_size=dp(12), bold=True,
                                             size_hint=(1, 1), radius=14)
        self.btn_tab_overview.bind(on_press=lambda *a: self.switch_tab(0))
        self.tab_bar.add_widget(self.btn_tab_overview)

        self.btn_tab_details = ModernButton(text="开销细目", font_size=dp(12),
                                            size_hint=(1, 1), radius=14)
        self.btn_tab_details.bind(on_press=lambda *a: self.switch_tab(1))
        self.tab_bar.add_widget(self.btn_tab_details)

        self.btn_tab_tools = ModernButton(text="规划工具", font_size=dp(12),
                                          size_hint=(1, 1), radius=14)
        self.btn_tab_tools.bind(on_press=lambda *a: self.switch_tab(2))
        self.tab_bar.add_widget(self.btn_tab_tools)

        self.root_layout.add_widget(self.tab_bar)

        # =====================================================================
        # 页面一：【收支算盘】(核心数显大屏 + 收入/还债/目标控制 + 简明四柱图)
        # =====================================================================
        self.page_overview = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
        self.page_overview.bind(minimum_height=self.page_overview.setter('height'))

        # 大号计算器核心数显大屏
        self.display_card = SoftCard(bg_color=THEMES[self.current_theme_key]["bg_display"], radius=14, padding=dp(10), spacing=dp(4))
        formula_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(38), spacing=dp(2))
        self.lbl_disp_income = Label(text="到手 ￥0", font_size=dp(13), bold=True,
                                     color=THEMES[self.current_theme_key]["accent"], halign='center', valign='middle')
        self.lbl_disp_minus_debt = Label(text="", font_size=dp(14), bold=True,
                                         color=THEMES[self.current_theme_key]["text_secondary"], size_hint_x=None, width=0)
        self.lbl_disp_debt = Label(text="", font_size=dp(13), bold=True,
                                   color=THEMES[self.current_theme_key]["accent_red"], size_hint_x=None, width=0, halign='center', valign='middle')
        self.lbl_disp_minus = Label(text="-", font_size=dp(14), bold=True,
                                    color=THEMES[self.current_theme_key]["text_secondary"], size_hint_x=None, width=dp(10))
        self.lbl_disp_exp = Label(text="支出 ￥0", font_size=dp(13), bold=True,
                                  color=THEMES[self.current_theme_key]["text_primary"], halign='center', valign='middle')
        self.lbl_disp_equal = Label(text="=", font_size=dp(14), bold=True,
                                    color=THEMES[self.current_theme_key]["text_secondary"], size_hint_x=None, width=dp(10))
        self.lbl_disp_surplus = Label(text="结余 ￥0", font_size=dp(14), bold=True,
                                      color=THEMES[self.current_theme_key]["accent_surplus"], halign='center', valign='middle')

        formula_box.add_widget(self.lbl_disp_income)
        formula_box.add_widget(self.lbl_disp_minus_debt)
        formula_box.add_widget(self.lbl_disp_debt)
        formula_box.add_widget(self.lbl_disp_minus)
        formula_box.add_widget(self.lbl_disp_exp)
        formula_box.add_widget(self.lbl_disp_equal)
        formula_box.add_widget(self.lbl_disp_surplus)
        self.display_card.add_widget(formula_box)

        self.lbl_disp_sub = Label(text="支出占比 0% | 自由结余率 0%", font_size=dp(11),
                                  color=THEMES[self.current_theme_key]["text_secondary"], size_hint_y=None, height=dp(18), halign='center')
        self.display_card.add_widget(self.lbl_disp_sub)
        self.page_overview.add_widget(self.display_card)

        # 核心交互控制卡片
        self.ctrl_card = SoftCard(bg_color=THEMES[self.current_theme_key]["bg_card"], radius=14, padding=dp(10), spacing=dp(8))

        # 第一排：月收入输入 + 性别切换双胶囊
        row1 = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36), spacing=dp(8))
        self.lbl_in_title = Label(text="税前月薪:", font_size=dp(12), color=THEMES[self.current_theme_key]["text_primary"],
                                  size_hint_x=None, width=dp(60), halign='left')
        self.lbl_in_title.bind(size=self.lbl_in_title.setter('text_size'))
        row1.add_widget(self.lbl_in_title)

        self.in_income = RoundedInput(text="4200", input_filter='float',
                                      font_size=dp(13), size_hint=(0.42, 1), padding=[dp(8), dp(8)],
                                      bg_color=THEMES[self.current_theme_key]["bg_input"],
                                      foreground_color=THEMES[self.current_theme_key]["text_primary"])
        self.in_income.bind(text=self.on_input_change)
        row1.add_widget(self.in_income)

        self.btn_male = ModernButton(text="男生版", font_size=dp(12), radius=14,
                                     size_hint=(0.28, 1), bg_color=(1, 1, 1, 1),
                                     color=THEMES[self.current_theme_key]["text_secondary"])
        self.btn_male.bind(on_press=lambda *a: self.switch_gender("male"))
        row1.add_widget(self.btn_male)

        self.btn_female = ModernButton(text="女生版", font_size=dp(12), bold=True, radius=14,
                                       size_hint=(0.28, 1), bg_color=THEMES[self.current_theme_key]["accent_female"],
                                       color=(1, 1, 1, 1))
        self.btn_female.bind(on_press=lambda *a: self.switch_gender("female"))
        row1.add_widget(self.btn_female)
        self.ctrl_card.add_widget(row1)

        # 第二排：身份选择 + 一键智能精算
        row2 = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(38), spacing=dp(8))
        self.btn_identity = ModernButton(
            text=f"{self.active_identity}  ▼",
            font_size=dp(11),
            size_hint=(0.55, 1),
            radius=14,
            bg_color=THEMES[self.current_theme_key]["bg_input"],
            color=THEMES[self.current_theme_key]["text_primary"]
        )
        self.btn_identity.bind(on_press=self.show_identity_picker)
        row2.add_widget(self.btn_identity)

        self.btn_smart_plan = ModernButton(
            text="一键智能精算",
            font_size=dp(12),
            bold=True,
            size_hint=(0.45, 1),
            radius=14,
            bg_color=THEMES[self.current_theme_key]["btn_plan_bg"],
            color=THEMES[self.current_theme_key]["btn_plan_fg"]
        )
        self.btn_smart_plan.bind(on_press=self.do_smart_plan)
        row2.add_widget(self.btn_smart_plan)
        self.ctrl_card.add_widget(row2)

        # 第三排：月还负债
        row_debt = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(32), spacing=dp(8))
        self.lbl_debt_title = Label(text="月还负债:", font_size=dp(12), color=THEMES[self.current_theme_key]["text_secondary"],
                                    size_hint_x=None, width=dp(60), halign='left')
        self.lbl_debt_title.bind(size=self.lbl_debt_title.setter('text_size'))
        row_debt.add_widget(self.lbl_debt_title)

        self.in_debt = RoundedInput(text="0", input_filter='float',
                                    font_size=dp(12), size_hint=(0.38, 1), padding=[dp(8), dp(6)],
                                    bg_color=THEMES[self.current_theme_key]["bg_input"],
                                    foreground_color=THEMES[self.current_theme_key]["text_primary"])
        self.in_debt.bind(text=self.on_input_change)
        row_debt.add_widget(self.in_debt)

        self.lbl_debt_status = Label(text="零负债 无月供压力", font_size=dp(11),
                                     color=THEMES[self.current_theme_key]["accent_surplus"],
                                     size_hint=(0.62, 1), halign='center', valign='middle')
        self.lbl_debt_status.bind(size=self.lbl_debt_status.setter('text_size'))
        row_debt.add_widget(self.lbl_debt_status)
        self.ctrl_card.add_widget(row_debt)

        # 第四排：目标储蓄
        row3 = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(32), spacing=dp(8))
        self.lbl_target_title = Label(text="目标储蓄:", font_size=dp(12), color=THEMES[self.current_theme_key]["text_secondary"],
                                      size_hint_x=None, width=dp(60), halign='left')
        self.lbl_target_title.bind(size=self.lbl_target_title.setter('text_size'))
        row3.add_widget(self.lbl_target_title)

        self.in_target_surplus = RoundedInput(text="500", input_filter='float',
                                              font_size=dp(12), size_hint=(0.38, 1), padding=[dp(8), dp(6)],
                                              bg_color=THEMES[self.current_theme_key]["bg_input"],
                                              foreground_color=THEMES[self.current_theme_key]["text_primary"])
        self.in_target_surplus.bind(text=self.on_input_change)
        row3.add_widget(self.in_target_surplus)

        self.lbl_target_status = Label(text="月度结余自由达成", font_size=dp(11),
                                       color=THEMES[self.current_theme_key]["accent_surplus"],
                                       size_hint=(0.62, 1), halign='center', valign='middle')
        self.lbl_target_status.bind(size=self.lbl_target_status.setter('text_size'))
        row3.add_widget(self.lbl_target_status)
        self.ctrl_card.add_widget(row3)

        # 第五排：建议储蓄目标提示与一键应用计算
        row4 = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(32), spacing=dp(6))
        self.lbl_sug_title = Label(text="建议目标:", font_size=dp(12), color=THEMES[self.current_theme_key]["text_secondary"],
                                   size_hint_x=None, width=dp(60), halign='left')
        self.lbl_sug_title.bind(size=self.lbl_sug_title.setter('text_size'))
        row4.add_widget(self.lbl_sug_title)

        self.lbl_sug_desc = Label(text="￥360 (黄金20%)", font_size=dp(12), bold=True,
                                  color=THEMES[self.current_theme_key]["accent"],
                                  size_hint=(0.42, 1), halign='left', valign='middle')
        self.lbl_sug_desc.bind(size=self.lbl_sug_desc.setter('text_size'))
        row4.add_widget(self.lbl_sug_desc)

        self.btn_apply_sug = ModernButton(
            text="采用建议并计算",
            font_size=dp(11),
            bold=True,
            size_hint=(0.58, 1),
            radius=14,
            bg_color=THEMES[self.current_theme_key]["btn_plan_bg"],
            color=THEMES[self.current_theme_key]["btn_plan_fg"]
        )
        self.btn_apply_sug.bind(on_press=self.apply_suggested_target)
        row4.add_widget(self.btn_apply_sug)
        self.ctrl_card.add_widget(row4)

        # 第六排：三阶储蓄比例快捷胶囊 (极简10% / 稳健20% / 进阶30%)
        row5 = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(28), spacing=dp(6))
        self.btn_ratio_10 = ModernButton(text="极简 10%: ￥180", font_size=dp(10), size_hint=(1, 1), radius=12,
                                         bg_color=THEMES[self.current_theme_key]["bg_input"],
                                         color=THEMES[self.current_theme_key]["text_primary"])
        self.btn_ratio_10.bind(on_press=lambda *a: self.apply_ratio_target(0.10))
        row5.add_widget(self.btn_ratio_10)

        self.btn_ratio_20 = ModernButton(text="黄金 20%: ￥360", font_size=dp(10), bold=True, size_hint=(1.15, 1), radius=12,
                                         bg_color=THEMES[self.current_theme_key]["bg_input"],
                                         color=THEMES[self.current_theme_key]["accent"])
        self.btn_ratio_20.bind(on_press=lambda *a: self.apply_ratio_target(0.20))
        row5.add_widget(self.btn_ratio_20)

        self.btn_ratio_30 = ModernButton(text="进阶 30%: ￥540", font_size=dp(10), size_hint=(1, 1), radius=12,
                                         bg_color=THEMES[self.current_theme_key]["bg_input"],
                                         color=THEMES[self.current_theme_key]["text_primary"])
        self.btn_ratio_30.bind(on_press=lambda *a: self.apply_ratio_target(0.30))
        row5.add_widget(self.btn_ratio_30)
        self.ctrl_card.add_widget(row5)

        self.page_overview.add_widget(self.ctrl_card)

        # 极简收支对比柱状图
        self.chart_card = SoftCard(bg_color=THEMES[self.current_theme_key]["bg_card"], radius=14, padding=dp(10), spacing=dp(4))
        self.cashflow_chart = MiniCashflowWidget()
        self.chart_card.add_widget(self.cashflow_chart)
        self.page_overview.add_widget(self.chart_card)

        # 直通细目页引导圆角大胶囊
        self.btn_jump_details = ModernButton(
            text="去配置各项支出细目 →",
            font_size=dp(12),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            radius=16,
            bg_color=THEMES[self.current_theme_key]["btn_plan_bg"],
            color=THEMES[self.current_theme_key]["btn_plan_fg"]
        )
        self.btn_jump_details.bind(on_press=lambda *a: self.switch_tab(1))
        self.page_overview.add_widget(self.btn_jump_details)

        # =====================================================================
        # 页面二：【开销细目】(分三栏：基础生存刚需 / 个性品质生活 / 机动与补充项)
        # =====================================================================
        self.page_details = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
        self.page_details.bind(minimum_height=self.page_details.setter('height'))

        # 顶部总控卡片 (总计 + 全锁/全解)
        self.details_summary_card = SoftCard(bg_color=THEMES[self.current_theme_key]["bg_card"], radius=14, padding=dp(10), spacing=dp(6))
        sum_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30), spacing=dp(6))
        self.lbl_details_summary = Label(
            text="支出总计: ￥0  |  到手: ￥0  |  结余: ￥0",
            font_size=dp(11),
            bold=True,
            color=THEMES[self.current_theme_key]["text_primary"],
            size_hint_x=1,
            halign='left',
            valign='middle'
        )
        self.lbl_details_summary.bind(size=self.lbl_details_summary.setter('text_size'))
        sum_row.add_widget(self.lbl_details_summary)

        self.btn_lock = ModernButton(text="全锁", font_size=dp(10), size_hint=(None, 1), width=dp(46), radius=12,
                                     bg_color=(1, 1, 1, 1), color=THEMES[self.current_theme_key]["accent"])
        self.btn_lock.bind(on_press=self.lock_all)
        sum_row.add_widget(self.btn_lock)

        self.btn_unlock = ModernButton(text="全解", font_size=dp(10), size_hint=(None, 1), width=dp(46), radius=12,
                                       bg_color=(1, 1, 1, 1), color=THEMES[self.current_theme_key]["accent"])
        self.btn_unlock.bind(on_press=self.unlock_all)
        sum_row.add_widget(self.btn_unlock)
        self.details_summary_card.add_widget(sum_row)
        self.page_details.add_widget(self.details_summary_card)

        # 【第一栏·基础生存刚需】
        self.card_essential = SoftCard(bg_color=THEMES[self.current_theme_key]["bg_card"], radius=14, padding=dp(10), spacing=dp(6))
        self.lbl_title_essential = Label(
            text="【第一栏·基础生存刚需】 (三餐、房租、通勤、话费、医疗等)",
            font_size=dp(12),
            bold=True,
            color=THEMES[self.current_theme_key]["accent"],
            size_hint_y=None,
            height=dp(24),
            halign='left'
        )
        self.lbl_title_essential.bind(size=self.lbl_title_essential.setter('text_size'))
        self.card_essential.add_widget(self.lbl_title_essential)

        self.box_essential = BoxLayout(orientation='vertical', spacing=dp(4), size_hint_y=None)
        self.box_essential.bind(minimum_height=self.box_essential.setter('height'))
        self.card_essential.add_widget(self.box_essential)
        self.page_details.add_widget(self.card_essential)

        # 【第二栏·个性品质生活】
        self.card_lifestyle = SoftCard(bg_color=THEMES[self.current_theme_key]["bg_card"], radius=14, padding=dp(10), spacing=dp(6))
        self.lbl_title_lifestyle = Label(
            text="【第二栏·品质生活画像】 (美妆穿搭、百货、数码、萌宠、社交等)",
            font_size=dp(12),
            bold=True,
            color=THEMES[self.current_theme_key]["accent_female"],
            size_hint_y=None,
            height=dp(24),
            halign='left'
        )
        self.lbl_title_lifestyle.bind(size=self.lbl_title_lifestyle.setter('text_size'))
        self.card_lifestyle.add_widget(self.lbl_title_lifestyle)

        self.box_lifestyle = BoxLayout(orientation='vertical', spacing=dp(4), size_hint_y=None)
        self.box_lifestyle.bind(minimum_height=self.box_lifestyle.setter('height'))
        self.card_lifestyle.add_widget(self.box_lifestyle)
        self.page_details.add_widget(self.card_lifestyle)

        # 【第三栏·机动与补充项】
        self.card_growth = SoftCard(bg_color=THEMES[self.current_theme_key]["bg_card"], radius=14, padding=dp(10), spacing=dp(6))
        self.lbl_title_growth = Label(
            text="【第三栏·机动与补充项】 (自我成长提升、机动备用金与自定义项)",
            font_size=dp(12),
            bold=True,
            color=THEMES[self.current_theme_key]["accent"],
            size_hint_y=None,
            height=dp(24),
            halign='left'
        )
        self.lbl_title_growth.bind(size=self.lbl_title_growth.setter('text_size'))
        self.card_growth.add_widget(self.lbl_title_growth)

        self.box_growth = BoxLayout(orientation='vertical', spacing=dp(4), size_hint_y=None)
        self.box_growth.bind(minimum_height=self.box_growth.setter('height'))
        self.card_growth.add_widget(self.box_growth)
        self.page_details.add_widget(self.card_growth)

        # 直通报告页引导圆角大胶囊
        self.btn_jump_tools = ModernButton(
            text="查看全维财务规划报告 →",
            font_size=dp(12),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            radius=16,
            bg_color=THEMES[self.current_theme_key]["btn_plan_bg"],
            color=THEMES[self.current_theme_key]["btn_plan_fg"]
        )
        self.btn_jump_tools.bind(on_press=lambda *a: self.switch_tab(2))
        self.page_details.add_widget(self.btn_jump_tools)

        # =====================================================================
        # 页面三：【规划工具】(全维财务报告 + 实用计算工具箱 + 界面风格直选)
        # =====================================================================
        self.page_tools = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
        self.page_tools.bind(minimum_height=self.page_tools.setter('height'))

        # 卡片 1: 全维财务规划诊断报告 (内嵌直接阅读 + 一键复制大胶囊)
        self.report_card = SoftCard(bg_color=THEMES[self.current_theme_key]["bg_card"], radius=14, padding=dp(12), spacing=dp(8))
        rpt_hdr = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(34), spacing=dp(6))
        self.lbl_title_report = Label(
            text="【全维财务规划诊断报告】",
            font_size=dp(13),
            bold=True,
            color=THEMES[self.current_theme_key]["accent"],
            size_hint_x=1,
            halign='left',
            valign='middle'
        )
        self.lbl_title_report.bind(size=self.lbl_title_report.setter('text_size'))
        rpt_hdr.add_widget(self.lbl_title_report)

        self.btn_copy_report = ModernButton(
            text="一键复制",
            font_size=dp(11),
            bold=True,
            size_hint=(None, 1),
            width=dp(80),
            radius=14,
            bg_color=THEMES[self.current_theme_key]["btn_report_bg"],
            color=THEMES[self.current_theme_key]["btn_report_fg"]
        )
        self.btn_copy_report.bind(on_press=self.copy_embedded_report)
        rpt_hdr.add_widget(self.btn_copy_report)
        self.report_card.add_widget(rpt_hdr)

        self.lbl_embedded_report = DynamicLabel(
            text="",
            font_size=dp(11),
            color=THEMES[self.current_theme_key]["text_primary"]
        )
        self.report_card.add_widget(self.lbl_embedded_report)
        self.page_tools.add_widget(self.report_card)

        # 卡片 2: 实用精算工具箱
        self.tools_box_card = SoftCard(bg_color=THEMES[self.current_theme_key]["bg_card"], radius=14, padding=dp(12), spacing=dp(8))
        self.lbl_title_tools = Label(
            text="【实用精算工具箱】",
            font_size=dp(13),
            bold=True,
            color=THEMES[self.current_theme_key]["accent"],
            size_hint_y=None,
            height=dp(24),
            halign='left'
        )
        self.lbl_title_tools.bind(size=self.lbl_title_tools.setter('text_size'))
        self.tools_box_card.add_widget(self.lbl_title_tools)

        tools_grid = BoxLayout(orientation='horizontal', spacing=dp(6), size_hint_y=None, height=dp(36))
        t = THEMES[self.current_theme_key]
        self.btn_meal = ModernButton(text="餐饮折算", font_size=dp(11), radius=14,
                                     bg_color=t["btn_tool_bg"], color=t["btn_tool_fg"])
        self.btn_meal.bind(on_press=self.show_meal_calculator)
        tools_grid.add_widget(self.btn_meal)

        self.btn_sem = ModernButton(text="学期分摊", font_size=dp(11), radius=14,
                                    bg_color=t["btn_tool_bg"], color=t["btn_tool_fg"])
        self.btn_sem.bind(on_press=self.show_semester_calculator)
        tools_grid.add_widget(self.btn_sem)

        self.btn_soc = ModernButton(text="五险一金", font_size=dp(11), radius=14,
                                    bg_color=t["btn_tool_bg"], color=t["btn_tool_fg"])
        self.btn_soc.bind(on_press=self.show_social_calculator)
        tools_grid.add_widget(self.btn_soc)

        self.btn_custom = ModernButton(text="加自定义", font_size=dp(11), radius=14,
                                       bg_color=t["btn_tool_bg"], color=t["btn_tool_fg"])
        self.btn_custom.bind(on_press=self.show_add_custom_popup)
        tools_grid.add_widget(self.btn_custom)
        self.tools_box_card.add_widget(tools_grid)
        self.page_tools.add_widget(self.tools_box_card)

        # 卡片 3: 界面主题风格直选
        self.theme_picker_card = SoftCard(bg_color=THEMES[self.current_theme_key]["bg_card"], radius=14, padding=dp(12), spacing=dp(8))
        self.lbl_title_themes = Label(
            text="【界面风格随心换】",
            font_size=dp(13),
            bold=True,
            color=THEMES[self.current_theme_key]["accent"],
            size_hint_y=None,
            height=dp(24),
            halign='left'
        )
        self.lbl_title_themes.bind(size=self.lbl_title_themes.setter('text_size'))
        self.theme_picker_card.add_widget(self.lbl_title_themes)

        theme_row = BoxLayout(orientation='horizontal', spacing=dp(6), size_hint_y=None, height=dp(36))
        self.btn_theme_light = ModernButton(text="晴空白", font_size=dp(11), radius=14, size_hint=(1, 1))
        self.btn_theme_light.bind(on_press=lambda *a: self.select_theme("light"))
        theme_row.add_widget(self.btn_theme_light)

        self.btn_theme_pink = ModernButton(text="樱粉浪漫", font_size=dp(11), radius=14, size_hint=(1, 1))
        self.btn_theme_pink.bind(on_press=lambda *a: self.select_theme("pink"))
        theme_row.add_widget(self.btn_theme_pink)

        self.btn_theme_warm = ModernButton(text="护眼暖阳", font_size=dp(11), radius=14, size_hint=(1, 1))
        self.btn_theme_warm.bind(on_press=lambda *a: self.select_theme("warm"))
        theme_row.add_widget(self.btn_theme_warm)

        self.btn_theme_dark = ModernButton(text="曜石极夜", font_size=dp(11), radius=14, size_hint=(1, 1))
        self.btn_theme_dark.bind(on_press=lambda *a: self.select_theme("dark"))
        theme_row.add_widget(self.btn_theme_dark)

        self.theme_picker_card.add_widget(theme_row)
        self.page_tools.add_widget(self.theme_picker_card)

        # 默认社保参数
        self.social_mode = "单位代缴"
        self.social_base = 3800.0
        self.tax_deduction = 0.0

        # 从 JSON 文件中自动无缝载入上一次的所有内容
        self.load_from_saved_profile()
        self.switch_tab(0)
        self.is_initializing = False

        return self.root_layout

    def switch_tab(self, tab_idx):
        self.active_tab_idx = tab_idx
        self.scroll_content.clear_widgets()
        if tab_idx == 0:
            self.scroll_content.add_widget(self.page_overview)
        elif tab_idx == 1:
            self.scroll_content.add_widget(self.page_details)
        elif tab_idx == 2:
            if hasattr(self, "lbl_embedded_report"):
                self.lbl_embedded_report.text = self.generate_report_text()
            self.scroll_content.add_widget(self.page_tools)
        self.scroll.scroll_y = 1.0
        self._update_tab_buttons()

    def _update_tab_buttons(self):
        t = THEMES[self.current_theme_key]
        theme_key = self.current_theme_key
        if theme_key == "warm":
            inactive_bg = (0.92, 0.88, 0.79, 1.0)
            inactive_fg = (0.48, 0.39, 0.28, 1.0)
        elif theme_key == "dark":
            inactive_bg = (0.18, 0.24, 0.35, 1.0)
            inactive_fg = (0.60, 0.68, 0.78, 1.0)
        elif theme_key == "pink":
            inactive_bg = (1.0, 0.94, 0.96, 1.0)
            inactive_fg = (0.65, 0.44, 0.52, 1.0)
        else:
            inactive_bg = (0.92, 0.95, 1.0, 1.0)
            inactive_fg = (0.42, 0.50, 0.62, 1.0)

        tabs = [
            (self.btn_tab_overview, 0),
            (self.btn_tab_details, 1),
            (self.btn_tab_tools, 2),
        ]
        for btn, idx in tabs:
            if self.active_tab_idx == idx:
                btn.set_style(t["accent"], (1, 1, 1, 1))
                btn.bold = True
            else:
                btn.set_style(inactive_bg, inactive_fg)
                btn.bold = False

    def _update_theme_buttons(self):
        if not hasattr(self, "btn_theme_light"):
            return
        t = THEMES[self.current_theme_key]
        theme_key = self.current_theme_key
        if theme_key == "warm":
            inactive_bg = (0.92, 0.88, 0.79, 1.0)
            inactive_fg = (0.48, 0.39, 0.28, 1.0)
        elif theme_key == "dark":
            inactive_bg = (0.18, 0.24, 0.35, 1.0)
            inactive_fg = (0.60, 0.68, 0.78, 1.0)
        elif theme_key == "pink":
            inactive_bg = (1.0, 0.94, 0.96, 1.0)
            inactive_fg = (0.65, 0.44, 0.52, 1.0)
        else:
            inactive_bg = (0.92, 0.95, 1.0, 1.0)
            inactive_fg = (0.42, 0.50, 0.62, 1.0)

        theme_btns = [
            (self.btn_theme_light, "light"),
            (self.btn_theme_pink, "pink"),
            (self.btn_theme_warm, "warm"),
            (self.btn_theme_dark, "dark"),
        ]
        for btn, k in theme_btns:
            if self.current_theme_key == k:
                btn.set_style(t["accent"], (1, 1, 1, 1))
                btn.bold = True
            else:
                btn.set_style(inactive_bg, inactive_fg)
                btn.bold = False

    def select_theme(self, theme_key):
        self.apply_theme_by_key(theme_key)
        self.auto_save_profile()

    def copy_embedded_report(self, *a):
        rpt = self.generate_report_text()
        Clipboard.copy(rpt)
        if hasattr(self, "btn_copy_report"):
            self.btn_copy_report.text = "已复制！"

    def _update_root_bg(self):
        self.root_bg_rect.pos = self.root_layout.pos
        self.root_bg_rect.size = self.root_layout.size

    def _update_header_bg(self):
        self.header_bg_rect.pos = self.header.pos
        self.header_bg_rect.size = self.header.size

    def _update_tab_bar_bg(self):
        if hasattr(self, "tab_bar_bg_rect") and hasattr(self, "tab_bar"):
            self.tab_bar_bg_rect.pos = self.tab_bar.pos
            self.tab_bar_bg_rect.size = self.tab_bar.size

    # ==================== JSON 自动保存与自动载入引擎 ====================
    def load_from_saved_profile(self):
        prof = self.user_data.get("active_profile", {})
        self.current_gender = prof.get("gender", "female")
        target_theme = prof.get("theme", ("pink" if self.current_gender == "female" else "light"))
        self.active_identity = prof.get("identity", "职场新人（1-3年）")
        self.btn_identity.text = f"{self.active_identity}  ▼"
        self.in_income.text = str(prof.get("income", "4200"))
        if hasattr(self, "in_debt"):
            self.in_debt.text = str(prof.get("debt", "0"))
        self.in_target_surplus.text = str(prof.get("target_surplus", "500"))
        self.social_mode = prof.get("social_mode", "单位代缴")
        self.social_base = float(prof.get("social_base", 3800))
        self.tax_deduction = float(prof.get("tax_deduction", 0))

        self.custom_items = []
        for ci in prof.get("custom_items", []):
            self.custom_items.append((ci["key"], ci["name"], str(ci["amount"]), 0.01, 0.08, "自定义补充项目"))

        self._build_expense_rows()
        saved_expenses = prof.get("expenses", {})
        for it in self.expense_widgets:
            if it["key"] in saved_expenses:
                edata = saved_expenses[it["key"]]
                it["txt"].text = str(edata.get("amount", "0"))
                it["lock"].set_locked(edata.get("is_locked", False))

        self.apply_theme_by_key(target_theme)

    def auto_save_profile(self):
        if self.is_initializing:
            return
        expenses_dict = {}
        for it in self.expense_widgets:
            expenses_dict[it["key"]] = {
                "name": it["name"],
                "amount": it["txt"].text.strip() or "0",
                "is_locked": it["lock"].is_locked
            }

        cust_list = []
        for key, name, d_val, lo, hi, tip in self.custom_items:
            val = d_val
            for it in self.expense_widgets:
                if it["key"] == key:
                    val = it["txt"].text.strip()
                    break
            cust_list.append({"key": key, "name": name, "amount": val, "is_locked": False})

        active_prof = {
            "gender": self.current_gender,
            "theme": self.current_theme_key,
            "identity": self.active_identity,
            "income": self.in_income.text.strip(),
            "debt": self.in_debt.text.strip() if hasattr(self, "in_debt") else "0",
            "target_surplus": self.in_target_surplus.text.strip(),
            "social_mode": self.social_mode,
            "social_base": self.social_base,
            "tax_deduction": self.tax_deduction,
            "expenses": expenses_dict,
            "custom_items": cust_list
        }
        self.user_data["active_profile"] = active_prof
        storage.save_user_data(self.user_data)

    def on_input_change(self, *a):
        self.refresh_preview()
        self.auto_save_profile()

    # ==================== 性别切换逻辑 (女生男生完全解耦定制) ====================
    def switch_gender(self, gender):
        if self.current_gender == gender:
            return
        self.current_gender = gender
        target_theme = "pink" if gender == "female" else "light"
        self.current_theme_key = target_theme

        # 1. 重新构建性别专属的开销细目列表 (男生专属/女生专属)
        self._build_expense_rows()
        self.apply_identity_defaults(self.active_identity)

        # 2. 对所有已有组件应用主题样式 (确保新生成的锁按钮与文字彻底换色)
        self.apply_theme_by_key(target_theme)

        # 3. 重新计算并持久化
        self.refresh_preview()
        self.auto_save_profile()

    # ==================== 统一主题应用系统 ====================
    def apply_theme_by_key(self, theme_key):
        self.current_theme_key = theme_key
        t = THEMES[theme_key]

        # 1. 根底色与顶栏、底栏
        self.root_bg_color.rgba = t["bg_root"]
        self.header_bg_color.rgba = t["bg_header"]
        self.lbl_app_title.color = t["text_header"]
        if hasattr(self, "tab_bar_bg_color"):
            self.tab_bar_bg_color.rgba = t["bg_card"]

        # 2. 底部三栏导航按钮
        self._update_tab_buttons()

        # 3. 页面卡片软底
        if hasattr(self, "display_card"):
            self.display_card.set_theme_bg(t["bg_display"])
        if hasattr(self, "ctrl_card"):
            self.ctrl_card.set_theme_bg(t["bg_card"])
        if hasattr(self, "chart_card"):
            self.chart_card.set_theme_bg(t["bg_card"])
        if hasattr(self, "details_summary_card"):
            self.details_summary_card.set_theme_bg(t["bg_card"])
        if hasattr(self, "card_essential"):
            self.card_essential.set_theme_bg(t["bg_card"])
        if hasattr(self, "card_lifestyle"):
            self.card_lifestyle.set_theme_bg(t["bg_card"])
        if hasattr(self, "card_growth"):
            self.card_growth.set_theme_bg(t["bg_card"])
        if hasattr(self, "report_card"):
            self.report_card.set_theme_bg(t["bg_card"])
        if hasattr(self, "tools_box_card"):
            self.tools_box_card.set_theme_bg(t["bg_card"])
        if hasattr(self, "theme_picker_card"):
            self.theme_picker_card.set_theme_bg(t["bg_card"])

        # 4. Tab 1 输入框与文字
        if hasattr(self, "lbl_in_title"):
            self.lbl_in_title.color = t["text_primary"]
        if hasattr(self, "lbl_target_title"):
            self.lbl_target_title.color = t["text_secondary"]
        if hasattr(self, "in_income"):
            self.in_income.set_theme_input(t["bg_input"], t["text_primary"])
        if hasattr(self, "in_target_surplus"):
            self.in_target_surplus.set_theme_input(t["bg_input"], t["text_primary"])

        if hasattr(self, "lbl_debt_title"):
            self.lbl_debt_title.color = t["text_secondary"]
        if hasattr(self, "in_debt"):
            self.in_debt.set_theme_input(t["bg_input"], t["text_primary"])

        # 建议储蓄元素样式
        if hasattr(self, "lbl_sug_title"):
            self.lbl_sug_title.color = t["text_secondary"]
        if hasattr(self, "lbl_sug_desc"):
            self.lbl_sug_desc.color = t["accent"]
        if hasattr(self, "btn_apply_sug"):
            self.btn_apply_sug.set_style(t["btn_plan_bg"], t["btn_plan_fg"])
        if hasattr(self, "btn_ratio_10"):
            self.btn_ratio_10.set_style(t["bg_input"], t["text_primary"])
        if hasattr(self, "btn_ratio_20"):
            self.btn_ratio_20.set_style(t["bg_input"], t["accent"])
        if hasattr(self, "btn_ratio_30"):
            self.btn_ratio_30.set_style(t["bg_input"], t["text_primary"])

        # 男女胶囊按钮高亮适配 (全主题彻底同步)
        if theme_key == "warm":
            inactive_bg = (0.92, 0.88, 0.79, 1.0)
            inactive_fg = (0.48, 0.39, 0.28, 1.0)
        elif theme_key == "dark":
            inactive_bg = (0.18, 0.24, 0.35, 1.0)
            inactive_fg = (0.60, 0.68, 0.78, 1.0)
        elif theme_key == "pink":
            inactive_bg = (1.0, 0.94, 0.96, 1.0)
            inactive_fg = (0.65, 0.44, 0.52, 1.0)
        else:
            inactive_bg = (0.92, 0.95, 1.0, 1.0)
            inactive_fg = (0.42, 0.50, 0.62, 1.0)

        if hasattr(self, "btn_male") and hasattr(self, "btn_female"):
            if self.current_gender == "male":
                self.btn_male.set_style(t["accent_male"], (1, 1, 1, 1))
                self.btn_male.bold = True
                self.btn_female.set_style(inactive_bg, inactive_fg)
                self.btn_female.bold = False
            else:
                self.btn_female.set_style(t["accent_female"], (1, 1, 1, 1))
                self.btn_female.bold = True
                self.btn_male.set_style(inactive_bg, inactive_fg)
                self.btn_male.bold = False

        if hasattr(self, "btn_identity"):
            self.btn_identity.set_style(t["bg_input"], t["text_primary"])
        if hasattr(self, "btn_smart_plan"):
            self.btn_smart_plan.set_style(t["btn_plan_bg"], t["btn_plan_fg"])
        if hasattr(self, "btn_jump_details"):
            self.btn_jump_details.set_style(t["btn_plan_bg"], t["btn_plan_fg"])

        # 5. Tab 2 细目控制与分类标题
        if hasattr(self, "lbl_details_summary"):
            self.lbl_details_summary.color = t["text_primary"]
        if hasattr(self, "btn_lock"):
            self.btn_lock.set_style(inactive_bg, t["accent"])
        if hasattr(self, "btn_unlock"):
            self.btn_unlock.set_style(inactive_bg, t["accent"])
        if hasattr(self, "lbl_title_essential"):
            self.lbl_title_essential.color = t["accent"]
        if hasattr(self, "lbl_title_lifestyle"):
            self.lbl_title_lifestyle.color = t["accent_female"] if self.current_gender == "female" else t["accent_male"]
        if hasattr(self, "lbl_title_growth"):
            self.lbl_title_growth.color = t["accent"]
        if hasattr(self, "btn_jump_tools"):
            self.btn_jump_tools.set_style(t["btn_plan_bg"], t["btn_plan_fg"])

        # 6. Tab 3 工具栏与主题切换
        if hasattr(self, "lbl_title_report"):
            self.lbl_title_report.color = t["accent"]
        if hasattr(self, "btn_copy_report"):
            self.btn_copy_report.set_style(t["btn_report_bg"], t["btn_report_fg"])
        if hasattr(self, "lbl_embedded_report"):
            self.lbl_embedded_report.color = t["text_primary"]
        if hasattr(self, "lbl_title_tools"):
            self.lbl_title_tools.color = t["accent"]
        if hasattr(self, "btn_meal"):
            self.btn_meal.set_style(t["btn_tool_bg"], t["btn_tool_fg"])
        if hasattr(self, "btn_sem"):
            self.btn_sem.set_style(t["btn_tool_bg"], t["btn_tool_fg"])
        if hasattr(self, "btn_soc"):
            self.btn_soc.set_style(t["btn_tool_bg"], t["btn_tool_fg"])
        if hasattr(self, "btn_custom"):
            self.btn_custom.set_style(t["btn_tool_bg"], t["btn_tool_fg"])
        if hasattr(self, "lbl_title_themes"):
            self.lbl_title_themes.color = t["accent"]
        self._update_theme_buttons()

        # 7. 刷新各细目行样式
        for it in self.expense_widgets:
            it["txt"].set_theme_input(t["bg_input"], t["text_primary"])
            it["lbl"].color = t["text_primary"]
            it["pct"].color = t["accent"]
            it["lock"].refresh_state(t)

        self.refresh_preview()

    def cycle_theme(self, *a):
        keys = ["light", "pink", "warm", "dark"]
        idx = (keys.index(self.current_theme_key) + 1) % len(keys)
        self.apply_theme_by_key(keys[idx])
        self.auto_save_profile()

    # ==================== 现代化身份选择弹窗 ====================
    def show_identity_picker(self, *a):
        t = THEMES[self.current_theme_key]
        content = ModalCard(bg_color=t["bg_card"], radius=16, padding=dp(16), spacing=dp(10))

        lbl_t = Label(text="选择您的当前财务身份", font_size=dp(14), bold=True,
                      size_hint_y=None, height=dp(28), color=t["accent"], halign='center')
        content.add_widget(lbl_t)

        popup = Popup(title="", separator_height=0, content=content,
                      size_hint=(0.86, 0.60), background="", background_color=(0, 0, 0, 0.65))

        for id_name in IDENTITY_PRESETS.keys():
            is_active = (id_name == self.active_identity)
            bg = t["accent"] if is_active else t["bg_input"]
            fg = (1, 1, 1, 1) if is_active else t["text_primary"]
            btn = ModernButton(text=f"{'● ' if is_active else '○ '}{id_name}",
                               font_size=dp(12), bold=is_active, radius=14,
                               size_hint_y=None, height=dp(38),
                               bg_color=bg, color=fg)
            def make_picker(name):
                def select_and_close(*e):
                    self.active_identity = name
                    self.btn_identity.text = f"{name}  ▼"
                    self.apply_identity_defaults(name)
                    self.refresh_preview()
                    self.auto_save_profile()
                    popup.dismiss()
                return select_and_close
            btn.bind(on_press=make_picker(id_name))
            content.add_widget(btn)

        btn_cancel = ModernButton(text="取消", font_size=dp(12), radius=14, size_hint_y=None, height=dp(34),
                                  bg_color=t.get("btn_secondary_bg", (0.85, 0.88, 0.92, 1)),
                                  color=t.get("btn_secondary_fg", t["text_primary"]))
        btn_cancel.bind(on_press=popup.dismiss)
        content.add_widget(btn_cancel)

        popup.open()

    # ==================== 构建全维支出行 (分批分三栏分类构建) ====================
    def _build_expense_rows(self):
        if not hasattr(self, "box_essential"):
            return
        self.box_essential.clear_widgets()
        self.box_lifestyle.clear_widgets()
        self.box_growth.clear_widgets()
        self.expense_widgets = []
        t = THEMES[self.current_theme_key]

        is_female = (self.current_gender == "female")
        ess_list = FEMALE_ESSENTIAL if is_female else MALE_ESSENTIAL
        life_list = FEMALE_LIFESTYLE if is_female else MALE_LIFESTYLE

        if is_female:
            self.lbl_title_essential.text = "【第一栏·基础生存刚需】 (三餐、房租、通勤、话费、医疗、生理个护与美发)"
            self.lbl_title_lifestyle.text = "【第二栏·女生品质生活】 (护肤美妆、穿搭鞋包、网购百货、茶饮、社交与旅行)"
        else:
            self.lbl_title_essential.text = "【第一栏·基础生存刚需】 (三餐、房租、通勤、话费、医疗与理发修容)"
            self.lbl_title_lifestyle.text = "【第二栏·男生质感生活】 (数码科技、游戏电竞、运动健身、潮流鞋服与社交)"
        self.lbl_title_growth.text = "【第三栏·机动与补充项】 (自我成长提升、机动备用金与自定义项)"

        # 第一栏：生存刚需
        for key, name, lo, hi, tip in ess_list:
            self._add_single_row(self.box_essential, key, name, "0", lo, hi, tip)

        # 第二栏：品质生活 (排除 study 和 other，这二者归入第三栏成长与机动)
        for key, name, lo, hi, tip in life_list:
            if key in ("study", "other"):
                continue
            self._add_single_row(self.box_lifestyle, key, name, "0", lo, hi, tip)

        # 第三栏：机动与补充项 (study + other + 自定义项目)
        for key, name, lo, hi, tip in life_list:
            if key in ("study", "other"):
                self._add_single_row(self.box_growth, key, name, "0", lo, hi, tip)

        if self.custom_items:
            for key, name, default_amt, lo, hi, tip in self.custom_items:
                self._add_single_row(self.box_growth, key, name, default_amt, lo, hi, tip)

    def _add_single_row(self, parent_box, key, label_name, default_amt, lo, hi, tip):
        t = THEMES[self.current_theme_key]
        row = BoxLayout(orientation='horizontal', spacing=dp(6), size_hint_y=None, height=dp(34))

        btn_lock_badge = LockBadgeButton()
        btn_lock_badge.refresh_state(t)
        row.add_widget(btn_lock_badge)

        lbl_name = Label(text=label_name, font_size=dp(12), color=t["text_primary"],
                         size_hint_x=None, width=dp(80), halign='left', valign='middle')
        lbl_name.bind(size=lbl_name.setter('text_size'))
        row.add_widget(lbl_name)

        lbl_pct = Label(text="0%", font_size=dp(11), color=t["accent"],
                        size_hint_x=None, width=dp(40), halign='right', valign='middle')
        lbl_pct.bind(size=lbl_pct.setter('text_size'))
        row.add_widget(lbl_pct)

        txt_amt = RoundedInput(text=default_amt, multiline=False, input_filter='float',
                               font_size=dp(12), size_hint=(1, 1), padding=[dp(8), dp(6)],
                               bg_color=t["bg_input"], foreground_color=t["text_primary"])
        txt_amt.bind(text=self.on_input_change)
        row.add_widget(txt_amt)

        parent_box.add_widget(row)
        self.expense_widgets.append({
            "key": key, "name": label_name, "lock": btn_lock_badge, "txt": txt_amt,
            "lbl": lbl_name, "pct": lbl_pct, "lo": lo, "hi": hi, "tip": tip
        })

    def lock_all(self, *a):
        for it in self.expense_widgets:
            it["lock"].set_locked(True)
        self.refresh_preview()
        self.auto_save_profile()

    def unlock_all(self, *a):
        for it in self.expense_widgets:
            it["lock"].set_locked(False)
        self.refresh_preview()
        self.auto_save_profile()

    # ==================== 核心计算与目标存储匹配 ====================
    def _num(self, txt_widget):
        try:
            return float(txt_widget.text.strip() or 0)
        except Exception:
            return 0.0

    def apply_identity_defaults(self, ident_name):
        if ident_name not in IDENTITY_PRESETS:
            return
        p = IDENTITY_PRESETS[ident_name]
        is_student = (ident_name == "全日制大学生")

        self.in_income.text = p["income"]
        self.in_target_surplus.text = p.get("target_surplus", "200" if is_student else "500")
        self.social_mode = p.get("social_mode", "无社保" if is_student else "单位代缴")
        self.social_base = float(p.get("social_base", 0 if is_student else 3800))

        defaults_dict = p.get("female_defaults" if self.current_gender == "female" else "male_defaults", {})

        for item in self.expense_widgets:
            default_val = defaults_dict.get(item["key"], "50")
            item["txt"].text = default_val

            if is_student and item["key"] in STUDENT_LOCKED_KEYS:
                item["lock"].set_locked(True)
                item["txt"].text = "0"
            elif not is_student:
                item["lock"].set_locked(False)

    def compute(self):
        income = self._num(self.in_income)
        mode = self.social_mode
        base = self.social_base if self.social_base > 0 else income

        rates = SOCIAL_RATES.get(mode, SOCIAL_RATES["无社保"])
        social_p = base * (rates["pension_p"] + rates["medical_p"] + rates["unemp_p"] + rates["fund_p"])
        
        if mode == "单位代缴":
            social_e = base * (rates["pension_e"] + rates["medical_e"] + rates["unemp_e"] +
                               rates["injury_e"] + rates["birth_e"] + rates["fund_e"])
        else:
            social_e = 0.0

        taxable = income - social_p - 5000.0 - self.tax_deduction
        tax = compute_tax(taxable) if mode != "无社保" and taxable > 0 else 0.0
        if mode == "无社保":
            tax = compute_tax(taxable)

        takehome = max(0.0, income - social_p - tax)
        debt = self._num(self.in_debt) if hasattr(self, "in_debt") else 0.0
        expenses = {it["key"]: self._num(it["txt"]) for it in self.expense_widgets}
        total_exp = sum(expenses.values())
        
        # 核心算式：结余 = 实发到手 - 月度还债 - 生活开销
        surplus = takehome - debt - total_exp
        surplus_rate = (surplus / takehome) if takehome > 0 else 0.0
        debt_rate = (debt / takehome) if takehome > 0 else 0.0

        essential_keys = {"housing", "food", "transport", "phone", "health", "period", "hair", "groom"}
        essential = sum(expenses.get(k, 0) for k in essential_keys)
        flexible = total_exp - essential

        target_surplus = self._num(self.in_target_surplus)

        return {
            "income": income, "debt": debt, "debt_rate": debt_rate,
            "takehome": takehome, "social_p": social_p, "social_e": social_e,
            "tax": tax, "expenses": expenses, "total_exp": total_exp, "surplus": surplus,
            "surplus_rate": surplus_rate, "essential": essential, "flexible": flexible,
            "target_surplus": target_surplus
        }

    def refresh_preview(self, *args):
        d = self.compute()
        takehome = d["takehome"]
        debt = d["debt"]
        debt_rate = d["debt_rate"]
        total_exp = d["total_exp"]
        surplus = d["surplus"]
        sr = d["surplus_rate"]
        target = d["target_surplus"]
        t = THEMES[self.current_theme_key]

        self.lbl_disp_income.text = f"到手 ￥{fmt(takehome)}"
        if debt > 0:
            self.lbl_disp_debt.text = f"还款 ￥{fmt(debt)}"
            self.lbl_disp_debt.size_hint_x = None
            self.lbl_disp_debt.width = dp(76)
            self.lbl_disp_minus_debt.text = "-"
            self.lbl_disp_minus_debt.size_hint_x = None
            self.lbl_disp_minus_debt.width = dp(10)
        else:
            self.lbl_disp_debt.text = ""
            self.lbl_disp_debt.size_hint_x = None
            self.lbl_disp_debt.width = 0
            self.lbl_disp_minus_debt.text = ""
            self.lbl_disp_minus_debt.size_hint_x = None
            self.lbl_disp_minus_debt.width = 0

        self.lbl_disp_exp.text = f"支出 ￥{fmt(total_exp)}"
        
        if surplus >= 0:
            self.lbl_disp_surplus.text = f"结余 ￥{fmt(surplus)}"
            self.lbl_disp_surplus.color = t["accent_surplus"]
            if debt > 0:
                sub_eval = f"偿债率 {debt_rate*100:.0f}% | 支出占 {total_exp/takehome*100:.0f}% | 结余率 {sr*100:.0f}%" if takehome > 0 else "请输入有效月薪"
            else:
                sub_eval = f"支出占 {total_exp/takehome*100:.0f}% | 自由结余率 {sr*100:.0f}%" if takehome > 0 else "请输入有效月薪"
        else:
            self.lbl_disp_surplus.text = f"超支 -￥{fmt(-surplus)}"
            self.lbl_disp_surplus.color = t["accent_red"]
            sub_eval = f"注意：预算超支赤字 ￥{fmt(-surplus)}"

        self.lbl_disp_sub.text = sub_eval

        # 动态负债状态提示 (温和柔性，不生硬)
        if hasattr(self, "lbl_debt_status"):
            if debt <= 0:
                self.lbl_debt_status.text = "零负债 无月供压力"
                self.lbl_debt_status.color = t["accent_surplus"]
            elif takehome <= 0:
                self.lbl_debt_status.text = f"月还款 ￥{fmt(debt)}"
                self.lbl_debt_status.color = t["accent_red"]
            elif debt_rate <= 0.20:
                self.lbl_debt_status.text = f"偿债率 {debt_rate*100:.0f}%·负债压力轻微"
                self.lbl_debt_status.color = t["accent_surplus"]
            elif debt_rate <= 0.40:
                self.lbl_debt_status.text = f"偿债率 {debt_rate*100:.0f}%·月供适中可控"
                self.lbl_debt_status.color = t["accent"]
            elif debt_rate <= 0.60:
                self.lbl_debt_status.text = f"偿债率 {debt_rate*100:.0f}%·负债偏重 建议优先还款"
                self.lbl_debt_status.color = t["accent_red"]
            else:
                self.lbl_debt_status.text = f"偿债率 {debt_rate*100:.0f}%·高负债预警 需严控开支"
                self.lbl_debt_status.color = t["accent_red"]

        if target > 0:
            if surplus >= target:
                self.lbl_target_status.text = f"达成目标！达标率 {surplus/target*100:.0f}%"
                self.lbl_target_status.color = t["accent_surplus"]
            else:
                gap = target - surplus
                self.lbl_target_status.text = f"还差 ￥{fmt(gap)} 达成储蓄目标"
                self.lbl_target_status.color = t["accent_red"]
        else:
            self.lbl_target_status.text = "自由结余，无硬性储蓄指标"
            self.lbl_target_status.color = t["text_secondary"]

        for it in self.expense_widgets:
            amt = self._num(it["txt"])
            pct = (amt / takehome * 100) if takehome > 0 else 0
            it["pct"].text = f"{pct:.0f}%"

        # 实时测算建议储蓄目标 (基于扣除欠款还款后的净可支配额)
        disposable = max(0.0, takehome - debt)
        sug_20 = int(max(0.0, round(disposable * 0.20 / 10) * 10)) if disposable > 0 else 0
        sug_10 = int(max(0.0, round(disposable * 0.10 / 10) * 10)) if disposable > 0 else 0
        sug_30 = int(max(0.0, round(disposable * 0.30 / 10) * 10)) if disposable > 0 else 0
        if hasattr(self, "lbl_sug_desc"):
            self.lbl_sug_desc.text = f"￥{fmt(sug_20)} (黄金20%)"
        if hasattr(self, "btn_ratio_10"):
            self.btn_ratio_10.text = f"极简 10%: ￥{fmt(sug_10)}"
        if hasattr(self, "btn_ratio_20"):
            self.btn_ratio_20.text = f"黄金 20%: ￥{fmt(sug_20)}"
        if hasattr(self, "btn_ratio_30"):
            self.btn_ratio_30.text = f"进阶 30%: ￥{fmt(sug_30)}"

        if hasattr(self, "cashflow_chart"):
            self.cashflow_chart.update_data(takehome, d["essential"], d["flexible"], surplus, t)

        if hasattr(self, "lbl_details_summary"):
            self.lbl_details_summary.text = f"总支出: ￥{fmt(total_exp)}  |  到手: ￥{fmt(takehome)}  |  结余: ￥{fmt(surplus)}"

        if hasattr(self, "lbl_embedded_report") and getattr(self, "active_tab_idx", 0) == 2:
            self.lbl_embedded_report.text = self.generate_report_text()

    def apply_suggested_target(self, *a):
        d = self.compute()
        disposable = max(0.0, d["takehome"] - d["debt"])
        sug_20 = int(max(0.0, round(disposable * 0.20 / 10) * 10)) if disposable > 0 else 0
        self.in_target_surplus.text = str(sug_20)
        self.do_smart_plan()
        self.refresh_preview()
        self.auto_save_profile()

    def apply_ratio_target(self, ratio):
        d = self.compute()
        disposable = max(0.0, d["takehome"] - d["debt"])
        sug_val = int(max(0.0, round(disposable * ratio / 10) * 10)) if disposable > 0 else 0
        self.in_target_surplus.text = str(sug_val)
        self.do_smart_plan()
        self.refresh_preview()
        self.auto_save_profile()

    # ==================== 国际文献经学算法 (锁定项动态重平衡 + 恩格尔阶梯消费弹性) ====================
    def do_smart_plan(self, *args):
        d = self.compute()
        takehome = d["takehome"]
        debt = d["debt"]
        if takehome <= 0:
            return

        unlocked_items = [it for it in self.expense_widgets if not it["lock"].is_locked]
        if not unlocked_items:
            return

        locked_sum = sum(self._num(it["txt"]) for it in self.expense_widgets if it["lock"].is_locked)
        # 必须先保障还债，剩余部分才是可用于生活消费的资金池
        disposable = max(0.0, takehome - debt)
        available = max(0.0, disposable - locked_sum)

        ident = self.active_identity
        is_student = (ident == "全日制大学生")
        target_save = d["target_surplus"]

        if target_save > 0 and target_save < available:
            target_spend = available - target_save
        elif is_student:
            target_spend = available * 0.95
        elif disposable <= 5000:
            target_spend = available * 0.86
        elif disposable <= 10000:
            target_spend = available * 0.78
        else:
            target_spend = available * 0.68

        if self.current_gender == "female":
            base_weights = {
                "food": 0.22, "housing": 0.20, "transport": 0.04, "phone": 0.02, "health": 0.03,
                "period": 0.03, "hair": 0.03,
                "beauty": 0.09, "clothes": 0.09, "shop": 0.08, "drink": 0.04,
                "fun": 0.04, "travel": 0.05, "pet": 0.02, "digital": 0.02,
                "study": 0.04, "other": 0.02
            }
        else:
            base_weights = {
                "food": 0.23, "housing": 0.20, "transport": 0.04, "phone": 0.02, "health": 0.03,
                "groom": 0.03,
                "digital": 0.08, "game": 0.06, "sport": 0.06, "fun": 0.06,
                "clothes": 0.06, "shop": 0.05, "travel": 0.05, "pet": 0.02,
                "study": 0.04, "other": 0.02
            }

        housing_locked_val = None
        for it in self.expense_widgets:
            if it["key"] == "housing" and it["lock"].is_locked:
                housing_locked_val = self._num(it["txt"])
                break

        weights = {}
        for it in unlocked_items:
            k = it["key"]
            w = base_weights.get(k, 0.04)

            if takehome >= 8000:
                if k in ("travel", "shop", "pet", "study", "digital", "beauty", "clothes", "game"):
                    w *= 1.35
                elif k in ("food", "phone"):
                    w *= 0.85

            if housing_locked_val is not None and housing_locked_val == 0:
                if k in ("shop", "travel", "study", "pet", "beauty", "game"):
                    w *= 1.40

            weights[k] = max(0.005, w)

        total_weight = sum(weights.values())
        if total_weight <= 0:
            return

        for it in unlocked_items:
            k = it["key"]
            alloc = target_spend * (weights[k] / total_weight)
            final_alloc = max(0, int(round(alloc / 10.0) * 10))
            it["txt"].text = str(final_alloc)

        self.refresh_preview()
        self.auto_save_profile()

    # ==================== 场景化餐饮与聚餐智能精算器 (支持不吃早餐、聚餐规划等) ====================
    def show_meal_calculator(self, *a):
        t = THEMES[self.current_theme_key]
        content = ModalCard(bg_color=t["bg_card"], radius=16, padding=dp(16), spacing=dp(8))

        lbl_title = Label(text="场景化餐饮与聚餐智能精算器", font_size=dp(14), bold=True,
                          size_hint_y=None, height=dp(26), color=t["accent"], halign='center')
        content.add_widget(lbl_title)

        # 1. 快捷场景预设栏 (包含不吃早餐等年轻族群真实画像)
        lbl_pre_tip = Label(text="快捷场景一键填入：", font_size=dp(10), color=t["text_secondary"],
                            size_hint_y=None, height=dp(18), halign='left')
        lbl_pre_tip.bind(size=lbl_pre_tip.setter('text_size'))
        content.add_widget(lbl_pre_tip)

        pre_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(28), spacing=dp(4))
        content.add_widget(pre_box)

        # 滚动区域放置细分项目
        sv = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        form_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(6))
        form_box.bind(minimum_height=form_box.setter('height'))

        inputs = {}
        def add_form_row(k, title, default_val, placeholder):
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(32), spacing=dp(6))
            l = Label(text=title, font_size=dp(11), color=t["text_primary"], size_hint_x=0.62, halign='left')
            l.bind(size=l.setter('text_size'))
            ti = RoundedInput(text=default_val, multiline=False, input_filter='float', font_size=dp(11),
                              size_hint_x=0.38, padding=[dp(6), dp(6)],
                              bg_color=t["bg_input"], foreground_color=t["text_primary"])
            row.add_widget(l)
            row.add_widget(ti)
            form_box.add_widget(row)
            inputs[k] = ti

        # 早餐规划 (支持不吃早餐设为0)
        lbl_sec1 = Label(text="【早餐规划】(不吃早饭设为0天或0元)", font_size=dp(10), bold=True,
                         size_hint_y=None, height=dp(18), color=t["accent"], halign='left')
        lbl_sec1.bind(size=lbl_sec1.setter('text_size'))
        form_box.add_widget(lbl_sec1)
        add_form_row("b_cost", "早餐单价 (元/顿):", "8", "8")
        add_form_row("b_days", "每月吃早餐天数 (天/月):", "22", "22")

        # 工作日午餐与晚饭
        lbl_sec2 = Label(text="【日常工作餐与晚餐】", font_size=dp(10), bold=True,
                         size_hint_y=None, height=dp(18), color=t["accent"], halign='left')
        lbl_sec2.bind(size=lbl_sec2.setter('text_size'))
        form_box.add_widget(lbl_sec2)
        add_form_row("lunch", "工作日午餐 (日均元):", "20", "20")
        add_form_row("dinner", "日常晚饭 (日均元):", "18", "18")

        # 外出社交大餐与聚会 (用户核心关切)
        lbl_sec3 = Label(text="【外出社交大餐与聚会】", font_size=dp(10), bold=True,
                         size_hint_y=None, height=dp(18), color=t["accent"], halign='left')
        lbl_sec3.bind(size=lbl_sec3.setter('text_size'))
        form_box.add_widget(lbl_sec3)
        add_form_row("gather_count", "每月聚餐次数 (次/月):", "2", "2")
        add_form_row("gather_avg", "聚餐单次人均 (元/次):", "120", "120")

        # 下午茶咖啡与夜宵
        lbl_sec4 = Label(text="【下午茶咖啡与夜宵】", font_size=dp(10), bold=True,
                         size_hint_y=None, height=dp(18), color=t["accent"], halign='left')
        lbl_sec4.bind(size=lbl_sec4.setter('text_size'))
        form_box.add_widget(lbl_sec4)
        add_form_row("tea_snack", "月度茶饮夜宵预算 (元/月):", "80", "80")

        sv.add_widget(form_box)
        content.add_widget(sv)

        # 实时分类明细与总金额展示
        lbl_detail = Label(text="日常三餐: ￥0  |  社交聚餐: ￥0  |  茶饮: ￥0", font_size=dp(10),
                           color=t["text_secondary"], size_hint_y=None, height=dp(18), halign='center')
        content.add_widget(lbl_detail)

        lbl_total = Label(text="月度折算餐饮总额: ￥0", font_size=dp(13), bold=True,
                          size_hint_y=None, height=dp(26), color=t["accent_surplus"], halign='center')
        content.add_widget(lbl_total)

        def calc_meal(*e):
            try:
                b_c = float(inputs["b_cost"].text or 0)
                b_d = float(inputs["b_days"].text or 0)
                b_tot = b_c * b_d

                l_c = float(inputs["lunch"].text or 0)
                d_c = float(inputs["dinner"].text or 0)
                # 按照 30 天计算常态午晚饭
                ld_tot = (l_c + d_c) * 30

                g_cnt = float(inputs["gather_count"].text or 0)
                g_avg = float(inputs["gather_avg"].text or 0)
                gather_tot = g_cnt * g_avg

                tea_tot = float(inputs["tea_snack"].text or 0)

                m_tot = b_tot + ld_tot + gather_tot + tea_tot
                lbl_detail.text = f"日常三餐: ￥{fmt(b_tot + ld_tot)} | 聚餐({fmt(g_cnt)}次): ￥{fmt(gather_tot)} | 茶饮夜宵: ￥{fmt(tea_tot)}"
                lbl_total.text = f"月度折算餐饮总额: ￥{fmt(m_tot)}"
                return m_tot
            except Exception:
                return 0.0

        for ti in inputs.values():
            ti.bind(text=calc_meal)

        # 4 个场景快捷按钮动作
        def set_preset_vals(bc, bd, lc, dc, gc, ga, ts):
            inputs["b_cost"].text = str(bc)
            inputs["b_days"].text = str(bd)
            inputs["lunch"].text = str(lc)
            inputs["dinner"].text = str(dc)
            inputs["gather_count"].text = str(gc)
            inputs["gather_avg"].text = str(ga)
            inputs["tea_snack"].text = str(ts)
            calc_meal()

        p_defs = [
            ("不吃早餐/打工", lambda *a: set_preset_vals(0, 0, 22, 18, 2, 120, 80)),
            ("节俭下厨",     lambda *a: set_preset_vals(5, 22, 15, 12, 1, 100, 30)),
            ("聚餐探店",     lambda *a: set_preset_vals(8, 30, 25, 20, 4, 150, 150)),
            ("学生食堂",     lambda *a: set_preset_vals(5, 30, 12, 12, 2, 80, 40)),
        ]
        for p_title, p_func in p_defs:
            pb = ModernButton(text=p_title, font_size=dp(9), size_hint=(1, 1), radius=12,
                              bg_color=t["bg_input"], color=t["text_primary"])
            pb.bind(on_press=p_func)
            pre_box.add_widget(pb)

        calc_meal()

        btn_bar = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(10))
        btn_apply = ModernButton(text="同步填入餐饮开销", font_size=dp(12), bold=True, radius=14,
                                 bg_color=t["btn_plan_bg"], color=t["btn_plan_fg"])
        btn_close = ModernButton(text="关闭", font_size=dp(12), radius=14,
                                 bg_color=t.get("btn_secondary_bg", (0.85, 0.88, 0.92, 1)),
                                 color=t.get("btn_secondary_fg", t["text_primary"]))

        popup = Popup(title="", separator_height=0, content=content,
                      size_hint=(0.92, 0.88), background="", background_color=(0, 0, 0, 0.65))

        def apply_and_close(*e):
            val = calc_meal()
            for it in self.expense_widgets:
                if it["key"] == "food":
                    it["txt"].text = str(int(round(val)))
                    break
            self.refresh_preview()
            self.auto_save_profile()
            popup.dismiss()

        btn_apply.bind(on_press=apply_and_close)
        btn_close.bind(on_press=popup.dismiss)
        btn_bar.add_widget(btn_apply)
        btn_bar.add_widget(btn_close)
        content.add_widget(btn_bar)

        popup.open()

    def show_semester_calculator(self, *a):
        t = THEMES[self.current_theme_key]
        content = ModalCard(bg_color=t["bg_card"], radius=16, padding=dp(16), spacing=dp(8))

        lbl_title = Label(text="大学学期平摊精算 (月度折算)", font_size=dp(14), bold=True,
                          size_hint_y=None, height=dp(28), color=t["accent"], halign='center')
        content.add_widget(lbl_title)

        inputs = {}
        fields = [
            ("tuition", "学期总学杂费 (元):", "5000"),
            ("months",  "学期预计月数 (月):", "5"),
            ("support", "每月家庭资助 (元):", "1800"),
        ]

        for k, name, d_val in fields:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(32), spacing=dp(6))
            l = Label(text=name, font_size=dp(12), color=t["text_primary"], size_hint_x=0.6, halign='left')
            l.bind(size=l.setter('text_size'))
            ti = RoundedInput(text=d_val, multiline=False, input_filter='float', font_size=dp(12),
                              size_hint_x=0.4, bg_color=t["bg_input"], foreground_color=t["text_primary"])
            row.add_widget(l)
            row.add_widget(ti)
            content.add_widget(row)
            inputs[k] = ti

        lbl_result = Label(text="每月平摊预算: ￥0", font_size=dp(13), bold=True,
                           size_hint_y=None, height=dp(28), color=t["accent_surplus"], halign='center')
        content.add_widget(lbl_result)

        def calc_sem(*e):
            try:
                tui = float(inputs["tuition"].text or 0)
                m = max(1.0, float(inputs["months"].text or 1))
                sup = float(inputs["support"].text or 0)
                m_cost = tui / m
                lbl_result.text = f"月均学杂费: ￥{fmt(m_cost)} | 建议月支配: ￥{fmt(sup)}"
                return sup
            except Exception:
                return 0.0

        for ti in inputs.values():
            ti.bind(text=calc_sem)
        calc_sem()

        btn_bar = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(10))
        btn_apply = ModernButton(text="同步填入", font_size=dp(12), bold=True, radius=14,
                                 bg_color=t["btn_plan_bg"], color=t["btn_plan_fg"])
        btn_close = ModernButton(text="关闭", font_size=dp(12), radius=14,
                                 bg_color=t.get("btn_secondary_bg", (0.85, 0.88, 0.92, 1)),
                                 color=t.get("btn_secondary_fg", t["text_primary"]))

        popup = Popup(title="", separator_height=0, content=content,
                      size_hint=(0.88, 0.58), background="", background_color=(0, 0, 0, 0.65))

        def apply_and_close(*e):
            sup = calc_sem()
            self.in_income.text = str(int(round(sup)))
            self.refresh_preview()
            self.auto_save_profile()
            popup.dismiss()

        btn_apply.bind(on_press=apply_and_close)
        btn_close.bind(on_press=popup.dismiss)
        btn_bar.add_widget(btn_apply)
        btn_bar.add_widget(btn_close)
        content.add_widget(btn_bar)

        popup.open()

    def show_social_calculator(self, *a):
        t = THEMES[self.current_theme_key]
        content = ModalCard(bg_color=t["bg_card"], radius=16, padding=dp(16), spacing=dp(10))

        lbl_title = Label(text="五险一金实发税后精算", font_size=dp(14), bold=True,
                          size_hint_y=None, height=dp(28), color=t["accent"], halign='center')
        content.add_widget(lbl_title)

        lbl_m_tip = Label(text="选择参保缴纳模式：", font_size=dp(11), color=t["text_secondary"],
                          size_hint_y=None, height=dp(20), halign='left')
        lbl_m_tip.bind(size=lbl_m_tip.setter('text_size'))
        content.add_widget(lbl_m_tip)

        mode_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(34), spacing=dp(6))
        modes = ["单位代缴", "灵活就业", "无社保"]
        mode_buttons = {}

        selected_mode = {"val": self.social_mode}

        def update_mode_buttons():
            for m_key, btn_obj in mode_buttons.items():
                if m_key == selected_mode["val"]:
                    btn_obj.set_style(t["accent"], (1, 1, 1, 1))
                    btn_obj.bold = True
                else:
                    unselected_bg = t["bg_input"]
                    btn_obj.set_style(unselected_bg, t["text_primary"])
                    btn_obj.bold = False

        for m_name in modes:
            b = ModernButton(text=m_name, font_size=dp(11), size_hint=(1, 1), radius=14)
            def make_handler(m):
                def on_click(*e):
                    selected_mode["val"] = m
                    update_mode_buttons()
                return on_click
            b.bind(on_press=make_handler(m_name))
            mode_box.add_widget(b)
            mode_buttons[m_name] = b

        update_mode_buttons()
        content.add_widget(mode_box)

        row_base = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(6))
        lbl_b = Label(text="社保基数:", font_size=dp(12), color=t["text_primary"], size_hint_x=0.4, halign='left')
        lbl_b.bind(size=lbl_b.setter('text_size'))
        ti_base = RoundedInput(text=str(int(self.social_base)), multiline=False, input_filter='float',
                               font_size=dp(12), size_hint_x=0.6, bg_color=t["bg_input"], foreground_color=t["text_primary"])
        row_base.add_widget(lbl_b)
        row_base.add_widget(ti_base)
        content.add_widget(row_base)

        row_tax = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(6))
        lbl_t = Label(text="附加扣除:", font_size=dp(12), color=t["text_primary"], size_hint_x=0.4, halign='left')
        lbl_t.bind(size=lbl_t.setter('text_size'))
        ti_tax = RoundedInput(text=str(int(self.tax_deduction)), multiline=False, input_filter='float',
                              font_size=dp(12), size_hint_x=0.6, bg_color=t["bg_input"], foreground_color=t["text_primary"])
        row_tax.add_widget(lbl_t)
        row_tax.add_widget(ti_tax)
        content.add_widget(row_tax)

        btn_bar = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(10))
        btn_apply = ModernButton(text="保存更新", font_size=dp(12), bold=True, radius=14,
                                 bg_color=t["btn_plan_bg"], color=t["btn_plan_fg"])
        btn_close = ModernButton(text="关闭", font_size=dp(12), radius=14,
                                 bg_color=t.get("btn_secondary_bg", (0.85, 0.88, 0.92, 1)),
                                 color=t.get("btn_secondary_fg", t["text_primary"]))

        popup = Popup(title="", separator_height=0, content=content,
                      size_hint=(0.88, 0.60), background="", background_color=(0, 0, 0, 0.65))

        def save_and_close(*e):
            self.social_mode = selected_mode["val"]
            self.social_base = float(ti_base.text or 0)
            self.tax_deduction = float(ti_tax.text or 0)
            self.refresh_preview()
            self.auto_save_profile()
            popup.dismiss()

        btn_apply.bind(on_press=save_and_close)
        btn_close.bind(on_press=popup.dismiss)
        btn_bar.add_widget(btn_apply)
        btn_bar.add_widget(btn_close)
        content.add_widget(btn_bar)

        popup.open()

    def show_add_custom_popup(self, *a):
        t = THEMES[self.current_theme_key]
        content = ModalCard(bg_color=t["bg_card"], radius=16, padding=dp(16), spacing=dp(10))

        lbl_title = Label(text="添加自定义预算项", font_size=dp(14), bold=True,
                          size_hint_y=None, height=dp(28), color=t["accent"], halign='center')
        content.add_widget(lbl_title)

        row_name = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(6))
        lbl_n = Label(text="项目名称:", font_size=dp(12), color=t["text_primary"], size_hint_x=0.35, halign='left')
        lbl_n.bind(size=lbl_n.setter('text_size'))
        ti_name = RoundedInput(text="兴趣特长", multiline=False, font_size=dp(12),
                               size_hint_x=0.65, bg_color=t["bg_input"], foreground_color=t["text_primary"])
        row_name.add_widget(lbl_n)
        row_name.add_widget(ti_name)
        content.add_widget(row_name)

        row_val = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(6))
        lbl_v = Label(text="每月预算:", font_size=dp(12), color=t["text_primary"], size_hint_x=0.35, halign='left')
        lbl_v.bind(size=lbl_v.setter('text_size'))
        ti_val = RoundedInput(text="200", multiline=False, input_filter='float', font_size=dp(12),
                              size_hint_x=0.65, bg_color=t["bg_input"], foreground_color=t["text_primary"])
        row_val.add_widget(lbl_v)
        row_val.add_widget(ti_val)
        content.add_widget(row_val)

        btn_bar = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(10))
        btn_add = ModernButton(text="确认添加", font_size=dp(12), bold=True, radius=14,
                               bg_color=t["btn_plan_bg"], color=t["btn_plan_fg"])
        btn_close = ModernButton(text="取消", font_size=dp(12), radius=14,
                                 bg_color=t.get("btn_secondary_bg", (0.85, 0.88, 0.92, 1)),
                                 color=t.get("btn_secondary_fg", t["text_primary"]))

        popup = Popup(title="", separator_height=0, content=content,
                      size_hint=(0.85, 0.52), background="", background_color=(0, 0, 0, 0.65))

        def add_and_close(*e):
            name = ti_name.text.strip() or "自定义项"
            val = ti_val.text.strip() or "0"
            key = f"cust_{len(self.custom_items) + 1}"
            self.custom_items.append((key, name, val, 0.01, 0.08, "自定义补充支出"))
            self._build_expense_rows()
            self.refresh_preview()
            self.auto_save_profile()
            popup.dismiss()

        btn_add.bind(on_press=add_and_close)
        btn_close.bind(on_press=popup.dismiss)
        btn_bar.add_widget(btn_add)
        btn_bar.add_widget(btn_close)
        content.add_widget(btn_bar)

        popup.open()

    def generate_report_text(self):
        d = self.compute()
        takehome = max(1.0, d["takehome"])
        debt = d["debt"]
        debt_rate = d["debt_rate"]
        total_exp = d["total_exp"]
        surplus = d["surplus"]
        sr = d["surplus_rate"]
        target = d["target_surplus"]
        g_name = "男生版 (科技爱好画像)" if self.current_gender == "male" else "女生版 (品质生活画像)"

        # 1. 财务健康综合评估
        if surplus < 0:
            health_grade = "【预警赤字】"
            grade_desc = f"当前月度收支倒挂 -￥{fmt(-surplus)} 元，存在透支风险，建议削减非刚需或重组债务。"
        elif sr < 0.10:
            health_grade = "【紧平衡型】"
            grade_desc = f"每月结余 ￥{fmt(surplus)} 元，收支接近平衡，抗风险缓冲偏弱，建议适当压缩弹性支出。"
        elif sr < 0.25:
            health_grade = "【稳健成长型】"
            grade_desc = f"每月结余 ￥{fmt(surplus)} 元 (结余率 {sr*100:.1f}%)，现金流良好，具备稳定抗风险能力。"
        else:
            health_grade = "【充裕结余型】"
            grade_desc = f"每月结余 ￥{fmt(surplus)} 元 (结余率 {sr*100:.1f}%)，资金充沛，资产积累潜力强劲。"

        # 2. 负债与偿债诊断 (温和客观)
        if debt <= 0:
            debt_eval = "零负债状态，无月供还款负担，资金支配自由度高。"
        elif debt_rate <= 0.20:
            debt_eval = f"月供 ￥{fmt(debt)} 元，偿债率 {debt_rate*100:.1f}%，处于安全良性区间，月供压力轻微。"
        elif debt_rate <= 0.40:
            debt_eval = f"月供 ￥{fmt(debt)} 元，偿债率 {debt_rate*100:.1f}%，月供适中可控，建议保留3个月流动资金防备还款波动。"
        elif debt_rate <= 0.60:
            debt_eval = f"月供 ￥{fmt(debt)} 元，偿债率 {debt_rate*100:.1f}%，负债压力偏重，每月超三成收入用于还债，建议优先偿还高息借贷。"
        else:
            debt_eval = f"月供 ￥{fmt(debt)} 元，偿债率 {debt_rate*100:.1f}%，处于高负债预警区间，需严格节流并暂停一切新增分期消费。"

        # 3. 目标储蓄达成评估
        if target > 0:
            if surplus >= target:
                achieve_rate = (surplus / target * 100)
                target_eval = f"达成储蓄目标 (达成率 {achieve_rate:.0f}%)，超额 ￥{fmt(surplus - target)} 元"
            else:
                gap = target - surplus
                target_eval = f"距 ￥{fmt(target)} 目标尚差 ￥{fmt(gap)} 元，可通过微调生活消费达成"
        else:
            target_eval = "未设定储蓄目标，当前为自由结余模式"

        # 4. 三层收支架构
        essential_keys = {"housing", "food", "transport", "phone", "health", "period", "hair", "groom"}
        lifestyle_keys = {"shop", "pet", "travel", "digital", "beauty", "clothes", "drink", "sport", "game", "fun"}
        growth_keys = {"study", "other"}

        exp_map = d["expenses"]
        sum_ess = sum(exp_map.get(k, 0) for k in essential_keys)
        sum_life = sum(exp_map.get(k, 0) for k in lifestyle_keys)
        sum_growth = sum(exp_map.get(k, 0) for k in growth_keys)

        pct_ess = sum_ess / takehome * 100
        pct_life = sum_life / takehome * 100
        pct_growth = (sum_growth + max(0, surplus)) / takehome * 100

        # 5. 务实优化建议
        advice = []
        if surplus < 0:
            advice.append("· 预算当前处于透支状态，建议使用[一键智能精算]自动重新平摊预算。")
        if debt_rate > 0.40:
            advice.append("· 偿债负担偏重，建议暂停非必要分期付款，加速清偿高成本债务。")

        food_val = exp_map.get("food", 0)
        food_pct = food_val / takehome * 100
        if food_pct > 32:
            advice.append(f"· 伙食占到手 {food_pct:.0f}% 略高，可通过下厨或控制周末聚餐频次平抑开支。")

        shop_val = exp_map.get("shop", 0)
        if shop_val / takehome > 0.15:
            advice.append("· 网购消费占比偏高，建议针对非急需好物设置48小时冷静期。")

        pet_val = exp_map.get("pet", 0)
        if pet_val > 0:
            advice.append(f"· 宠物养护每月预算 ￥{fmt(pet_val)} 元，建议提前预留宠物医疗应急资金。")

        travel_val = exp_map.get("travel", 0)
        if travel_val > 0:
            advice.append(f"· 旅游出行每月平摊 ￥{fmt(travel_val)} 元，适合采用专项活期定存按月积累。")

        if not advice:
            advice.append("· 当前各项开销结构合理，现金流健康，保持当前规划节奏即可。")

        # 组装清晰纯净的报告文本 (无说教、无冗余安全提示)
        lines = [
            "【个人财务规划分析报告】",
            "",
            "一、核心收支与负债总览",
            f"· 规划模型：{g_name}  |  身份：{self.active_identity}",
            f"· 税前月薪：￥{fmt(d['income'])}  |  实发到手：￥{fmt(takehome)}",
            f"· 月度负债还款：￥{fmt(debt)}  |  偿债诊断：{debt_eval}",
            f"· 预算生活支出：￥{fmt(total_exp)}  |  支出率：{total_exp/takehome*100:.1f}%",
            f"· 月度净结余：{'-￥' + fmt(-surplus) if surplus < 0 else '￥' + fmt(surplus)} (结余率 {sr*100:.1f}%)",
            f"· 财务评级：{health_grade} - {grade_desc}",
            f"· 目标储蓄：￥{fmt(target)}  |  状态：{target_eval}",
            "",
            "二、资金分布架构 (参考 50/30/20 分布模型)",
            f"1.【生存刚需】：￥{fmt(sum_ess)} ({pct_ess:.1f}%)",
            f"   涵盖餐饮、房租、通勤、话费、医疗、生理/修容美发等刚性支出。",
            f"2.【品质与兴趣】：￥{fmt(sum_life)} ({pct_life:.1f}%)",
            f"   涵盖穿搭、数码、美妆、茶饮、社交娱乐、旅游、宠物等生活体验。",
            f"3.【成长与结余】：￥{fmt(sum_growth + max(0, surplus))} ({pct_growth:.1f}%)",
            f"   涵盖自我提升、机动备用与每月实际沉淀结余。",
            "",
            "三、财务优化建议",
            "\n".join(advice),
            "",
            "四、支出细目精算清单"
        ]

        for it in self.expense_widgets:
            amt = self._num(it["txt"])
            pct = (amt / takehome * 100) if takehome > 0 else 0
            lock_str = " [已锁定]" if it["lock"].is_locked else ""
            lines.append(f"· {it['name']}：￥{fmt(amt)} ({pct:.0f}%){lock_str}")

        return "\n".join(lines)

    def show_report_popup(self, *args):
        t = THEMES[self.current_theme_key]
        report_text = self.generate_report_text()

        content = ModalCard(bg_color=t["bg_card"], radius=16, padding=dp(16), spacing=dp(10))

        lbl_p_title = Label(text="个人财务精算报告", font_size=dp(15), bold=True,
                            size_hint_y=None, height=dp(28), color=t["accent"], halign='center')
        content.add_widget(lbl_p_title)

        sv = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        lbl_rpt = DynamicLabel(text=report_text, font_size=dp(12), color=t["text_primary"])
        sv.add_widget(lbl_rpt)
        content.add_widget(sv)

        btn_bar = BoxLayout(size_hint_y=None, height=dp(38), spacing=dp(10))
        btn_copy = ModernButton(text="一键复制简报", font_size=dp(12), bold=True,
                                bg_color=t["btn_report_bg"], color=t["btn_report_fg"])
        btn_close = ModernButton(text="关闭", font_size=dp(12),
                                 bg_color=t.get("btn_secondary_bg", (0.85, 0.88, 0.92, 1)),
                                 color=t.get("btn_secondary_fg", t["text_primary"]))

        popup = Popup(title="", separator_height=0, content=content,
                      size_hint=(0.92, 0.85), background="", background_color=(0, 0, 0, 0.65))

        def copy_and_toast(instance):
            Clipboard.copy(report_text)
            btn_copy.text = "已复制到手机剪贴板！"

        btn_copy.bind(on_press=copy_and_toast)
        btn_close.bind(on_press=popup.dismiss)
        btn_bar.add_widget(btn_copy)
        btn_bar.add_widget(btn_close)
        content.add_widget(btn_bar)

        popup.open()


if __name__ == "__main__":
    FinancePlannerApp().run()
