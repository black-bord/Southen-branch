# -*- coding: utf-8 -*-
"""
个人智能财务与安全规划系统 v9.8 Pro · 移动旗舰优化版
优化亮点：
1. ☀️ 晴空白 / 📖 护眼暖 / 🌙 曜石黑 三重护眼主题无缝即时切换，所有弹窗与文本高对比度自适应。
2. 彻底修复柱状图不动的问题（固定柱状结构 + 动态尺寸重算，100% 响应数值更新）。
3. 彻底修复图表数字与文字不显示的 Bug（环形图中心大字 + 右侧明细清单，柱状图顶端精准金额与百分比，底部居中标签）。
4. 深度优化报告生成模块：移除所有冗余横线杂音，优化排版间距与大字号（dp(13)），无论深色浅色均清晰易读。
5. 现代化流行移动 UI：圆角微阴影卡片、胶囊渐变按钮、细腻触控反馈。
6. 全功能全要素：微信账单智能分类、餐饮精算、学期分摊、五险一金精算、23类支出管理与全维安全规划。
"""

import os
import sys
import re
from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.core.clipboard import Clipboard
from kivy.utils import platform
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Rectangle, Ellipse, Line

# 模拟手机竖屏分辨率（电脑预览时）
if platform not in ("android", "ios"):
    Window.size = (410, 820)

# ==================== 全局中文字体注册 ====================
def setup_global_font():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_font = os.path.join(base_dir, "font.ttf")
    font_file = None
    if os.path.exists(local_font):
        font_file = local_font
    else:
        for p in [
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/msyh.ttf",
            "/system/fonts/NotoSansSC-Regular.otf",
            "/system/fonts/NotoSansCJK-Regular.ttc",
            "/system/fonts/DroidSansFallback.ttf",
            "/system/fonts/SourceHanSansCN-Regular.otf",
            "/system/fonts/MiSans-Regular.ttf",
        ]:
            if os.path.exists(p):
                font_file = p
                break
    if font_file:
        try:
            LabelBase.register(DEFAULT_FONT, font_file)
            LabelBase.register("AppFont", font_file)
            return font_file
        except Exception as e:
            print("Font register error:", e)
    return "Roboto"

FONT_PATH = setup_global_font()


# ==================== 三重主题调色系统 ====================
THEMES = {
    "light": {
        "name": "☀️ 晴空白",
        "bg_root": (0.94, 0.97, 1.0, 1.0),        # #f0f7ff 浅冰蓝
        "bg_card": (1.0, 1.0, 1.0, 1.0),          # #ffffff 纯白
        "border_card": (0.86, 0.91, 0.97, 1.0),
        "bg_header": (0.10, 0.29, 0.69, 1.0),      # #1a4baf 深海科技蓝
        "text_header": (1.0, 1.0, 1.0, 1.0),
        "text_sub": (0.80, 0.90, 1.0, 1.0),
        "text_primary": (0.09, 0.13, 0.24, 1.0),  # #0f172a
        "text_secondary": (0.35, 0.42, 0.52, 1.0),# #475569
        "accent": (0.14, 0.39, 0.92, 1.0),        # #2563eb
        "accent_green": (0.05, 0.62, 0.45, 1.0),
        "bg_input": (0.96, 0.98, 1.0, 1.0),
        "text_input": (0.09, 0.13, 0.24, 1.0),
        "tier_bg": (0.92, 0.96, 1.0, 1.0),
    },
    "warm": {
        "name": "📖 护眼暖",
        "bg_root": (0.97, 0.95, 0.89, 1.0),        # #f8f2e4 羊皮纸暖黄
        "bg_card": (0.99, 0.98, 0.94, 1.0),        # #fdfaf3 柔和暖白
        "border_card": (0.88, 0.84, 0.74, 1.0),
        "bg_header": (0.46, 0.30, 0.16, 1.0),      # #78350f 暖木棕
        "text_header": (1.0, 0.98, 0.92, 1.0),
        "text_sub": (0.93, 0.85, 0.73, 1.0),
        "text_primary": (0.24, 0.17, 0.10, 1.0),  # #3d2e1e 柔和深棕
        "text_secondary": (0.48, 0.39, 0.28, 1.0),
        "accent": (0.68, 0.40, 0.15, 1.0),        # #b45309 琥珀暖金
        "accent_green": (0.22, 0.54, 0.32, 1.0),
        "bg_input": (0.94, 0.91, 0.84, 1.0),
        "text_input": (0.24, 0.17, 0.10, 1.0),
        "tier_bg": (0.95, 0.92, 0.84, 1.0),
    },
    "dark": {
        "name": "🌙 曜石黑",
        "bg_root": (0.07, 0.09, 0.14, 1.0),        # #0f172a 深空黑
        "bg_card": (0.12, 0.16, 0.24, 1.0),        # #1e293b 曜石黑
        "border_card": (0.20, 0.26, 0.36, 1.0),
        "bg_header": (0.08, 0.11, 0.18, 1.0),      # #080c14
        "text_header": (0.94, 0.96, 1.0, 1.0),
        "text_sub": (0.62, 0.72, 0.85, 1.0),
        "text_primary": (0.94, 0.96, 0.98, 1.0),  # #f1f5f9
        "text_secondary": (0.60, 0.68, 0.78, 1.0),# #94a3b8
        "accent": (0.24, 0.54, 0.98, 1.0),        # #3b82f6
        "accent_green": (0.10, 0.75, 0.52, 1.0),
        "bg_input": (0.18, 0.23, 0.34, 1.0),
        "text_input": (0.95, 0.97, 1.0, 1.0),
        "tier_bg": (0.15, 0.20, 0.30, 1.0),
    }
}


