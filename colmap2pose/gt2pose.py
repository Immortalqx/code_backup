import json

gt_file = "data/gt_pos.dat"
# ====================== 读取ground truth ======================
f = open(gt_file)
lines = f.read().split("\n")[:-1]

gt_pose = []
for line in lines:
    line = line.split("\t")
    idx = int(line[0].split("C")[-1].split(".")[0])
    xyz = [float(line[2]), float(line[3]), float(line[4])]
    gt_pose.append(
        {
            "idx": idx,
            "xyz": xyz
        }
    )
gt_pose = sorted(gt_pose, key=lambda e: e.__getitem__('idx'))

# 保存处理好的gt_pose到文件中
gt_pose_IDXYZ = open("gt_xyz.json", mode='w')
json.dump({"frames_with_xyz": gt_pose}, gt_pose_IDXYZ, indent=4)
