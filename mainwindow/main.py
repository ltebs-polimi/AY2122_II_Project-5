## ---------------------------------------------------------------------------------------
##
## PYQT APPLICATION FOR DATA VISUALIZATION OF ACCELEROMETER DATA + SLEEP POSITION ANALYSIS
##
## Electronic Technologies and Biosensors Laboratory
##
## Franke Patrick, Canavate Chloé, Alfonzo Massimo
##
## ---------------------------------------------------------------------------------------


## Importing necessary libraries
import sys
import time
import logging
import csv
# from datetime import date
import datetime

from PyQt5 import QtCore
from PyQt5.QtCore import (
    QObject,
    QThreadPool,
    QRunnable,
    pyqtSignal,
    pyqtSlot
)

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QComboBox,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QLabel,
)

import serial
import serial.tools.list_ports


# Globals
CONN_STATUS = False


# Logging config
logging.basicConfig(format="%(message)s", level=logging.INFO)


#########################
# SERIAL_WORKER_SIGNALS #
#########################
class SerialWorkerSignals(QObject):
    """!
    @brief Class that defines the signals available to a serialworker.

    Available signals (with respective inputs) are:
        - device_port:
            str --> port name to which a device is connected
        - status:
            str --> port name
            int --> macro representing the state (0 - error during opening, 1 - success)
    """
    device_port = pyqtSignal(str)
    status = pyqtSignal(str, int)


#################
# SERIAL_WORKER #
#################
class SerialWorker(QRunnable):
    """!
    @brief Main class for serial communication: handles connection with device.
    """
    def __init__(self, serial_port_name):
        """!
        @brief Init worker.
        """
        self.is_killed = False
        super().__init__()
        # init port, params and signals
        self.port = serial.Serial()
        self.port_name = serial_port_name
        self.baudrate = 9600 # hard coded but can be a global variable, or an input param
        self.signals = SerialWorkerSignals()

    @pyqtSlot()
    def run(self):
        """!
        @brief Establish connection with desired serial port.
        """
        global CONN_STATUS

        if not CONN_STATUS:
            try:
                self.port = serial.Serial(port=self.port_name, baudrate=self.baudrate,
                                        write_timeout=0, timeout=2)
                if self.port.is_open:
                    CONN_STATUS = True
                    self.signals.status.emit(self.port_name, 1)
                    print("Successfully connected to port {}.".format(self.port_name))
                    time.sleep(0.01)

            except serial.SerialException:
                logging.info("Error with port {}.".format(self.port_name))
                self.signals.status.emit(self.port_name, 0)
                time.sleep(0.01)


    @pyqtSlot()
    def sample(self):
        """!
        @brief Sample data from desired serial port
        """

        if CONN_STATUS:
            try:
                # Set button_start from "Start" to "Stop"
                # button_start.setText("Stop")

                # Initialize list for incoming data
                data = []

                # Sample for 18 minutes
                t_end = time.time() + 10

                print("Start sampling.")

                line = ''

                while time.time() < t_end:

                    read = str(self.port.read())
                    read = read[2]

                    if (read != 'E'):
                        line += read

                    # add error handling for when S is missing

                    if (read == 'E'):
                        line = line[2:]
                        data.append(line.split(','))
                        line = ''

                print("End of sampling.")
                print(data)

                # Print data for debugging
                #print(data)

                # Data transformation for better reading
                # tbd

                # data rows of csv file (for testing, delete later)
                # rows = [ ['0', '250', '250', '250', '0', '250'],
                #          ['2', '251', '245', '251', '5', '247'],
                #          ['4', '250', '247', '252', '7', '243']]
                #
                # Saving data as CSV file
                labels = ['x1', 'y1', 'z1', 'x2', 'y2', 'z2']

                date = datetime.datetime.now()
                date = date.strftime("%Y%m%d_%H%M%S")
                csv_name = "bluetooth_data_{}.csv".format(date)

                with open(csv_name, 'w') as f:

                    # using csv.writer method from CSV package
                    write = csv.writer(f)

                    write.writerow(labels)
                    write.writerows(data)

                time.sleep(0.01)

            except: # except serial.SerialException:
                logging.info("Error with reading data from port {}.".format(self.port_name))
                # self.signals.status.emit(self.port_name, 0)
                time.sleep(0.01)

        else:
            print("Not connected to any port. Please first connect to a port.")


    @pyqtSlot()
    def send(self, char):
        """!
        @brief Basic function to send a single char on serial port.
        """
        try:
            self.port.write(char.encode('utf-8'))
            logging.info("Written {} on port {}.".format(char, self.port_name))
        except:
            logging.info("Could not write {} on port {}.".format(char, self.port_name))


    @pyqtSlot()
    def killed(self):
        """!
        @brief Close the serial port before closing the app.
        """
        global CONN_STATUS
        if self.is_killed and CONN_STATUS:
            self.port.close()
            time.sleep(0.01)
            CONN_STATUS = False
            self.signals.device_port.emit(self.port_name)

        logging.info("Killing the process")


