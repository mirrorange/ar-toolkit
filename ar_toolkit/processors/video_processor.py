import cv2
from tqdm import tqdm
from ar_toolkit.core.detector import ARDetector
from ar_toolkit.core.overlay_image import OverlayImage
from ar_toolkit.core.overlay_3d import Overlay3D

class VideoProcessor:
    def __init__(self, overlay_image_path=None, use_3d=False):
        """
        初始化视频处理器
        
        Args:
            use_3d: 是否使用3D模型渲染
        """
        self.detector = ARDetector()
        self.use_3d = use_3d
        self.overlay = Overlay3D() if use_3d else OverlayImage()
        if not self.use_3d:
            if overlay_image_path is None:
                raise ValueError("图片叠加时，图片路径不能为空")
            self.overlay.load_image(overlay_image_path)

    def process_frame(self, frame):
        """
        处理单帧视频
        
        Args:
            frame: OpenCV图像对象
            
        Returns:
            numpy.ndarray: 处理后的图像
        """
        if frame is None:
            return None
            
        # 检测标记
        corners, ids = self.detector.detect(frame)
        
        # 如果检测到标记，进行渲染
        if ids is not None:
            frame = self.overlay.apply(frame, corners)
            
        return frame

    def process_video(self, source=0, output_path=None, show_preview=True):
        """
        处理视频流或视频文件
        
        Args:
            source: 视频源（摄像头索引或视频文件路径），默认为0（默认摄像头）
            output_path: 输出视频文件路径，默认为None（不保存结果）
            show_preview: 是否显示预览窗口，默认为True
            
        Returns:
            bool: 处理是否成功完成
        """
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            print(f"无法打开视频源: {source}")
            return False

        # 如果需要保存视频，设置VideoWriter
        video_writer = None
        if output_path:
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

        # 获取视频总帧数
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_count = 0
        
        try:
            # 创建进度条
            with tqdm(total=total_frames, desc="处理视频") as pbar:
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    processed_frame = self.process_frame(frame)
                    if processed_frame is None:
                        break

                    # 保存处理后的帧
                    if video_writer:
                        video_writer.write(processed_frame)

                    # 显示预览
                    if show_preview:
                        cv2.imshow('AR View', processed_frame)
                        # 按'q'退出
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

                    frame_count += 1
                    pbar.update(1)

        finally:
            cap.release()
            if video_writer:
                video_writer.release()
            if show_preview:
                cv2.destroyAllWindows()

        if output_path:
            print(f"共处理 {frame_count} 帧，结果已保存至: {output_path}")
        
        return True

