from unittest import main, mock, TestCase
import subprocess
from main import main as program

ticket_booking_inputs = [
      "Inception 8 10",
      "1",
      "4",
      "B03",
      "",
      "1",
      "77",
      "12",
      "B05",
      ""
    ]

# Hard-coded booking ids since session information is not stored after program termination for this exercise.
booking_ids = ["GIC0001", "GIC0002"]

check_booking_inputs = [
  "2",
  booking_ids[0],
  booking_ids[1],
  ""
]

class TestMain(TestCase):
  @mock.patch("builtins.input")
  def test_0(self, mocked_input):
    """
    Test ticket booking
    """
    print("Starting test 0: Test create booking and change seats\n")
    test_inputs = ticket_booking_inputs + ["3"]
    # print(test_inputs)
    mocked_input.side_effect = test_inputs
    program()

  @mock.patch("builtins.input")
  def test_1(self, mocked_input):
    """
    Test check bookings
    """
    print("Starting test 0: Test check booking and exiting app\n")
    test_inputs = ticket_booking_inputs + check_booking_inputs + ["3"]
    # print(test_inputs)
    mocked_input.side_effect = test_inputs
    program()

if __name__ == "__main__":
  main()