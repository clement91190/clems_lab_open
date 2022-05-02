#%% 
import serial  #pip install pyserial
from IPython.display import clear_output, display
import time 
import pandas as pd  # only for plot of results 


ARDUINO_PORT = '/dev/ttyUSB0'
ARDUINO_PORT = '/dev/cu.usbserial-1110'
# %%


class RocketStandInterface():
    def __init__(self, timeout=10, timeout_recording_after_launch=10):
        """
        timeout_recording_after_launch : stop recording data x seconds after launch
        """
        self.ser = serial.Serial(ARDUINO_PORT, 115200, timeout=1)
        self.thrust_data = []
        self.in_launch_seq = False
        self.launched = False
        # (Time of start countdown, countdown value)
        self.launch_time_val = (None, None)
        self.timeout_recording_after_launch = timeout_recording_after_launch
        self.timeout = timeout
        self.test_over = True
        self.last_cd_print = time.time()
    
    def reset(self):
        self.thrust_data = []
        self.launched = False
        self.in_launch_seq = False

    def test_connection(self):
        time.sleep(1)
        return self.ser.inWaiting() > 0

    def start_recording(self, timeout_after_launch = 10):

        self.record = True
        if (self.ser.inWaiting() > 0):
            # clean buffer
            data_str = self.ser.read(self.ser.inWaiting()).decode('ascii') 

    def stop_recording(self):
        self.record = False 

    def check_recording(self):
        if self.record:
            if (self.ser.inWaiting() > 0):
                # read the bytes and convert from binary array to ASCII
                data_str = self.ser.read(self.ser.inWaiting()).decode('ascii') 
                # print the incoming string without putting a new-line
                # ('\n') automatically after every print()
                thrust_in_g = int(data_str.split('\r\n')[0])
                self.thrust_data.append(dict(ts=-self.get_countdown_val() , thrust_in_g=thrust_in_g))


    def check_test_over(self):
        
        count_down_val = self.get_countdown_val()
        #print ("comparing", count_down_val, self.timeout_recording_after_launch)
        if count_down_val is not None and self.timeout_recording_after_launch <= -count_down_val:
            self.stop_recording()
            self.test_over = True 

    def launch(self):
        # starts the charge using the relay board.
        # don't use directly 
        print("LAUNCH")
        self.launched = True 

    def start_countdown(self):
        """ timeout int to start countdown from. """
        self.reset()
        self.start_recording()
        self.test_over = False
        self.in_launch_seq = True
        self.launch_time_val = (time.time(), self.timeout)
        while not self.test_over:
            self.run()
    
    def get_countdown_val(self):
        tstart, timeout = self.launch_time_val
        if tstart is not None and timeout is not None: 
            count_down_val = timeout - (time.time() - tstart)
            return count_down_val
        else:
            return None
      
    def check_countdown(self):
        if self.in_launch_seq:
            count_down_val = self.get_countdown_val()

            if time.time() - self.last_cd_print > 1.0:
                clear_output(wait=False)
                format_cd = "{:.2f}".format(- int(count_down_val))
                print('Countdown', format_cd)
                self.last_cd_print = time.time()
        
            if count_down_val < 0:
                if not self.launched:
                    self.launch()

    def run(self):
        self.check_recording()
        self.check_countdown()
        self.check_test_over()

    def display_result(self):
        df = pd.DataFrame(self.thrust_data)
        print(df)
        df = df.set_index('ts')
        pl = df['thrust_in_g'].plot()
        t = int(time.time())
        df.to_csv("data{t}.csv".format(t=t))
        pl.get_figure().savefig("plot{}.png".format(t))
        pl.get_figure().show()
    

# %%
rs = RocketStandInterface()

# %%
while (not rs.test_connection()):    
    print("No connection, keep trying ")
    

rs.start_countdown()
rs.display_result()

# %%
