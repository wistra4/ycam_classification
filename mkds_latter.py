# mkds_4to7
import os
import glob
import pydub
from pydub import AudioSegment
import math
import librosa
import soundfile as sf

ds_file = "/.DS_Store" # ds_storeディレクトリ名
p_nums = []

b_path = "./targets" # baseパス
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
        print("DS_File was removed.")
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

    if rate != 44100:
        y, sr = librosa.core.load(wav_path, sr=44100, mono=True)
        sf.write(wav_path, y, sr, subtype="PCM_16")
        wav_file = AudioSegment.from_file(wav_path, "wav")
        channel = wav_file.channels

    if channel != 2:
        wav_file = wav_file.set_channels(2)
        wav_file.export(wav_path, format="wav")
        wav_file = AudioSegment.from_file(wav_path, "wav")

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
