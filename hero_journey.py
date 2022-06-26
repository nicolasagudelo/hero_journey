#Author: Nicolas Agudelo.


from os import system
from random import randint, random
from time import sleep

clear = lambda: system('cls')
minion_list = ['Slime', 'Wolf', 'Orc', 'Dark Knight', 'Undead']

class Hero():
    def __init__(self, name, attack, defense, speed, critchance, statpoints):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.critchance = critchance
        self.statpoints = statpoints
        self.health = 10
        self.maxhealth = 10
        self.lvl = 1
        self.exp = 0
        self.money = 0
        self.potions = 0        
    
    def __repr__(self):
        print("You are the Hero {name}.".format(name = self.name))
        print("These are your current stats:\n\nLevel: {lvl}\nAttack: {attack}\nDefense: {defense}\nSpeed: {speed}\nCrit Chance: {critchance}\nExp: {exp}\n".format(lvl = self.lvl, attack = self.attack, defense = self.defense, speed = self.speed, critchance = self.critchance, exp = self.exp))
        print("You have {potions} potions".format(potions = self.potions))
        return ("\nYou have {money} money\n".format(money = self.money))

    def train(self):
        keep_figthing = True
        while keep_figthing == True:
            # We get a minion name from the minion list and create it to fight the hero.
            minion = spawnminion(self.attack,self.defense, self.speed, self.critchance, self.maxhealth)
            #####################
            # Battle logic here #
            #####################
            clear()
            print("You have encountered a {minion} prepare to fight!\n".format(minion = minion.name))
            combat = True
            while combat == True:
                try:
                    print(f'{"HP:":7}  {"{health}/{maxhealth}"}'.format(health = self.health, maxhealth = self.maxhealth))
                    print(f'{"Potions:":7}  {"{potions}"}'.format(potions = self.potions))
                    decision = int(input('\nIt\'s your turn {hero} what do you want to do?\n1. Attack\n2. Use potion\n'.format(hero = self.name)))
                    match decision:
                        case 1:
                            # If the player chooses 1 then we start the combat logic.
                            combat = self.attack_enemy(minion)
                            if combat == True:
                                print("\nCarefull {enemy} is attacking now!\n".format(enemy = minion.name))
                                combat = minion.attack_hero(self)
                            else:
                                self.exp += 5
                                self.money += randint(1,3)
                                print ("You got {money}$ now.\n".format(money = self.money))
                                if (random()*100 < 20 and self.potions < 10):
                                        random_potions = randint (1, 2)
                                        print("What's that? It seems like the monster was carrying some potions.\n\nYou got {potions} more potion(s)".format(potions = random_potions))
                                        self.potions += random_potions
                                        if self.potions > 10: 
                                            self.potions = 10
                                            print("\n\nYou have got the maximum amount of potions you will have to leave some behind.\n")
                                if self.exp >= 10:
                                    self.health += 3
                                    self.maxhealth += 5
                                    self.lvl += 1
                                    self.exp -= 10
                                    self.statpoints += 1
                                    print ("\nYou leveled up sir {hero}! you are now level {lvl} and have {statpoints} stat points available to use when you go back to the village\n\nYou have recovered 3 health points and have 5 more maximum health points.\n".format(hero = self.name, lvl = self.lvl, statpoints = self.statpoints))
                                    
                        case 2: 
                            # If the player choose to use a potion we call the use_potion method.
                            potion_was_used = self.use_potion() 
                            if not potion_was_used: continue
                        case _:
                            print("Please type only 1 or 2 on your keyboard to choose an option.")
                            continue
                except ValueError:
                    print("Sorry we didn't get that please try again.")
            if self.health == 0: break
            keep_figthing = False
            while True:
                try:
                    decision = int(input('You have {health}/{maxhealth} HP remaining and {potions} potions, do you wish to continue training or you want to go back to the village?\n1. Continue training\n2. Go back.\n'.format(health = self.health, maxhealth = self.maxhealth, potions = self.potions)))
                    match decision:
                        case 1:
                            keep_figthing = True
                            break
                        case 2:
                            keep_figthing = False
                            clear()
                            print("Gotcha!, going back to the village now.", flush= True)
                            sleep(1)
                            clear()
                            break
                        case _:
                            print("Please type only 1 or 2 on your keyboard to choose an option.")
                            continue
                except ValueError: 
                    print("Sorry we didn't get that please try again.")
            
    def use_potion(self):
        # Uses a potion on the hero to recover 20% of his health. (If he has potions left.)
        if self.potions > 0:
            while True:
                # If the hero is at it's current maximum HP inform him about it.
                if self.health == self.maxhealth:
                    print('You already have all your HP {name}'.format(name = self.name))
                    return False
                else:
                # If we get here we give the potion to the hero and reduce the amount of potions that he has by 1
                    self.gainhealth()
                    self.potions -= 1
                    return True
                    break
        else: print('You don\'t have any potions left.'); return False

    def gainhealth(self):
        self.health += round(self.maxhealth * 0.2)
        if self.health > self.maxhealth:
            self.health = self.maxhealth
        print('You used a potion and have now {health}/{maxhealth} HP'.format(health = self.health, maxhealth = self.maxhealth))
    
    def attack_enemy(self, enemy):
        dodge = enemy.dodge()
        if dodge:
            print("\n{enemy} is too fast!, he dodged your attack.".format(enemy = enemy.name))
            return True
        else:
            crit = self.crit()
            return (enemy.lose_health(round((self.maxhealth * 0.75 + self.attack) - (enemy.maxhealth * 0.5 + enemy.defense))*crit))
            
    
    def crit(self):
        if (random()*100 < self.critchance * 5):
            print("\nYou land a critical strike!\n")
            return 2
        return 1
    def dodge(self):
        if ((random()*100) < self.speed*3.3):
            return True
        return False
    def lose_health(self, damage):
        print("\nYou take {damage} damage!\n".format(damage = damage))
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print("\nYou have been defeated!\nYou will be transported back to the village and lose some money.")
            self.money -= round(self.money * 0.25)
            sleep(1)
            clear()
            return False
        else:
            print ("\nYou have {health}/{maxhealth} points remaining\n".format(health = self.health, maxhealth = self.maxhealth))
            return True

        

