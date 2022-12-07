from pop import Pilot, AI, LiDAR
import time
    

lidar = LiDAR.Rplidar()
lidar.connect()
lidar.startMotor()

cam = Pilot.Camera(width=224, height=224)
car = Pilot.AutoCar()

object_follow = AI.Object_Follow(cam)
object_follow.load_model()

find_num = 0
real_steer = 0

while True:
    Rear_Raw = 0
    ret = object_follow.detect(index='person')
    if ret is not None: # 사람이 감지되었을 때
        find_num = 0
        ret_steer = ret['x'] * 4
        real_steer = 1 if ret_steer > 1 else -1 if ret_steer < -1 else ret_steer # 위 Ret값에서 4를 곱한 값이 1 이상이면 1, 아니면 -1 / -1 이하이면 -1, 아니면 1 -> 결국 1 / -1 두 값 중 하나로만 간다는 것.
        car.steering = real_steer
        size_value = ret['size_rate'] # 감지 사이즈 %단위로 나옴.
        if (size_value <= 0.1): # 아주 멀리서 감지되었을 때 (10% 이하)
            car.forward(60)
        elif (0.1 < size_value <= 0.15): # 멀리서 감지되었을 때 (10% 초과 15% 이하)
            car.forward(40)
        else: # 너무 가까울 때(30% 이상)
            car.steering = (- real_steer)
            Raw = lidar.getVectors()
            for v in Raw:
                if (v[0] >= 360 - 200 and v[0] <= 360 - 160): # 후방 3-도
                    Rear_Raw = v[1]
                    # print(Rear_Raw)
            if (Rear_Raw <= 300):
                car.stop()
                print("후방 감지")
                time.sleep(1)
            else:
                car.backward(60)
                time.sleep(0.3) # 0.3초동안 강하게 후진
                    
    else: # 사람이 감지되지 않았을 때
        if find_num < 3:
            car.forward(40)
            car.steering = real_steer
            find_num += 1
            time.sleep(0.5)
        else: # 1.5초 이상 찾아봤는데 없을 때
            car.steering = 0
            car.stop()
            print("3초 이상 사람이 감지되지 않았습니다.")