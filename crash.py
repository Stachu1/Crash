import random
import sys
import select
import time


class Color:
    RED = "\x1b[0;31m"
    GREEN = "\x1b[0;32m"
    YELLOW = "\x1b[0;33m"
    CYAN = "\x1b[0;36m"
    BLUE = "\x1b[0;34m"
    PURPLE = "\x1b[0;35m"
    RESET = "\x1b[0m"


class Crash:
    def __init__(self, fee=0):
        self.fee = fee
    
    def run(self):
        balance = 100
        
        while True:
            try:
                bet = float(input("\n" + "="*10 + f" Balance: {Color.CYAN}{round(balance, 2)}{Color.RESET} " + "="*10 + "\nBet: "))
                if bet > balance:
                    print(f"{Color.RED}Not enough balance{Color.RESET}")
                    continue
            except ValueError:
                print(f"{Color.RED}Invalid bet{Color.RESET}")
                continue
            
            balance -= bet
            
            rnd = random.random()
            crash_point = 1 * (1 - self.fee) / (rnd)
            
            mulimlier = 1
            while True:
                print(f"{round(mulimlier, 2)}x", end="\r")
                
                mulimlier += 0.01
                if mulimlier >= crash_point:
                    print(f"{Color.RED}{round(mulimlier, 2)}x{Color.RESET}")
                    break
                
                time.sleep(0.1)
                if select.select([sys.stdin], [], [], 0)[0]:
                    print(f"\x1b[F{Color.GREEN}{round(mulimlier, 2)}x{Color.RESET}")
                    input()
                    balance += bet * mulimlier
                    break


if __name__ == "__main__":
    crash = Crash()
    try:
        crash.run()
    except KeyboardInterrupt:
        print(f"\x1b[G\x1b[2K{Color.YELLOW}Closing...")
        sys.exit(0)