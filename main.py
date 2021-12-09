# library
import os

import soundfile
import sounddevice as sd
import time

# functions
from pitch_detection import find_pitches
from real_time_io import startVoiceRecording

# static values
from real_time_io import FILE_NAME


# filename의 파일에서 pitch data를 가져오는 함수
def getPitchFromFile(filename):
    with open(filename, 'r') as file:
        pitches = []
        lines = file.readlines()

        # \n 제거
        for index, line in enumerate(lines):
            lines[index] = line.rstrip('\n')

        return lines


# test.wav 의 전체 pitch값 계산
origin_file = soundfile.SoundFile('test.wav')
#data, fs = soundfile.read('test.wav')
data = origin_file.read()
data = data[:, 0]

# 기존의 텍스트파일 삭제 코드
if os.path.isfile(FILE_NAME):
    os.remove(FILE_NAME)

# 실시간 마이크 input pitch 계산
#sd.play(data)
print("Starting Music")
startVoiceRecording()
print("Done Music")

"""
# wav파일의 duration을 구하는 과정
duration_second = origin_file.frames / origin_file.samplerate

# 구한 duration을 사용해서 프로그램을 sleep시킴 -> ms단위여서 * 1000
sd.sleep(int(duration_second * 1000)) # duration_second * 1000
print("DONE")"""

# 원본의 pitch 데이터 가져오기
origin_pitches = find_pitches(data)

# 녹음된 pitch 데이터 가져오기
user_pitches = getPitchFromFile(FILE_NAME)


# orginal_pitches의 값과 user_pitches의 값들을 비교하기
score = 0  # 스코어 값 집계를 위한 paramter
number = 0  # 피치의 수 집계를 위한 paramter

for index, user_pitch in enumerate(user_pitches):
    #print("오리지널 : " + str(origin_pitches[index]) + "  녹음된거 : " + str(user_pitches))
    if index == len(origin_pitches):
        break

    if int(origin_pitches[index]) == int(user_pitch):
        print("Original: " + str(origin_pitches[index]) + " User: " + str(user_pitch) + "   Perfect!")
        score += 3
        number += 1
    elif abs(int(origin_pitches[index]) - int(user_pitch)) < 70:
        print("Original: " + str(origin_pitches[index]) + " User: " + str(user_pitch) + "   Excellent!")
        score += 1.5
        number += 1
    else:
        print("Original: " + str(origin_pitches[index]) + " User: " + str(user_pitch) + "   Good!")
        score += 0.7
        number += 1

print()
print("Your Score: " + str(round((score / number) * 100, 1)))
