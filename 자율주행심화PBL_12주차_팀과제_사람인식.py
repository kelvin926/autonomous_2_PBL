
#%%
from pop import Pilot, AI

cam = Pilot.Camera(width=224, height=224)
car = Pilot.AutoCar()

object_follow = AI.Object_Follow(cam)
object_follow.load_model()

#%%
while True:
    ret = object_follow.detect(index='person')

    if ret is not None:
        steer = ret['x'] * 4
        car.steering = 1 if steer > 1 else -1 if steer < -1 else steer
        
        if object_follow['size_rate'] < 0.20: #실제 이 값으로 대상이 멀어졌다고 판단하기 힘듬
            car.forward(50)
        else:
            car.stop()
    else:
        car.stop()