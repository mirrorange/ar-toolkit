import cv2
import argparse
from pathlib import Path
from ar_toolkit.processors.image_processor import ImageProcessor
from ar_toolkit.processors.video_processor import VideoProcessor
from ar_toolkit.utils import generate_aruco_marker

def process_ar(args):
    """处理 AR 视觉任务"""
    overlay_path = Path(args.overlay) if args.overlay else None
    input_source = args.input
    output_path = args.output
    use_3d = args.use_3d

    if overlay_path is None and not use_3d:
        raise ValueError("图片叠加时，图片路径不能为空")

    # 尝试将input_source转换为摄像头索引
    try:
        camera_idx = int(input_source)
        # 使用视频处理器处理摄像头输入
        processor = VideoProcessor(use_3d=use_3d, overlay_image_path=overlay_path)
        processor.process_video(camera_idx, output_path)
        return
        
    except ValueError:
        pass

    # 处理文件输入
    input_path = Path(input_source)
    
    # 根据文件扩展名判断处理方式
    if input_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
        # 处理图片
        processor = ImageProcessor(overlay_image_path=overlay_path, use_3d=use_3d)
        result = processor.process_image(input_path, output_path)
        if result is not None and output_path is None:
            # 如果没有指定输出路径，显示结果
            cv2.imshow('AR Result', result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
    elif input_path.suffix.lower() in ['.mp4', '.avi', '.mov']:
        # 处理视频文件
        processor = VideoProcessor(use_3d=use_3d, overlay_image_path=overlay_path)
        # 如果指定了输出路径，则不显示预览
        processor.process_video(str(input_path), output_path, show_preview=output_path is None)
    else:
        print(f"不支持的文件类型: {input_path.suffix}")

def generate_marker(args):
    """生成 ArUco 标记"""
    generate_aruco_marker(
        output_path=args.output,
        marker_id=args.id,
        marker_size=args.size
    )

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='AR 工具包命令行工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # AR 处理子命令
    process_parser = subparsers.add_parser('process', help='处理 AR 视觉任务')
    process_parser.add_argument('input', help='输入源 (图片/视频文件路径或摄像头索引)')
    process_parser.add_argument('--output', '-o', help='输出文件路径')
    process_parser.add_argument('--overlay', '-ov', help='叠加图片路径')
    process_parser.add_argument('--3d', dest='use_3d', action='store_true',
                             help='使用3D模型渲染 (默认: False)')
    
    # 标记生成子命令
    marker_parser = subparsers.add_parser('generate', help='生成 ArUco 标记')
    marker_parser.add_argument('--output', '-o', default='aruco_marker.png',
                             help='输出文件路径 (默认: aruco_marker.png)')
    marker_parser.add_argument('--id', '-i', type=int, default=0,
                             help='标记 ID (默认: 0)')
    marker_parser.add_argument('--size', '-s', type=int, default=512,
                             help='标记大小，以像素为单位 (默认: 512)')
    
    args = parser.parse_args()
    
    if args.command == 'process':
        process_ar(args)
    elif args.command == 'generate':
        generate_marker(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
