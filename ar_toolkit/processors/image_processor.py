import cv2
from ar_toolkit.core.detector import ARDetector
from ar_toolkit.core.overlay_image import OverlayImage
from ar_toolkit.core.overlay_3d import Overlay3D

class ImageProcessor:
    def __init__(self, overlay_image_path=None, use_3d=False):
        """
        初始化图像处理器
        
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

    def process_image(self, image_path, output_path=None):
        """
        处理单张图片
        
        Args:
            image_path: 输入图片路径
            output_path: 输出图片路径，默认为None（不保存结果）
            
        Returns:
            numpy.ndarray: 处理后的图片
        """
        # 读取图片
        image = cv2.imread(str(image_path))
        if image is None:
            print(f"无法加载图片: {image_path}")
            return None

        # 处理图片
        result = self.process_frame(image)
        
        # 保存结果
        if result is not None and output_path:
            cv2.imwrite(str(output_path), result)
            print(f"结果已保存至: {output_path}")
            
        return result

    def process_frame(self, frame):
        """
        处理单帧图像
        
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
