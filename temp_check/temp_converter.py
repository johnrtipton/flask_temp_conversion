# -*- coding: utf-8 -*-
#
# Temperature Conversion Checker
# Checks the conversions between Kelvin, Celsius, Fahrenheit, and Rankine
#
# Calculations used in this class
# R = K * 1.8
# F = (K − 273.15) × 1.8 + 32 = -459.7
# C = K − 273.15
#
# K = R / 1.8
# K = (F -32) / 1.8 + 273.15
# K = C + 273.1
#

ACCEPTED_UNITS = [
    'Kelvin',
    'Fahrenheit',
    'Celsius',
    'Rankine'
]


class TempConverter(object):
    """
    Temperature Conversion Checker
    Checks the conversions between Kelvin, Celsius, Fahrenheit, and Rankine
    Example:
    >>> TempConverter.check_conversion(starting_value='84.2 Fahrenheit', student_answer=543.5, desired_unit='Rankine')
    """

    @classmethod
    def check_conversion(cls, starting_value=None, student_answer=None, desired_unit=None):
        """
        Checks Temperature conversion between units

        :param starting_value: Starting temperature value and unit
        :param student_answer: Temperature given by student
        :param desired_unit: Desired unit to convert to
        :return: str: 'incorrect', 'invalid', 'correct'
        """

        # Try to parse starting value string into temperature and unit
        try:
            starting_temp, unit = starting_value.split(' ')
            starting_temp = float(starting_temp)
        except ValueError:
            return 'invalid'

        # Check Units are valid
        try:
            assert unit in ACCEPTED_UNITS, 'Starting unit is not valid'
            assert desired_unit in ACCEPTED_UNITS, 'Desired unit is not valid'
        except AssertionError:
            return 'invalid'

        # Check Answer is a valid Float
        try:
            student_answer = float(student_answer)
        except (AssertionError, ValueError):
            return 'incorrect'

        correct_answer = cls.perform_conversion(starting_temp, unit, desired_unit)
        return cls.check_answer(student_answer, correct_answer)

    @classmethod
    def check_answer(cls, student_answer, correct_value):
        """
        Check for correct answer rounded to the ones place
        :param student_answer: Answer provided by student
        :param correct_value: Correct value
        :return: str: 'correct', 'incorrect'
        """
        # print('Student value: %s\t\tCorrect value: %s' % (round(student_answer), round(correct_value)))
        if round(student_answer) == round(correct_value):
            return 'correct'
        return 'incorrect'

    @classmethod
    def perform_conversion(cls, starting_temp, unit, desired_unit):
        """
        Perform conversion from starting unit to desired unit
        :param starting_temp: Starting Temperature
        :param unit: Starting Unit
        :param desired_unit: Desired Unit
        :return: float: Temperature in desired unit
        """
        # Convert to Kelvin
        kelvin = cls.to_kelvin(starting_temp, unit)

        # Convert to Desired Unit
        correct_value = cls.from_kelvin(kelvin, desired_unit)
        return correct_value

    @staticmethod
    def to_kelvin(value, unit):
        """
        Converts given value to Kelvin
        :param value: Starting temperature
        :param unit: Starting temperature unit
        :return: float: Temperature in Kelvin
        """
        if unit == 'Rankine':
            return value / 1.8
        elif unit == 'Fahrenheit':
            return ((value - 32) / 1.8) + 273.15
        elif unit == 'Celsius':
            return value + 273.1
        elif unit == 'Kelvin':
            return value
        return 'invalid'

    @staticmethod
    def from_kelvin(kelvin, desired_unit):
        """
        Converts given Kelvin temperature to desired unit
        :param kelvin: Kelvin temperature
        :param desired_unit: Desired unit to convert temperature to
        :return: float: Temperature in desired unit
        """
        if desired_unit == 'Rankine':
            return kelvin * 1.8
        elif desired_unit == 'Fahrenheit':
            return ((kelvin - 273.15) * 1.8) + 32
        elif desired_unit == 'Celsius':
            return kelvin - 273.15
        elif desired_unit == 'Kelvin':
            return kelvin
        return 'invalid'
