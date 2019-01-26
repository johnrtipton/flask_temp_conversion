from .temp_converter import TempConverter


def test_correct_answers():
    """Check correct answers."""
    assert TempConverter.check_conversion(
        starting_value='84.2 Fahrenheit', student_answer=543.5, desired_unit='Rankine') == 'correct'

    assert TempConverter.check_conversion(
        starting_value='-45.14 Celsius', student_answer=227.51, desired_unit='Kelvin') == 'correct'

    assert TempConverter.check_conversion(
        starting_value='317.33 Kelvin', student_answer=112, desired_unit='Fahrenheit') == 'correct'

    assert TempConverter.check_conversion(
        starting_value='444.5 Rankine', student_answer=-26, desired_unit='Celsius') == 'correct'


def test_incorrect_answers():
    """Test incorrect answers."""
    assert TempConverter.check_conversion(
        starting_value='317.33 Kelvin', student_answer=110.5, desired_unit='Fahrenheit') == 'incorrect'

    assert TempConverter.check_conversion(
        starting_value='444.5 Rankine', student_answer=-10, desired_unit='Celsius') == 'incorrect'


def test_invalid_input():
    """Test invalid input"""
    # Invalid student_answer
    assert TempConverter.check_conversion(
        starting_value='6.5 Fahrenheit', student_answer='dog', desired_unit='Rankine') == 'incorrect'
    # Invalid starting_value
    assert TempConverter.check_conversion(
        starting_value='dog', student_answer='45.32', desired_unit='Celsius') == 'invalid'
    # Misspelled desired_unit
    # noinspection SpellCheckingInspection
    assert TempConverter.check_conversion(
        starting_value='444.5 Rankine', student_answer=-26, desired_unit='Celsiu') == 'invalid'
    # Misspelled starting_value
    assert TempConverter.check_conversion(
        starting_value='444.5 Rankin', student_answer=-26, desired_unit='Celsius') == 'invalid'
