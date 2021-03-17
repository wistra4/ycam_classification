# mkds_4to7
import os
import glob
import pydub
from pydub import AudioSegment
import math
import librosa
import soundfile as sf
import random
import csv

ds_file = "/.DS_Store" # ds_storeディレクトリ名
p_nums = []
c_dic = {}

b_path = "./master/audio" # baseパス
# print(b_path)
if os.path.exists(b_path + ds_file): # DS_Storeファイルを消去
    os.remove(b_path + ds_file)
    # print("DS_File was removed.")
c_dirs= os.listdir(b_path) # classディレクトリを抽出
# print(c_dirs)
f_num = 1
# ここにCSV書き込み用のディクショナリ生成とクラス番号割り振りのコードを作る
for c_dir in c_dirs:
    before_path = b_path + "/" + c_dir
    if f_num <= 9:
        f_numstr = "0" + str(f_num)
    elif 10 <= f_num:
        f_numstr = str(f_num)
    f_num += 1
    after_path = b_path + "/" + f_numstr + "_" + c_dir.split("_")[1]
    # print(after_path)
    os.rename(before_path, after_path)

c_dirs= os.listdir(b_path)
for c_dir in c_dirs:
    c_path = b_path + "/" + c_dir # classパス
    c_num = c_dir.split("_")[0]
    c_category = c_dir.split("_")[1]
    c_dic[c_num] = c_category
    # print(c_num)
    # print(c_path)
    if os.path.exists(c_path + ds_file): # DS_Storeファイルを消去
        os.remove(c_path + ds_file)
        # print("DS_File was removed.")
    d_files = os.listdir(c_path) # genusディレクトリを抽出
    # print(d_files)
    
    for d_file in d_files:
        before_path = c_path + "/" + d_file
        if c_num[0] == "0":
            p_num = d_file.split(".")[0] + "_" + c_num[1:]
            # print(p_num + "if")
        else:
            p_num = d_file.split(".")[0] + "_" + c_num
            # print(p_num)
        after_path = b_path + "/" + p_num + d_file[-4:]

        # print("before_path:" + before_path)
        # print("after_path:" + after_path)
        os.rename(before_path, after_path)
        p_nums.append(p_num)

for c_dir in c_dirs:
    c_path = b_path + "/" + c_dir # classパス
    os.rmdir(c_path)

# print(p_nums)
# print(len(p_nums))

# 10分のファイルまで耐えるscript40行辺りまでで一度検証しても良い

# print(b_path)
if os.path.exists(b_path + ds_file): # DS_Storeファイルを消去
    os.remove(b_path + ds_file)
    print("DS_File was removed.")

mp3_paths= glob.glob(b_path + "/*.mp3") # mp3ファイルを抽出
# print(mp3_paths)
# print(len(mp3_paths))
for mp3_path in mp3_paths:
    # print(mp3_path)
    mp3_file = pydub.AudioSegment.from_mp3(mp3_path)
    mp3_file.export("."+mp3_path.split(".")[1]+".wav", format="wav")
    os.remove(mp3_path)

wav_dirs = os.listdir(b_path)
for wav_dir in wav_dirs:
    wav_path = b_path + "/" + wav_dir 
    # print(wav_dir)

    wav_file = AudioSegment.from_file(wav_path, "wav")

    time = wav_file.duration_seconds # 再生時間(秒)
    rate = wav_file.frame_rate  # サンプリングレート(Hz)
    channel = wav_file.channels  # チャンネル数(1:mono, 2:stereo)
    splits = math.floor(time/5.0)
    # print('再生時間：', time)
    # print("分割数 : ", splits)
    # print("サンプリングレート：")
    # print('チャンネル数：', channel)

    # sampling_rataを44100に変更
    if rate != 44100:
        y, sr = librosa.core.load(wav_path, sr=44100, mono=True)
        sf.write(wav_path, y, sr, subtype="PCM_16")
        wav_file = AudioSegment.from_file(wav_path, "wav")
        channel = wav_file.channels

    # monoをstereoに変更
    if channel != 2:
        wav_file = wav_file.set_channels(2)
        wav_file.export(wav_path, format="wav")
        wav_file = AudioSegment.from_file(wav_path, "wav")

    # take_alphaを付与
    num2alpha = {1:"A", 2:"B", 3:"C", 4:"D", 5:"E", 6:"F", 7:"G", 8:"H", 9:"I", 10:"J", 11:"K", 12:"L", 13:"M", 14:"N", 15:"O", 16:"P", 17:"Q", 18:"R", 19:"S", 20:"T", 21:"U", 22:"V", 23:"W", 24:"X", 25:"Y", 26:"Z"}
    for split in range(1, splits+1):
        cut_start = (split-1)*5000
        cut_end = split*5000
        wav_cut = wav_file[cut_start:cut_end]
        if split <= 26:
            take = num2alpha[split]
        elif 26 < split <= 52:
            split52 = split - 26
            take = num2alpha[split52]*2
        elif 52 < split <= 78:
            split78 = split - 52
            take = num2slpha[split78]**3
        elif 78 < split <= 104:
            split104 = split - 78
            take = num2alpha[split104]**4
        elif 104 < split <= 130:
            split130 = split - 104
            take = num2alpha[split130]**5
        take_path = b_path + "/" + wav_dir.split("_")[0] + "_" + take + "_" + wav_dir.split("_")[1]
        wav_cut.export(take_path, format="wav")

    os.remove(wav_path)