class Minion():
    def __init__(self, name, attack, defense, speed, critchance, health):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.critchance = critchance
        self.health = health
        self.maxhealth = health
    def __repr__(self):
        return("This minion is a {name}, Attack: {attack}, Defense: {defense}, Speed: {speed}, CritChance = {critchance}, HP = {hp}, Max HP = {maxhp}".format(name = self.name, attack = self.attack, defense = self.defense, speed = self.speed, critchance = self.critchance, hp = self.health, maxhp = self.maxhealth))
    def dodge(self):
        if ((random()*100) < self.speed*3.3):
            return True
        return False
    def lose_health(self, damage):
        print("\n{minion} takes {damage} damage!\n".format(minion = self.name, damage = damage))
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print("\nYou have defeated {enemy}!\n".format(enemy = self.name))
            return False
        else:
            print ("\n{enemy} has {health}/{maxhealth} HP remaining\n".format(enemy = self.name, health = self.health, maxhealth = self.maxhealth))
            return True
    def crit(self):
        if (random()*100 < self.critchance * 5):
            print("\n{minion} lands a critical strike!\n".format(minion = self.name))
            return 2
        return 1
    def attack_hero(self, hero):
        dodge = hero.dodge()
        if dodge:
            print("You dodged the {enemy} attack!".format(enemy = self.name))
            return True
        else:
            crit = self.crit()
            return (hero.lose_health(round((self.maxhealth * 0.75 + self.attack) - (hero.maxhealth * 0.5 + hero.defense))*crit))


def spawnminion(attack, defense, speed, critchance, maxhealth):
    index = randint(0,4)
    lower_stats = randint(75,90)
    percentage_lower_stats = lower_stats/100
    return Minion(minion_list[index], round(attack*percentage_lower_stats), round(defense*percentage_lower_stats), round(speed * percentage_lower_stats), round(critchance * percentage_lower_stats), round(maxhealth * percentage_lower_stats))

