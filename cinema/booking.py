class Booking:
  def __init__(self, id, count, seats=None, confirmed=False):
    """
    seats are dictionaries with the following shape:
    {
      row_idx: [List of seat_idx]
    }

    Row and seat are 0-indexed and refer to position in theatre matrix.
    """
    self.id: str = id
    self.count: int = count
    self.seats: dict = seats.copy() if seats else {}
    self.confirmed: bool = confirmed

class Bookings:
  def __init__(self, bookings=None):
    """
    bookings are dictionaries with the following shape:
    {
      booking_id: Booking object
    }
    """
    self.bookings: dict = bookings.copy() if bookings else {}

  def create_booking(self, tickets: int=0, selection: dict=None) -> Booking:
    booking_id = f"GIC{(len(self.bookings.values()) + 1):04d}"
    new_booking = Booking(booking_id, tickets, selection)
    # If there are other avenues to create booking, should add validation to ensure uniqueness
    self.bookings[booking_id] = new_booking
    return new_booking
  
  def update_booking(self, booking_id, selection: dict) -> Booking:
    booking = self.get_booking(booking_id)
    if not booking:
      # Within the scope of assessment, update_booking is only called for unconfirmed bookings when changing seats,
      # as such, they would have been verified prior to calling this method.
      raise Exception("Booking not found!")
    # Change seats dictionary reference
    booking.seats = selection
    return booking
  
  def get_booking(self, booking_id, fallback=None):
    return self.bookings.get(booking_id, fallback)