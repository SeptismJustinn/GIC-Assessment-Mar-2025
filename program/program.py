class Program():
  def run(self):
    # Application start
    init_params = self.application_start()
    if not init_params:
      return self.exit()
    print(f"Captured: {init_params}")
    

  def application_start(self):
    """
    Function containing logic to capture requisite user inputs to initialize application

    :return: Returns the parameters required to initialize Program or None if program should terminate.
    """
    # Application start
    init_movie_inputs = input("Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:\n")
    init_movie_params = init_movie_inputs.strip().split()

    # Validate number of inputs
    if len(init_movie_params) != 3:
      # Can also just fail <3 inputs and take first 3 when excess.
      exit_input = input(f"{init_movie_params} does not adhere to the format specified!\nEnter 3 to exit or any other key to retry...\n")
      if exit_input == "3":
        return
      return self.run()
    return init_movie_params

  def exit(self):
    return print("Thank you for using GIC Cinemas system. Bye!")