def main():
    #Printing a welcome message for the player:
    welcome_message()
    clear()
    #We create our player:
    hero = create_player()
    clear()
    print ("Welcome to the village {name} here you can choose between 4 different options".format(name = hero.name))
    print(f'{"Training":12}  ==>  {"This is how you level up and get money"}')
    print(f'{"Store":12}  ==>  {"Here you can get potions"}')
    print(f'{"Stats":12}  ==>  {"Here you can see your stats and use your stats points"}')
    print(f'{"Battle Boss":12}  ==>  {"Here you can battle the 3 generals and the demon king. (One at a time)"}')
    input("Press Enter to continue")
    clear()
    while True:
        hero.health = hero.maxhealth
        try:
            decision = int(input("Where do you want to go now Hero?\n1. Training grounds\n2. Store\n3. Check my stat points\n4. Battle Boss\n5. Exit\n"))
            match decision:
                case 1:
                    hero.train()
                case 2:
                    store(hero)
                    clear()
                case 3:
                    stats(hero)
                case 4:
                    ################# Battle the Bosses of the game ##########################
                    pass
                case 5:
                    print("Thanks for playing!")
                    sleep(1)
                    clear()
                    exit()
        except ValueError:
            print("That is not a valid option try again.")

def stats(hero):
    clear()
    print(hero)
    if hero.statpoints == 0:
        print("\nYou don't have any statpoints to spend right now.\n")
        input("Press Enter to return to the village.")
        clear()
    else:
        while True:
            try:
                answer = input("You have {statpoints} statpoints available to use.\nDo you want to spend them now? Y/N\n".format(statpoints = hero.statpoints)).upper().strip()
                match answer:
                    case 'Y':
                        assign_stats(hero)
                        break
                    case 'N':
                        clear()
                        break
                    # In case they write anything else.
                    case _: 
                        print("Please type Y for yes, or, N for no. Other answers are not supported.") 
                        continue
            except ValueError:
                print("\nWe didn't get that, please try again.")
    
def assign_stats(hero):
    while True:
        clear()
        print(f'{"Stat Points":12}  ==>  {hero.statpoints:3d}')
        print(f'{"Attack":12}  ==>  {hero.attack:3d}')
        print(f'{"Defense":12}  ==>  {hero.defense:3d}')
        print(f'{"Speed":12}  ==>  {hero.speed:3d}')
        print(f'{"Crit. Chance":12}  ==>  {hero.critchance:3d}')
        try:
            attribute = int(input("Select the attribute you want to upgrade:\n1. Attack\n2. Defense\n3. Speed\n4. Crit Chance\n5. Go back to the Village\n"))
            match attribute:
                case 1:
                    if hero.attack == 10:
                        print("\nYou have already maxed out this stat, please choose another one.\n")
                        input("\nPress Enter to continue\n")
                        continue
                    try:
                        upgrade_stats = int(input("How many points do you want to spend increasing your attack stats?\n"))
                        if upgrade_stats > hero.statpoints:
                            print("\nYou don't have that many stat points please try again.\n")
                            input("\nPress Enter to continue\n")
                            continue
                        increase_stats(upgrade_stats, attribute, hero)
                    except ValueError:
                        print("\nWe didn't get that, please try again.\n")
                        input("\nPress Enter to continue\n")
                case 2:
                    if hero.defense == 10:
                        print("\nYou have already maxed out this stat, please choose another one.\n")
                        input("\nPress Enter to continue\n")
                        continue
                    try:
                        upgrade_stats = int(input("How many points do you want to spend increasing your defense stats?\n"))
                        if upgrade_stats > hero.statpoints:
                            print("\nYou don't have that many stat points please try again.\n")
                            input("\nPress Enter to continue\n")
                            continue
                        increase_stats(upgrade_stats, attribute, hero)
                    except ValueError:
                        print("\nWe didn't get that, please try again.\n")
                        input("\nPress Enter to continue\n")
                case 3:
                    if hero.speed == 10:
                        print("\nYou have already maxed out this stat, please choose another one.\n")
                        input("\nPress Enter to continue\n")
                        continue
                    try:
                        upgrade_stats = int(input("How many points do you want to spend increasing your speed stats?\n"))
                        if upgrade_stats > hero.statpoints:
                            print("\nYou don't have that many stat points please try again.\n")
                            input("\nPress Enter to continue\n")
                            continue
                        increase_stats(upgrade_stats, attribute, hero)
                    except ValueError:
                        print("\nWe didn't get that, please try again.\n")
                        input("\nPress Enter to continue\n")
                case 4:
                    if hero.critchance == 10:
                        print("You have already maxed out this stat, please choose another one.")
                        input("\nPress Enter to continue\n")
                        continue
                    try:
                        upgrade_stats = int(input("How many points do you want to spend increasing your crit chance stats?\n"))
                        if upgrade_stats > hero.statpoints:
                            print("\nYou don't have that many stat points please try again.\n")
                            input("\nPress Enter to continue\n")
                            continue
                        increase_stats(upgrade_stats, attribute, hero)
                    except ValueError:
                        print("\nWe didn't get that, please try again.\n")
                        input("\nPress Enter to continue\n")
                case 5:
                    print("Going back to the Village!",flush=True)
                    sleep(1.5)
                    clear()
                    break
                case _:
                    print("\nNot a valid option, please try again.\n")
                    input("\nPress Enter to continue\n")
                    continue
            
        except ValueError:
            print("\nWe didn't get that, please try again.")
            input("\nPress Enter to continue\n")