# mkds_4to7

left = 1
pre_idx = 1
c_datas = []
all_datas = []

datas = os.listdir(b_path)
datas.sort()
# print(datas)
for data in datas:
    c_idx = data.split("_")[2].split(".")[0]
    if c_idx != pre_idx:
        # print("class"+str(int(c_idx)-1))
        # print(len(c_datas))
        k_num = 1
        k_split = math.floor(len(c_datas)/5)
        # print(k_split)
        k_spcopy = k_split
        random.shuffle(c_datas)
        # print(c_datas)
        for c_data in c_datas:
            # print(c_data)
            before_path = b_path + "/" + c_data
            if k_spcopy != 0:
                k_spcopy -= 1
            else:
                k_spcopy = k_split-1
                k_num += 1
            
            if k_num <= 5:
                after_path = b_path + "/" + str(k_num) + "-" + c_data
            elif k_num == 6:
                # print("k_num:",str(left))
                after_path = b_path + "/" + str(left) + "-" + c_data
                if left < 5:
                    left += 1
                else:
                    left = 1
            else:
                print("k_num_error")
            # print(before_path)
            # print(after_path)
            os.rename(before_path, after_path)
        c_datas = []
        c_datas.append(data)
    else:
        c_datas.append(data)
    pre_idx = c_idx
    all_datas.append(data)
# print("class"+c_idx)
# print(len(c_datas))
k_num = 1
k_split = math.floor(len(c_datas)/5)
# print(k_split)
k_spcopy = k_split
random.shuffle(c_datas)
# print(c_datas)
for c_data in c_datas:
    # print(c_data)
    before_path = b_path + "/" + c_data
    if k_spcopy != 0:
        k_spcopy -= 1
    else:
        k_spcopy = k_split-1
        k_num += 1

    if k_num <= 5:
        after_path = b_path + "/" + str(k_num) + "-" + c_data
    elif k_num == 6:
        # print("k_num:",str(left))
        after_path = b_path + "/" + str(left) + "-" + c_data
        if left < 5:
            left += 1
        else:
            left = 1
    else:
        print("k_num_error")
    # print(before_path)
    # print(after_path)
    os.rename(before_path, after_path)
print(len(all_datas))

meta_dir = "./master/meta"
if not os.path.exists(meta_dir):
    os.mkdir(meta_dir)

with open(meta_dir + "/ycam.csv", "w") as f:
    ycam_csv = csv.writer(f)
    ycam_csv.writerow(["filename", "fold", "target", "category", "esc10", "src_file", "take"])

data_files= os.listdir(b_path) # classディレクトリを抽出
# print(c_dic)
esc10 = "False"
for filename in data_files:
    # print(filename)
    fold = filename.split("-")[0]
    # print(fold)
    target = filename.split("_")[2].split(".")[0]
    # print(target)
    if len(target) == 1:
        c_key = "0"+target
    else:
        c_key = target
    category = c_dic[c_key]
    # print(target)
    # print(category)
    src_file = filename.split("-")[1].split("_")[0]
    # print(src_file)
    take = filename.split("_")[1]
    # print(take)
    with open(meta_dir + "/ycam.csv", "a", newline="") as f:
        ycam_csv = csv.writer(f)
        ycam_csv.writerow([filename, fold, target, category, esc10, src_file, take])