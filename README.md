# Electronic Technologies and Biosensors Laboratory

## Academic Year 2021/2022 - II Semester

## Final Project - Project 5 - Sleep position classifier
## Objective
The aim of this project was to develop a system able to correctly classify and forecast 12 typical sleep positions, using the data from two accelerometes LIS3DH placed one on the chest and one on the right ankle. 
The finished project includes: 
- development of the wearable device
- data acquisition
- data processing
- GUI for data visualization
- machine learning architecture able to perform sleep position classification

The PSoC communicates with the LIS3DH sensors using I2C communication with sampling frequency set at 10Hz. 
The communication between PSoC device and the pc was created using a HC05 Bluetooth module, in order to make the device wearable.
Also for wearability, the device is powered with a 9V battery and a subsequent 9 to 5 voltage transformer.
### Hardware
- 2 LIS3DH accelerometers
- 1 HC05 Bluetooth module
- 1 9V battery
- 1 9to5 voltage transformer
- 1 PSoC CY8CKIT-059 
- 1 breadboard
- 2 3D printed casings used to encapsulate the accelerometers and place them on the body
- 6 2m long cables to connect the accelerometers to the PSoC
- 2 modular velcro bands to fix the accelerometers in place 

The links between the PSoC and the different components can be found in the dedicated folder in the form of the $hardware setup$ paper and the eagle schematic and board files.
The casing's 3D model can also be found in the dedicated folder.

### PSoC code
This file contains all the code needed by the GUI to access to the data sampled and averaged by the accelerometers. 
This section of code is responsible for data acquisition and processing, which includes managing the PSoC registers (reading them, writing them and averaging the values sampled by both sensors) and for the communication between the bluetooth module and the pc. 
The different operations are managed with an UART which parses through the operations based on the data it receives from the GUI. 
When the user clicks $Start sampling$ the PSoC code is put into motion, the data from the accelerometers is sampled, averaged, and sent back to the GUI with the bluetooth module, for each position.
All code files of this section have been individually commented for clarity.

### GUI code



