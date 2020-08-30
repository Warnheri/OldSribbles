from random import random, randint
class Creature(object):
    def __init__(self, name, max_health, max_energy, speed):
        self.name = name
        self.max_health = max_health
        self.max_energy = max_energy
        self.speed = speed
        self.health = max_health
        self.energy = max_energy
        self.attacks = []
        
    def __str__(self):
        return (self.name + " "*(20-len(self.name)) + str(self.health) + " "*7 + str(self.energy) + " "*8 + str(self.speed))
    
    def add_attack(self, attack):
        self.attacks.append(attack)

    def show_attacks(self):
        print(" "*5 + "name" + " "*15 + "power  accuracy  difficulty")
        for i in range(len(self.attacks)):
            x = self.attacks[i]
            print("[" + str(i+1) + "] " + str(x))

    def attack(self, number):
        if self.energy < self.attacks[number - 1].difficulty:
            self.energy += self.max_energy//20
            print(self.name + " does not have enought energy for this attack.")
            return -1
        print(self.name + " used " + self.attacks[number - 1].name + "!")
        self.energy -= self.attacks[number - 1].difficulty
        x = randint(0, 100)
        if x > self.attacks[number - 1].accuracy:
            print(self.name + " missed.")
            return 0
        y = (self.attacks[number - 1].power//3)
        return int(self.attacks[number - 1].power + randint(-y, y))

    def undertake_attack(self, damage):
        if damage < 1: return
        self.health -= damage
        print(self.name + " was hit and lost " + str(damage) + " health points.")

    def is_defeated(self):
        return self.health < 1
    
class Attack(object):
    def __init__(self, name, power, accuracy, difficulty):
        self.name = name
        self.power = power
        self.accuracy = accuracy
        self.difficulty = difficulty

    def __str__(self):
        return (self.name + (19 - len(self.name)) * " " + str(self.power) +
                " "*(10 - len(str(self.power))) + str(self.accuracy) +
                " "*(13 - len(str(self.accuracy))) + str(self.difficulty))
    
class CreatureCollection(object): 
    def __init__(self, name):
        self.creatures = []
        self.name = name

    def __str__(self):
        print(" "*5 + "name" + " "*15 + "health    energy      speed")
        i = 0
        for i in range(len(self.creatures)):
            x = str(self.creatures[i])
            print("[" + str(i+1) + "] " + x)       
        return ""
        
    def add_creature(self, creature):
        self.creatures.append(creature)

    def remove_creature(self, creature):
        x = []
        for i in range(len(self.creatures)):
            if self.creatures[i] != creature:
                x.append(self.creatures[i])
        self.creatures = x

class PreMatch(object):
    def __init__(self, player1, player2):       
        self.player1 = player1                  
        self.player2 = player2
        self.mode = 2

    def select_mode(self):
        print("-"*50)
        print("[1] single-player")
        print("[2] multiplayer")
        print("-"*50)
        return int(input("Select game mode: "))

    def select_creature(self,player):
        print(player.name)
        print("-"*50)
        print(player)
        print("-"*50)
        return int(input("Select creature: ")) - 1
    
    def run(self):
        self.mode = self.select_mode()
        print()
        creature1 = self.select_creature(self.player1)
        print("You have chosen " + self.player1.creatures[creature1].name)
        print()
        if self.mode == 1:
            x = randint(0, len(self.player2.creatures) - 1)
            print("Computer has chosen " + self.player2.creatures[x].name)
            return (self.player1.creatures[creature1], self.player2.creatures[x], self.mode)
        creature2 = self.select_creature(self.player2)
        print("You have chosen " + self.player2.creatures[creature2].name)
        print()
        return (self.player1.creatures[creature1], self.player2.creatures[creature2], self.mode)
        
    
class Match(object):
    def __init__(self, creature1, creature2, mode):
        self.mode = mode
        self.attacker = creature1
        self.defender = creature2
        self.creatures = [creature1, creature2]

    def show_bar(self, my_max, curr):
        x = "|"
        piece = my_max//10
        for i in range(10):
            if curr > 0:
                x += "#"
                curr -= piece
            else: x += "-"
        x += "|"
        return x
    
    def __str__(self): 
        print(self.attacker.name + (20 - len(self.attacker.name))*" " +
              str(self.show_bar(self.attacker.max_health, self.attacker.health))
              + " " + str(self.attacker.health) + "/" + str(self.attacker.max_health), end = "")
        print("    " + str(self.show_bar(self.attacker.max_energy, self.attacker.energy))
              + " " + str(self.attacker.energy) + "/" + str(self.attacker.max_energy))
        x = ""
        for i in range(len(self.attacker.name)):
            x += "-"
        print(x + (21 - len(x))*" " + "health" + " "*20 + "energy")
        print(self.defender.name + (20 - len(self.defender.name))*" "
              + str(self.show_bar(self.defender.max_health, self.defender.health))
              + " " + str(self.defender.health) + "/" + str(self.defender.max_health), end = "")
        print("    " + str(self.show_bar(self.defender.max_energy, self.defender.energy))
              + " " + str(self.defender.energy) + "/" + str(self.defender.max_energy))
        x = ""
        for i in range(len(self.defender.name)):
            x += "-"
        return(x + " "*(21 - len(x)) + "health" + " "*20 + "energy")

    def run(self):
        attacker = self.attacker
        defender = self.defender
        if attacker.speed < defender.speed:
            attacker, defender = defender, attacker 
        print(attacker.name, "begins")
        while not (attacker.is_defeated() or defender.is_defeated()):
            print(self)
            print("-"*50)
            attacker.show_attacks()
            print("-"*50)
            choice = int(input("Select attack: "))
            print()
            defender.undertake_attack(attacker.attack(choice))
            print()
            if defender.is_defeated(): break
            print(self)
            print("-"*50)
            defender.show_attacks()
            print("-"*50)
            if self.mode == 1:
                x = 0
                choice = randint(0, len(defender.attacks) - 1)
                for i in range(len(defender.attacks)):
                    if defender.attacks[i].difficulty <= defender.energy:
                        x =+ 1
                print(x)
                if x > 0:
                    while defender.attacks[choice].difficulty > defender.energy:
                        choice = randint(0, len(defender.attacks)-1)
                choice += 1
            else: choice = int(input("Select attack:"))
            print()
            attacker.undertake_attack(defender.attack(choice))
            print()
            
        if attacker.is_defeated():
            print(attacker.name + " is defeated.")
            print(defender.name + " wins.")        
        else:
            print(defender.name + " is defeated.")
            print(attacker.name + " wins.")
def main():
    Charizard = Creature("Charizard", 200, 120, 100)
    Machamp = Creature("Machamp", 180, 140, 90)
    Flareon = Creature("Flareon", 140, 140, 110)
    wing_attack = Attack("wing attack", 30, 90, 15)
    seismix_toss = Attack("seismic toss", 110, 70, 60)
    cut = Attack("cut", 15, 90, 5)
    flamethrower = Attack("flamethrower", 60, 80, 35)
    mega_punch = Attack("mega punch", 70, 75, 40)
    leer = Attack("leer", 0, 50, 50)
    punch = Attack("punch", 15, 90, 50)
    Charizard.add_attack(wing_attack)
    Charizard.add_attack(seismix_toss)
    Charizard.add_attack(cut)
    Charizard.add_attack(flamethrower)
    Machamp.add_attack(mega_punch)
    Machamp.add_attack(seismix_toss)
    Machamp.add_attack(leer)
    Machamp.add_attack(punch)
    Flareon.add_attack(seismix_toss)
    Flareon.add_attack(cut)
    Flareon.add_attack(flamethrower)
    Player1 = CreatureCollection("Player 1")
    Player2 = CreatureCollection("Player 2")
    Player1.add_creature(Charizard)
    Player1.add_creature(Flareon)
    Player2.add_creature(Charizard)
    Player2.add_creature(Machamp)
    Player2.add_creature(Flareon)
    Prematch1 = PreMatch(Player1, Player2)
    x = Prematch1.run()
    Match1 = Match(x[0], x[1], x[2]) 
    Match1.run()
    
main()
