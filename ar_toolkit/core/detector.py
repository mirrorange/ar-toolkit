import cv2

class ARDetector:
    def __init__(self):
        """初始化AR检测器"""
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        self.aruco_params = cv2.aruco.DetectorParameters()

    def detect(self, frame):
        """
        检测图像中的ArUco标记
        
        Args:
            frame: OpenCV图像对象(numpy.ndarray)
            
        Returns:
            tuple: (corners, ids)
                - corners: 检测到的标记角点列表
                - ids: 检测到的标记ID列表
        """
        if frame is None:
            return None, None
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _rejected = cv2.aruco.detectMarkers(
            gray, self.aruco_dict, parameters=self.aruco_params
        )
        return corners, ids
