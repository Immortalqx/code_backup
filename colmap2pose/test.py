import json
import numpy as np

gt_file = "gt_xyz.json"
colmap_file = "colmap_xyz.json"

# ====================== 打开json文件 ======================
with open(gt_file) as f1:
    gt_data = json.load(f1)
with open(colmap_file) as f2:
    colmap_data = json.load(f2)

# ====================== 获取frames信息 ======================
gt_frames = gt_data["frames_with_xyz"]
colmap_frames = colmap_data["frames"]

# 为了方便查询，构建一个不一样的字典
gt_pose = {}
for gt_frame in gt_frames:
    gt_pose[gt_frame["idx"]] = gt_frame["xyz"]

# 先把对应的XYZ坐标取出来
gt_XYZ = []
colmap_XYZ = []
for colmap_frame in colmap_frames:
    gt_XYZ.append(gt_pose[colmap_frame["idx"]])
    colmap_XYZ.append(colmap_frame["xyz"])

gt_XYZ = np.array(gt_XYZ)
colmap_XYZ = np.array(colmap_XYZ)

# 设置打印的信息
np.set_printoptions(threshold=np.inf)
np.set_printoptions(suppress=True)

# 打印坐标的误差
print(gt_XYZ - colmap_XYZ)
