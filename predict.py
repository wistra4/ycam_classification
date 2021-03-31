# 音声データの前処理
import os
import glob
import pydub
from pydub import AudioSegment
import librosa
import soundfile as sf
import math

ds_file = "/.DS_Store"

b_path = "./master/recording"

'''
if os.path.exists(b_path + ds_file):
    os.remove(b_path + ds_file)
r_dirs = os.listdir(b_path)

for r_dir in r_dirs:
    r_path = b_path + "/" + r_dir
    if os.path.exists(r_path + ds_file):
        os.remove(r_path + ds_file)
    r_files = os.listdir(r_path)
    r_num = 1

    for r_file in r_files:
        before_path = r_path + "/" + r_file
        if r_num <= 9:
            r_numstr = "0" + str(r_num)
        elif 10 <= r_num:
            r_numstr = str(r_num)
        r_num += 1 
        after_path = b_path + "/" + r_dir + r_numstr + r_file[-4:]
        os.rename(before_path, after_path)

for r_dir in r_dirs:
    r_path = b_path + "/" + r_dir
    os.rmdir(r_path)

mp3_paths= glob.glob(b_path + "/*.MP3") # mp3ファイルを抽出
for mp3_path in mp3_paths:
    # print(mp3_path)
    mp3_file = pydub.AudioSegment.from_mp3(mp3_path)
    mp3_file.export("."+mp3_path.split(".")[1]+".wav", format="wav")
    os.remove(mp3_path)
'''

'''
wav_dirs = os.listdir(b_path)
for wav_dir in wav_dirs:
    wav_path = b_path + "/" + wav_dir 
    print(wav_dir)

    wav_file = AudioSegment.from_file(wav_path, "wav")

    time = wav_file.duration_seconds # 再生時間(秒)
    rate = wav_file.frame_rate  # サンプリングレート(Hz)
    channel = wav_file.channels  # チャンネル数(1:mono, 2:stereo)
    splits = math.floor(time/5.0)
    print('再生時間：', time)
    print("分割数 : ", splits)
    print("サンプリングレート：", rate)
    print('チャンネル数：', channel)

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

    s_num = 1
    for split in range(1, splits+1):
        cut_start = (split-1)*5000
        cut_end = split*5000
        wav_cut = wav_file[cut_start:cut_end]
        if s_num <= 9:
            s_numstr = "0" + str(s_num)
        elif 10 <= s_num:
            s_numstr = str(s_num)
        s_num += 1 
        take_path = b_path + "/" + wav_dir.split(".")[0] + "_" + s_numstr + ".wav"
        # print(take_path)
        wav_cut.export(take_path, format="wav")

    os.remove(wav_path)
'''

from keras.models import load_model
import numpy as np

model = load_model("./master/models/esc50_.58.hdf5")

rec = []
rec_dirs = os.listdir(b_path)
if os.path.exists(b_path + ds_file):
    os.remove(b_path + ds_file)
for rec_dir in rec_dirs:
    rec_path = b_path + "/" + rec_dir
    rec.append(rec_path)
# print(rec)
# print(len(rec))
rec.sort()

freq = 128
time = 1723
def calculate_melsp(x, n_fft=1024, hop_length=128):
    stft = np.abs(librosa.stft(x, n_fft=n_fft, hop_length=hop_length))**2
    log_stft = librosa.power_to_db(stft)
    melsp = librosa.feature.melspectrogram(S=log_stft,n_mels=128)
    return melsp

c_dic = {1:"hiyodori", 2:"kogera", 3:"mejiro", 4:"yamagara", 5:"shijukara"}
for r_num in range(len(rec)):
    np_data = np.zeros(freq*time).reshape(1, freq, time)
    _rec, fs = librosa.load(rec[r_num], sr=44100)
    _rec = calculate_melsp(_rec)
    np_data = _rec

    test_num = len(rec)
    np_data = np_data.reshape(1, freq, time, 1)
    # print(np_data)
    result = model.predict(np_data)
    print(rec[r_num])
    # print(result)
    predict_classes = np.argmax(result, axis=1)
    print(str(predict_classes[0])+":"+str(c_dic[predict_classes[0]]))