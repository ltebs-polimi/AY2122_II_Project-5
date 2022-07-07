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
This section contains all the code needed by the GUI to access to the data sampled and averaged by the accelerometers. 
This section of code is responsible for data acquisition and processing, which includes managing the PSoC registers (reading them, writing them and averaging the values sampled by both sensors) and for the communication between the bluetooth module and the pc. 

The different operations are managed with an UART which parses through the operations based on the data it receives from the GUI. 
When the user clicks $Start  sampling$ the PSoC code is put into motion, the data from the accelerometers is sampled, averaged, and sent back to the GUI with the bluetooth module, for each position.


All code files of this section have been individually commented for clarity.

### GUI code
This section of code deals with establishing a connection between pc and PSoC device via bluetooth module, visualizing the data sampled in real time and producing a csv files with all the samplings used to train the machine learning module. 
It follows a description of the most important subsections of code, but the code has been commented throughout for clarity.
#### $Serial interface$
This subsection is devoted to scanning all serial ports and createing a list used in the drowp down menu
#### $Serial Worker$
The **Serial Worker** class handles the connection with the PSoC device by estabilishing a connection with desired serial port (selectable in a drop down menu), reading data from desired serial port from start (S) to end (E) tokens, **storing iteratively** the read lines in the data object and saving them at the end of the protocol in a single csv file.  
It's also responsible for sending char data on the serial port and closing the serial port before closing the app.
#### $Graphic interface$ 
This sub-section of code deals with creating the window used by all the plot widgets and the various buttons. 
It's worth noting that the 6 data charts are plotted on the same window by first removing oldest element, then adding the new elements, and finally updating the data.
#### $Main$
The main is responsible for setting the window size, creating the thread handler and initializing all the functions previously mentioned.

### Machine Learning
#### $Install$
The Machine Learning portion of this project was created using a shared Jupyter Notebook. It requires the following Python libraries:
- [NumPy](http://www.numpy.org/)
- [Pandas](http://pandas.pydata.org)
- [seaborn](https://seaborn.pydata.org/)
- [matplotlib](http://matplotlib.org/)
- [scikit-learn](http://scikit-learn.org/stable/)

Every library used and any function needed is clearly listed and commented troughout the code.

#### $Data$
In order to run the code, it's necessary to download the csv files produced by us during the sampling, and either install them in the path 
/content/drive/MyDrive/Sleep_classifier/, or change the path used in that cell while running the code.

The data consists in 11 csv files sampled from 11 different people, it's worth nothing that the file 'fabio_20220601_193018.csv' was discarted 
due to errors during the sampling procedure, thus we ended up with 10 different people, in order to guarantee inter-subject variabilty.

##### $Run$
To run the code, simply run sequentially every data cell. 
The gridsearch function will be available, but only the best parameters will be provided for each model. 

#### $Features$
The data was gathered from 2 accelerometers, one on the chest and one on the right ankle therefore we have 6 inputs:
- x_chest
- y_chest
- z_chest
- x_ankle
- y_ankle
- z_ankle

#### $Target Variable$
The variable that we need to predict is the sleeping position. It can be one of twelve position

