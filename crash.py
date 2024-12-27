import sys, select, time, random, os


class Color:
    RED = "\x1b[0;31m"
    ORANGE = "\x1b[38;5;214m"
    YELLOW = "\x1b[0;33m"
    GREEN = "\x1b[0;32m"
    CYAN = "\x1b[0;36m"
    BLUE = "\x1b[0;34m"
    PURPLE = "\x1b[0;35m"
    RESET = "\x1b[0m"


class Crash:
    def __init__(self, balance=100, fee=0, multiplier_tick=1.01):
        self.balance = balance
        self.fee = fee
        self.multiplier_tick = multiplier_tick
        self.bet = None
        self.rocket_trail = "."*50 + f",`,`:;*!&%$%#@#@"
    
    def get_crash_point(self):
        rnd = random.random()
        if rnd == 0:
            return self.get_crash_point()
        return (1 - self.fee) / (rnd)
    
    
    def run(self):
        try:
            while True:
                try:
                    self.bet = float(input(f"\n{Color.RESET}" + "="*10 + f" Balance: {Color.CYAN}{self.balance:.2f}{Color.RESET} " + "="*10 + "\nBet: "))
                    if self.bet > self.balance:
                        print(f"{Color.RED}Not enough balance{Color.RESET}")
                        continue
                except ValueError:
                    print(f"{Color.RED}Invalid bet{Color.RESET}")
                    continue
                
                self.balance -= self.bet
                crash_point = self.get_crash_point()
                self.go(crash_point)
                
        except KeyboardInterrupt:
            print(f"\x1b[G\x1b[2K{Color.YELLOW}Closing...")
            sys.exit(0)
    
    
    def go(self, crash_point):
        multiplier = 1
        while True:
            print(Color.ORANGE + self.rocket(multiplier), end="\r")

            time.sleep(0.1)
            if select.select([sys.stdin], [], [], 0)[0]:
                print(f"\x1b[F{Color.GREEN}" + self.rocket(multiplier) + f" {Color.RESET}Crashed at {Color.PURPLE}{crash_point:.2f}x")
                input()
                self.balance += self.bet * multiplier
                break
            
            if multiplier == crash_point:
                print(Color.RED + self.rocket(multiplier))
                break
            
            multiplier *= self.multiplier_tick
            if multiplier > crash_point:
                multiplier = crash_point
    
    
    def rocket(self, multiplier):
        result = f"[{multiplier:.2f}x]🚀"
        width = os.get_terminal_size().columns - len(result) - 1
        distance = (1 - 1 / (multiplier**0.5)) * width
        trail_len = round(distance) + 1
        trail = (" "*width + self.rocket_trail)[-trail_len::]
        return trail + result
            
            


if __name__ == "__main__":
    crash = Crash()
    crash.run()
    