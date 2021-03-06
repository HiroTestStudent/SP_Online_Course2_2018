"""
Unit tests for the water-regulation module
"""

import urllib.request
import unittest
from unittest.mock import MagicMock
from pump import Pump
from sensor import Sensor
from controller import Controller
from decider import Decider


class DeciderTests(unittest.TestCase):
    """Unit tests for the Decider class"""

    def setUp(self):
        """Set up each test with an actions dict"""
        self.actions = {'PUMP_IN': 1,
                        'PUMP_OFF': 0,
                        'PUMP_OUT': -1}
        self.decider = Decider(100, 0.05)

    def test_pump_off_and_height_below_margin(self):
        """
        1. If the pump is off and the height is below the margin region,
        then the pump should be turned to PUMP_IN.
        """
        self.assertEqual(1, self.decider.decide(101, 0, self.actions))

    def test_pump_off_and_height_above_margin(self):
        """
        2. If the pump is off and the height is above the margin region,
        then the pump should be turned to PUMP_OUT.
        """
        self.assertEqual(-1, self.decider.decide(106, 0, self.actions))

    def test_pump_off_and_height_is_above_target_but_equal_margin(self):
        """
        3. If the pump is off and the height is within the margin region
        or on the exact boundary of the margin region, then the pump shall
         remain at PUMP_OFF.
        """
        self.assertEqual(0, self.decider.decide(105, 0, self.actions))

    def test_pump_on_and_height_above_margin(self):
        """
4a. If the pump is performing PUMP_IN and the height is above the target
             height, then the pump shall be turned to PUMP_OFF
        """
        self.assertEqual(0, self.decider.decide(110, 1, self.actions))

    def test_pump_on_and_height_below_margin(self):
        """
4b. If the pump is performing PUMP_IN and the height is below the target
             height, then the pump shall remain PUMP_IN
        """
        self.assertEqual(1, self.decider.decide(99, 1, self.actions))

    def test_pump_out_and_height_below_margin(self):
        """
5a. If the pump is performing PUMP_OUT and the height is below the target
             height, then the pump shall be turned to PUMP_OFF
        """
        self.assertEqual(0, self.decider.decide(90, -1, self.actions))

    def test_pump_out_and_height_above_margin(self):
        """
5b. If the pump is performing PUMP_OUT and the height is above the target
             height, then the pump shall remain PUMP_OUT
        """
        self.assertEqual(-1, self.decider.decide(190, -1, self.actions))


class ControllerTests(unittest.TestCase):
    """Unit tests for the Controller class"""

    def setUp(self):
        """A controller with basic configuration."""
        self.ip_addr = '127.0.0.1'
        self.port = '8000'
        urllib.request.urlopen = MagicMock(return_value=5)
        self.sensor = Sensor(self.ip_addr, self.port)
        self.pump = Pump(self.ip_addr, self.port)
        self.pump.set_state(MagicMock(return_value=True))
        self.decider = Decider(100, 0.05)
        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_controller_tick(self):
        """Verify the Controller ticks as expected"""
        self.sensor.measure = MagicMock(return_value=110)
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_IN)
        self.decider.decide = MagicMock(return_value=self.pump.PUMP_OFF)
        self.pump.set_state = MagicMock(return_value=True)

        self.controller.tick()

        self.sensor.measure.assert_called_with()
        self.pump.get_state.assert_called_with()
        self.decider.decide.assert_called_with(110, self.pump.PUMP_IN)
        self.pump.set_state.assert_called_with(self.pump.PUMP_OFF)
