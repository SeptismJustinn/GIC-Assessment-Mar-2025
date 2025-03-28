from cinema.booking import Bookings

class Screening:
  def __init__(self, title, rows, spr):
    # Store inputs
    self.title = title
    self.rows = rows
    self.spr = spr

    # Generate theatre based on rows and spr
    # Seats are initialized as 0, indicating unoccupied. Occupied seats should be indicated by booking ID.
    self.theatre = [spr * [0] for i in range(rows)]
    # Separate vacancies counter to prevent needing to iterate through matrix to count empty seats.
    self.vacancies = rows * spr

    # Initialize empty dict of bookings. Shape: {'booking_id': < Booking object >}
    # Could convert this to a data structure to add functionality to keep track of booking IDs
    self.bookings = Bookings()

  def get_vacancy(self) -> int:
    """
    Getter to get empty seat count
    """
    # return self._count_empty_seats()
    return self.vacancies
  
  def get_title_availability(self) -> str:
    return f"{self.title} ({self.vacancies} {'seat' if self.vacancies == 1 else 'seats'} available)"
  
  def get_theatre(self, selection={}):
    # Get width of alphabet labels on left hand. Need to match this with trailing space on right to maintain symmetry
    vertical_label_width = (self.rows // 26) + 1
    row_width = self.spr * 3
    # Calculate number of hyphens to represent screen width. Written in this "redundant" way for visualization.
    screen_width = vertical_label_width + row_width + vertical_label_width

    # Find starting index to place "S C R E E N". Displaced to the left for even number widths
    screen_label_index = (screen_width - 11) // 2
    screen_label = (" " * screen_label_index) + "S C R E E N" + (" " * screen_label_index)
    screen_repr = "-" * screen_width

    visual = [screen_label, screen_repr]


    def generate_row(row: int, seats: list[int]):
      output = self.row_to_alpha_row(row)
      for idx, seat in enumerate(seats):
        # Check if seat is within selection, output "o" if so.
        if idx in selection.get(row, []):
          seat_repr = "o"
        elif seat == 1:
          seat_repr = "#"
        else:
          seat_repr = "."
        output += f" {seat_repr} "
      return output.rstrip()
    
    for idx, seats in reversed(list(enumerate(self.theatre))):
      visual.append(generate_row(idx, seats))
    
    column_labels = vertical_label_width * " "
    for i in range(1, self.spr + 1):
      column_labels += f" {i} "
    visual.append(column_labels)

    return "\n".join(visual)
  
  def create_booking(self, tickets):
    """
    Creates booking based on number of tickets.

    Attempts to place group with the following rules:
    1) Start from furthest row from the screen
    2) Start from the middle-most possible col.
    3) When a row is not enough to accomodate the number of tickets, it should overflow to the next row closer to the screen.

    For odd-numbered groups, round down mid index.
    :param tickets: Number of seats to reserve
    """
    selection = {}
    remaining_tickets = tickets
    for idx, row in enumerate(self.theatre):
      availability = row.count(0)
      if availability > 0:
        # If there are any available seats, attempt to shove people in
        if availability <= remaining_tickets:
          # If row can fit all remaining_tickets or needs to overflow, fill up row as much as possible.
          selection[idx] = [seat_idx for seat_idx, seat in enumerate(row) if seat == 0]
        else:
          # Otherwise, the row can accomodate all remaining tickets
          # Find middle most position then slowly check left and right for any available positions 
          # (based on rules, don't have to seat together?)
          empty_stack = []
          check_left = True
          if len(row) % 2 == 0:
            # For [0, 0, 0, 0], length 4, the middle idx is 4 // 2 - 1 = 1. Check "middle", then right then left...
            mid_idx = len(row) // 2 - 1
            left_idx = mid_idx
            right_idx = mid_idx + 1
          else:
            # For [0, 0, 0, 0 ,0], length 5, the middle idx is 5 // 2 = 2. Check middle, then left then right...
            mid_idx = len(row) // 2
            left_idx = mid_idx - 1
            right_idx = mid_idx
            check_left = False
          
          # Loop through seats in row, starting from middle then Right, Left, Right...
          while len(empty_stack) < remaining_tickets and left_idx >= 0 and right_idx < len(row):
            if check_left:
              if row[left_idx] == 0:
                # Append coordinates if seat is empty
                empty_stack.append(left_idx)
              left_idx -= 1
            else:
              if row[right_idx] == 0:
                empty_stack.append(right_idx)
              right_idx += 1
            # Invert check_left flag to 
            check_left = not check_left
          selection[idx] = empty_stack
        remaining_tickets -= availability
    
    # Create booking_id and "save" booking
    booking = self.bookings.create_booking(selection)

    return booking.id

  def check_booking(self, booking_id):
    booking = self.bookings.get_booking(booking_id, None)
    return booking

  def _count_empty_seats(self) -> int:
    """
    Iterate through matrix to count seats identified as unoccupied.
    O(rows * spr) time complexity may cause slowdown of program for large theatres.
    """
    count = 0
    for row in self.theatre:
      count += row.count(0)
    return count
  
  def row_to_alpha_row(self, row:int) -> str:
    alpha_row = ""
    while row > 25:
      alpha_row += chr(row % 26 + 65)
      row -= 26
    alpha_row += chr(row + 65)
    return alpha_row
  
  def alpha_row_to_row(self, alpha_row:str) -> int:
    row = (len(alpha_row) - 1) * 26
    for char in alpha_row.upper():
      row += ord(char) - 65
    return row
  
  def seat_to_row_coord(self, alpha_row:str, seat_num:str) -> tuple[int, int]:
    """
    :param alpha_row: Capitalized string of alphabets
    :param seat_num: Numeric, preferably integer, representing 1-index of seat number in the row.
    """
    seat = int(seat_num) - 1
    row = self.alpha_row_to_row(alpha_row)
    
    return (row, seat)
  
  def row_coord_to_seat(self, row:int, seat:int) -> tuple[str, str]:
    """
    :param row: 0-index of row in theatre matrix.
    :param seat: 0-index of seat in theatre matrix.
    """
    alpha_row = self.row_to_alpha_row(row)
    
    seat_num = str(seat)
    if seat < 10:
      seat_num = "0" + seat_num
    
    return (alpha_row, seat_num)
  
  def check_valid_coord(self, row:int, seat:int) -> bool:
    return row < self.rows and seat < self.spr
  
  def check_valid_seat(self, alpha_row:str, seat_num:str) -> bool:
    row, seat = self.seat_to_row_coord(alpha_row, seat_num)
    return self.check_valid_coord(row, seat)