from pop import Pilot, AI, LiDAR
import time

lidar = LiDAR.Rplidar() # Lidar 객체 생성
lidar.connect() # Lidar 연결
lidar.startMotor() # Lidar 모터 작동

cam = Pilot.Camera(width=224, height=224) # 자동차 카메라 객체 생성
car = Pilot.AutoCar() # 자동차 객체 생성

object_follow = AI.Object_Follow(cam) # Object_Follow 객체 생성 (카메라 가져옴)
object_follow.load_model() # Object_Follow 모델 로드

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
        
        elif (Size_Far < Size_value <= Size_Half): # 멀리서 감지되었을 때
            car.forward(Speed_Slow) # 속도를 느리게 함.
        
        else: # 너무 가까울 때(15% 이상)
            car.steering = (- Real_Steer) # 후진하는 동안에는 반대 방향으로 조향
            Raw = lidar.getVectors() # Lidar 값을 Raw로 받아옴
            for v in Raw:
                if (v[0] >= 360 - 170 and v[0] <= 360 - 190): # 후방 20도
                    Rear_Raw = v[1] # 후방 거리값
                    # print(Rear_Raw) # 후방 거리값 출력
            
            if (Rear_Raw <= Distance_Close): # 약간의 공간은 있음 -> 실제로는 생각보다 가까이 멈추기 때문에(가속도 때문), 조금 더 높여야 할 필요가 있음. (수정 필요)
                car.backward(Speed_Slow) # 느리게 후진
                print("공간이 거의 없어요!") # 모델에 따라 행동을 변경해야 함 (수정 필요)
            
            elif (Rear_Raw <= Distance_Very_Close): # 완전 공간 없음
                car.stop() # 후방에 장애물이 감지되었기 때문에, 정지
                print("공간 없어요!") # 모델에 따라 행동을 변경해야 함 (수정 필요)
            
            else: # 후방에 장애물이 감지되지 않았을 때
                car.backward(Speed_Middle) # 계속 후진
                time.sleep(0.3) # 0.3초동안 후진 (수정 필요)

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