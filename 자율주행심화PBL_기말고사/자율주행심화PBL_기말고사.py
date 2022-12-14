'''
[충성심이 있고 겁이 좀 있는 강아지]

아주 멀리 있을 때 : 잠깐 기다렸다가 빠른 속도로 따라옴(헥헥대는 소리 또는 짖는 소리 결정 못함 아직 mp3모델이 많아서)

멀리 있을 때 : 충성심 있는 강아지라 주인을 졸졸 따라다님(강아지들 산책할 때 헥헥대는 소리)

너무 가까울 때 : 겁이 좀 있는 강아지라 조금 가까우면 (낑낑대면서) 물러남

너무 가까우면서 후방에 물체가 있을 때 : 놀라서 놀랄 때 내는 소리 집어넣으면 좋을 것 같음
'''

"""
[기말고사]
1. Lidar를 이용해서 충돌하지 않고 잘 따라오도록 만드는 것. (완료)
2. 뒤로 물러설수도 있어야 함 (라이다를 통해, 뒤가 막혀있으면 옆으로 갈 수도 있을 것) (완료)
3. 다 막혔을 땐 움직이지 않고, 가만히 있는다 (사람이 움직이면 다시 오기) 
4. 부드럽게 움직이기 (완료)
5. 소리 출력 (강아지라고 생각하거나, 2살짜리 아기라고 생각하거나 … -> 모델링) (완료)
6. 목적성 (애완견(주인 보면 애교부리는)인가, 나를 케어하는 반려견인가, 방범로봇(가만히 있다가 사람이 등장하면 경고하며 사진찍기) (완료)
7. 사람은 한 명만 있다고 가정함. (완료)
"""

'''
close.wav : 가까이 있을 때
far.wav : 멀리 있을 때
very_far.wav : 엄청 멀리있을 때
ggam_nol.wav : 깜짝 놀랐을 때
missing.wav : 사람이 사라졌을 때
'''

from pop import Pilot, AI, LiDAR
import time
from playsound import playsound
from threading import Thread

lidar = LiDAR.Rplidar() # Lidar 객체 생성
lidar.connect() # Lidar 연결
lidar.startMotor() # Lidar 모터 작동

cam = Pilot.Camera(width=224, height=224) # 자동차 카메라 객체 생성
car = Pilot.AutoCar() # 자동차 객체 생성

object_follow = AI.Object_Follow(cam) # Object_Follow 객체 생성 (카메라 가져옴)
object_follow.load_model() # Object_Follow 모델 로드


# ---------- 각종 변수들 ---------- #
Real_Steer = 0 # 실제 자동차에 반영될 조향값

Speed_Slow = 50
Speed_Middle = 60
Speed_Fast = 80

Size_Far = 0.1 # 10%
Size_Half = 0.15 # 15%
Size_Big = 0.30 # 20%

Distance_Close = 500 # 50cm
Distance_Very_Close = 300 # 30cm

global now_sound
now_sound = "very_far.wav"


def say(nope):
    while True:
        global now_sound
        playsound(now_sound)
        time.sleep(0.1)

s = Thread(target = say, args=(None,)).start()

while True: # 무한 반복
    ret = object_follow.detect(index='person') # 사람 감지
    if ret is not None: # 사람이 감지되었을 때
        ret_steer = ret['x'] * 4 # 사람 감지 좌표값(박스의 정 중앙)을 4로 곱함.
        Real_Steer = 1 if ret_steer > 1 else -1 if ret_steer < -1 else ret_steer # 위 Ret값에서 4를 곱한 값이 1 이상이면 1, 아니면 -1 / -1 이하이면 -1, 아니면 1 -> 결국 1 / -1 두 값 중 하나로만 간다는 것.
        car.steering = Real_Steer # 위에서 구한 실제 조향 값 대입.
        Size_value = ret['size_rate'] # 감지 사이즈 %단위로 나옴.
        
        if (Size_value <= Size_Far): # 아주 멀리서 감지되었을 때
            car.forward(Speed_Middle) # 속도를 보통으로 함
            now_sound = "very_far.wav"
        
        elif ((Size_Far < Size_value) and (Size_value <= Size_Half)): # 멀리서 감지되었을 때
            car.forward(Speed_Slow) # 속도를 느리게 함.
            now_sound = "far.wav"
        
        elif ((Size_Half < Size_value) and (Size_value <= Size_Big)): # 가까움
            global Rear_Raw
            Rear_Raw = 0 # Lidar 후방 거리값
            car.steering = (- Real_Steer) # 후진하는 동안에는 반대 방향으로 조향
            Raw = lidar.getVectors() # Lidar 값을 Raw로 받아옴
            for v in Raw:
                if (v[0] >= 360 - 185 and v[0] <= 360 - 175): # 후방 10도
                    Rear_Raw = v[1] # 후방 거리값
                    print(Rear_Raw) # 후방 거리값 출력
            
            if ((Distance_Very_Close < Rear_Raw) and (Rear_Raw <= Distance_Close)): # 약간의 공간은 있음
                car.backward(Speed_Slow) # 느리게 후진
                now_sound = "close.wav"
            
            elif (Rear_Raw <= Distance_Very_Close): # 완전 공간 없음
                car.stop() # 후방에 장애물이 감지되었기 때문에, 정지
                now_sound = "ggam_nol.wav"
            
            else: # 후방에 장애물이 감지되지 않았을 때
                car.backward(Speed_Slow) # 계속 후진
                now_sound = "close.wav"
                
        else: # 너무 가까울 때
            car.stop()
            now_sound = "very_far.wav"
            time.sleep(1)
                
    else: # 사람이 감지되지 않았을 때 -> 모델에 따라 행동을 변경해야 함.
        car.stop() # 일단 정지 -> 모델에 따라 행동을 변경해야 함.
        now_sound = "missing.wav"