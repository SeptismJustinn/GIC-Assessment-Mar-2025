from cinema.booking import Booking

class Screening:
  def __init__(self, title, rows, spr):
    # Store inputs
    self.title = title
    self.rows = rows
    self.spr = spr

    # Generate theatre based on rows and spr
    # Seats are initialized as 0, indicating unoccupied. Occupied seats should be indicated by booking ID.
    self.theatre = rows * [spr * [0]]
    # Separate vacancies counter to prevent needing to iterate through matrix to count empty seats.
    self.vacancies = rows * spr

    # Initialize empty dict of bookings. Shape: {'booking_id': < Booking object >}
    self.bookings = {}

    # Initialize starting booking number
    self.new_booking_num = 1
  
  def get_vacancy(self) -> int:
    """
    Getter to get empty seat count
    """
    # return self._count_empty_seats()
    return self.vacancies
  
  def get_title_availability(self) -> str:
    return f"{self.title} ({self.vacancies} {'seat' if self.vacancies == 1 else 'seats'} available)"
  
  def book_tickets(self):
    print("Start booking ticekts")
    pass

  def check_bookings(self):
    pass

  def _count_empty_seats(self) -> int:
    """
    Iterate through matrix to count seats identified as unoccupied.
    O(rows * spr) time complexity may cause slowdown of program for large theatres.
    """
    count = 0
    for row in self.theatre:
      count += row.count(0)
    return count
  