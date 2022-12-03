from pop import Pilot, AI
import time

cam = Pilot.Camera(width=224, height=224)
car = Pilot.AutoCar()

object_follow = AI.Object_Follow(cam)
object_follow.load_model()

find_num = 0
real_steer = 0

find_num = 0
real_steer = 0

while True:
    ret = object_follow.detect(index='person')
    if ret is not None: # 사람이 감지되었을 때
        find_num = 0
        ret_steer = ret['x'] * 4
        real_steer = 1 if ret_steer > 1 else -1 if ret_steer < -1 else ret_steer # 위 Ret값에서 4를 곱한 값이 1 이상이면 1, 아니면 -1 / -1 이하이면 -1, 아니면 1 -> 결국 1 / -1 두 값 중 하나로만 간다는 것.
        car.steering = real_steer
        size_value = ret['size_rate'] # 감지 사이즈 %단위로 나옴.
        if (size_value <= 0.1): # 아주 멀리서 감지되었을 때 (10% 이하)
            car.forward(60)
        # elif (0.1 < size_value <= 0.15):
        #     car.forward(50)
        elif (0.1 < size_value <= 0.15):
            car.forward(40)
        else: # 너무 가까울 때(30% 이상)
            car.steering = (- real_steer)
            car.backward(60)
            time.sleep(0.3) # 0.3초동안 강하게 후진
    else: # 사람이 감지되지 않았을 때
        if find_num < 3:
            car.forward(40)
            car.steering = real_steer
            find_num += 1
            time.sleep(0.5)
        else: # 1초 이상 찾아봤는데 없을 때
            car.steering = 0
            car.stop()
            print("3초 이상 사람이 감지되지 않았습니다.")

"""
[과제]
1. 사람이 이동 중 사라질 때 찾기 (상태변수를 따로 하나 만들기, 이동하는 중에 좌회전을 하고 있었는지, 
우회전 하고 있었는지 저장한 다음, 사람이 사라지면 그 방향으로 조금 더 회전하기)
Hint : 속도 부분들을 가변으로 주어야 함.
못찾았을 땐 속도를 조금 더 높여야 함.

2. 사람이 다가오면 뒤로 조금 물러서기
Hint : 20%의 거리가 좀 멀음 (1m) 가까워지면 점점 %가 높아짐 (멀리 있을 땐 더 빠르게)
사람 가까움의 최고 %는 30%, 대신 가까워지면 점점 느리게 주행해야 함.

3. 후진 할 때 뒤에 장애물 탐지해서, 장애물이 있으면 멈추기 (Lidar, Sonar) -> Lidar 사용해서 뒤에 계속 감지(후진할 때만), 뒤에 사물 있으면 삐 소리 내면서 정지하기
"""