def increase_stats(points, attribute,hero):
    match attribute:
        case 1:
            attack_before = hero.attack
            hero.attack += points
            if hero.attack > 10: 
                hero.attack = 10
                print("\nYou have maxed out this stat! We'll leave it at 10 and return any unused points.\n")
                input("\nPress Enter to continue\n")
            hero.statpoints -= (hero.attack - attack_before)
            print("\nDone!\n")
            input("\nPress Enter to continue\n")
        case 2:
            def_before = hero.defense
            hero.defense += points
            if hero.defense > 10: 
                hero.defense = 10
                print("\nYou have maxed out this stat! We'll leave it at 10 and return any unused points.\n")
                input("\nPress Enter to continue\n")
            hero.statpoints -= (hero.defense - def_before)
            print("\nDone!\n")
            input("\nPress Enter to continue\n")
        case 3:
            speed_before = hero.speed
            hero.speed += points
            if hero.speed > 10: 
                hero.speed = 10
                print("\nYou have maxed out this stat! We'll leave it at 10 and return any unused points.\n")
                input("\nPress Enter to continue\n")
            hero.statpoints -= (hero.speed - speed_before)
            print("\nDone!\n")
            input("\nPress Enter to continue\n")
        case 4:
            crit_before = hero.critchance
            hero.critchance += points
            if hero.critchance > 10: 
                hero.critchance = 10
                print("\nYou have maxed out this stat! We'll leave it at 10 and return any unused points.\n")
                input("\nPress Enter to continue\n")
            hero.statpoints -= (hero.critchance - crit_before)
            print("\nDone!\n")
            input("\nPress Enter to continue\n")

def store(hero):
    while True:
        clear()
        print ("Welcome to the store {name} here you can buy potions for your adventures\n".format(name = hero.name))
        print (f'{"Item:":6}    {"Price:"}')
        print (f'{"Potion":6}    {"5$"}')
        try:
            potions_to_buy = int(input("\nYou have {potions} potions and {money}$, how many potions would you like to buy?\nWrite 0 if you want to go back to the village\n".format(potions = hero.potions, money = hero.money)))
            # If the player writes 0 we take him back to the village
            if potions_to_buy == 0:
                print("\nWe hope to have you back soon!")
                input("Press Enter to go back to the Village.\n")
                break
            # We set a maximum amount of potions so that the player can't just buy them infinitely
            if potions_to_buy > 10: potions_to_buy = 10; print("\nYou can't carry more than 10 potions we will assume you want 10 potions\n")
            # If the player set an amount that is going to go over 10 potions we max out his number of potions to 10 instead without making him pay extra money.
            if hero.potions + potions_to_buy > 10: potions_to_buy = potions_to_buy - hero.potions; print("\nYou don't have space on your inventory for that amount of potions, we will max out your potions to 10.\n")
            if (potions_to_buy * 5) > hero.money:
                print("\nYou don't have enough money to buy that many potions, please select a lower number.\n")
                input("Press Enter to go back to the Store.\n")
                continue
            else:
                hero.potions += potions_to_buy
                hero.money -= potions_to_buy * 5
                print("\nThanks for your purchase! you now have {potions} potions\nCome back soon!".format(potions = hero.potions))
                input("Press Enter to go back to the Village.\n")
                break
        except ValueError:
            print("\nThe value you wrote is not valid, please try again.\n")
            input("Press Enter to go back to the Store.\n")

