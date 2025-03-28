class Booking:
  def __init__(self, id, seats=[], confirmed=False):
    self.id = id
    self.seats = seats
    self.confirmed = confirmed

class Bookings:
  def __init___(self, bookings: dict={}):
    # Dictionary of Booking objects. Keys are the Booking.id
    self.bookings = bookings

  def create_booking(self, selection: list[tuple[int, int]]=[]) -> Booking:
    booking_id = f"GIC{len(self.bookings.values() + 1):04d}"
    new_booking = Booking(booking_id, selection)
    # If there are other avenues to create booking, should add validation to ensure uniqueness
    self.bookings[booking_id] = new_booking
    return new_booking
  
  def get_booking(self, booking_id, fallback=None):
    return self.bookings.get(booking_id, fallback)