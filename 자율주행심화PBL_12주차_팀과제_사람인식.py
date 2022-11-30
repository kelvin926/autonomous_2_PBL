from pop import Pilot, AI

cam = Pilot.Camera(width=224, height=224)
car = Pilot.AutoCar()

object_follow = AI.Object_Follow(cam)
object_follow.load_model()

while True:
    ret = object_follow.detect(index='person')
    if ret is not None:
        steer = ret['x'] * 4
        car.steering = 1 if steer > 1 else -1 if steer < -1 else steer
        size_value = ret['size_rate']
        if (size_value <= 0.1):
            car.forward(80)
        elif (0.125 < size_value <= 0.175):
            car.forward(50)
        elif (0.175 < size_value <= 0.25):
            car.forward(30)
        else:
            car.backward(80)
    else:
        car.stop()

"""
[과제]
1. 사람이 이동 중 사라질 때 찾기 (상태변수를 따로 하나 만들기, 이동하는 중에 좌회전을 하고 있었는지, 
우회전 하고 있었는지 저장한 다음, 사람이 사라지면 그 방향으로 조금 더 회전하기)
Hint : 속도 부분들을 가변으로 주어야 함.
못찾았을 땐 속도를 조금 더 높여야 함.

2. 사람이 다가오면 뒤로 조금 물러서기
Hint : 20%의 거리가 좀 멀음 (1m) 가까워지면 점점 %가 높아짐 (멀리 있을 땐 더 빠르게)
사람 가까움의 최고 %는 30%, 대신 가까워지면 점점 느리게 주행해야 함.

3. 후진 할 때 뒤에 장애물 탐지해서, 장애물이 있으면 멈추기 (Lidar, Sonar)
"""