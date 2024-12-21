import cv2
import numpy as np

class Overlay3D:
    def __init__(self, camera_matrix=None, dist_coeffs=None, marker_length=0.05):
        """
        初始化 3D 渲染器
        
        Args:
            camera_matrix (numpy.ndarray): 相机内参矩阵 (3x3)，若不传则自动估计
            dist_coeffs (numpy.ndarray):   畸变系数，默认为 None（假设无畸变）
            marker_length (float):         标记的边长（单位可自行定义，比如米），默认为 0.05
        """
        self.camera_matrix = camera_matrix
        self.dist_coeffs = dist_coeffs if dist_coeffs is not None else np.zeros((4, 1))
        self.marker_length = marker_length

    def _estimate_camera_matrix(self, frame):
        """
        在未提供相机内参时，根据图像大小进行简单估计。
        """
        h, w = frame.shape[:2]
        # 简单假设焦距与图像最大尺寸成比例
        focal_length = max(h, w)
        # 光心估计为图像中心
        cx, cy = w / 2, h / 2
        camera_matrix = np.array([
            [focal_length, 0,            cx],
            [0,            focal_length, cy],
            [0,            0,            1 ]
        ], dtype=np.float32)
        return camera_matrix

    def _draw_cube(self, frame, projected_points):
        """
        根据投影到图像上的 8 个顶点坐标绘制立方体
        Args:
            frame (numpy.ndarray): 当前图像帧
            projected_points (list/ndarray): 立方体 8 个顶点投影后的 2D 坐标
        """
        # 定义立方体 12 条边在顶点列表中的匹配关系
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # 底面
            (4, 5), (5, 6), (6, 7), (7, 4),  # 顶面
            (0, 4), (1, 5), (2, 6), (3, 7)   # 侧面连线
        ]
        
        for (start, end) in edges:
            pt1 = tuple(projected_points[start].ravel().astype(int))
            pt2 = tuple(projected_points[end].ravel().astype(int))
            cv2.line(frame, pt1, pt2, (255, 0, 0), 5)

    def apply(self, frame, corners):
        """
        在检测到的标记平面上渲染立方体
        
        Args:
            frame (numpy.ndarray): 原始图像帧
            corners (list): 检测到的标记角点列表
        
        Returns:
            numpy.ndarray: 在标记平面渲染了 3D 模型后的图像
        """
        # 若未提供相机内参，则尽量根据画面尺寸做一个粗略估计
        if self.camera_matrix is None:
            self.camera_matrix = self._estimate_camera_matrix(frame)
        
        # 绘制一个立方体
        # 立方体的底面与标记平面重合，高度与边长相同
        cube_points_3d = np.array([
            [0, 0, 0],
            [self.marker_length, 0, 0],
            [self.marker_length, self.marker_length, 0],
            [0, self.marker_length, 0],

            [0, 0, -self.marker_length],
            [self.marker_length, 0, -self.marker_length],
            [self.marker_length, self.marker_length, -self.marker_length],
            [0, self.marker_length, -self.marker_length]
        ], dtype=np.float32)

        # 标记平面的 3D 角点（与 marker_length 对应），用于 solvePnP
        obj_points_3d = np.array([
            [0, 0, 0],
            [self.marker_length, 0, 0],
            [self.marker_length, self.marker_length, 0],
            [0, self.marker_length, 0]
        ], dtype=np.float32)

        # 对于每个检测到的标记
        for corner in corners:
            # corner 的维度通常是 (1, 4, 2)
            # 取其中 (4,2) 的数组
            image_points_2d = corner[0].astype(np.float32)

            # solvePnP：计算旋转向量 rvec、平移向量 tvec
            success, rvec, tvec = cv2.solvePnP(
                obj_points_3d,
                image_points_2d,
                self.camera_matrix,
                self.dist_coeffs,
                flags=cv2.SOLVEPNP_ITERATIVE
            )

            if not success:
                continue

            # 将 3D 立方体的 8 个顶点投影到 2D，得到像素坐标
            projected_points_2d, _ = cv2.projectPoints(
                cube_points_3d,
                rvec,
                tvec,
                self.camera_matrix,
                self.dist_coeffs
            )

            # 在 frame 上绘制立方体
            self._draw_cube(frame, projected_points_2d)

        return frame