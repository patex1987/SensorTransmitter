from PyQt4 import QtGui
from PyQt4.QtCore import QThread, SIGNAL, QTimer
import sys
import ui_design_updated
from data_manipulation import GetSensorsThread
from data_manipulation import XYBuffer
import time
import datetime as dt
import numpy as np


class SensorProcessor(QtGui.QMainWindow, ui_design_updated.Ui_frm_main):

    def __init__(self):
        super(SensorProcessor, self).__init__()
        self.setupUi(self)
        self._init_elems()
        self.btn_Start.clicked.connect(self.start_retrieval)
        self.btn_Stop.clicked.connect(self.finish_retrieval)
        self._retrieval_thread = GetSensorsThread()
        self._connect_signals()
        self._init_buffers()
        self._stop_plot = False
        self.graph_timer = QTimer()

    def _init_elems(self):
        '''initializes the elements on the GUI
        '''
        #self.inp_Lower_Temp.setEnabled(False)
        #self.inp_Upper_Temp.setEnabled(False)
        self.btn_Apply_Limit.setEnabled(False)
        self.btn_Stop.setEnabled(False)
        self.lbl_Temp_Value.setText('')
        self.lbl_Humidity_Value.setText('')

    def _connect_signals(self):
        '''Connects signals betwwen the main thread and the background thread
        '''
        self.connect(self._retrieval_thread,
                     SIGNAL('update_values(PyQt_PyObject)'),
                     self._process_values)
        self.connect(self._retrieval_thread, SIGNAL('handle_error()'),
                     self._sensor_error)
        self.connect(self._retrieval_thread, SIGNAL('finished()'),
                     self._finished)

    def _init_buffers(self):
        '''Initializes ring buffers to hold data for the graphs, later can be
        used to empty the buffers
        '''
        update_interval = self._retrieval_thread.update_interval_secs
        self.temperature_buffer = XYBuffer(update_interval_secs=update_interval,
                                           total_secs=3600,
                                           data_type=float)
        self.humidity_buffer = XYBuffer(update_interval_secs=update_interval,
                                        total_secs=3600,
                                        data_type=float)

    def start_retrieval(self):
        '''Runs the background thread to collect the data from the generator
        API
        '''
        if self._retrieval_thread.isRunning():
            return
        self.btn_Start.setEnabled(False)
        self.btn_Stop.setEnabled(True)
        self._retrieval_thread.start_thread = True
        self._retrieval_thread.start()
        self._stop_plot = False
        self.update_direct_graphs()

    def finish_retrieval(self):
        '''Sends a flag to the background thread to finish its activity

        The thread finishes its last cycle (if one is in progress), then it
        can safely turn off the GUI
        '''
        if not self._retrieval_thread.isRunning():
            return
        self._finished()
        self._retrieval_thread.start_thread = False
        self._stop_plot = True

    def _process_values(self, sensor_values):
        '''Processes the data coming from the background thread
        '''
        temp_val = sensor_values['temperature']['actual_value']
        temp_unit = sensor_values['temperature']['unit']
        humid_val = sensor_values['humidity']['actual_value']
        humid_unit = sensor_values['humidity']['unit']
        self.update_direct_labels(temp_val, temp_unit, humid_val, humid_unit)
        self.temperature_buffer.append_value(temp_val)
        self.humidity_buffer.append_value(humid_val)

    def _finished(self):
        self.btn_Start.setEnabled(True)
        self.btn_Stop.setEnabled(False)

    def _sensor_error(self):
        '''Error handler. Fired when the background thread can't read the
        sensor values
        '''
        pass

    def update_direct_labels(self, temp_val, temp_unit, humid_val,
                             humid_unit):
        '''Updates temperature and humidity value labels
        '''
        temperature = '{0:.2f} {1}'.format(temp_val, temp_unit)
        humidity = '{0:.2f} {1}'.format(humid_val, humid_unit)
        self.lbl_Temp_Value.setText(temperature)
        self.lbl_Humidity_Value.setText(humidity)

    def update_direct_graphs(self):
        '''Updates the Temperature and humidity plot
        '''
        x_temp, y_temp = self.temperature_buffer.get_actual_filled_values()
        x_humid, y_humid = self.humidity_buffer.get_actual_filled_values()

        self.gr_Temperature.plot(x_temp, y_temp, pen='r', clear=True)
        self.gr_Humidity.plot(x_humid, y_humid, pen='r', clear=True)

        if not self._stop_plot:
            self.graph_timer.singleShot(3, self.update_direct_graphs)

    def closeEvent(self, event):
        pass


def main():
    app = QtGui.QApplication(sys.argv)
    form = SensorProcessor()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
