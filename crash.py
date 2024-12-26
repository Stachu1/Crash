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
    def __init__(self, balance=100, fee=0):
        self.balance = balance
        self.fee = fee
        self.bet = None
    
    
    def get_crash_point(self):
        rnd = random.random()
        if rnd == 0:
            return self.get_crash_point()
        return 1 * (1 - self.fee) / (rnd)


    def start_round(self, crash_point):
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
                self.balance += self.bet * mulimlier
                break
    
    
    def run(self):
        try:
            while True:
                try:
                    self.bet = float(input("\n" + "="*10 + f" Balance: {Color.CYAN}{round(self.balance, 2)}{Color.RESET} " + "="*10 + "\nBet: "))
                    if self.bet > self.balance:
                        print(f"{Color.RED}Not enough balance{Color.RESET}")
                        continue
                except ValueError:
                    print(f"{Color.RED}Invalid bet{Color.RESET}")
                    continue
                
                self.balance -= self.bet
                crash_point = self.get_crash_point()
                self.start_round(crash_point)
                
        except KeyboardInterrupt:
            print(f"\x1b[G\x1b[2K{Color.YELLOW}Closing...")
            sys.exit(0)
            
            


if __name__ == "__main__":
    crash = Crash()
    crash.run()
    