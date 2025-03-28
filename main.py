from program.program import Program

def main():
  try:
    prog = Program()
    prog.run(prog.l_start)
  except SystemExit:
    print("Exiting app...")


if __name__ == "__main__":
  main()