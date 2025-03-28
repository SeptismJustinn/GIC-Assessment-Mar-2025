import re

from cinema.screening import Screening

class Program():
  """
  Class bearing functions which represent the various stages of the UI. Each method is designed to loop until a valid user input
  either exits the program or proceeds to a different UI stage.
  UI stages:
  1) start -> main_menu
  2) main_menu -> book_tickets, check_booking
  3a) book_tickets -> select_seats, main_menu
  3b) check_booking -> check_booking, main_menu
  4a) select_seats -> select_seats, main_menu
  """
  def __init__(self):
    """
    Empty screening initialized to elucidate more familiar errors when other functions try to access Screening too early, i.e. before proper init.
    """
    self.screening = Screening("None", 0, 0)

  def l_start(self):
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
      return True, {}
    
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
      return True, {}
    # Initialize and store screening object.
    self.screening = Screening(title, int(row), int(spr))
    
    # Proceed with next UI
    self.run(self.l_main_menu)

  
  def l_main_menu(self):
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
      # Restart function by looping
      return True, {}
    
    if menu_input == "1":
      instructions = self.run(self.l_book_tickets)
      return instructions.get("return", False), {}
    elif menu_input == "2":
      instructions = self.run(self.l_check_booking)
      return instructions.get("return", False), {}
    else:
      return self.exit()
    
  def l_book_tickets(self):
    """
    Third A stage of UI: Creating a ticket reservation.
    """
    tickets_to_book = input("Enter number of tickets to book, or enter blank to go back to main menu:\n> ")
    if tickets_to_book == "":
      # If blank, return to main menu
      return False, {"return": True}
    elif not tickets_to_book.isnumeric():
      exit_input = input(f"\"{tickets_to_book}\" is not a valid number!\nEnter 3 to exit or any other key to try again!\n> ")
      if exit_input == "3":
        return self.exit()
      # Restart function by looping
      return True, {}
    
    booking_id = self.screening.create_booking(int(tickets_to_book))
    if booking_id:
      print(f"Successfully reserved {tickets_to_book} {self.screening.title} tickets.\n")
      self.run(self.l_select_seats, booking_id)
      # select_seats won't need to return to booking interface, but go directly back to main menu
      return False, {"return": True}
    else:
      vacancy = self.screening.get_vacancy()
      print(f"Sorry, there are only {vacancy} {'seat' if vacancy == 1 else 'seats'} available.")
      return True, {}
    
  def l_select_seats(self, booking_id: str):
    """
    Fourth A stage of UI: Modifying the selected seats of an unconfirmed booking an/or confirming a booking.
    """
    # Theoretically this method is only accessed after succesfully creating a booking, so booking should never be None
    booking_id, theatre = self.screening.check_booking(booking_id)

    if not booking_id:
      # If booking somehow is not found, raise Exception, throwing the "Not found" message from Screening.check_booking method
      raise Exception(theatre)

    # Print out theatre matrix and prompt for confirmation
    print(theatre)

    new_seat = input("Enter blank to accept seat selection, or enter new seating position:\n> ")

    if new_seat == "":
      # If blank, conclude booking and return to main menu
      booking_id = self.screening.confirm_booking(booking_id)
      print(f"Booking id: {booking_id} confirmed.\n")
      return False, {}
    
    # Otherwise, process input and attempt to find new seat.
    alpha_row, seat_num = self._split_alpha_num(new_seat)
    
    if any([alpha_row == "", seat_num == ""]):
      exit_input = input(f"\"{new_seat}\" is not a valid seat number, please check the diagram again!\nEnter 3 to exit or any other key to try again!\n> ")
      if exit_input == "3":
        return self.exit()
      # Restart function by looping
      return True, {}
    
    # For valid inputs, attempt to switch seats for the user
    booking_id = self.screening.change_seats(booking_id, alpha_row, seat_num)
    return True, {}
  
  def l_check_booking(self):
    """
    Third B stage of UI: Prompt and check booking ID.
    """
    booking_id = input("Enter booking id, or enter blank to go back to main menu:\n> ")
    if booking_id == "":
      # If blank, return to main menu
      return False, {"return": True}
    
    # Check if provided booking_id exists, use found_id from hereon
    found_id, message = self.screening.check_booking(booking_id)
    if not found_id:
      exit_input = input(f"{message}Enter 3 to exit or any other key to try again!\n> ")
      if exit_input == "3":
        return self.exit()
      # Restart function by looping
    else:
      print(message)
    # Continuously loop this method until main menu clicked.
    return True, {}
    
  def run(self, method, *args, **kwargs):
    """
    Method for looping another method repeatedly.

    Methods to be looped here are expected to return a boolean value and a dictionary containing
    additional instructions, which can be returned to parent methods when they are exiting the loop,
      and these instructions should be handled by the parent method that called this run().

    By organizing the pages following a tree-like structure, we end up with n nested while loops, 1 for each function and
    max(n) would be the longest consecutive page sequence, e.g. main_menu > book_tickets > select_seats.
    This avoids the "max recursion depth reached" issue with the previous implementation, which can more easily be reached in
    the current page structure by constantly navigating back and forth between pages, or even by checking 1000 booking numbers.
    """
    running = True
    while running:
      running, instructions = method(*args, **kwargs)
    return instructions

  def exit(self):
    """
    Method to handle exiting program
    """
    print("Thank you for using GIC Cinemas system. Bye!")
    quit()

  
  def _split_alpha_num(self, alphanum:str) -> tuple[str, str]:
    """
    Method to take in a string containing a mix of alphabets and numbers.

    Currently configured to find

    """
    seat_alphanum = re.findall("(\d+|\D+)", alphanum.strip())
    # Check that only an alpha set and a numeric set is passed as a seat number. E.g. AAA032
    if len(seat_alphanum) == 2:
      alpha_row, seat_num = seat_alphanum
      checks = [
        (alpha_row.isalpha() and seat_num.isnumeric()), 
        self.screening.check_valid_seat(alpha_row, seat_num)
      ]
      if all(checks):
        # If all checks passed, return the separated row and seat num strings
        return alpha_row, seat_num
    return "", ""
    
  