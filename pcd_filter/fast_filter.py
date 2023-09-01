import os
import open3d as o3d
import numpy as np

# ======================== 创建坐标轴阈值 ========================
LIMITS = {
    "x_up": 0,
    "x_low": -1.0,
    "y_up": -0.9,
    "y_low": -1.9,
    "z_up": 50,
    "z_low": 45
}

def filter_points(point_cloud):
    """
    输入open3d读入的pcd点云数据point_cloud，输出指定方框内的点云point_cloud_filtered
    """
    points_array = np.asarray(point_cloud.points)

    x = points_array[:, 0]
    y = points_array[:, 1]
    z = points_array[:, 2]

    field_x1 = x < LIMITS["x_up"]
    field_x2 = x > LIMITS["x_low"]
    field_y1 = y < LIMITS["y_up"]
    field_y2 = y > LIMITS["y_low"]
    field_z1 = z < LIMITS["z_up"]
    field_z2 = z > LIMITS["z_low"]

    field = np.logical_and(field_x1, field_x2)
    field = np.logical_and(field, np.logical_and(field_y1, field_y2))
    field = np.logical_and(field, np.logical_and(field_z1, field_z2))
    points_array = points_array[field, :]

    point_cloud_filtered = o3d.geometry.PointCloud()
    point_cloud_filtered.points = o3d.utility.Vector3dVector(points_array)

    return point_cloud_filtered


def filter_dir(file_path):
    filelist = [os.path.join(file_path, f) for f in os.listdir(file_path)]
    for dir in filelist:
        m_filelist = [os.path.join(dir, f) for f in os.listdir(dir)]
        for pcd_file in m_filelist:
            point = o3d.io.read_point_cloud(pcd_file)
            point_filtered = filter_points(point)
            #o3d.visualization.draw_geometries([point_filtered])
            o3d.io.write_point_cloud(pcd_file.split(".")[0] + "_filtered.pcd", point_filtered, write_ascii=True)


def bin_asc(file_path):
    filelist = [os.path.join(file_path, f) for f in os.listdir(file_path)]
    for dir in filelist:
        m_filelist = [os.path.join(dir, f) for f in os.listdir(dir)]
        for pcd_file in m_filelist:
            point = o3d.io.read_point_cloud(pcd_file)
            o3d.io.write_point_cloud(pcd_file, point, write_ascii=True)


if __name__ == "__main__":
    filter_dir("data/10")
    # bin_asc("data")
