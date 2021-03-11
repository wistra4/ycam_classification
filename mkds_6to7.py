# mkds_4to7
import os
import glob
isx_list = []
idx_set = set()
ds_file = "/.DS_Store" # ds_storeディレクトリ名

b_path = "./targets" # baseパス
if os.path.exists(b_path + ds_file): # DS_Storeファイルを消去
    os.remove(b_path + ds_file)
    print("DS_File was removed.")
datas = os.listdir(b_path)
print(datas)
for data in datas:
    c_idx = data.split("_")[2].split(".")[0]
    if c_idx in idx_set:
        print("ft")
    else:
        idx_set.add(c_idx)
print(idx_set)
print(len(idx_set))