def create_player():
    print("""
You will now start your adventure to defeat the Demon King and his three generals, they have started a war against humanity and seek to exterminate them. 
The Hero is the only one capable of stopping them. 
You will have to train, face enemies, level up and gather resources before taking on to the generals and finally the Demon King.
    """, flush=True)
    input("Press Enter to continue:")
    while True:
        clear()
        # Prompt the player for their name
        name = input("Let\'s start by getting your name sir Hero.\nPlease type your name:\n")
        try:
            # We confirm with the player whether the name they wrote is right or not.
            clear()
            answer = input("The name you wrote is {name}. Is this the correct name Hero? \n(Type Y for yes, or, N for no)\n".format(name = name)).upper().strip()
            match answer:
                case 'Y': break
                # If not we keep asking the player for their name.
                case 'N': 
                    print("Let\'s try that again shall we?\n")
                    input("Press Enter to continue")
                    continue
                # In case they write anything else.
                case _: 
                    print("Please type Y for yes, or, N for no. Other answers are not supported.")
                    input("Press Enter to continue")
                    continue
        # In case an ValueError happens.
        except ValueError :
            print("Sorry we didn\'t get that, please try again\n")
            input("Press Enter to continue")
            continue
    clear()
    print("Sir {name} then, the outcome of your battles and how well you prepare yourself to face this challenge will forever change the destiny of humanity and the world.\n".format(name = name))
    input("Press Enter to continue")
     
    stat_points = 10
    clear()
    print("""
Now is the time to distribute your initial stats you will receive {stat_points} for the start of your adventure. You will be able to distribute them in four different categories:
>  Attack: Determines how much damage you will deal to your enemies.
>  Defense: Determines how much damage reduction you will have against enemies.
>  Speed: Determines the chance of avoiding damage from an attack.
>  Crit Chance: Determines the chance of dealing extra damage when you attack an enemie.
    """.format(stat_points = stat_points))
    input("Press Enter to continue")
    while True:
        try:
            while True:
                clear()
                # We make sure that everytime we start this loop the stat_points is equal to 10.
                stat_points = 10
                attack_points = 0
                defense_points = 0
                speed_points = 0
                crit_points = 0
                print("Stat points remaining = {stat_points}\n".format(stat_points = stat_points))
                # We ask the player for the attack points he wants to get
                attack_points = int(input("Write the number of points you wish to invest towards ATTACK.\n"))
                # We check that the amount written is valid, if it is we reduce the total amount of points remaining.
                if attack_points > stat_points:
                    print("Calm down sir {name} you don't have that many points yet\n".format(name = name))
                    input("Press Enter to continue")
                    continue
                else:
                    stat_points -= attack_points
                # If the player doesn't have any more points to use we exit the loop.
                if stat_points == 0: break 
                clear()
                print("Stat points remaining = {stat_points}\n".format(stat_points = stat_points))
                # We ask the player for the defense points he wants to get
                defense_points = int(input("Write the number of points you wish to invest towards DEFENSE.\n"))
                # We check that the amount written is valid, if it is we reduce the total amount of points remaining.
                if defense_points > stat_points:
                    print("Calm down sir {name} you don't have that many points yet\n".format(name = name))
                    input("Press Enter to continue")
                    continue
                else:
                    stat_points -= defense_points
                # If the player doesn't have any more points to use we exit the loop.
                if stat_points == 0: break
                clear()
                # We ask the player for the speed points he wants to get
                print("Stat points remaining = {stat_points}\n".format(stat_points = stat_points))
                speed_points = int(input("Write the number of points you wish to invest towards SPEED.\n"))
                # We check that the amount written is valid, if it is we reduce the total amount of points remaining.
                if speed_points > stat_points:
                    print("Calm down sir {name} you don't have that many points yet\n".format(name = name))
                    input("Press Enter to continue")
                    continue
                else:
                    stat_points -= speed_points
                # If the player doesn't have any more points to use we exit the loop.
                if stat_points == 0: break
                clear()
                # We ask the player for the crit chance he wants to get
                print("Stat points remaining = {stat_points}\n".format(stat_points = stat_points))
                crit_points = int(input("Write the number of points you wish to invest towards CRIT CHANCE.\n"))
                # We check that the amount written is valid, if it is we reduce the total amount of points remaining.
                if crit_points > stat_points:
                    print("Calm down sir {name} you don't have that many points yet\n".format(name = name))
                    input("Press Enter to continue")
                    continue
                else:
                    stat_points -= crit_points
                break       
        except ValueError:
            print("Please use only numbers to select your stats\n")
            input("Press Enter to continue")
        clear()
        print("This is how everything looks:\n")
        print(f'{"Attack":12}  ==>  {attack_points:3d}')
        print(f'{"Defense":12}  ==>  {defense_points:3d}')
        print(f'{"Speed":12}  ==>  {speed_points:3d}')
        print(f'{"Crit. Chance":12}  ==>  {crit_points:3d}')
        while True:
            answer = input("Confirm if this is okay \n(Type Y for yes, or, N for no)\n".format(name = name)).upper().strip()
            match answer:
                case 'Y': break
                # If not we keep asking the player for their name.
                case 'N': 
                    print("Let\'s try that again shall we?\n")
                    input("Press Enter to continue")
                    break
                # In case they write anything else.
                case _: 
                    print("Please type Y for yes, or, N for no. Other answers are not supported.") 
                    continue
        if answer == 'N': continue
        clear()
        print("Thanks Hero, your adventure will now start, your will be transported to the village where you will be able to choose what to do next. if you have any unused stat points left you will be able to use them there too.\nI wish you the best of luck in your journey!")
        input('Press Enter to continue')
        break

    # Create player once we have all his information collected:
    return(Hero(name, attack_points, defense_points, speed_points, crit_points, stat_points))
    
