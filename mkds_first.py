# mkds_2to3
import os

ds_file = "/.DS_Store" # ds_storeディレクトリ名
p_nums = []

b_path = "./dataset" # baseパス
# print(b_path)
if os.path.exists(b_path + ds_file): # DS_Storeファイルを消去
    os.remove(b_path + ds_file)
    # print("DS_File was removed.")
c_dirs= os.listdir(b_path) # classディレクトリを抽出
# print(c_dirs)

for c_dir in c_dirs:
    c_path = b_path + "/" + c_dir # classパス
    c_num = c_dir.split("_")[0]
    # print(c_num)
    # print(c_path)
    if os.path.exists(c_path + ds_file): # DS_Storeファイルを消去
        os.remove(c_path + ds_file)
        # print("DS_File was removed.")
    g_dirs = os.listdir(c_path) # genusディレクトリを抽出
    # print(g_dirs)

    for g_dir in g_dirs:
        g_path = c_path + "/" + g_dir # genusパス
        g_num = c_num + g_dir.split("_")[0]
        # print(g_path)
        # print(g_num)
        if os.path.exists(g_path + ds_file): # DS_Storeファイルを消去
            os.remove(g_path + ds_file)
            # print("DS_File was removed.")
        s_dirs = os.listdir(g_path) # speciesディレクトリを抽出
        # print(s_dirs)

        for s_dir in s_dirs:
            s_path = g_path + "/" + s_dir # speciesパス
            s_num = g_num + s_dir.split("_")[0]
            # print(s_num)
            # print(s_path)
            if os.path.exists(s_path + ds_file): # DS_Storeファイルを消去
                os.remove(s_path + ds_file)
                # print("DS_File was removed.")
            d_files = os.listdir(s_path) # dataファイルを抽出
            # print(d_files)
            d_num = 1

            for d_file in d_files:
                before_path = s_path + "/" + d_file
                if d_num <= 9:
                    d_numstr = "0" + str(d_num)
                elif 10 <= d_num:
                    d_numstr = str(d_num)
                p_num = s_num + d_numstr
                d_num += 1
                after_path = s_path + "/" + p_num + d_file[-4:]
                # print(p_num)
                # print("before_path:" + before_path)
                # print("after_path:" + after_path)
                os.rename(before_path, after_path)
                p_nums.append(p_num)
# print(p_nums)
print(len(p_nums))