# ==================== 现代微交互组件 ====================
class ModernButton(Button):
    def __init__(self, bg_color=(0.14, 0.39, 0.92, 1), radius=10, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.bg_color = list(bg_color)
        self.radius = dp(radius)
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

    def on_press(self):
        self.c_color.rgba = [min(1.0, c * 1.15) for c in self.bg_color[:3]] + [self.bg_color[3]]

    def on_release(self):
        self.c_color.rgba = self.bg_color


class CardLayout(BoxLayout):
    def __init__(self, bg_color=(1, 1, 1, 1), border_color=(0.88, 0.92, 0.96, 1), radius=12, auto_height=True, **kwargs):
        super().__init__(**kwargs)
        self.padding = dp(12)
        self.spacing = dp(8)
        self.orientation = "vertical"
        self.auto_height = auto_height
        if auto_height:
            self.size_hint_y = None
            self.bind(minimum_height=self.setter('height'))
        self.bg_color = list(bg_color)
        self.border_color = list(border_color)
        self.radius = dp(radius)
        with self.canvas.before:
            self.c_border = Color(*self.border_color)
            self.rect_border = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
            self.c_bg = Color(*self.bg_color)
            self.rect_bg = RoundedRectangle(pos=(self.x + dp(1), self.y + dp(1)),
                                            size=(max(0, self.width - dp(2)), max(0, self.height - dp(2))),
                                            radius=[max(0, self.radius - dp(1))])
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect_border.pos = self.pos
        self.rect_border.size = self.size
        self.rect_bg.pos = (self.x + dp(1), self.y + dp(1))
        self.rect_bg.size = (max(0, self.width - dp(2)), max(0, self.height - dp(2)))

    def set_theme_colors(self, bg_color, border_color):
        self.bg_color = list(bg_color)
        self.border_color = list(border_color)
        self.c_bg.rgba = self.bg_color
        self.c_border.rgba = self.border_color


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
        self.text_size = (max(dp(50), self.width - dp(10)), None)

    def _update_height(self, *args):
        self.height = max(dp(26), self.texture_size[1] + dp(12))


# ==================== 核心财务模型与阶梯矩阵 ====================
TIER_DEFINITIONS = [
    {
        "max": 3000,
        "name": "极简生存阶梯",
        "tag": "🌱 极简生存阶梯 (≤3000元)",
        "desc": "生存底线兜底 · 房租1000/餐饮1000绝对优先 · 剔除一切弹性消费 · 积攒小额急用金",
        "target_savings_rate": 0.12,
        "security_level": "⚠️ 基础生存防御期（严禁负债/先存3000元防线）",
        "student_allowed": ["food", "transport", "phone", "study", "other"],
        "normal_allowed": ["food", "housing", "transport", "phone", "other"],
    },
    {
        "max": 5000,
        "name": "温饱起步阶梯",
        "tag": "🌿 温饱起步阶梯 (3000~5000元)",
        "desc": "基本生活自立 · 严控租房与外卖 · 解锁小额提升与基础社交 · 储蓄率提升至20%",
        "target_savings_rate": 0.20,
        "security_level": "🛡️ 活期安全垫构建期（目标存满2个月生活费）",
        "student_allowed": ["food", "transport", "phone", "study", "fun", "shopping", "health", "drink", "other"],
        "normal_allowed": ["food", "housing", "transport", "phone", "study", "fun", "shopping", "health", "drink", "other"],
    },
    {
        "max": 8000,
        "name": "基础自立阶梯",
        "tag": "🚀 基础自立阶梯 (5000~8000元)",
        "desc": "走向收支平衡 · 解锁基础人身医疗险 · 建立3~6个月应急池 · 储蓄率提升至28%",
        "target_savings_rate": 0.28,
        "security_level": "🛡️ 综合风险防御期（配置百万医疗险+意外险）",
        "student_allowed": ["food", "transport", "phone", "study", "fun", "shopping", "health", "beauty", "subscription", "drink", "love", "travel", "other"],
        "normal_allowed": ["food", "housing", "transport", "phone", "study", "fun", "shopping", "health", "beauty", "subscription", "love", "insurance", "drink", "other"],
    },
    {
        "max": 10000,
        "name": "稳健成长阶梯",
        "tag": "🏆 稳健成长阶梯 (8000~10000元)",
        "desc": "迈入万元门槛 · 抑制生活方式通胀 · 锁定生活成本加速储蓄 · 储蓄率提升至32%",
        "target_savings_rate": 0.32,
        "security_level": "⚡ 稳健抗风险期（应急池充裕+开启低波理财）",
        "student_allowed": None,
        "normal_allowed": ["food", "housing", "transport", "phone", "study", "fun", "shopping", "health", "beauty", "subscription", "love", "insurance", "gift", "fitness", "electronics", "parents", "drink", "other"],
    },
    {
        "max": 20000,
        "name": "强储蓄积累阶梯",
        "tag": "⚡ 强储蓄积累阶梯 (10000~20000元)",
        "desc": "刚需占比大幅钝化 · 储蓄率跨越40%~48% · 资本积累黄金期",
        "target_savings_rate": 0.45,
        "security_level": "💎 资产复利与家庭防火墙期（全员重疾+大类配置）",
        "student_allowed": None,
        "normal_allowed": None,
    },
    {
        "max": float("inf"),
        "name": "财富增值扩张阶梯",
        "tag": "👑 财富增值扩张阶梯 (20000+元)",
        "desc": "边际消费最低 · 超55%归入资本扩张 · 被动收益飞轮",
        "target_savings_rate": 0.55,
        "security_level": "👑 综合财富传承与资本护城河",
        "student_allowed": None,
        "normal_allowed": None,
    }
]

def get_tier_info(income):
    for t in TIER_DEFINITIONS:
        if income <= t["max"]:
            return t
    return TIER_DEFINITIONS[-1]

PRESET_EXPENSES = [
    ("food",         "餐饮饮食",  "1050", 0.20, 0.35, "刚需。日均35元工作餐，避免高频外卖"),
    ("housing",      "住房房租",  "1050", 0.15, 0.30, "刚需。控制在30%以内，城中村单间/合租"),
    ("transport",    "交通通勤",  "150",  0.03, 0.10, "地铁/公交/单车优先"),
    ("phone",        "通讯话费",  "60",   0.01, 0.04, "大流量优惠卡，防套餐超标"),
    ("fun",          "娱乐社交",  "150",  0.05, 0.15, "适度社交，量入为出"),
    ("shopping",     "购物网购",  "120",  0.03, 0.10, "必需品清单制，延迟满足"),
    ("study",        "学习提升",  "80",   0.02, 0.08, "高回报自我投资，买书/技能考证"),
    ("health",       "医疗健康",  "50",   0.01, 0.05, "常备药、体检与基础健康储备"),
    ("insurance",    "商业保险",  "0",    0.02, 0.06, "百万医疗险/意外险，工薪期必配"),
    ("beauty",       "服装美容",  "80",   0.02, 0.10, "理发与基础护肤，理性消费"),
    ("drink",        "烟酒茶饮",  "40",   0.01, 0.05, "奶茶咖啡最易偷走储蓄"),
    ("subscription", "订阅会员",  "20",   0.01, 0.04, "定期清理不用的自动续费"),
    ("love",         "恋爱资金",  "0",    0.03, 0.12, "节日与日常，适度理性"),
    ("gift",         "人情往来",  "0",    0.02, 0.08, "份子钱、礼品"),
    ("electronics",  "电子数码",  "0",    0.02, 0.08, "设备折旧更新储备"),
    ("fitness",      "健身运动",  "0",    0.01, 0.06, "居家/户外跑步，谨慎大额办卡"),
    ("parents",      "孝敬父母",  "0",    0.05, 0.15, "量力而行，心意为主"),
    ("travel",       "旅游度假",  "0",    0.03, 0.10, "年度旅游平摊"),
    ("debt",         "债务还款",  "0",    0.00, 0.20, "严禁消费贷，优先结清高息负债"),
    ("car",          "车辆费用",  "0",    0.05, 0.15, "油费/停车/车险"),
    ("other",        "其他杂项",  "60",   0.00, 0.08, "零散日常日用品支出"),
]

IDENTITY_PRESETS = {
    "全日制大学生": {
        "income": "1800", "savings": "800", "invest": "0", "target": "200", "social_mode": "无社保", "social_base": "0",
        "defaults": {"food": "1000", "housing": "0", "transport": "50", "phone": "40", "fun": "150", "shopping": "100", "study": "100", "health": "30", "beauty": "50", "drink": "40", "subscription": "20", "other": "50"},
        "emergency_months": 1,
        "feature": "零房租、无社保税负；以食堂餐饮与学业提升为主，攒下人生第一笔小额备用金。"
    },
    "职场新人（1-3年）": {
        "income": "4200", "savings": "3000", "invest": "0", "target": "500", "social_mode": "单位代缴", "social_base": "3800",
        "defaults": {"food": "1050", "housing": "1050", "transport": "150", "phone": "60", "fun": "150", "shopping": "120", "study": "80", "health": "50", "beauty": "80", "drink": "40", "subscription": "20", "other": "60"},
        "emergency_months": 2,
        "feature": "基层新人现实中位数（3500~5000元），房租约千元+温饱兜底，严控非必需开销，每月实打实攒下500元。"
    },
    "自由职业/灵活就业": {
        "income": "4500", "savings": "6000", "invest": "0", "target": "600", "social_mode": "无社保", "social_base": "0",
        "defaults": {"food": "1050", "housing": "1100", "transport": "100", "phone": "60", "fun": "100", "shopping": "100", "study": "80", "health": "50", "beauty": "50", "drink": "40", "subscription": "20", "other": "50"},
        "emergency_months": 3,
        "feature": "普通接单/零工起步常态（3500~5500元），收入易波动，手头备1~2个月现金流防断粮，严控固定开支。"
    },
    "职场工薪（3-5年）": {
        "income": "7500", "savings": "20000", "invest": "8000", "target": "1600", "social_mode": "单位代缴", "social_base": "6500",
        "defaults": {"food": "1300", "housing": "1500", "transport": "240", "phone": "80", "fun": "260", "shopping": "220", "study": "120", "health": "80", "insurance": "120", "beauty": "120", "drink": "70", "subscription": "30", "parents": "200", "other": "80"},
        "emergency_months": 3,
        "feature": "工薪扎实稳定期（6000~8000元），收支有余，配置百万医疗险，稳步充实应急储备池。"
    },
    "高薪骨干（1.5万+）": {
        "income": "18000", "savings": "60000", "invest": "50000", "target": "6500", "social_mode": "单位代缴", "social_base": "18000",
        "defaults": {"food": "2200", "housing": "3200", "transport": "450", "phone": "100", "fun": "500", "shopping": "500", "study": "300", "health": "180", "insurance": "500", "beauty": "300", "drink": "150", "subscription": "50", "parents": "600", "travel": "400", "car": "400", "other": "150"},
        "emergency_months": 6,
        "feature": "高收入骨干，边际储蓄率显著提升，全方位家庭风险防御与大类资产配置。"
    }
}

STUDENT_LOCKED_KEYS = ["housing", "car", "parents", "debt", "insurance"]

def fmt(v):
    return f"{v:,.0f}"

def compute_tax(taxable):
    if taxable <= 0:
        return 0.0
    brackets = [
        (3000, 0.03, 0), (12000, 0.10, 210), (25000, 0.20, 1410),
        (35000, 0.25, 2660), (55000, 0.30, 4410), (80000, 0.35, 7160),
        (float("inf"), 0.45, 15160),
    ]
    for limit, rate, deduct in brackets:
        if taxable <= limit:
            return taxable * rate - deduct
    return taxable * 0.45 - 15160


# ==================== 彻底修复柱状图与数字显示的看板组件 ====================
class FixedChartsWidget(BoxLayout):
    """
    双图表看板：
    1. 环形甜甜圈图：Canvas 绘制高饱和色块，右侧垂直列表详细呈现各项【真实金额】与【百分比】。
    2. 收支对比五色柱状图：常驻 5 根动态柱子，顶端大字标注【¥金额 + 占比】，底部居中展示【分类名称】。
    彻底解决柱状图不动、数字看不见的 Bug！
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(470)
        self.padding = dp(8)
        self.spacing = dp(10)

        # 标题栏
        self.lbl_head = Label(text="📊 月度收支结构与目标对比可视化 (全数字清晰看板)", font_size=dp(13), bold=True,
                              color=(0.14, 0.39, 0.92, 1), size_hint_y=None, height=dp(24))
        self.add_widget(self.lbl_head)

        # 1. 环形图容器
        donut_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(180), spacing=dp(8))
        self.pie_draw_box = BoxLayout(size_hint=(0.48, 1))
        donut_box.add_widget(self.pie_draw_box)
        self.pie_draw_box.bind(pos=self.redraw_pie, size=self.redraw_pie)

        self.pie_legend_box = BoxLayout(orientation="vertical", size_hint=(0.52, 1), spacing=dp(4))
        donut_box.add_widget(self.pie_legend_box)
        self.add_widget(donut_box)

        # 2. 柱状图容器 (常驻柱子架构，杜绝销毁卡顿)
        bar_box = BoxLayout(orientation="vertical", size_hint=(1, 1), spacing=dp(4))
        self.bar_title = Label(text="📈 收支流向与储蓄目标柱状对比", font_size=dp(11), bold=True,
                               color=(0.35, 0.45, 0.55, 1), size_hint_y=None, height=dp(18))
        bar_box.add_widget(self.bar_title)

        self.bar_cols_layout = BoxLayout(orientation="horizontal", spacing=dp(6), size_hint=(1, 1))
        bar_box.add_widget(self.bar_cols_layout)
        self.add_widget(bar_box)

        # 预先构建 5 根常驻柱子结构
        self.bar_cols = []
        cols_cfg = [
            ("到手", (0.10, 0.28, 0.65, 1)),
            ("刚需", (0.14, 0.39, 0.92, 1)),
            ("弹性", (0.55, 0.25, 0.85, 1)),
            ("结余", (0.02, 0.65, 0.55, 1)),
            ("目标", (0.01, 0.52, 0.78, 1)),
        ]
        for name, col in cols_cfg:
            c_box = BoxLayout(orientation="vertical", spacing=dp(2), size_hint=(1, 1))
            lbl_top = Label(text="¥0\n0%", font_size=dp(10), bold=True, size_hint_y=None, height=dp(30))
            
            wgt_bar = Widget(size_hint=(1, 1))
            with wgt_bar.canvas:
                c_track = Color(0.85, 0.90, 0.96, 0.40)
                rect_track = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(4), dp(4), 0, 0])
                c_inst = Color(*col)
                rect_inst = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(4), dp(4), 0, 0])
            
            lbl_bot = Label(text=name, font_size=dp(11), bold=True, size_hint_y=None, height=dp(20))
            
            c_box.add_widget(lbl_top)
            c_box.add_widget(wgt_bar)
            c_box.add_widget(lbl_bot)
            self.bar_cols_layout.add_widget(c_box)
            
            self.bar_cols.append({
                "name": name, "color": col, "lbl_top": lbl_top,
                "wgt_bar": wgt_bar, "c_track": c_track, "rect_track": rect_track,
                "c_inst": c_inst, "rect_inst": rect_inst,
                "lbl_bot": lbl_bot
            })
            wgt_bar.bind(pos=lambda *a: self.redraw_bars(), size=lambda *a: self.redraw_bars())

        self.chart_data = {"takehome": 1, "essential": 0, "flexible": 0, "surplus": 0, "target": 0, "expenses": {}}
        self.slice_colors = [
            (0.14, 0.39, 0.92, 1), (0.02, 0.65, 0.55, 1), (0.95, 0.40, 0.14, 1),
            (0.55, 0.25, 0.85, 1), (0.10, 0.70, 0.90, 1), (0.90, 0.70, 0.10, 1),
            (0.85, 0.20, 0.40, 1), (0.40, 0.60, 0.20, 1)
        ]

    def update_data(self, data, theme):
        self.chart_data = data
        self.current_theme = theme
        self.lbl_head.color = theme["accent"]
        self.bar_title.color = theme["text_secondary"]
        self.redraw_pie()
        self.redraw_bars()

    def redraw_pie(self, *a):
        self.pie_draw_box.canvas.clear()
        self.pie_legend_box.clear_widgets()

        w = self.pie_draw_box.width
        h = self.pie_draw_box.height
        x = self.pie_draw_box.x
        y = self.pie_draw_box.y

        if w <= 10 or h <= 10:
            return

        cx = x + w * 0.5
        cy = y + h * 0.5
        r = min(w * 0.44, h * 0.44)

        expenses = self.chart_data.get("expenses", {})
        total_exp = sum(expenses.values())
        sorted_exp = sorted(expenses.items(), key=lambda it: it[1], reverse=True)

        with self.pie_draw_box.canvas:
            start_angle = 0
            if total_exp > 0:
                for idx, (name, amt) in enumerate(sorted_exp[:7]):
                    if amt <= 0:
                        continue
                    span = (amt / total_exp) * 360.0
                    Color(*self.slice_colors[idx % len(self.slice_colors)])
                    Ellipse(pos=(cx - r, cy - r), size=(r * 2, r * 2),
                            angle_start=start_angle, angle_end=start_angle + span)
                    start_angle += span

                theme_card_bg = getattr(self, "current_theme", THEMES["light"])["bg_card"]
                Color(*theme_card_bg)
                inner_r = r * 0.58
                Ellipse(pos=(cx - inner_r, cy - inner_r), size=(inner_r * 2, inner_r * 2))
            else:
                Color(0.8, 0.85, 0.9, 1)
                Ellipse(pos=(cx - r, cy - r), size=(r * 2, r * 2))

        theme_txt_p = getattr(self, "current_theme", THEMES["light"])["text_primary"]
        theme_txt_s = getattr(self, "current_theme", THEMES["light"])["text_secondary"]

        head_row = Label(text=f"总支出: ¥{fmt(total_exp)}", font_size=dp(13), bold=True,
                         color=theme_txt_p, size_hint_y=None, height=dp(20), halign="left")
        head_row.bind(size=head_row.setter('text_size'))
        self.pie_legend_box.add_widget(head_row)

        for idx, (name, amt) in enumerate(sorted_exp[:6]):
            if amt <= 0:
                continue
            pct = (amt / total_exp * 100) if total_exp > 0 else 0
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(22), spacing=dp(4))
            
            col_box = Widget(size_hint=(None, None), size=(dp(10), dp(10)), pos_hint={"center_y": 0.5})
            c = self.slice_colors[idx % len(self.slice_colors)]
            with col_box.canvas:
                Color(*c)
                RoundedRectangle(pos=col_box.pos, size=col_box.size, radius=[dp(2)])
            col_box.bind(pos=lambda *a, cb=col_box: setattr(cb.canvas.children[-1], 'pos', cb.pos))
            row.add_widget(col_box)

            lbl_info = Label(text=f"{name}: ¥{fmt(amt)} ({pct:.0f}%)", font_size=dp(11),
                             color=theme_txt_s, halign="left", valign="middle")
            lbl_info.bind(size=lbl_info.setter('text_size'))
            row.add_widget(lbl_info)

            self.pie_legend_box.add_widget(row)

    def redraw_bars(self, *a):
        """动态更新 5 根常驻柱子，高频响应输入，杜绝冻结！"""
        takehome = max(1.0, self.chart_data.get("takehome", 1.0))
        values = [
            self.chart_data.get("takehome", 0),
            self.chart_data.get("essential", 0),
            self.chart_data.get("flexible", 0),
            max(0, self.chart_data.get("surplus", 0)),
            self.chart_data.get("target", 0)
        ]
        max_val = max(values + [1.0])
        theme = getattr(self, "current_theme", THEMES["light"])
        theme_txt_p = theme["text_primary"]
        theme_txt_s = theme["text_secondary"]
        is_dark = (theme.get("bg_root") == THEMES["dark"]["bg_root"])

        for col_info, val in zip(self.bar_cols, values):
            pct = (val / takehome * 100) if takehome > 0 else 0
            col_info["lbl_top"].text = f"¥{fmt(val)}\n{pct:.0f}%"
            col_info["lbl_top"].color = theme_txt_p
            col_info["lbl_bot"].color = theme_txt_s
            
            wb = col_info["wgt_bar"]
            if wb.height > 0 and wb.width > 0:
                bw = min(dp(26), max(dp(10), wb.width * 0.60))
                bx = wb.x + (wb.width - bw) / 2
                by = wb.y

                # 背景轨道底槽
                col_info["rect_track"].pos = (bx, by)
                col_info["rect_track"].size = (bw, wb.height)
                col_info["c_track"].rgba = (0.35, 0.45, 0.55, 0.20) if is_dark else (0.85, 0.90, 0.96, 0.45)

                # 动态填充柱
                bh = (val / max_val) * wb.height if max_val > 0 else dp(4)
                bh = max(dp(4), min(wb.height, bh))
                col_info["rect_inst"].pos = (bx, by)
                col_info["rect_inst"].size = (bw, bh)


# ==================== 主应用程序 ====================
class FinancePlannerApp(App):
    def build(self):
        self.title = "个人财务与安全规划 Pro"
        self.current_theme_key = "light"
        self.custom_items = []
        self.expense_widgets = []

        # 根布局
        self.root_layout = BoxLayout(orientation='vertical')
        with self.root_layout.canvas.before:
            self.root_bg_color = Color(*THEMES["light"]["bg_root"])
            self.root_bg_rect = Rectangle(pos=self.root_layout.pos, size=self.root_layout.size)
        self.root_layout.bind(pos=lambda *a: setattr(self.root_bg_rect, 'pos', self.root_layout.pos),
                              size=lambda *a: setattr(self.root_bg_rect, 'size', self.root_layout.size))

        # 1. 顶部 Header
        self.header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(70), padding=[dp(14), dp(8)], spacing=dp(8))
        with self.header.canvas.before:
            self.header_bg_color = Color(*THEMES["light"]["bg_header"])
            self.header_bg_rect = Rectangle(pos=self.header.pos, size=self.header.size)
        self.header.bind(pos=lambda *a: setattr(self.header_bg_rect, 'pos', self.header.pos),
                         size=lambda *a: setattr(self.header_bg_rect, 'size', self.header.size))

        title_box = BoxLayout(orientation='vertical', size_hint=(0.75, 1))
        self.lbl_title = Label(text="🧭 个人智能财务安全规划", font_size=dp(15), bold=True,
                               color=(1, 1, 1, 1), halign='left', valign='middle')
        self.lbl_title.bind(size=self.lbl_title.setter('text_size'))
        self.lbl_sub = Label(text="全维防御网 · 生存底线优先 · 阶梯式匹配", font_size=dp(10),
                             color=THEMES["light"]["text_sub"], halign='left', valign='middle')
        self.lbl_sub.bind(size=self.lbl_sub.setter('text_size'))
        title_box.add_widget(self.lbl_title)
        title_box.add_widget(self.lbl_sub)
        self.header.add_widget(title_box)

        # 胶囊主题切换按钮
        self.btn_theme = ModernButton(text="☀️ 晴空", font_size=dp(11), bold=True,
                                      size_hint=(0.25, None), height=dp(38),
                                      pos_hint={"center_y": 0.5}, bg_color=(0.22, 0.45, 0.95, 1))
        self.btn_theme.bind(on_press=self.cycle_theme)
        self.header.add_widget(self.btn_theme)

        self.root_layout.add_widget(self.header)

        # 2. 中间滚动主体
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.content = BoxLayout(orientation='vertical', size_hint_y=None, padding=dp(10), spacing=dp(10))
        self.content.bind(minimum_height=self.content.setter('height'))

        # ---------- 卡片 1: 身份与基础资金 ----------
        self.card1 = CardLayout()
        self.c1_head = Label(text="① 身份选择与资金基础", font_size=dp(14), bold=True,
                             color=THEMES["light"]["accent"], size_hint_y=None, height=dp(22))
        self.card1.add_widget(self.c1_head)

        self.spinner_id = Spinner(
            text="职场新人（1-3年）",
            values=list(IDENTITY_PRESETS.keys()),
            font_size=dp(13),
            size_hint_y=None,
            height=dp(38),
            background_color=THEMES["light"]["accent"],
            color=(1, 1, 1, 1)
        )
        self.spinner_id.bind(text=self.on_identity_change)
        self.card1.add_widget(self.spinner_id)

        grid_in = GridLayout(cols=2, spacing=dp(6), size_hint_y=None)
        grid_in.bind(minimum_height=grid_in.setter('height'))

        self.lbl_in_income = Label(text="每月税前收入(元):", font_size=dp(12), color=THEMES["light"]["text_secondary"], size_hint_y=None, height=dp(32))
        grid_in.add_widget(self.lbl_in_income)
        self.in_income = TextInput(text="4200", multiline=False, input_filter='float', font_size=dp(13), size_hint_y=None, height=dp(34))
        self.in_income.bind(text=self.refresh_preview)
        grid_in.add_widget(self.in_income)

        self.lbl_in_savings = Label(text="现有活期存款(元):", font_size=dp(12), color=THEMES["light"]["text_secondary"], size_hint_y=None, height=dp(32))
        grid_in.add_widget(self.lbl_in_savings)
        self.in_savings = TextInput(text="3000", multiline=False, input_filter='float', font_size=dp(13), size_hint_y=None, height=dp(34))
        self.in_savings.bind(text=self.refresh_preview)
        grid_in.add_widget(self.in_savings)

        self.lbl_in_invest = Label(text="理财投资(元):", font_size=dp(12), color=THEMES["light"]["text_secondary"], size_hint_y=None, height=dp(32))
        grid_in.add_widget(self.lbl_in_invest)
        self.in_invest = TextInput(text="0", multiline=False, input_filter='float', font_size=dp(13), size_hint_y=None, height=dp(34))
        self.in_invest.bind(text=self.refresh_preview)
        grid_in.add_widget(self.in_invest)

        self.lbl_in_target = Label(text="月储蓄目标(元):", font_size=dp(12), color=THEMES["light"]["text_secondary"], size_hint_y=None, height=dp(32))
        grid_in.add_widget(self.lbl_in_target)
        self.in_target = TextInput(text="500", multiline=False, input_filter='float', font_size=dp(13), size_hint_y=None, height=dp(34))
        self.in_target.bind(text=self.refresh_preview)
        grid_in.add_widget(self.in_target)

        self.card1.add_widget(grid_in)
        self.content.add_widget(self.card1)

        # ---------- 卡片 2: 薪资阶梯与安全感知徽章 ----------
        self.card2 = CardLayout(bg_color=THEMES["light"]["tier_bg"])
        self.lbl_tier_tag = DynamicLabel(text="🌱 阶梯定位：计算中...", font_size=dp(13), bold=True, color=THEMES["light"]["accent"])
        self.card2.add_widget(self.lbl_tier_tag)

        self.lbl_tier_desc = DynamicLabel(text="", font_size=dp(12), color=THEMES["light"]["text_secondary"])
        self.card2.add_widget(self.lbl_tier_desc)

        self.lbl_tier_sec = DynamicLabel(text="", font_size=dp(12), bold=True, color=THEMES["light"]["accent_green"])
        self.card2.add_widget(self.lbl_tier_sec)

        self.content.add_widget(self.card2)

        # ---------- 卡片 3: 月度收支健康度大看板 ----------
        self.card3 = CardLayout()
        self.c3_head = Label(text="② 月度收支健康度看板", font_size=dp(14), bold=True,
                             color=THEMES["light"]["accent"], size_hint_y=None, height=dp(22))
        self.card3.add_widget(self.c3_head)

        self.lbl_kpi_row1 = Label(text="到手可用: 0 元 ｜ 预算支出: 0 元", font_size=dp(12),
                                  bold=True, color=THEMES["light"]["text_primary"], size_hint_y=None, height=dp(22))
        self.card3.add_widget(self.lbl_kpi_row1)

        self.lbl_kpi_row2 = Label(text="每月净结余: 0 元 ｜ 实际储蓄率: 0%", font_size=dp(12),
                                  bold=True, color=THEMES["light"]["accent_green"], size_hint_y=None, height=dp(22))
        self.card3.add_widget(self.lbl_kpi_row2)

        self.lbl_kpi_row3 = Label(text="住房+餐饮刚需: 0 元 (0%)", font_size=dp(11),
                                  color=THEMES["light"]["text_secondary"], size_hint_y=None, height=dp(20))
        self.card3.add_widget(self.lbl_kpi_row3)
        self.content.add_widget(self.card3)

        # ---------- 核心操作工具栏 ----------
        tools_grid = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(96))

        self.btn_plan = ModernButton(text="⚡ 薪资分阶智能规划\n(生存优先自动锁项)", font_size=dp(12), bold=True,
                                     bg_color=THEMES["light"]["accent"], color=(1, 1, 1, 1))
        self.btn_plan.bind(on_press=self.do_smart_plan)
        tools_grid.add_widget(self.btn_plan)

        self.btn_report = ModernButton(text="🛡️ 全维安全与财务报告\n(清晰纯净无杂线版)", font_size=dp(12), bold=True,
                                       bg_color=THEMES["light"]["accent_green"], color=(1, 1, 1, 1))
        self.btn_report.bind(on_press=self.show_report_popup)
        tools_grid.add_widget(self.btn_report)

        self.btn_meal = ModernButton(text="🍚 餐饮细分精算器", font_size=dp(12),
                                     bg_color=(0.18, 0.52, 0.88, 1), color=(1, 1, 1, 1))
        self.btn_meal.bind(on_press=self.show_meal_calculator)
        tools_grid.add_widget(self.btn_meal)

        self.btn_wechat = ModernButton(text="🧾 微信账单智能导入", font_size=dp(12),
                                       bg_color=(0.08, 0.62, 0.38, 1), color=(1, 1, 1, 1))
        self.btn_wechat.bind(on_press=self.show_wechat_bill_popup)
        tools_grid.add_widget(self.btn_wechat)

        self.content.add_widget(tools_grid)

        # 二级工具栏
        sub_tools = BoxLayout(spacing=dp(6), size_hint_y=None, height=dp(36))
        self.btn_semester = ModernButton(text="🎓 学期分摊", font_size=dp(11), bg_color=(0.35, 0.55, 0.80, 1))
        self.btn_semester.bind(on_press=self.show_semester_calculator)
        sub_tools.add_widget(self.btn_semester)

        self.btn_social = ModernButton(text="🏛️ 五险一金", font_size=dp(11), bg_color=(0.35, 0.55, 0.80, 1))
        self.btn_social.bind(on_press=self.show_social_calculator)
        sub_tools.add_widget(self.btn_social)

        self.btn_custom = ModernButton(text="➕ 加自定义项", font_size=dp(11), bg_color=(0.35, 0.55, 0.80, 1))
        self.btn_custom.bind(on_press=self.show_add_custom_popup)
        sub_tools.add_widget(self.btn_custom)

        self.content.add_widget(sub_tools)

        # ---------- 原生 Canvas 可视化图表卡片 ----------
        self.charts_card = CardLayout()
        self.charts_widget = FixedChartsWidget()
        self.charts_card.add_widget(self.charts_widget)
        self.content.add_widget(self.charts_card)

        # ---------- 卡片 4: 支出明细项管理 ----------
        self.card4 = CardLayout()
        c4_top = BoxLayout(size_hint_y=None, height=dp(26))
        self.c4_head = Label(text="③ 支出分类精算列表", font_size=dp(13), bold=True,
                             color=THEMES["light"]["accent"], halign='left')
        self.c4_head.bind(size=self.c4_head.setter('text_size'))
        c4_top.add_widget(self.c4_head)

        self.btn_lock_all = ModernButton(text="🔒全锁", font_size=dp(10), size_hint=(None, 1), width=dp(52), bg_color=(0.60, 0.68, 0.76, 1))
        self.btn_lock_all.bind(on_press=self.lock_all)
        c4_top.add_widget(self.btn_lock_all)

        self.btn_unlock_all = ModernButton(text="🔓全解", font_size=dp(10), size_hint=(None, 1), width=dp(52), bg_color=(0.60, 0.68, 0.76, 1))
        self.btn_unlock_all.bind(on_press=self.unlock_all)
        c4_top.add_widget(self.btn_unlock_all)

        self.card4.add_widget(c4_top)

        self.expense_container = BoxLayout(orientation='vertical', spacing=dp(4), size_hint_y=None)
        self.expense_container.bind(minimum_height=self.expense_container.setter('height'))
        self.card4.add_widget(self.expense_container)

        self._build_expense_rows()
        self.content.add_widget(self.card4)

        scroll.add_widget(self.content)
        self.root_layout.add_widget(scroll)

        # 社保高级参数
        self.social_mode = "单位代缴"
        self.social_base = 3800.0
        self.tax_deduction = 0.0

        # 初始化数据
        self.apply_identity_defaults("职场新人（1-3年）")
        self.refresh_preview()

        return self.root_layout

    # ==================== 三重主题切换逻辑 ====================
    def cycle_theme(self, *a):
        order = ["light", "warm", "dark"]
        curr_idx = order.index(self.current_theme_key)
        new_key = order[(curr_idx + 1) % len(order)]
        self.apply_theme(new_key)

    def apply_theme(self, theme_key):
        self.current_theme_key = theme_key
        t = THEMES[theme_key]

        self.root_bg_color.rgba = t["bg_root"]
        self.header_bg_color.rgba = t["bg_header"]
        self.lbl_sub.color = t["text_sub"]
        self.btn_theme.text = t["name"]

        self.card1.set_theme_colors(t["bg_card"], t["border_card"])
        self.card2.set_theme_colors(t["tier_bg"], t["border_card"])
        self.card3.set_theme_colors(t["bg_card"], t["border_card"])
        self.charts_card.set_theme_colors(t["bg_card"], t["border_card"])
        self.card4.set_theme_colors(t["bg_card"], t["border_card"])

        self.c1_head.color = t["accent"]
        self.c3_head.color = t["accent"]
        self.c4_head.color = t["accent"]
        self.lbl_tier_tag.color = t["accent"]
        self.lbl_tier_desc.color = t["text_secondary"]
        self.lbl_tier_sec.color = t["accent_green"]

        for lbl in [self.lbl_in_income, self.lbl_in_savings, self.lbl_in_invest, self.lbl_in_target]:
            lbl.color = t["text_secondary"]

        self.lbl_kpi_row1.color = t["text_primary"]
        self.lbl_kpi_row2.color = t["accent_green"]
        self.lbl_kpi_row3.color = t["text_secondary"]

        self.btn_plan.set_bg_color(t["accent"])
        self.btn_report.set_bg_color(t["accent_green"])
        self.spinner_id.background_color = t["accent"]

        for txt in [self.in_income, self.in_savings, self.in_invest, self.in_target]:
            txt.foreground_color = t["text_input"]
            txt.background_color = t["bg_input"]

        for it in self.expense_widgets:
            it["txt"].foreground_color = t["text_input"]
            it["txt"].background_color = t["bg_input"]
            it["lbl"].color = t["text_primary"]
            it["pct"].color = t["accent"]

        self.refresh_preview()

    def _build_expense_rows(self):
        self.expense_container.clear_widgets()
        self.expense_widgets = []
        t = THEMES[self.current_theme_key]

        all_items = list(PRESET_EXPENSES) + self.custom_items
        for key, name, default_amt, lo, hi, tip in all_items:
            row = BoxLayout(orientation='horizontal', spacing=dp(6), size_hint_y=None, height=dp(34))
            
            cb = CheckBox(size_hint_x=None, width=dp(28))
            row.add_widget(cb)

            lbl_name = Label(text=name, font_size=dp(12), color=t["text_primary"],
                             size_hint_x=None, width=dp(72), halign='left', valign='middle')
            lbl_name.bind(size=lbl_name.setter('text_size'))
            row.add_widget(lbl_name)

            txt_amt = TextInput(text=default_amt, multiline=False, input_filter='float',
                                font_size=dp(12), size_hint=(1, 1), padding=[dp(6), dp(6)],
                                foreground_color=t["text_input"], background_color=t["bg_input"])
            txt_amt.bind(text=self.refresh_preview)
            row.add_widget(txt_amt)

            lbl_pct = Label(text="0%", font_size=dp(11), color=t["accent"],
                            size_hint_x=None, width=dp(45))
            row.add_widget(lbl_pct)

            self.expense_container.add_widget(row)
            self.expense_widgets.append({
                "key": key, "name": name, "lock": cb, "txt": txt_amt,
                "lbl": lbl_name, "pct": lbl_pct, "lo": lo, "hi": hi, "tip": tip
            })

    def lock_all(self, *a):
        for it in self.expense_widgets:
            it["lock"].active = True

    def unlock_all(self, *a):
        for it in self.expense_widgets:
            it["lock"].active = False

    # ==================== 核心计算逻辑 ====================
    def _num(self, txt_widget):
        try:
            return float(txt_widget.text.strip() or 0)
        except Exception:
            return 0.0

    def on_identity_change(self, spinner, text):
        self.apply_identity_defaults(text)
        self.refresh_preview()

    def apply_identity_defaults(self, ident_name):
        if ident_name not in IDENTITY_PRESETS:
            return
        p = IDENTITY_PRESETS[ident_name]
        is_student = (ident_name == "全日制大学生")

        self.in_income.text = p["income"]
        self.in_savings.text = p["savings"]
        self.in_invest.text = p["invest"]
        self.in_target.text = p["target"]
        self.social_mode = p.get("social_mode", "单位代缴")
        self.social_base = float(p.get("social_base", 3800))

        for item in self.expense_widgets:
            default_val = p["defaults"].get(item["key"], "0")
            item["txt"].text = default_val

            if is_student and item["key"] in STUDENT_LOCKED_KEYS:
                item["lock"].active = True
                item["txt"].text = "0"
            elif not is_student:
                item["lock"].active = False

    def compute(self):
        income = self._num(self.in_income)
        ident = self.spinner_id.text
        is_student = (ident == "全日制大学生")
        
        if is_student or self.social_mode == "无社保":
            social_p = 0.0
            social_e = 0.0
            tax = 0.0
        elif self.social_mode == "个人全额自缴":
            social_p = self.social_base * 0.28
            social_e = 0.0
            tax = 0.0
        else: # 单位代缴
            social_p = self.social_base * 0.175
            social_e = self.social_base * 0.283
            taxable = max(0.0, income - social_p - 5000 - self.tax_deduction)
            tax = compute_tax(taxable)

        takehome = max(0.0, income - social_p - tax)
        expenses = {it["key"]: self._num(it["txt"]) for it in self.expense_widgets}
        total_exp = sum(expenses.values())
        surplus = takehome - total_exp
        savings_target = self._num(self.in_target)
        sr = (surplus / takehome) if takehome > 0 else 0.0

        essential = expenses.get("housing", 0) + expenses.get("food", 0)
        flexible = total_exp - essential
        ess_pct = (essential / takehome) if takehome > 0 else 0.0

        return {
            "income": income, "takehome": takehome, "social_p": social_p, "social_e": social_e,
            "tax": tax, "expenses": expenses, "total_exp": total_exp, "surplus": surplus,
            "savings_target": savings_target, "savings_rate": sr,
            "savings": self._num(self.in_savings), "invest": self._num(self.in_invest),
            "essential": essential, "flexible": flexible, "ess_pct": ess_pct
        }

    def refresh_preview(self, *args):
        d = self.compute()
        takehome = d["takehome"]
        tier = get_tier_info(takehome)

        self.lbl_tier_tag.text = tier["tag"]
        self.lbl_tier_desc.text = tier["desc"]
        self.lbl_tier_sec.text = f"{tier['security_level']} ｜ 推荐储蓄: {tier['target_savings_rate']*100:.0f}%"

        self.lbl_kpi_row1.text = f"到手实拿: {fmt(takehome)} 元 ｜ 预算支出: {fmt(d['total_exp'])} 元"
        self.lbl_kpi_row2.text = f"每月净结余: {fmt(d['surplus'])} 元 ｜ 储蓄率: {d['savings_rate']*100:.1f}%"
        self.lbl_kpi_row3.text = f"住房+餐饮刚需: {fmt(d['essential'])} 元（占支配比 {d['ess_pct']*100:.1f}%）"

        for it in self.expense_widgets:
            amt = self._num(it["txt"])
            pct = (amt / takehome * 100) if takehome > 0 else 0
            it["pct"].text = f"{pct:.1f}%"

        # 动态触发图表更新
        if hasattr(self, "charts_widget"):
            chart_exp = {it["name"]: self._num(it["txt"]) for it in self.expense_widgets}
            t = THEMES[self.current_theme_key]
            self.charts_widget.update_data({
                "takehome": takehome, "essential": d["essential"], "flexible": d["flexible"],
                "surplus": d["surplus"], "target": d["savings_target"], "expenses": chart_exp
            }, t)

    def do_smart_plan(self, *args):
        d = self.compute()
        takehome = d["takehome"]
        if takehome <= 0:
            return

        ident = self.spinner_id.text
        is_student = (ident == "全日制大学生")
        tier = get_tier_info(takehome)
        allowed_keys = tier["student_allowed"] if is_student else tier["normal_allowed"]

        rec_target = round(takehome * tier["target_savings_rate"], -1)
        curr_target = self._num(self.in_target)
        if curr_target <= 0 or (curr_target < rec_target * 0.5):
            self.in_target.text = f"{rec_target:.0f}"
            curr_target = rec_target

        for it in self.expense_widgets:
            if is_student and it["key"] in STUDENT_LOCKED_KEYS:
                it["lock"].active = True
                it["txt"].text = "0"
            if allowed_keys is not None and it["key"] not in allowed_keys and self._num(it["txt"]) == 0:
                it["lock"].active = True
                it["txt"].text = "0"

        locked_amt = 0.0
        unlocked = []
        for it in self.expense_widgets:
            if it["lock"].active:
                locked_amt += self._num(it["txt"])
            else:
                unlocked.append(it)

        available = takehome - curr_target - locked_amt
        if available <= 0 or not unlocked:
            self.refresh_preview()
            return

        if takehome <= 3000:
            if is_student:
                w_map = {"food": 0.65, "transport": 0.08, "phone": 0.05, "study": 0.12, "other": 0.10}
            else:
                w_map = {"housing": 0.42, "food": 0.42, "transport": 0.06, "phone": 0.03, "other": 0.07}
        elif takehome <= 5000:
            w_map = {"housing": 0.35, "food": 0.33, "transport": 0.06, "phone": 0.03,
                     "study": 0.06, "fun": 0.05, "shopping": 0.06, "health": 0.03, "drink": 0.02, "other": 0.01}
            if is_student:
                w_map["housing"] = 0.0
                w_map["food"] = 0.52
        elif takehome <= 8000:
            w_map = {"housing": 0.30, "food": 0.25, "transport": 0.05, "phone": 0.02,
                     "study": 0.05, "fun": 0.07, "shopping": 0.06, "beauty": 0.04, "insurance": 0.04,
                     "drink": 0.02, "health": 0.03, "parents": 0.04, "other": 0.03}
        else:
            w_map = {"housing": 0.24, "food": 0.18, "transport": 0.04, "phone": 0.01,
                     "study": 0.04, "fun": 0.07, "shopping": 0.06, "beauty": 0.04,
                     "insurance": 0.05, "parents": 0.06, "drink": 0.02, "travel": 0.05, "other": 0.04}

        weights = {it["key"]: w_map.get(it["key"], 0.02) for it in unlocked}
        sum_w = sum(weights.values()) or 1.0
        for it in unlocked:
            val = available * (weights.get(it["key"], 0.02) / sum_w)
            it["txt"].text = f"{val:.0f}"

        self.refresh_preview()

    # ==================== 专项工具弹窗 (适配主题与字体) ====================
    def show_meal_calculator(self, *a):
        t = THEMES[self.current_theme_key]
        box = CardLayout(bg_color=t["bg_card"], border_color=t["border_card"], radius=14, auto_height=False)
        box.add_widget(DynamicLabel(text="🍚 餐饮一日三餐细分精算器 (自动按30天折算)", font_size=dp(13), bold=True, color=t["accent"]))

        g = GridLayout(cols=2, spacing=dp(6), size_hint_y=None)
        g.bind(minimum_height=g.setter('height'))

        fields = [
            ("早餐(日均元):", "6"),
            ("午餐(日均元):", "15"),
            ("晚餐(日均元):", "15"),
            ("加餐饮品(日均元):", "0"),
            ("周末聚餐(每周元):", "50"),
        ]
        inputs = {}
        for label_text, def_val in fields:
            g.add_widget(Label(text=label_text, font_size=dp(12), color=t["text_secondary"], size_hint_y=None, height=dp(30)))
            ti = TextInput(text=def_val, multiline=False, input_filter='float', font_size=dp(12), size_hint_y=None, height=dp(32),
                           foreground_color=t["text_input"], background_color=t["bg_input"])
            inputs[label_text] = ti
            g.add_widget(ti)

        box.add_widget(g)
        lbl_res = DynamicLabel(text="月度折算总餐饮: 1,280 元", color=t["accent_green"], bold=True, font_size=dp(13))
        box.add_widget(lbl_res)

        def calc_meal(*e):
            b = float(inputs["早餐(日均元):"].text or 0)
            l = float(inputs["午餐(日均元):"].text or 0)
            d = float(inputs["晚餐(日均元):"].text or 0)
            snack = float(inputs["加餐饮品(日均元):"].text or 0)
            wk = float(inputs["周末聚餐(每周元):"].text or 0)
            tot = (b + l + d + snack) * 30 + (wk * 4.3)
            lbl_res.text = f"月度折算总餐饮: {fmt(tot)} 元"
            return tot

        for ti in inputs.values():
            ti.bind(text=calc_meal)

        btn_bar = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(8))
        btn_apply = ModernButton(text="✅ 同步填入月度餐饮", font_size=dp(12), bg_color=t["accent"])
        btn_cancel = ModernButton(text="关闭", font_size=dp(12), bg_color=(0.55, 0.60, 0.68, 1))
        popup = Popup(title="", separator_height=0, content=box, size_hint=(0.92, 0.65), background="", background_color=(0, 0, 0, 0.65))

        def apply_and_close(*e):
            val = calc_meal()
            for it in self.expense_widgets:
                if it["key"] == "food":
                    it["txt"].text = f"{val:.0f}"
                    break
            self.refresh_preview()
            popup.dismiss()

        btn_apply.bind(on_press=apply_and_close)
        btn_cancel.bind(on_press=popup.dismiss)
        btn_bar.add_widget(btn_apply)
        btn_bar.add_widget(btn_cancel)
        box.add_widget(btn_bar)
        popup.open()

    def show_semester_calculator(self, *a):
        t = THEMES[self.current_theme_key]
        box = CardLayout(bg_color=t["bg_card"], border_color=t["border_card"], radius=14, auto_height=False)
        box.add_widget(DynamicLabel(text="🎓 学期大额费用平摊器 (按月折算到固定开销)", font_size=dp(13), bold=True, color=t["accent"]))

        g = GridLayout(cols=2, spacing=dp(6), size_hint_y=None)
        g.bind(minimum_height=g.setter('height'))

        fields = [
            ("学年学费(元):", "5000"),
            ("学年住宿费(元):", "1200"),
            ("寒暑假往返车票(元):", "600"),
            ("教材资料费(元):", "400"),
            ("折算周期(月):", "10"),
        ]
        inputs = {}
        for label_text, def_val in fields:
            g.add_widget(Label(text=label_text, font_size=dp(12), color=t["text_secondary"], size_hint_y=None, height=dp(30)))
            ti = TextInput(text=def_val, multiline=False, input_filter='float', font_size=dp(12), size_hint_y=None, height=dp(32),
                           foreground_color=t["text_input"], background_color=t["bg_input"])
            inputs[label_text] = ti
            g.add_widget(ti)

        box.add_widget(g)
        lbl_res = DynamicLabel(text="每月需分摊准备: 720 元/月", color=t["accent_green"], bold=True, font_size=dp(13))
        box.add_widget(lbl_res)

        def calc_sem(*e):
            t1 = float(inputs["学年学费(元):"].text or 0)
            t2 = float(inputs["学年住宿费(元):"].text or 0)
            t3 = float(inputs["寒暑假往返车票(元):"].text or 0)
            t4 = float(inputs["教材资料费(元):"].text or 0)
            m = max(1.0, float(inputs["折算周期(月):"].text or 10))
            per_m = (t1 + t2 + t3 + t4) / m
            lbl_res.text = f"每月需分摊准备: {fmt(per_m)} 元/月"
            return per_m

        for ti in inputs.values():
            ti.bind(text=calc_sem)

        btn_bar = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(8))
        btn_apply = ModernButton(text="✅ 同步至学习提升项", font_size=dp(12), bg_color=t["accent"])
        btn_cancel = ModernButton(text="关闭", font_size=dp(12), bg_color=(0.55, 0.60, 0.68, 1))
        popup = Popup(title="", separator_height=0, content=box, size_hint=(0.92, 0.65), background="", background_color=(0, 0, 0, 0.65))

        def apply_and_close(*e):
            val = calc_sem()
            for it in self.expense_widgets:
                if it["key"] == "study":
                    it["txt"].text = f"{val:.0f}"
                    break
            self.refresh_preview()
            popup.dismiss()

        btn_apply.bind(on_press=apply_and_close)
        btn_cancel.bind(on_press=popup.dismiss)
        btn_bar.add_widget(btn_apply)
        btn_bar.add_widget(btn_cancel)
        box.add_widget(btn_bar)
        popup.open()

    def show_social_calculator(self, *a):
        t = THEMES[self.current_theme_key]
        box = CardLayout(bg_color=t["bg_card"], border_color=t["border_card"], radius=14, auto_height=False)
        box.add_widget(DynamicLabel(text="🏛️ 五险一金扣缴与个税参数配置", font_size=dp(13), bold=True, color=t["accent"]))

        g = GridLayout(cols=2, spacing=dp(6), size_hint_y=None)
        g.bind(minimum_height=g.setter('height'))

        g.add_widget(Label(text="缴纳方式:", font_size=dp(12), color=t["text_secondary"], size_hint_y=None, height=dp(32)))
        sp_mode = Spinner(text=self.social_mode, values=["无社保", "单位代缴", "个人全额自缴"], font_size=dp(12), size_hint_y=None, height=dp(32),
                          background_color=t["accent"])
        g.add_widget(sp_mode)

        g.add_widget(Label(text="社保公积金基数:", font_size=dp(12), color=t["text_secondary"], size_hint_y=None, height=dp(32)))
        ti_base = TextInput(text=f"{self.social_base:.0f}", multiline=False, input_filter='float', font_size=dp(12), size_hint_y=None, height=dp(32),
                            foreground_color=t["text_input"], background_color=t["bg_input"])
        g.add_widget(ti_base)

        g.add_widget(Label(text="个税专项扣除(元):", font_size=dp(12), color=t["text_secondary"], size_hint_y=None, height=dp(32)))
        ti_deduct = TextInput(text=f"{self.tax_deduction:.0f}", multiline=False, input_filter='float', font_size=dp(12), size_hint_y=None, height=dp(32),
                              foreground_color=t["text_input"], background_color=t["bg_input"])
        g.add_widget(ti_deduct)

        box.add_widget(g)

        btn_bar = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(8))
        btn_apply = ModernButton(text="✅ 保存生效", font_size=dp(12), bg_color=t["accent"])
        btn_cancel = ModernButton(text="关闭", font_size=dp(12), bg_color=(0.55, 0.60, 0.68, 1))
        popup = Popup(title="", separator_height=0, content=box, size_hint=(0.92, 0.55), background="", background_color=(0, 0, 0, 0.65))

        def save_and_close(*e):
            self.social_mode = sp_mode.text
            self.social_base = float(ti_base.text or 0)
            self.tax_deduction = float(ti_deduct.text or 0)
            self.refresh_preview()
            popup.dismiss()

        btn_apply.bind(on_press=save_and_close)
        btn_cancel.bind(on_press=popup.dismiss)
        btn_bar.add_widget(btn_apply)
        btn_bar.add_widget(btn_cancel)
        box.add_widget(btn_bar)
        popup.open()

    def show_add_custom_popup(self, *a):
        t = THEMES[self.current_theme_key]
        box = CardLayout(bg_color=t["bg_card"], border_color=t["border_card"], radius=14, auto_height=False)
        box.add_widget(DynamicLabel(text="➕ 添加自定义月度支出项", font_size=dp(13), bold=True, color=t["accent"]))

        g = GridLayout(cols=2, spacing=dp(6), size_hint_y=None)
        g.bind(minimum_height=g.setter('height'))

        g.add_widget(Label(text="支出名称:", font_size=dp(12), color=t["text_secondary"], size_hint_y=None, height=dp(32)))
        ti_name = TextInput(text="额外分期/还贷", multiline=False, font_size=dp(12), size_hint_y=None, height=dp(32),
                            foreground_color=t["text_input"], background_color=t["bg_input"])
        g.add_widget(ti_name)

        g.add_widget(Label(text="预设金额(元):", font_size=dp(12), color=t["text_secondary"], size_hint_y=None, height=dp(32)))
        ti_amt = TextInput(text="500", multiline=False, input_filter='float', font_size=dp(12), size_hint_y=None, height=dp(32),
                            foreground_color=t["text_input"], background_color=t["bg_input"])
        g.add_widget(ti_amt)

        box.add_widget(g)

        btn_bar = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(8))
        btn_add = ModernButton(text="✅ 确认添加", font_size=dp(12), bg_color=t["accent"])
        btn_cancel = ModernButton(text="取消", font_size=dp(12), bg_color=(0.55, 0.60, 0.68, 1))
        popup = Popup(title="", separator_height=0, content=box, size_hint=(0.88, 0.45), background="", background_color=(0, 0, 0, 0.65))

        def add_and_close(*e):
            name = ti_name.text.strip()
            amt = ti_amt.text.strip() or "0"
            if name:
                key = f"custom_{len(self.custom_items)+1}"
                self.custom_items.append((key, name, amt, 0.0, 0.15, "自定义支出项目"))
                self._build_expense_rows()
                self.refresh_preview()
            popup.dismiss()

        btn_add.bind(on_press=add_and_close)
        btn_cancel.bind(on_press=popup.dismiss)
        btn_bar.add_widget(btn_add)
        btn_bar.add_widget(btn_cancel)
        box.add_widget(btn_bar)
        popup.open()

    def show_wechat_bill_popup(self, *a):
        t = THEMES[self.current_theme_key]
        box = CardLayout(bg_color=t["bg_card"], border_color=t["border_card"], radius=14, auto_height=False)
        box.add_widget(DynamicLabel(text="🧾 微信账单文本识别 (粘贴微信支付文本或账单记录)", font_size=dp(13), bold=True, color=t["accent"]))

        sample_demo = "美团外卖 35.5元\n瑞幸咖啡 14.9元\n滴滴出行 18.0元\n朴朴超市 56.2元\n中国移动话费 50.0元"
        ti_bill = TextInput(text=sample_demo, multiline=True, font_size=dp(12), size_hint=(1, 1),
                            foreground_color=t["text_input"], background_color=t["bg_input"])
        box.add_widget(ti_bill)

        lbl_parse = DynamicLabel(text="点击【智能识别】自动归类餐饮、茶饮、出行、网购等", font_size=dp(12), color=t["accent_green"])
        box.add_widget(lbl_parse)

        parsed_totals = {}

        def parse_text(*e):
            nonlocal parsed_totals
            parsed_totals = {}
            lines = ti_bill.text.split("\n")
            count = 0
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                nums = re.findall(r"(\d+(?:\.\d+)?)", line)
                if nums:
                    val = float(nums[-1])
                    key = "other"
                    for k, n, kws in [
                        ("drink", "烟酒茶饮", ["瑞幸", "咖啡", "奶茶", "蜜雪", "喜茶"]),
                        ("food", "餐饮饮食", ["美团", "饿了么", "快餐", "食堂", "外卖", "面馆"]),
                        ("transport", "交通通勤", ["滴滴", "地铁", "公交", "单车", "出行"]),
                        ("phone", "通讯话费", ["话费", "移动", "联通", "电信"]),
                        ("shopping", "购物网购", ["超市", "淘宝", "京东", "拼多多", "便利店"]),
                    ]:
                        for kw in kws:
                            if kw.lower() in line.lower():
                                key = k
                                break
                    parsed_totals[key] = parsed_totals.get(key, 0.0) + val
                    count += 1
            summary_str = " ｜ ".join([f"{k}:{fmt(v)}元" for k, v in parsed_totals.items()])
            lbl_parse.text = f"✅ 已成功识别 {count} 笔账单！\n汇总: {summary_str}"

        btn_parse = ModernButton(text="🔍 智能分析分类", font_size=dp(12), size_hint_y=None, height=dp(36), bg_color=(0.18, 0.52, 0.88, 1))
        btn_parse.bind(on_press=parse_text)
        box.add_widget(btn_parse)

        btn_bar = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(8))
        btn_sync = ModernButton(text="📥 一键同步到预算表", font_size=dp(12), bg_color=(0.08, 0.62, 0.38, 1))
        btn_cancel = ModernButton(text="关闭", font_size=dp(12), bg_color=(0.55, 0.60, 0.68, 1))
        popup = Popup(title="", separator_height=0, content=box, size_hint=(0.95, 0.75), background="", background_color=(0, 0, 0, 0.65))

        def sync_and_close(*e):
            for k, val in parsed_totals.items():
                for it in self.expense_widgets:
                    if it["key"] == k:
                        it["txt"].text = f"{val:.0f}"
            self.refresh_preview()
            popup.dismiss()

        btn_sync.bind(on_press=sync_and_close)
        btn_cancel.bind(on_press=popup.dismiss)
        btn_bar.add_widget(btn_sync)
        btn_bar.add_widget(btn_cancel)
        box.add_widget(btn_bar)
        popup.open()

    # ==================== 全维安全与财务规划报告生成 (无杂线·纯净排版) ====================
    def generate_security_report(self):
        d = self.compute()
        takehome = d["takehome"]
        tier = get_tier_info(takehome)
        assets = d["savings"] + d["invest"]
        ident = self.spinner_id.text
        p = IDENTITY_PRESETS.get(ident, {})
        em_need = d["total_exp"] * p.get("emergency_months", 2)
        em_gap = max(0.0, em_need - assets)

        L = []
        L.append("🛡️ 个人全维财务与安全规划报告")
        L.append("")
        L.append("【基础档案与现金流概况】")
        L.append(f"• 身份定位：{ident}")
        L.append(f"• 现实特质：{p.get('feature', '')}")
        L.append(f"• 薪资梯队：{tier['tag']}")
        L.append(f"• 到手可用：¥{fmt(takehome)} 元/月")
        L.append(f"• 预算支出：¥{fmt(d['total_exp'])} 元/月")
        L.append(f"• 每月净结余：¥{fmt(d['surplus'])} 元 (实际储蓄率 {d['savings_rate']*100:.1f}%)")
        L.append("")
        L.append("【一、现金流与到手实拿拆解】")
        L.append(f"• 名义税前收入：¥{fmt(d['income'])} 元")
        L.append(f"• 社保个人代扣：-¥{fmt(d['social_p'])} 元 (缴存方式: {self.social_mode})")
        L.append(f"• 个人所得税：-¥{fmt(d['tax'])} 元")
        L.append(f"• 实拿到手净额：¥{fmt(takehome)} 元")
        if d['social_e'] > 0:
            L.append(f"• 单位隐性福利配缴：约 ¥{fmt(d['social_e'])} 元/月")
        L.append("")
        L.append("【二、资金链与三阶蓄水池安全防线】")
        L.append("1. 第一级：日常周转池 (0.5~1个月支出)")
        L.append(f"   存放工具：微信零钱通 / 支付宝余额宝")
        L.append(f"   建议额度：约 ¥{fmt(d['total_exp']*0.5)} ~ ¥{fmt(d['total_exp'])} 元，随用随扣")
        L.append("2. 第二级：刚性应急防线 (2~3个月支出)")
        L.append(f"   安全底线：{p.get('emergency_months', 2)} 个月基础开销 = ¥{fmt(em_need)} 元")
        L.append(f"   当前储备：¥{fmt(assets)} 元")
        if em_gap > 0:
            save_per_m = max(100, d['surplus'])
            m_reach = em_gap / save_per_m
            L.append(f"   补充进度：尚差 ¥{fmt(em_gap)} 元，每月结余填充预计约 {m_reach:.1f} 个月达成！")
        else:
            L.append("   状态评估：应急防线已足额充实，护城河稳固！")
        L.append("3. 第三级：中期缓冲池 (3~6个月支出)")
        L.append("   存放工具：纯债基金 / 稳健低波理财，用于应对换城市、换工作空窗期跨周期抗风险")
        L.append("")
        L.append("【三、零负债与反信贷陷阱红线】")
        L.append("• 铁律准则：普通工薪与新人阶段，消费性负债坚决为 0！")
        L.append("• 揭露套路：免息分期表面手续费 0.6%/期，真实内部收益率(IRR)年化高达 13%~18%")
        L.append("• 杜绝最低还款：日息万五、全额罚息，折合年化高达 18.25%")
        L.append("• 坚决抵制任何网络小贷、借条及高息借贷，切莫以贷养贷")
        L.append("")
        L.append("【四、人身抗风险杠杆防护网】")
        L.append("• 基础兜底：必须参保国家基本医疗保险（职工医保或居民医保）")
        L.append("• 工薪必备核心杠杆：一年期【百万医疗险】")
        L.append("  年保费仅两三百元，享数百万保额，自费药特药100%报销，彻底阻断因病致贫")
        L.append("• 基础防身：一年期【综合意外险】(年费50~100元)")
        L.append("• 避坑提醒：低收入期严禁购买每年数千上万元的返还型终身重疾险，避免断缴损失本金")
        L.append("")
        L.append("【五、资产配置与务实理财分级】")
        L.append(f"• 当前流动总资产：¥{fmt(assets)} 元 (活期存款 ¥{fmt(d['savings'])} 元 + 理财 ¥{fmt(d['invest'])} 元)")
        if assets < 10000:
            L.append("• 阶段定位：活期安全垫筑基期 (总资产 < 1万元)")
            L.append("• 务实方案：100% 保持高流动性活期 (零钱通/余额宝)，严禁炒股与盲目定投，专心防身与开源！")
        elif assets < 50000:
            L.append("• 阶段定位：稳健防守积累期 (1万~5万元)")
            L.append("• 务实方案：60% 活期备用金 + 40% 低波纯债基金/同业存单，保本不亏、随时可取")
        else:
            L.append("• 阶段定位：多元资产配置期 (≥5万元)")
            L.append("• 务实方案：本金已初具规模，启动现金、纯债、宽基指数ETF定投及黄金的多元配置")
        return "\n".join(L)

    def show_report_popup(self, *args):
        report_text = self.generate_security_report()
        t = THEMES[self.current_theme_key]

        content = CardLayout(bg_color=t["bg_card"], border_color=t["border_card"], radius=14, auto_height=False)
        content.size_hint = (1, 1)

        top_box = BoxLayout(size_hint_y=None, height=dp(36))
        lbl_p_title = Label(text="🛡️ 全维安全与财务规划报告", font_size=dp(15), bold=True,
                            color=t["accent"], halign='left')
        lbl_p_title.bind(size=lbl_p_title.setter('text_size'))
        top_box.add_widget(lbl_p_title)
        content.add_widget(top_box)

        # 报告文本展示区域（大字号 dp(13.5) 高对比度）
        sv = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        lbl_rpt = DynamicLabel(text=report_text, font_size=dp(13.5), color=t["text_primary"])
        sv.add_widget(lbl_rpt)
        content.add_widget(sv)

        btn_bar = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(10))
        btn_copy = ModernButton(text="📋 一键复制完整报告", font_size=dp(13), bold=True,
                                bg_color=t["accent"], color=(1, 1, 1, 1))
        btn_close = ModernButton(text="关闭", font_size=dp(13),
                                 bg_color=(0.55, 0.60, 0.68, 1), color=(1, 1, 1, 1))

        popup = Popup(title="", separator_height=0, content=content,
                      size_hint=(0.95, 0.90), background="", background_color=(0, 0, 0, 0.65))

        def copy_and_toast(instance):
            Clipboard.copy(report_text)
            btn_copy.text = "✅ 已复制到手机剪贴板！"

        btn_copy.bind(on_press=copy_and_toast)
        btn_close.bind(on_press=popup.dismiss)
        btn_bar.add_widget(btn_copy)
        btn_bar.add_widget(btn_close)
        content.add_widget(btn_bar)

        popup.open()


if __name__ == "__main__":
    FinancePlannerApp().run()
