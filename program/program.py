import re

from cinema.screening import Screening

class Program():
  """
  Class bearing functions which represent the various stages of the UI. Each method is designed to recurse within itself until a valid user input
  either exits the program or proceeds to a different UI stage.
  UI stages:
  1) start -> main_menu
  2) main_menu -> book_tickets, check_booking
  3a) book_tickets -> select_seats, main_menu
  3b) check_booking -> main_menu
  """
  def __init__(self):
    """
    Empty screening initialized to elucidate more familiar errors when other functions try to access Screening too early, i.e. before proper init.
    """
    self.screening = Screening("None", 0, 0)

  def start(self):
    """
    First stage of UI: Declaring the movie title and cinema size
    """
    ###### 1) Application start #####
    init_movie_inputs = input("Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:\n> ")
    init_movie_params = init_movie_inputs.strip().split()

    # Validate number of inputs
    if len(init_movie_params) != 3:
      # Can also just fail when < 3 inputs and take first 3 when excess.
      exit_input = input(f"{init_movie_params} does not adhere to the format specified!\nEnter 3 to exit or any other key to retry...\n> ")
      if exit_input == "3":
        return self.exit()
      # Restart function by recursing
      return self.start()
    
    # Validate that inputs are appropriate
    title, row, spr = init_movie_params
    error_message = ""

    # # Validation for movies if there is a database/API to query valid movies.
    # if not title in valid_movies:
    #   error_message += f"{title} is not currently screening, please enter a valid movie [Title] from {valid_movies} for the 1st value!\n"
    if not row.isnumeric():
      error_message += f"{row} is not a valid number of [Rows], please enter an integer for the 2nd value!\n"
    if not spr.isnumeric():
      error_message += f"{row} is not a valid number of [Seats Per Row], please enter an integer for the 3rd value!\n"
    
    if error_message:
      # If any errors found, error_message would no longer be falsy
      exit_input = input(f"{error_message}Enter 3 to exit or any other key to retry...\n> ")
      if exit_input == "3":
        return self.exit()
      # Restart function by recursing
      return self.start()
    
    # Initialize and store screening object.
    self.screening = Screening(title, int(row), int(spr))
    
    # Proceed with next UI
    return self.main_menu()

  
  def main_menu(self):
    """
    Second stage of UI: Deciding actions regarding declared movie screening.
    """
    menu = "Welcome to GIC Cinemas\n"
    options = {
      "1": f"Book tickets for {self.screening.get_title_availability()}",
      "2": "Check bookings",
      "3": "Exit"
    }

    for idx, option in options.items():
      menu += f"[{idx}] {option}\n"
    menu += "Please enter your selection:\n> "
    menu_input = input(menu)

    # Validate if not number entered, or number is not part of menu options.
    if not menu_input.isnumeric() or not options.get(menu_input, False):
      exit_input = input(f"\"{menu_input}\" is not valid input!\nEnter 3 to exit or any other key to try again!\n> ")
      if exit_input == "3":
        return self.exit()
      # Restart function by recursing
      return self.main_menu()
    
    if menu_input == "1":
      return self.book_tickets()
    elif menu_input == "2":
      return
    else:
      return self.exit()
    
  def book_tickets(self):
    tickets_to_book = input("Enter number of tickets to book, or enter blank to go back to main menu:\n> ")
    if tickets_to_book == "":
      # If blank, return to main menu
      return self.main_menu()
    elif not tickets_to_book.isnumeric():
      exit_input = input(f"\"{tickets_to_book}\" is not a valid number!\nEnter 3 to exit or any other key to try again!\n> ")
      if exit_input == "3":
        return self.exit()
      # Restart function by recursing
      return self.book_tickets()
    
    booking_id = self.screening.create_booking(int(tickets_to_book))
    if booking_id:
      message = f"Successfully reserved {tickets_to_book} {self.screening.title} tickets.\n"
      return self.select_seats(booking_id, init_message=message)
    else:
      vacancy = self.screening.get_vacancy()
      message = f"Sorry, there are only {vacancy} {'seat' if vacancy == 1 else 'seats'} available."
      print(message)
      return self.book_tickets()
    
  def select_seats(self, booking_id: str, init_message=""):
    booking = self.screening.check_booking(booking_id)
    message = init_message + booking.get("message", "")
    print(message)

    new_seat = input("Enter blank to accept seat selection, or enter new seating position:\n> ")

    if new_seat == "":
      # If blank, conclude booking and return to main menu
      print(f"Booking id: {booking_id} confirmed.")
      return self.main_menu()
    
    # Otherwise, process input and attempt to find new seat.
    seat_alphanum = re.findall("(\d+|\D+)", new_seat.strip())
    # Check that only an alpha set and a numeric set is passed as a seat number. E.g. AAA032
    # Slowly break apart input 
    valid = len(seat_alphanum) == 2
    if valid:
      alpha_row, seat_num = seat_alphanum
      valid = (alpha_row.isalpha() and seat_num.isnumeric())
    if valid:
      valid = self.screening.check_valid_seat(alpha_row, seat_num)
    if not valid:
      exit_input = input(f"\"{new_seat}\" is not a valid seat number, please check the diagram again!\nEnter 3 to exit or any other key to try again!\n> ")
      if exit_input == "3":
        return self.exit()
      # Restart function by recursing
      return self.select_seats(booking_id)
    print(self.screening.seat_to_row_coord(alpha_row, seat_num))
    return self.select_seats(booking_id)


  def exit(self):
    """
    Method to handle exiting program
    """
    return print("Thank you for using GIC Cinemas system. Bye!")