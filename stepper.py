# Motor Class
# Cameron Vela, Vraj Patel, Lucas Billington


import time
import multiprocessing
from shifter import Shifter   

class Stepper:
   
    num_steppers = 0      # track number of Steppers instantiated
    shifter_outputs = 0   
    seq = [0b0001,0b0011,0b0010,0b0110,0b0100,0b1100,0b1000,0b1001] # CCW sequence
    delay = 10000          # delay between motor steps [us]
    steps_per_degree = (4096)/(360*4)    # 4096 steps/rev * 1/360 rev/deg

    def __init__(self, shifter, lock):
        self.s = shifter           # shift register
        self.angle = multiprocessing.Value('d') 
        self.step_state = 0        # track position in sequence
        self.shifter_bit_start = 4*Stepper.num_steppers  # starting bit position
        self.lock = lock           # multiprocessing lock

        Stepper.num_steppers += 1   # increment the instance count

    # Signum function:
    def __sgn(self, x):
        if x == 0: return(0)
        else: return(int(abs(x)/x))

   # Move a single +/-1 step in the motor sequence:
    def __step(self, dir):
        self.step_state += dir    # increment/decrement the step
        self.step_state %= 8      # ensure result stays in [0,7]
        mask = 0b1111 << self.shifter_bit_start 
        
        slock = Stepper.shifter_outputs.get_lock() # Wait for lock to be available and aquire
        slock.acquire()
        
        current = Stepper.shifter_outputs.value         # Assigns current bits to a variable to be manipulated without impacting the actual values yet           
        current &= ~mask                                # Prevents overwriting of second motor bits            
        current |= (Stepper.seq[self.step_state] << self.shifter_bit_start) # Inserts new 4 bits into correct position
        Stepper.shifter_outputs.value = current         # Assigns the actual bit values to their new values after they have been correctly changed            
        self.s.shiftByte(current)
        
        slock.release() 

        alock = self.angle.get_lock()
        alock.acquire()
        self.angle.value = (self.angle.value + dir/Stepper.steps_per_degree) % 360
        alock.release() 
        

    
    def __rotate(self, delta):
        self.lock.acquire()                
        numSteps = int(Stepper.steps_per_degree * abs(delta))    
        dir = self.__sgn(delta)        
        for s in range(numSteps):      
            self.__step(dir)
            time.sleep(Stepper.delay/1e6)
        self.lock.release()



    def rotate(self, delta):
        time.sleep(0.1)
        p = multiprocessing.Process(target=self.__rotate, args=(delta,))
        p.start()
        p.join()



    def goAngle(self, angle):
        alock = self.angle.get_lock()
        
        alock.acquire()
        currenta = self.angle.value
        alock.release()
        
        diff = ((angle - currenta + 180) % 360) - 180
        self.rotate(diff)


    def zero(self):
        alock = self.angle.get_lock()
        alock.acquire()
        self.angle.value = 0.0
        alock.release()

