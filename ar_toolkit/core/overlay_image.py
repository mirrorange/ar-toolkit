import cv2
import numpy as np

class OverlayImage:
    def __init__(self):
        """初始化图像叠加器"""
        self.overlay_img = None
        self.overlay_size = (0, 0)

    def load_image(self, image_path):
        """
        加载要叠加的图片
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            bool: 加载是否成功
        """
        try:
            overlay = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
            if overlay is None:
                raise FileNotFoundError(f"无法加载图片: {image_path}")
            
            # 处理带alpha通道的图片
            if overlay.shape[2] == 4:
                alpha = overlay[:, :, 3]
                overlay = overlay[:, :, :3]
                alpha = alpha / 255.0
                overlay = overlay * alpha[:, :, np.newaxis]
                overlay = overlay.astype(np.uint8)

            h, w = overlay.shape[:2]
            self.overlay_img = overlay
            self.overlay_size = (w, h)
            return True
            
        except Exception as e:
            print(f"加载图片时出错: {e}")
            return False

    def apply(self, frame, corners):
        """
        在检测到的标记位置叠加图片
        
        Args:
            frame: 原始图像帧
            corners: 检测到的标记角点列表
            
        Returns:
            numpy.ndarray: 叠加后的图像
        """
        if self.overlay_img is None:
            return frame

        frame_copy = frame.copy()
        
        for corner in corners:
            # 获取标记的四个角点
            pts = corner.reshape((4, 2))
            
            # 计算透视变换矩阵
            target_pts = np.array([
                [0, 0],
                [self.overlay_size[0], 0],
                [self.overlay_size[0], self.overlay_size[1]],
                [0, self.overlay_size[1]]
            ], dtype=np.float32)
            
            matrix = cv2.getPerspectiveTransform(target_pts, pts)
            
            # 对叠加图片进行透视变换
            overlay_warped = cv2.warpPerspective(
                self.overlay_img,
                matrix,
                (frame.shape[1], frame.shape[0])
            )
            
            # 创建遮罩
            mask = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)
            pts = pts.astype(np.int32)
            cv2.fillPoly(mask, [pts], 255)
            
            # 在原始帧上叠加变换后的图片
            mask = mask / 255.0
            frame_copy = frame_copy * (1 - mask[:, :, np.newaxis]) + overlay_warped * mask[:, :, np.newaxis]
            
        return frame_copy.astype(np.uint8)
