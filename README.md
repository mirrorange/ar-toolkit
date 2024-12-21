# AR Toolkit

*本项目是 2024 年深圳大学计算机视觉课程的课程设计项目。*

AR Toolkit 是一个简单易用的增强现实工具，支持图像和视频的 AR 效果处理。

## 功能特点

- 支持图片和视频文件的 AR 处理
- 支持实时摄像头输入
- 可叠加 2D 图片或渲染 3D 立方体
- 内置 ArUco 标记生成器

## 安装

```bash
git clone https://github.com/mirrorange/ar-toolkit.git
cd ar-toolkit
pip install -r requirements.txt
```

## 使用方法

### 生成 ArUco 标记

生成用于 AR 识别的 ArUco 标记：

```bash
ar-toolkit generate [-o 输出路径] [-i 标记ID] [-s 标记大小]
```

参数说明：
- `-o, --output`：输出文件路径（默认：aruco_marker.png）
- `-i, --id`：标记 ID（默认：0）
- `-s, --size`：标记大小，以像素为单位（默认：512）

示例：
```bash
ar-toolkit generate -o marker.png -i 1 -s 1024
```

### 处理 AR 效果

处理图片、视频或摄像头输入：

```bash
ar-toolkit process 输入源 [--output 输出路径] [--overlay 叠加图片] [--3d]
```

参数说明：
- `输入源`：可以是图片路径、视频文件路径或摄像头索引（整数）
- `-o, --output`：输出文件路径（可选）
- `-ov, --overlay`：要叠加的图片路径
- `--3d`：启用 3D 模型渲染模式

示例：
```bash
# 处理图片
ar-toolkit process input.jpg -o output.jpg --overlay overlay.png

# 处理视频
ar-toolkit process input.mp4 -o output.mp4 --overlay logo.png

# 使用摄像头（实时预览）
ar-toolkit process 0 --overlay overlay.png

# 渲染 3D 立方体
ar-toolkit process input.jpg --3d
```
