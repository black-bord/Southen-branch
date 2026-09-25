# 个人财务与安全规划系统 · 安卓移动端开发与打包指南

本项目已针对安卓移动设备进行深度 UI 优化与触控重构，采用原生跨平台移动框架 **Kivy** 开发，支持直接在手机端运行，也可以通过 **Buildozer** 编译为独立 `.apk` 安装包。

---

## 📱 手机端 UI 优化特色

1. **竖屏流式自适应**：
   - 适配各类安卓手机屏幕长宽比（19.5:9, 20:9 等），支持纵向丝滑手势滚动。
2. **大触控热区与蓝白现代卡片**：
   - 按钮高度与输入框按移动端交互标准（≥ 40dp）设计，单手触控轻松点击。
   - 保留深海科技蓝 Header 与浅冰蓝（#f0f7ff）舒适背景，视觉干净轻盈。
3. **分阶安全防御模型集成**：
   - 包含资金链三阶蓄水池、零负债防线、人身保险杠杆与阶梯资产配置。
   - 生成的规划报告支持 **一键复制到手机系统剪贴板**，方便发给家人或粘贴到备忘录。

---

## 🚀 三种运行与打包方案

### 方案一：手机端直接免打包运行（推荐最快体验方式，1分钟搞定）
如果您不想在电脑配置繁重的 Android SDK/NDK 编译链，直接在手机上运行体验：
1. 在安卓手机的应用商店（或酷安 / Google Play）下载安装 **Pydroid 3**（一款强大的安卓端 Python IDE）。
2. 打开 Pydroid 3，点击左侧菜单 -> **Pip** -> 搜索并安装 `kivy`。
3. 将本项目 `android_app/main.py` 传输到手机中（可通过微信传输助手、数据线或网盘）。
4. 在 Pydroid 3 中打开 `main.py`，点击右下角黄色的 **运行按钮 (▶)**，即可立刻在手机屏幕上全屏运行！

---

### 方案二：GitHub Actions 免费云端一键编译成 APK（无需本地环境，最省心）
利用 GitHub 提供的免费 Ubuntu 云服务器自动打包，免去本地安装几百兆环境的痛苦：
1. 将本代码推送到您的 GitHub 仓库。
2. 仓库根目录下包含我们预先写好的 `.github/workflows/build_apk.yml`。
3. 在 GitHub 网页端点击 **Actions** 标签页，触发 **Build Android APK** 工作流。
4. 等待 3~5 分钟编译完成后，直接在页面底部的 **Artifacts** 点击下载编译好的 `.apk` 安装包传输到手机安装即可！

---

### 方案三：本地环境通过 Buildozer 打包 APK（标准开发者方案）

> **注意**：Android NDK/SDK 编译链仅支持 Linux 或 macOS。在 Windows 上推荐使用 **WSL (Ubuntu)**。

#### 1. 准备 WSL (Ubuntu) 环境
在 Windows 终端中安装并启动 Ubuntu：
```bash
wsl --install
# 安装完成后进入 Ubuntu 终端
```

#### 2. 安装系统底层依赖
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev cython3
```

#### 3. 安装 Buildozer
```bash
pip3 install --user --upgrade buildozer cython==0.29.36
export PATH=$PATH:~/.local/bin
```

#### 4. 进入项目目录并开始打包
```bash
cd /mnt/e/Code/杂七杂八/android_app
buildozer -v android debug
```
> **首次打包说明**：Buildozer 会自动下载并解压 Android SDK 和 NDK（约需 5~10 分钟），请保持网络畅通。

#### 5. 获取 APK
打包完成后，生成的安装包位于：
```bash
android_app/bin/financeplanner-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
```
将该 `.apk` 文件通过微信或数据线发到安卓手机上即可直接点击安装运行！
