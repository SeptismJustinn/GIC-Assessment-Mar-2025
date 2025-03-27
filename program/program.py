from screening.screening import Screening

class Program():
  def run(self):
    ###### 1) Application start #####
    init_params = self.application_start()
    if not init_params:
      return self.exit()
    print(f"Captured: {init_params}")
    # Create the screening session based on init params
    screening = Screening(*init_params)
    running = True
    while running:
      output = self.main_menu(screening)
      if not output:
        return self.exit()
      break
    

  def application_start(self) -> tuple[str, int, int] | None:
    """
    Function containing logic to capture requisite user inputs to initialize application

    :return: Returns the parameters required to initialize Program or None if program should terminate.
    """
    # Application start
    init_movie_inputs = input("Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:\n")
    init_movie_params = init_movie_inputs.strip().split()

    # Validate number of inputs
    if len(init_movie_params) != 3:
      # Can also just fail when < 3 inputs and take first 3 when excess.
      exit_input = input(f"{init_movie_params} does not adhere to the format specified!\nEnter 3 to exit or any other key to retry...\n")
      if exit_input == "3":
        return
      # Restart function by recursing
      return self.application_start()
    
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
      exit_input = input(f"{error_message}Enter 3 to exit or any other key to retry...\n")
      if exit_input == "3":
        return
      # Restart function by recursing
      return self.application_start()

    return (title, int(row), int(spr))
  
  def main_menu(self, screening: Screening):
    menu = "Welcome to GIC Cinemas\n"
    options = {
      "1": f"Book tickets for {screening.get_title_availability()}",
      "2": "Check bookings",
      "3": "Exit"
    }

    for idx, option in options.items():
      menu += f"[{idx}] {option}\n"
    menu += "Please enter your selection:\n"
    menu_input = input(menu)

    # Validate if not number entered, or number is not part of menu options.
    if not menu_input.isnumeric() or not options.get(int(menu_input), False):
      exit_input = input(f"\"{menu_input}\" is not valid input!\nEnter 3 to exit or any other key to try again!\n")
      if exit_input == "3":
        return
      # Restart function by recursing
      return self.main_menu(screening)
    

    

  def exit(self):
    """
    Method to handle exiting program
    """
    return print("Thank you for using GIC Cinemas system. Bye!")