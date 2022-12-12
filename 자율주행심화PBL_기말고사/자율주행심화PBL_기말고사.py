'''
[충성심이 있고 겁이 좀 있는 강아지]

아주 멀리 있을 때 : 잠깐 기다렸다가 빠른 속도로 따라옴(헥헥대는 소리 또는 짖는 소리 결정 못함 아직 mp3모델이 많아서)

멀리 있을 때 : 충성심 있는 강아지라 주인을 졸졸 따라다님(강아지들 산책할 때 헥헥대는 소리)

너무 가까울 때 : 겁이 좀 있는 강아지라 조금 가까우면 (낑낑대면서) 물러남

너무 가까우면서 후방에 물체가 있을 때 : 놀라서 놀랄 때 내는 소리 집어넣으면 좋을 것 같음
'''

"""
[기말고사]
1. Lidar를 이용해서 충돌하지 않고 잘 따라오도록 만드는 것.
2. 뒤로 물러설수도 있어야 함 (라이다를 통해, 뒤가 막혀있으면 옆으로 갈 수도 있을 것)
3. 다 막혔을 땐 움직이지 않고, 가만히 있는다 (사람이 움직이면 다시 오기)
4. 부드럽게 움직이기
5. 소리 출력 (강아지라고 생각하거나, 2살짜리 아기라고 생각하거나 … -> 모델링)
6. 목적성 (애완견(주인 보면 애교부리는)인가, 나를 케어하는 반려견인가, 방범로봇(가만히 있다가 사람이 등장하면 경고하며 사진찍기)
7. 사람은 한 명만 있다고 가정함.
"""

from pop import Pilot, AI, LiDAR
import time
from playsound import playsound
from multiprocessing import Process

lidar = LiDAR.Rplidar() # Lidar 객체 생성
lidar.connect() # Lidar 연결
lidar.startMotor() # Lidar 모터 작동

cam = Pilot.Camera(width=224, height=224) # 자동차 카메라 객체 생성
car = Pilot.AutoCar() # 자동차 객체 생성
car._out_sound = None # 자동차 객체에 out_sound 변수 추가

object_follow = AI.Object_Follow(cam) # Object_Follow 객체 생성 (카메라 가져옴)
object_follow.load_model() # Object_Follow 모델 로드

def out_sound(wav_file):
    p = Process(target=playsound, args=(wav_file,))
    p.start()
    if (car._out_sound != None):
            car._out_sound.terminate()
            car._out_sound = None
    return p

# ---------- 각종 변수들 ---------- #
Real_Steer = 0 # 실제 자동차에 반영될 조향값

Speed_Slow = 40
Speed_Middle = 60
Speed_Fast = 80

Size_Far = 0.1 # 10%
Size_Half = 0.15 # 15%

Distance_Close = 500 # 50cm
Distance_Very_Close = 300 # 30cm

Rear_Raw = 0 # Lidar 후방 거리값
# find_num = 0 # 사람을 찾은 횟수 -> 모델에 따라 변경해야 함.


while True: # 무한 반복
    ret = object_follow.detect(index='person') # 사람 감지
    if ret is not None: # 사람이 감지되었을 때
        # find_num = 0
        ret_steer = ret['x'] * 4 # 사람 감지 좌표값(박스의 정 중앙)을 4로 곱함.
        Real_Steer = 1 if ret_steer > 1 else -1 if ret_steer < -1 else ret_steer # 위 Ret값에서 4를 곱한 값이 1 이상이면 1, 아니면 -1 / -1 이하이면 -1, 아니면 1 -> 결국 1 / -1 두 값 중 하나로만 간다는 것.
        car.steering = Real_Steer # 위에서 구한 실제 조향 값 대입.
        Size_value = ret['size_rate'] # 감지 사이즈 %단위로 나옴.
        
        if (Size_value <= Size_Far): # 아주 멀리서 감지되었을 때
            car.forward(Speed_Middle) # 속도를 보통으로 함
            out_sound("반가워서 짖는 소리")
        
        elif (Size_Far < Size_value <= Size_Half): # 멀리서 감지되었을 때
            car.forward(Speed_Slow) # 속도를 느리게 함.
            out_sound("산책할 때 헥헥대는 소리")
        
        else: # 너무 가까울 때(15% 이상)
            car.steering = (- Real_Steer) # 후진하는 동안에는 반대 방향으로 조향
            Raw = lidar.getVectors() # Lidar 값을 Raw로 받아옴
            for v in Raw:
                if (v[0] >= 360 - 170 and v[0] <= 360 - 190): # 후방 20도
                    Rear_Raw = v[1] # 후방 거리값
                    # print(Rear_Raw) # 후방 거리값 출력
            
            if (Rear_Raw <= Distance_Close): # 약간의 공간은 있음 -> 실제로는 생각보다 가까이 멈추기 때문에(가속도 때문), 조금 더 높여야 할 필요가 있음. (수정 필요)
                car.backward(Speed_Slow) # 느리게 후진
                out_sound("무서워서 낑낑거리는 소리 + 물러서는 소리")
            
            elif (Rear_Raw <= Distance_Very_Close): # 완전 공간 없음
                car.stop() # 후방에 장애물이 감지되었기 때문에, 정지
                out_sound("완전 무서워하는 소리 + 짖으면서..?")
            
            else: # 후방에 장애물이 감지되지 않았을 때
                car.backward(Speed_Middle) # 계속 후진
                out_sound("낑낑대는 소리 + 빠르게 물러서는 소리")
                time.sleep(0.3) # 0.3초동안 후진 (매끄럽게 수정 필요)

    else: # 사람이 감지되지 않았을 때 -> 모델에 따라 행동을 변경해야 함.
        # if find_num < 3:
        #     car.forward(Speed_Slow)
        #     car.steering = Real_Steer
        #     find_num += 1
        #     time.sleep(0.5)
        # else: # 1.5초 이상 찾아봤는데 없을 때
        #     car.steering = 0
        #     car.stop()
        #     print("3초 이상 사람이 감지되지 않았습니다.")
        car.stop() # 일단 정지 -> 모델에 따라 행동을 변경해야 함.
        out_sound("사람 찾는 소리")