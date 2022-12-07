
"""
[TodoList]
- 사람이 이동 중 사라질 때 찾기 (완료) (0.5초 단위로 찾아보면서 최대 3회 진행함)
- 사람이 다가오면 뒤로 조금 물러서기 (완료) (size_value는 마지노선 15%정도가 가장 적절한 것으로 판단됨.)
- 가변 속도 (완료) (40/60 그 이하나 이상은 불안정함.) (30 이하의 속도로 주행할 경우 전체적인 성능이 떨어지는 버그 발생.)


- Lidar 사용 (사람이 앞에 감지되지 않았더라도, 앞에 사물이 가깝게 있으면 뒤로 살짝 물러서기, 뒤에 사물이 있으면 멈추고 비프음 내기)
- 비프음 사용


1. Lidar를 이용해서 충돌하지 않고 잘 따라오도록 만드는 것.
2. 뒤로 물러설수도 있어야 함 (라이다를 통해, 뒤가 막혀있으면 옆으로 갈 수도 있을 것)
3. 다 막혔을 땐 움직이지 않고, 가만히 있는다 (사람이 움직이면 다시 오기)
4. 부드럽게 움직이기
5. 소리 출력 (강아지라고 생각하거나, 2살짜리 아기라고 생각하거나 … -> 모델링)
6. 목적성 (애완견(주인 보면 애교부리는)인가, 나를 케어하는 반려견인가, 방범로봇(가만히 있다가 사람이 등장하면 경고하며 사진찍기)
7. 사람은 한 명만 있다고 가정함.


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

from pop import Pilot, AI, LiDAR
import time
from threading import Thread

# lidar
def Lidar():
    lidar = LiDAR.Rplidar()
    lidar.connect()
    lidar.startMotor()
    def close():
        lidar.stopMotor()
    Lidar.close = close
    def _inner():
        return lidar.getVectors()
    return _inner


def on_lidar(car, lidar):
    on_lidar.is_stop = False
    while not on_lidar.is_stop:
        V = lidar()
        for v in V:
            if v[0] >= 360 - 135 and v[0] <= 360 - 225: # 후방 90도
                global Rear_Raw
                Rear_Raw = v[1]
        time.sleep(0.1)

def gogo(car, object_follow):
    gogo.is_stop = False
    
    while not gogo.is_stop:
        ret = object_follow.detect(index='person')
        if ret is not None: # 사람이 감지되었을 때
            find_num = 0
            ret_steer = ret['x'] * 4
            real_steer = 1 if ret_steer > 1 else -1 if ret_steer < -1 else ret_steer # 위 Ret값에서 4를 곱한 값이 1 이상이면 1, 아니면 -1 / -1 이하이면 -1, 아니면 1 -> 결국 1 / -1 두 값 중 하나로만 간다는 것.
            car.steering = real_steer
            size_value = ret['size_rate'] # 감지 사이즈 %단위로 나옴.
            if (size_value <= 0.1): # 아주 멀리서 감지되었을 때 (10% 이하)
                car.forward(60)
            elif (0.1 < size_value <= 0.15):
                car.forward(40)
            else: # 너무 가까울 때(15% 이상)
                car.steering = (- real_steer)
                if Rear_Raw <= 1000: # 후방 라이다 값이 500mm보다 작을 때
                    car.stop()
                    print("후방 감지")
                    time.sleep(5)
                else:
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
                # print("3초 이상 사람이 감지되지 않았습니다.")


def main():
    find_num = 0
    real_steer = 0
    
    object_follow = AI.Object_Follow(cam)
    object_follow.load_model()
    
    cam = Pilot.Camera(width=224, height=224)
    car = Pilot.AutoCar()
    lidar = Lidar()

    Thread(target=on_lidar, args=(car, lidar)).start()
    Thread(target=gogo, args=(car, object_follow, real_steer, find_num)).start()
    
    input()

    on_lidar.is_stop = True
    gogo.is_stop = True
    Lidar.close()
    car.stop()


if __name__ == "__main__":
    main()