###############
# MAIN WINDOW #
###############
class MainWindow(QMainWindow):
    def __init__(self):
        """!
        @brief Init MainWindow.
        """
        # define worker
        self.serial_worker = SerialWorker(None)

        super(MainWindow, self).__init__()

        # title and geometry
        self.setWindowTitle("Sleep Position Classification")
        width = 400
        height = 400
        self.setMinimumSize(width, height)

        # create thread handler
        self.threadpool = QThreadPool()

        self.connected = CONN_STATUS
        self.serialscan()
        self.initUI()


    #####################
    # GRAPHIC INTERFACE #
    #####################
    def initUI(self):
        """!
        @brief Set up the graphical interface structure.
        """
        # Layout
        label_choose = QLabel('Choose port for reading:')
        label_sample = QLabel('Start sampling data (for 18 mins):')

        self.button_start = QPushButton(
            text=('Start'),
            checkable=True,
            toggled=self.sample
        )

        label_data = QLabel('Accelerometer data:')

        layout = QVBoxLayout()
        layout.addWidget(label_choose)
        layout.addWidget(self.com_list_widget)
        layout.addWidget(self.conn_btn)
        layout.addWidget(label_sample)
        layout.addWidget(self.button_start)
        layout.addWidget(label_data)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    ####################
    # SERIAL INTERFACE #
    ####################
    def serialscan(self):
        """!
        @brief Scans all serial ports and creates a list.
        """
        # create the combo box to host port list
        self.port_text = ""
        self.com_list_widget = QComboBox()
        self.com_list_widget.currentTextChanged.connect(self.port_changed)

        # create the connection button
        self.conn_btn = QPushButton(
            text=("Connect to port {}".format(self.port_text)),
            checkable=True,
            toggled=self.on_toggle
        )

        # acquire list of serial ports and add it to the combo box
        serial_ports = [
                p.name
                for p in serial.tools.list_ports.comports()
            ]
        self.com_list_widget.addItems(serial_ports)


    ##################
    # SERIAL SIGNALS #
    ##################
    def port_changed(self):
        """!
        @brief Update conn_btn label based on selected port.
        """
        self.port_text = self.com_list_widget.currentText()
        self.conn_btn.setText("Connect to port {}".format(self.port_text))

    @pyqtSlot(bool)
    def on_toggle(self, checked):
        """!
        @brief Allow connection and disconnection from selected serial port.
        """
        if checked:
            # setup reading worker
            self.serial_worker = SerialWorker(self.port_text) # needs to be re defined
            # connect worker signals to functions
            self.serial_worker.signals.status.connect(self.check_serialport_status)
            self.serial_worker.signals.device_port.connect(self.connected_device)
            # execute the worker
            self.threadpool.start(self.serial_worker)
        else:
            # kill thread
            self.serial_worker.is_killed = True
            self.serial_worker.killed()
            self.com_list_widget.setDisabled(False) # enable the possibility to change port
            self.conn_btn.setText(
                "Connect to port {}".format(self.port_text)
            )

    def check_serialport_status(self, port_name, status):
        """!
        @brief Handle the status of the serial port connection.

        Available status:
            - 0  --> Error during opening of serial port
            - 1  --> Serial port opened correctly
        """
        if status == 0:
            self.conn_btn.setChecked(False)
        elif status == 1:
            # enable all the widgets on the interface
            self.com_list_widget.setDisabled(True) # disable the possibility to change COM port when already connected
            self.conn_btn.setText(
                "Disconnect from port {}".format(port_name)
            )

    def connected_device(self, port_name):
        """!
        @brief Checks on the termination of the serial worker.
        """
        logging.info("Port {} closed.".format(port_name))


    @pyqtSlot(bool)
    def sample(self, checked):
        """!
        @brief Samples data from the selected port.
        """

        if checked:
            print("Sample if")

            self.button_start.setText("Stop")

            self.serial_worker.sample()


            #self.threadpool.start(self.serial_worker)
            # # setup reading worker
            # self.serial_worker = SerialWorker(self.port_text) # needs to be re defined
            # # connect worker signals to functions
            # self.serial_worker.signals.status.connect(self.check_serialport_status)
            # self.serial_worker.signals.device_port.connect(self.connected_device)
            # # execute the worker
            # self.threadpool.start(self.serial_worker)
        else:
            print("Sample else")

            # self.serial_worker.is_killed = True
            # self.serial_worker.killed()
            # # kill thread
            # self.serial_worker.is_killed = True
            # self.serial_worker.killed()
            # self.com_list_widget.setDisabled(False) # enable the possibility to change port
            # self.conn_btn.setText(
            #     "Connect to port {}".format(self.port_text)
            # )



    def ExitHandler(self):
        """!
        @brief Kill every possible running thread upon exiting application.
        """
        self.serial_worker.is_killed = True
        self.serial_worker.killed()



#############
#  RUN APP  #
#############
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()

    app.aboutToQuit.connect(w.ExitHandler)
    w.show()
    sys.exit(app.exec_())