def welcome_message():
    print ("""
    
             U _____ u  _        ____   U  ___ u  __  __  U _____ u 
 __        __\| ___"|/ |"|    U /"___|   \/"_ \/U|' \/ '|u\| ___"|/ 
 \\"\      /"/ |  _|" U | | u  \| | u     | | | |\| |\/| |/ |  _|"   
 /\ \ /\ / /\ | |___  \| |/__  | |/__.-,_| |_| | | |  | |  | |___   
U  \ V  V /  U|_____|  |_____|  \____|\_)-\___/  |_|  |_|  |_____|  
.-,_\ /\ /_,-.<<   >>  //  \\\  _// \\\      \\\   <<,-,,-.   <<   >>  
 \_)-'  '-(_/(__) (__)(_")("_)(__)(__)    (__)   (./  \.) (__) (__) 

    """, flush = True)

    sleep(0.75)

    print("""
    
  _____   U  ___ u 
 |_ " _|   \/"_ \/ 
   | |     | | | | 
  /| |\.-,_| |_| | 
 u |_|U \_)-\___/  
 _// \\\_     \\\    
(__) (__)   (__)   

    """, flush = True)

    sleep(0.75)

    print("""

 (`-').-> (`-')  _   (`-')                (`-').->                                      (`-') <-. (`-')_  (`-')  _           
 (OO )__  ( OO).-/<-.(OO )      .->  ,--. ( OO)_                    .->        .->   <-.(OO )    \( OO) ) ( OO).-/     .->   
,--. ,'-'(,------.,------,)(`-')----.\  |(_)--\_)        <-.--.(`-')----. ,--.(,--.  ,------,),--./ ,--/ (,------. ,--.'  ,-.
|  | |  | |  .---'|   /`. '( OO).-.  '`-'/    _ /      (`-'| ,|( OO).-.  '|  | |(`-')|   /`. '|   \ |  |  |  .---'(`-')'.'  /
|  `-'  |(|  '--. |  |_.' |( _) | |  |   \_..`--.      (OO |(_|( _) | |  ||  | |(OO )|  |_.' ||  . '|  |)(|  '--. (OO \    / 
|  .-.  | |  .--' |  .   .' \|  |)|  |   .-._)   \    ,--. |  | \|  |)|  ||  | | |  \|  .   .'|  |\    |  |  .--'  |  /   /) 
|  | |  | |  `---.|  |\  \   '  '-'  '   \       /    |  '-'  /  '  '-'  '\  '-'(_ .'|  |\  \ |  | \   |  |  `---. `-/   /`  
`--' `--' `------'`--' '--'   `-----'     `-----'      `-----'    `-----'  `-----'   `--' '--'`--'  `--'  `------'   `--'    
 

    """, flush = True)

    sleep(0.5)

    input("Press Enter to continue:")    

main()

    
