import cv2
from pathlib import Path

def generate_aruco_marker(output_path='aruco_marker.png', marker_id=0, marker_size=512, dict_type=cv2.aruco.DICT_6X6_250):
    """
    生成 ArUco 标记并保存
    
    参数:
        output_path (str): 输出文件路径
        marker_id (int): 标记ID
        marker_size (int): 标记大小(像素)
        dict_type: ArUco 字典类型
    """
    # 创建 ArUco 字典
    aruco_dict = cv2.aruco.getPredefinedDictionary(dict_type)
    
    # 生成标记
    marker_image = aruco_dict.generateImageMarker(marker_id, marker_size)
    
    # 确保输出目录存在
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 保存标记
    cv2.imwrite(str(output_path), marker_image)
    print(f"ArUco 标记已保存为 '{output_path}'")
