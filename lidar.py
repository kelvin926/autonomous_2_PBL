from pop import Pilot
from pop import LiDAR
from threading import Thread
import time

number = 0

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


def first_turn(car):
    car.setSpeed(100)
    car.steering = 0
    time.sleep(2)
    car.steering = -1
    time.sleep(1)
    car.steering = 0
    car.setSpeed(75)

def on_lidar(car, lidar):
    on_lidar.is_stop = False

    while not on_lidar.is_stop:
        V = lidar()
        #라이다를 실행시킨후 좌, 우, 전방 순으로 물체를 확인한다
        # if, elif문을 사용하여 
        for v in V:
            if v[0] >= 360 - 100 and v[0] <= 360 - 65:     #우선적으로 좌측의 라이다 값을 받아온다  (260도~290도)          
                if v[1] >= 2300 and v[1] <= 3500:         #귀납적으로 첫번째 회전시 자동차와 벽장의 거리를 측정한뒤 그 거리에서만 회전할수 있게 값을 조정한다
                    global number
                    if number == 0:
                        first_turn(car)
                        number = 1
                        print("왼쪽 턴")
                    else:
                        on_drive.cmd = 33                     #커맨드 33은 더 강하게 좌회전하는 명령
                        print("왼쪽으로 회전 ", v[1])          #디버깅을 위해 print문 작성
                        print("왼쪽 조향값 ", car.steering)
                        
            elif v[0] >= 360 - 50 or v[0] <= 50:          #중복적으로 전방 100도 확인
                if v[0] <= 50 :                            #전방 우측 50도 '우선' 확인                                               
                    if v[1] <= 1150 :                     #전방 우측 50도 1.5m를 스캔후 물체가 있을경우
                        on_drive.cmd = 3                  #3번 커맨드를 통해 좌측으로 이동 
                        
                    if v[1] > 1150 :                      #전방 우측 50도 1.5m 스캔후 물체가 없을경우
                        while(car.steering < 0) :         #왼쪽으로 치우쳐져 있는 조향값을 0으로 복원시키는 코드
                            on_drive.cmd = 4              #중앙을 넘어가지않도록 왼쪽에서 오른쪽 조향
                            
                if v[0] >= 360 - 50 :                   #전방 좌측 50도 이후 확인 
                    if v[1] <= 1150 :                     #전방 좌측 50도 1.5m를 스캔후 물체가 있을경우
                        on_drive.cmd = 4                  #4번 커맨드를 통해 우측으로 이동 
                        
                    if v[1] > 1150 :                      #전방 좌측 50도 1.5m 스캔후 물체가 없을경우
                        while(car.steering > 0) :         #오른쪽으로 치우쳐져 있는 조향값을 0으로 복원시키는 코드
                            on_drive.cmd = 3              #중앙을 넘어가지않도록 오른쪽에서 왼쪽 조향
                            
        time.sleep(0.1)                                   #조향값을 0.1초동안 유지


def on_drive(car):
    on_drive.is_stop = False
    on_drive.cmd = 1

    steering = 0
    speed = 75

    car.steering = steering
    car.setSpeed(speed)

    while not on_drive.is_stop:

        if on_drive.cmd == 1:
            car.forward()
        elif on_drive.cmd == 2:
            car.backward()
        elif on_drive.cmd == 3:               #왼쪽
            steering -= 0.5
            steering = -1.0 if steering <= -1.0 else steering
            car.steering = steering

        elif on_drive.cmd == 33 :            #더강하게 왼쪽으로 틀기
            steering -= 1.0
            steering = -1.0 if steering <= -1.0 else steering
            car.steering = steering
            print("강한회전")
            
        elif on_drive.cmd == 4:
            steering += 0.5
            steering = 1.0 if steering > 1.0 else steering
            car.steering = steering

        elif on_drive.cmd == 44:
            steering += 0.9
            steering = 1.0 if steering > 1.0 else steering
            car.steering = steering
            
        if on_drive.cmd == 5:
            speed += 5
            speed = 99 if speed >= 99 else speed
            car.setSpeed(speed)

        elif on_drive.cmd == 6:
            speed -= 3
            speed = 20 if speed < 20 else speed
            car.setSpeed(speed)
        
        #print(steering, speed)

        on_drive.cmd = 0
        time.sleep(0.1)
    
    car.steering = 0
    car.stop()


def main():
    car = Pilot.AutoCar()
    lidar = Lidar()

    t = Thread(target=on_lidar, args=(car, lidar))
    Thread(target=on_drive, args=(car, )).start()
    t.daemon = True
    t.start()
    
    
    input()

    on_lidar.is_stop = True
    on_drive.is_stop = True
    Lidar.close()
    car.stop()


if __name__ == "__main__":
    main()