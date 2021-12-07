# Rocket Stand

Goal : Create a Test stand for measuring rocket motor performances 

## Hardware 

### Components
- LoadCell : 100kg load cell to measure force applied on one end by metal deflection. Link [FR](https://www.amazon.fr/gp/product/B07TXZL11N) [US](https://www.amazon.com/Electronic-CellScale-Precision-Parallel-Weighting/dp/B082Q1P87H/)
- Arduino NANO + Breadboard
- HXZ11 PCB breakout loadcell amplifier 
- Relay PCB breakout board for Electric Starter 


### Design 
- Based on scraps of 4040 aluminium extrusion 
- OpenRail linear rail [Example](https://openbuildspartstore.com/openrail-linear-rail/)
- 3D printed box for attaching electronics. (See .3mf file)


## Arduino Code 

Flashed on the arduino it reads the loadcell value and start the pyrotechnic charge using the relay 

Install arduino lib (available on Library Manager) [Github link](https://github.com/bogde/HX711/)

```
#include <HX711.h>
HX711 loadcell;

// 1. HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 3;
const int LOADCELL_SCK_PIN = 2;

void setup()
{

  // 3. Initialize library
  loadcell.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  loadcell.tare();
  loadcell.set_scale(38.81);
  Serial.begin(115200);
};

void loop()
{
  Serial.println (loadcell.get_units (1), 0);
}
```

## Python launch script 

You can launch the python script using the following command :

`python src/launch.py`

## Output 

The script will display the countdown and record data (by default countdown is set to 10 sec and the test will end at T +10s ).

One the test is done, you can look at the data saved as a csv and the plot of the value over time. 



