from PyQt4 import QtGui
from PyQt4.QtCore import QThread, SIGNAL, QTimer
import sys
import ui_design_updated
from data_manipulation import GetSensorsThread
from data_manipulation import ProcessActuators
from data_manipulation import XYBuffer
import time
import datetime as dt
import numpy as np


class SensorProcessor(QtGui.QMainWindow, ui_design_updated.Ui_frm_main):

    def __init__(self):
        super(SensorProcessor, self).__init__()
        self.setupUi(self)
        self._init_elems()
        self._assign_events()
        self._retrieval_thread = GetSensorsThread()
        self._actuator_thread = None
        self._connect_signals()
        self._init_buffers()
        self._stop_plot = False
        self._connection_error = 0
        self.graph_timer = QTimer()
        self.lbl_act_lower.setText(str(self.slider_lower.value()))
        self.lbl_act_upper.setText(str(self.slider_upper.value()))
        self.set_lower_limit = 10
        self.set_upper_limit = 40
        self.show_set_limits()

    def _init_elems(self):
        '''initializes the elements on the GUI
        Can be used on restarting the process
        '''
        self.btn_Apply_Limit.setEnabled(False)
        self.btn_Stop.setEnabled(False)
        self.lbl_Temp_Value.setText('')
        self.lbl_Humidity_Value.setText('')

    def _assign_events(self):
        '''Assigns events to the GUI elements
        '''
        self.btn_Start.clicked.connect(self.start_retrieval)
        self.btn_Stop.clicked.connect(self.finish_retrieval)
        self.slider_lower.valueChanged[int].connect(self._update_lower_slider)
        self.slider_upper.valueChanged[int].connect(self._update_upper_slider)
        self.btn_Apply_Limit.clicked.connect(self._try_update_limits)
        
    def _connect_signals(self):
        '''Connects signals between the main thread and the background thread
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
        self.heating_buffer = XYBuffer(update_interval_secs=update_interval,
                                       total_secs=3600,
                                       data_type=np.int8)
        self.cooling_buffer = XYBuffer(update_interval_secs=update_interval,
                                       total_secs=3600,
                                       data_type=np.int8)
        self.ventilation_buffer = XYBuffer(update_interval_secs=update_interval,
                                           total_secs=3600,
                                           data_type=float)
              

    def start_retrieval(self):
        '''Runs the background thread to collect the data from the generator
        API
        '''
        if self._retrieval_thread.isRunning():
            return
        self._connection_error = 0
        self.btn_Start.setEnabled(False)
        self.btn_Stop.setEnabled(True)
        self.btn_Apply_Limit.setEnabled(True)
        self._retrieval_thread.start_thread = True
        self._retrieval_thread.start()
        self._stop_plot = False
        self.update_direct_graphs()
        self.update_actuator_graphs()

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
        self._retrieval_thread.wait()
        self._init_elems()
        self._init_buffers()

    def update_direct_graphs(self):
        '''Updates the Temperature and humidity plot
        '''
        x_temp, y_temp = self.temperature_buffer.get_actual_filled_values()
        x_humid, y_humid = self.humidity_buffer.get_actual_filled_values()

        self.gr_Temperature.plot(x_temp, y_temp, pen='r', clear=True)
        self.gr_Humidity.plot(x_humid, y_humid, pen='r', clear=True)

        if not self._stop_plot:
            self.graph_timer.singleShot(1000, self.update_direct_graphs)

    def update_actuator_graphs(self):
        '''Updates the actuator graphs
        '''
        x_heating, y_heating = self.heating_buffer.get_actual_filled_values()
        x_cooling, y_cooling = self.cooling_buffer.get_actual_filled_values()
        x_ventilation, y_ventilation = self.ventilation_buffer.get_actual_filled_values()

        self.gr_Heat_State.plot(x_heating, y_heating, pen='r', clear=True)
        self.gr_Cooling_state.plot(x_cooling, y_cooling, pen='r', clear=True)
        self.gr_Venting.plot(x_ventilation, y_ventilation, pen='r', clear=True)

        if not self._stop_plot:
            self.graph_timer.singleShot(1000, self.update_actuator_graphs)

    def show_set_limits(self):
        '''updates the actually set limits on the GUI
        '''
        self.lbl_set_lower.setText(str(self.set_lower_limit))
        self.lbl_set_upper.setText(str(self.set_upper_limit))

    def update_direct_labels(self, temp_val, temp_unit, humid_val,
                             humid_unit):
        '''Updates temperature and humidity value labels
        '''
        temperature = '{0:.2f} {1}'.format(temp_val, temp_unit)
        humidity = '{0:.2f} {1}'.format(humid_val, humid_unit)
        self.lbl_Temp_Value.setText(temperature)
        self.lbl_Humidity_Value.setText(humidity)

    def closeEvent(self, event):
        '''Once the user exits, the app waits for the threads to finish (To
        terminate everything correctly)
        '''
        print('CLOSING')
        if self._retrieval_thread.isRunning():
            print('CLOSING retrieval')
            self._retrieval_thread.start_thread = False
            self._retrieval_thread.wait()
        if self._actuator_thread is None:
            return
        if self._actuator_thread.isRunning():
            print('CLOSING actuator calculation')
            self._actuator_thread.wait()

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
        self._start_actuator_thread(temp_val, humid_val)

    def _start_actuator_thread(self, act_temperature, act_humidity):
        '''Starts the actuator processing thread
        
        Opposed to the _retrieval_thread, this thread run one sequence of
        commands
        '''
        self._actuator_thread = ProcessActuators(act_temperature,
                                                 act_humidity,
                                                 self.set_lower_limit,
                                                 self.set_upper_limit)
        self.connect(self._actuator_thread,
                     SIGNAL('actuator_values(PyQt_PyObject)'),
                     self._update_actuators)
        self._actuator_thread.start()

    def _update_actuators(self, actuator_values):
        '''Processes the data received from the _actuator_thread, updates the
        buffers.
        '''
        self.heating_buffer.append_value(actuator_values.heating)
        self.cooling_buffer.append_value(actuator_values.cooling)
        self.ventilation_buffer.append_value(actuator_values.ventilation)

    def _finished(self):
        '''sets back the state of the buttons to the initial state
        '''
        self.btn_Start.setEnabled(True)
        self.btn_Stop.setEnabled(False)
        self.btn_Apply_Limit.setEnabled(False)


    def _sensor_error(self):
        '''Error handler. Fired when the background thread can't read the
        sensor values
        '''
        self._connection_error += 1
        if self._connection_error == 1:
            msgBox = QtGui.QMessageBox()
            msgBox.setText('Data is not available')
            msgBox.exec_()
        self.finish_retrieval()



    def  _update_lower_slider(self, slider_value):
        '''updates the label linked to the lower slider
        '''
        self.lbl_act_lower.setText(str(slider_value))

    def  _update_upper_slider(self, slider_value):
        '''updates the label linked to the lower slider
        '''
        self.lbl_act_upper.setText(str(slider_value))

    def _try_update_limits(self):
        '''Checks the values of the horizontal sliders, if the values are ok,
        then it updates the set values
        '''
        new_lower_limit = self.slider_lower.value()
        new_upper_limit = self.slider_upper.value()
        if new_lower_limit >= new_upper_limit:
            msgBox = QtGui.QMessageBox()
            msgBox.setText('Lower limit cant be higher (or equal) than upper limit.')
            msgBox.exec_()
            return
        if new_lower_limit == self.set_lower_limit and \
           new_upper_limit == self.set_upper_limit:
            return
        self.set_lower_limit = new_lower_limit
        self.set_upper_limit = new_upper_limit
        self.show_set_limits()


def main():
    app = QtGui.QApplication(sys.argv)
    form = SensorProcessor()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
