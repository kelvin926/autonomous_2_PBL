#%%
# 초반 보정
from pop.Pilot import AutoCar
from pop import AI
import numpy as np
import time

#%%
def train(car, learn_model_bool):
    dataset={ 'yaw' : [], 'steer' : [] }
    for n in np.arange(-0.9, 1.1, 0.3): # -0.9, 1.1, 0.1  #조향축 학습 시키는 부분
        n = round(n,1)
        car.steering = n
        car.forward()
        time.sleep(0.5)
        m = car.getEuler('yaw')
        time.sleep(0.5)
        car.backward()
        time.sleep(1)
        car.stop()
        dataset['yaw'].append(m)
        dataset['steer'].append(n)
        print({ 'yaw' : m , 'steer' : n })
    max_value = np.array(dataset['yaw']).max()
    min_value = np.array(dataset['yaw']).min()
    if max_value - min_value > 300:
        for num, y in enumerate(dataset['yaw']):
            if y > 180:
                dataset['yaw'][num] = round(y - 360, 3)

    LR = AI.Linear_Regression(restore = learn_model_bool, ckpt_name = "straight_model")
    LR.X_data=dataset['yaw']
    LR.Y_data=dataset['steer']
    LR.train(times=1000, print_every=10) # 1000번 학습
def yaw(car):
    return(car.getEuler('yaw'))

#%%
def main():
    car = AutoCar()
    car.setSensorStatus(euler=1)
    car.setSpeed(50)
    restore = input("새로운 모델 생성이면 '1'을, 기존 모델 전이 학습이면 '2'을, 모델을 사용하여 주행이면 '3'을 입력해주세요 : ")
    if int(restore) == 1: # 새로운 모델 생성
        train(car, False)
        raise Exception("새 모델 학습이 완료되었습니다")
    elif int(restore) == 2: # 기존 모델 전이 학습
        train(car, True)
        raise Exception("전이 학습이 완료되었습니다")
    elif int(restore) == 3: # 모델을 사용하여 주행
        start = input("주행을 시작할까요? (y/n) : ")
        if start == 'y':
            seconds = input("몇 초동안 주행할까요? (5m는 11초 추천): ")
            LR = AI.Linear_Regression(True, ckpt_name="straight_model") # 기존 모델 사용
            start_yaw = yaw(car) # 현재 yaw 센서 값 찾아옴
            straight_value = LR.run(start_yaw) # 모델에 현재 yaw 값을 넣어서 직진 기준 값 가져옴
            print("출발시의 전방 값")
            print(straight_value)
            acc_num = 5 # 조향 가중치
            car.forward()
            for i in range((int(seconds))*3): # 입력된 시간만큼 주행
                real_yaw = yaw(car)
                print("현재 yaw 값:")
                print(float(LR.run(real_yaw)))
                need = (float(straight_value) - float(LR.run(real_yaw))) # 정중앙 값 - 현재 값
                print("계산된 값:")
                print(need)
                car.steering = need * acc_num # 계산된 값을 조향값에 넣음
                time.sleep(0.1)

            car.stop() # 정지
            print("주행이 종료되었습니다.")
            raise SystemExit # 시스템 종료
        elif start == 'n':
            raise Exception("종료합니다.")
        else:
            raise Exception("y 또는 n을 입력해주세요.")

    else:
        raise Exception("잘못된 값을 입력했습니다.") # 잘못된 모델 입력
    
if __name__ == "__main__":
    main()
# %%