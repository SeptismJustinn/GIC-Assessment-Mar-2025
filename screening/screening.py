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
  
  def get_vacancy(self) -> int:
    """
    Getter to get empty seat count
    """
    # return self._count_empty_seats()
    return self.vacancies
  
  def get_features(self) -> dict:
    menu = {}
    # Convenience coding to encourage organizing of features based on placement in code block.
    idx = 1

    # Add booking feature to menu
    menu[idx] = {
      "option":(f"Book tickets for {self.title} ({'1 seat' if self.vacancies == 1 else f'{self.vacancies} seats'} available)"),
      "method": self.book_tickets
      }
    idx += 1

    # Add check bookings feature to menu
    menu[idx] = {
      "option": ("Check bookings"),
      "method": self.check_bookings
      }
    idx += 1

    return menu, idx
  
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
  