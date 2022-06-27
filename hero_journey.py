#Author: Nicolas Agudelo.

# Import the modules that will be used for the game.
from os import system
from random import randint, random
from time import sleep

# Global dictionary to keep track of the bosses that have been defeated. At the start none of them have been defeated hence we initialize all values to False
boss_defeat = {1: False, 2: False, 3: False, 4: False}
# Function to clean the windows command prompt to keep everything more organized.
clear = lambda: system('cls')
# List from where we will randomly get the name of the enemies the player will face while training.
minion_list = ['Slime', 'Wolf', 'Undead', 'Goblin', 'Bandit', 'Zombie', 'Ghoul', 
                'Orc', 'Dark Knight', 'Gremlin', 'Werewolf', 'Golem', 'Witch', 'Valkyrie',
                'Vampire', 'Chimera', 'Giant', 'Dragon', 'Minotaur', 'Devil', 'Manticore']
# Object Hero which will ultimately be the player, will keep track of his stats, money, potions, monsters killed and potions used.
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
        self.lvl = 0
        self.exp = 0
        self.money = 0
        self.potions = 0
        self.monsterskilled = 0
        self.potionsused = 0        
    
    # Using the __repr__ function so that the player can check his current stats.
    def __repr__(self):
        print("You are the Hero {name}.".format(name = self.name))
        print("These are your current stats:\n\nLevel: {lvl}\nAttack: {attack}\nDefense: {defense}\nSpeed: {speed}\nCrit Chance: {critchance}\nExp: {exp}\n".format(lvl = self.lvl, attack = self.attack, defense = self.defense, speed = self.speed, critchance = self.critchance, exp = self.exp))
        print("You have {potions} potions".format(potions = self.potions))
        return ("\nYou have {money} money\n".format(money = self.money))
    # The train function will set up the combat logic for the player to fight against minions, depending on the player level different minions will appear
    def train(self):
        # Max lvl is 30. We let the player know that he won't be getting any more levels but he can still grind for potions and money.
        if self.lvl >= 30:
            print("\nYou are at max level so you won't level up anymore, but you can still get potions and money from the monsters you defeat.\n")
            input("Press Enter to continue.")
        # keep_fighting keeps track of whether the player wants to keep fighting more minions or go back to the village to spend stat points, buy potions, fight a boss or just recover his health.
        # As we enter the loop we set the variable to True.
        keep_fighting = True
        while keep_fighting == True:
            # We get a minion name from the minion list and create it using the spawnminion function to fight the hero.
            # Depending on the player level we will get stronger enemies.
            if self.lvl <= 10:
                minion = spawnminion(self.attack,self.defense, self.speed, self.critchance, self.maxhealth, 1)
            elif self.lvl > 10 and self.lvl <= 20:
                minion = spawnminion(self.attack,self.defense, self.speed, self.critchance, self.maxhealth, 2)
            elif self.lvl > 20:
                minion = spawnminion(self.attack,self.defense, self.speed, self.critchance, self.maxhealth, 3)
            ############################
            # Battle logic starts here #
            ############################
            clear()
            print("You have encountered a {minion} prepare to fight!\n".format(minion = minion.name))
            combat = True
            while combat == True:
                try:
                    # We let the player know how much hp he has and how many potions he was at the beggining of this turn.
                    print(f'{"HP:":7}  {"{health}/{maxhealth}"}'.format(health = self.health, maxhealth = self.maxhealth))
                    print(f'{"Potions:":7}  {"{potions}"}'.format(potions = self.potions))
                    # We ask the player if he wants to attack or drink a potion.
                    decision = int(input('\nIt\'s your turn {hero} what do you want to do?\n1. Attack\n2. Use potion\n'.format(hero = self.name)))
                    match decision:
                        case 1:
                            clear()
                            # If the player chooses 1 then we start the combat by attacking the minion using the attack_enemy method.
                            combat = self.attack_enemy(minion)
                            # If the minion has any HP left the attack enemy function will return True in which case it's the minion's turn
                            if combat == True:
                                # The minion attacks the player.
                                print("\nCarefull {enemy} is attacking now!\n".format(enemy = minion.name))
                                # If the player has no more hp after the damage calculation then combat will be set to False and the Hero will be returned to the village.
                                combat = minion.attack_hero(self)
                            # If the minion does not have any HP left it means the player won the combat.
                            else:
                                # Increase the counter of how many monsters the player has killed.
                                self.monsterskilled += 1
                                # Give the player experience for winning the combat.
                                self.exp += 5
                                # If the player is at his max level he won't get any more exp points.
                                if self.lvl == 30: self.exp = 0
                                # Give the player 1 to 3 $ for winning the combat.
                                self.money += randint(1,3)
                                # Tell the player how many money he has now
                                print ("You got {money}$ now.\n".format(money = self.money))
                                # The player has 1/4 chances of getting some potions if he doesn't have the maximum amount of potions already (10)
                                if (random()*100 < 25 and self.potions < 10):
                                        # The player could get one or two potions from the minion.
                                        random_potions = randint (1, 2)
                                        print("What's that? It seems like the monster was carrying some potions.\n\nYou got {potions} more potion(s)".format(potions = random_potions))
                                        # Add the potions that the minion left to the player potions
                                        self.potions += random_potions
                                        if self.potions > 10: 
                                            self.potions = 10
                                            print("\n\nYou have got the maximum amount of potions you will have to leave some behind.\n")
                                # When the player hits 10 exp we will get a new level and reset his exp. The level_up method manages this.
                                if self.exp >= 10:
                                    self.level_up()
                                    
                        case 2: 
                            clear()
                            # If the player choose to use a potion we call the use_potion method.
                            self.use_potion()
                        case _:
                            # In case the player writes a number other than 1 or 2
                            print("Please type only 1 or 2 on your keyboard to choose an option.")
                            continue
                except ValueError:
                    # In case the player writes a value that is not a number
                    print("Sorry we didn't get that please try again.")
            # If the player has no more hp left then leave the combat logic.
            if self.health == 0: break
            # Keep asking the player what he wants to do until he chooses a valid answer.
            while True:
                try:
                    # Ask the player whether he wants to continue fighting or go back to the village.
                    decision = int(input('You have {health}/{maxhealth} HP remaining and {potions} potions, do you wish to continue training or you want to go back to the village?\n1. Continue training\n2. Go back.\n'.format(health = self.health, maxhealth = self.maxhealth, potions = self.potions)))
                    match decision:
                        # If the player selects to keep fighting set keep_fighting to True and break the current loop as a decision was made.
                        case 1:
                            keep_fighting = True
                            break
                        case 2:
                        # If the player selects to go back to the village set keep_fighting as False and break the current loop as a decision was made.
                            keep_fighting = False
                            clear()
                            print("Gotcha!, going back to the village now.", flush= True)
                            input("Press Enter to continue.")
                            clear()
                            break
                        case _:
                        # In case the player writes a number other than 1 or 2.
                            print("Please type only 1 or 2 on your keyboard to choose an option.")
                            continue
                except ValueError: 
                    # In case the player writes a value that is not a number.
                    print("Sorry we didn't get that please try again.")
    # The level_up method will level up the player when he gets 10 or more exp and cap the mas level at level 30.
    def level_up(self):
        # While the player has more than 10 exp, increase the level by one current health by 3 max health by 5 and reduce exp by 10
        while self.exp >= 10:
            self.lvl += 1
            # If the player already reached level 30 he won't get any more levels or stats.
            if self.lvl > 30:
                print("You have reached the maximum level you can get sir {hero}".format(hero = self.name))
                self.lvl = 30
                self.exp = 0
                return 0
            self.health += 3
            self.maxhealth += 5
            self.exp -= 10
            self.statpoints += 1
            # Let the player know he has leveled up.
            print ("\nYou leveled up sir {hero}! you are now level {lvl} and have {statpoints} stat points available to use when you go back to the village\n\nYou have recovered 3 health points and have 5 more maximum health points.\n".format(hero = self.name, lvl = self.lvl, statpoints = self.statpoints))
            
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
                    self.potionsused += 1
                    return True
                    break
        # If the player doesn't have potions, inform him about it and leave the method.
        else: print('You don\'t have any potions left.'); return False

    def gainhealth(self):
        # Recover 20% of the maximum health.
        self.health += round(self.maxhealth * 0.2)
        # If the amount of health was to exceed the amount of maximum health we make the current health equal to the maximum health.
        if self.health > self.maxhealth:
            self.health = self.maxhealth
        # Let the player know the potion was used and how much HP he has now.
        print('You used a potion and have now {health}/{maxhealth} HP'.format(health = self.health, maxhealth = self.maxhealth))
    
    def attack_enemy(self, enemy):
        # dodge will be set to True if the enemy dodged the attack or false if it did not.
        dodge = enemy.dodge()
        # If he dodges no damage calculation is made.
        if dodge:
            print("\n{enemy} is too fast!, he dodged your attack.\n".format(enemy = enemy.name))
            return True
        # If he did not dodge we make damage to the enemy
        else:
            # crit method will return 1 or 2 randomly. the higher your critchange the higher the chance of getting a crit.
            crit = self.crit()
            # If crit is equal to 2 the damage will be doubled.
            return (enemy.lose_health(round((self.maxhealth * 0.75 + self.attack) - (enemy.maxhealth * 0.5 + enemy.defense))*crit))
            
    
    def crit(self):
        # At max critchance (10) the player will have a 50% chance of hitting a crit strike.
        if (random()*100 < self.critchance * 5):
            # If the random number generated between 0 and 100 is lower than the players critchance then he lands a critical strike
            print("\nYou land a critical strike!\n")
            return 2
        return 1
    def dodge(self):
        # At max speed (10) the player will have a 33% chance of dodging an enemy attack.
        if ((random()*100) < self.speed*3.3):
            # If the random number generated between 0 and 100 is lower than the players speed then he dodges the enemy attack.
            return True
        return False
    def lose_health(self, damage):
        # Added check so that negative damages are not possible. And you always lose at least 1 health.
        if damage <= 0:
            damage = 1
        print("\nYou take {damage} damage!\n".format(damage = damage))
        # We reduce the amount of health of the player by the amount of damage taken.
        self.health -= damage
        # We check that the health never goes lower than 0. If the health hits 0 then the player has been defeated. Take 25% of his money and all his potions. Return False to end the combat.
        if self.health <= 0:
            self.health = 0
            # We inform the player that he has lost and will be transported back to the village with less money and no potions.
            print("\nYou have been defeated!\nYou will be transported back to the village and lose some money and your potions.")
            self.potions = 0
            self.money -= round(self.money * 0.25)
            input("\nPress Enter to continue\n")
            clear()
            return False
        # If the player has HP remaining then let him know how much HP he has left and continue with the combat returnint True.
        else:
            print ("\nYou have {health}/{maxhealth} points remaining\n".format(health = self.health, maxhealth = self.maxhealth))
            return True

        
# All the enemies in the game including the bosses are Minion objects. what changes about them is how their stats are calculated when using the spawnminion function.
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
    # The dodge method will determine if the minion dodges or not the attack of the hero.
    def dodge(self):
        if ((random()*100) < self.speed*3.3):
            return True
        return False
    # The lose_health method will carry out the damage calculation in case the minion has no hp after the damage calculation it will return False to finish the combat logic, otherwise it will return True to continue with the combat logic.
    def lose_health(self, damage):
        # Adding a check so that negative damages are not possible and there is always at least 1 damage.
        if damage <= 0:
            damage = 1
        print("\n{minion} takes {damage} damage!\n".format(minion = self.name, damage = damage))
        self.health -= damage
        # If the health was going to be lower than 0 set it to 0 instead.
        if self.health <= 0:
            self.health = 0
            # Let the player know that the enemy has no hp and therefore has been defeated.
            print("\nYou have defeated {enemy}!\n".format(enemy = self.name))
            return False
        else:
            # If the enemy still has HP after the damage calculation then let the player know how much HP the minion has and continue with the combat.
            print ("\n{enemy} has {health}/{maxhealth} HP remaining\n".format(enemy = self.name, health = self.health, maxhealth = self.maxhealth))
            return True
    def crit(self):
        # If the random generated number is lower than the minions critchance then he lands a crit strike on the player.
        if (random()*100 < self.critchance * 5):
            print("\n{minion} lands a critical strike!\n".format(minion = self.name))
            return 2
        return 1
    def attack_hero(self, hero):
        # Call the hero.dodge() method to check if the hero dodges the attack. If he does dodge will be set to True if not it will be set to False.
        dodge = hero.dodge()
        if dodge:
            # If the player dodged the attack inform him about it.
            print("You dodged {enemy}'s attack!\n".format(enemy = self.name))
            return True
        else:
            # If the player did not dodge continue with the damage calculation
            # if the crit method returns 2 it means is a critical strike and damage will be doubled. if not it will return 1.
            crit = self.crit()
            return (hero.lose_health(round((self.maxhealth * 0.75 + self.attack) - (hero.maxhealth * 0.5 + hero.defense))*crit))

# The spawnminion function will create minions for the player to fight against as the player progresses the enemies will be stronger.
def spawnminion(attack, defense, speed, critchance, maxhealth, lvl):
    # Depending of the lvl of the minion to be created we:
    # - Select the monster name if it's not a boss from the minion list. for the bosses we have set fixed names.
    # - Lower the stats of the monster for the minions so that the player is stronger than them.
    # - This changes with the bosses. 
    #   - The first boss will be 95% as strong as the player.
    #   - The second boss will be as strong as the player.
    #   - The third boss will be 5% stronger than the player.
    #   - The last boss will be 10% stronger than the player.
    # Also if the player has not trained enough (Doesn't have a set level against each boss then the bosses advantage will be even greater and in some cases virtually imposible to defeat until the player gets to that level.)
    # This is calculated on the boss() function.
    # Once this is defined a Minion object is created with the stats calculated to fight against the Hero.
    match lvl: 
        case 1:
            index = randint(0,6)
            lower_stats = randint(75,80)
            percentage_lower_stats = lower_stats/100
            return Minion(minion_list[index], round(attack*percentage_lower_stats), round(defense*percentage_lower_stats), round(speed * percentage_lower_stats), round(critchance * percentage_lower_stats), round(maxhealth * percentage_lower_stats))
        case 2:
            index = randint(7,13)
            lower_stats = randint(80,85)
            percentage_lower_stats = lower_stats/100
            return Minion(minion_list[index], round(attack*percentage_lower_stats), round(defense*percentage_lower_stats), round(speed * percentage_lower_stats), round(critchance * percentage_lower_stats), round(maxhealth * percentage_lower_stats))
        case 3:
            index = randint(14,20)
            lower_stats = randint(85,90)
            percentage_lower_stats = lower_stats/100
            return Minion(minion_list[index], round(attack*percentage_lower_stats), round(defense*percentage_lower_stats), round(speed * percentage_lower_stats), round(critchance * percentage_lower_stats), round(maxhealth * percentage_lower_stats))
        case 4:
            percentage_lower_stats = 95/100
            return Minion('Abadon', round(attack*percentage_lower_stats), round(defense*percentage_lower_stats), round(speed * percentage_lower_stats), round(critchance * percentage_lower_stats), round(maxhealth * percentage_lower_stats))
        case 5:
            percentage_lower_stats = 1
            return Minion('Mammon', round(attack*percentage_lower_stats), round(defense*percentage_lower_stats), round(speed * percentage_lower_stats), round(critchance * percentage_lower_stats), round(maxhealth * percentage_lower_stats))
        case 6:
            percentage_lower_stats = 105/100
            return Minion('Belphegor', round(attack*percentage_lower_stats), round(defense*percentage_lower_stats), round(speed * percentage_lower_stats), round(critchance * percentage_lower_stats), round(maxhealth * percentage_lower_stats))
        case 7:
            percentage_lower_stats = 110/100
            return Minion('Lucifer', round(attack*percentage_lower_stats), round(defense*percentage_lower_stats), round(speed * percentage_lower_stats), round(critchance * percentage_lower_stats), round(maxhealth * percentage_lower_stats))

# Where the magic starts.
def village():
    #Printing a welcome message for the player:
    welcome_message()
    clear()
    #We create our player:
    hero = create_player()
    clear()
    # Explaining the menu to the player.
    print ("Welcome to the village {name} here you can choose between 4 different options".format(name = hero.name))
    print(f'{"Training":12}  ==>  {"This is how you level up and get money"}')
    print(f'{"Store":12}  ==>  {"Here you can get potions"}')
    print(f'{"Stats":12}  ==>  {"Here you can see your stats and use your stats points"}')
    print(f'{"Battle Boss":12}  ==>  {"Here you can battle the 3 generals and the demon king. (One at a time)"}')
    input("Press Enter to continue")
    clear()
    while True:
        # Whenever the hero returns to the village he recovers his health.
        hero.health = hero.maxhealth
        # We check if the player has defeated all the bosses of the game with the game_over function.
        game_over(hero)
        try:
            # Prompt the player on what he wants to do now.
            decision = int(input("Where do you want to go now Hero?\n1. Training grounds\n2. Store\n3. Check my stat points\n4. Battle Boss\n5. Exit\n"))
            match decision:
                case 1:
                    # Take the player to fight minions.
                    hero.train()
                case 2:
                    # Take the player to the store where he can buy potions.
                    store(hero)
                    clear()
                case 3:
                    # Take the player to check his stats and spend stats points if he wants to.
                    stats(hero)
                case 4:
                    # Take the player to fight the bosses of the game.
                    boss(hero)
                    pass
                case 5:
                    # If the player decided to leave the game we thank him for playing and exit the program.
                    print("Thanks for playing!")
                    sleep(1)
                    clear()
                    exit()
                case _:
                    # If the player chooses anothe number print the menu again.
                    clear()
        except ValueError:
            # If the player writes something that is not a number then we show him this message.
            print("That is not a valid option try again.")
            input("Press Enter to continue.")
            clear()

def game_over(hero):
    global boss_defeat
    # If the final boss have been defeated the value of the dictionary for key 4 will be set to True in which case we proceed to congratulate the player and end the game creating a file with his final stats and opening a link to "We are the champions" song on Youtube.
    if boss_defeat[4] == True:
        try:
            with open('winner.txt', 'w') as f:
                f.write ("Congratulations {name}\n\nThis txt was created as proof of you finishing the game!\nYour final stats:\n\nAttack: {attack}\nDefense: {defense}\nSpeed: {speed}\nCrit Chance: {critchance}\nMonsters defeated: {monsters}\nPotions used: {potions}".format(name = hero.name, attack = hero.attack, defense = hero.defense, speed = hero.speed, critchance = hero.critchance, monsters = hero.monsterskilled, potions = hero.potionsused))
        except FileExistsError() as e:
            print(e)
        clear()
        print("You...", flush = True, sep= " ") 
        sleep(1.5)
        print("you have done it {hero}.".format(hero = hero.name), flush= True)
        sleep(2)
        print("You faced dangers like no other with courage and determination.", flush = True)
        input("Press Enter to continue.")
        clear()
        print("On your journey you defeated {monsters} monsters.".format(monsters = hero.monsterskilled), flush = True) 
        sleep(1.5)
        print("The 3 generals of the army.", flush= True)
        sleep(1.5)
        print("And the Demon King itself.", flush= True)
        input("Press Enter to continue.")
        clear()
        print("Your efforts have brought peace to this land, its inhabitants today celebrate and chant your name which will go down in history for generations.", flush = True)
        sleep(2.5)
        print("Your long journey ends here", flush = True)
        sleep(1.5)
        print("Thanks for everything.", flush = True)
        sleep(1.5)
        input("Press Enter to finish the game.")
        system('start winner.txt')
        system('start https://youtu.be/ym_jVTcBxSU')
        exit()

# If the player chooses the boss function will execute.
def boss(hero):
    global boss_defeat
    leveldif = 0
    # We check the value for each key of the dictionary boss defeat and decide the boss to face depending on which one has not been defeated yet
    if boss_defeat[1] == False:
        boss_level = 4
        # If the hero is not level 10 yet then make the boss stronger to make the player train more before facing him.
        if hero.lvl < 10:
            leveldif = 11 - hero.lvl
    elif boss_defeat[2] == False:
        boss_level = 5
        # If the hero is not level 20 yet then make the boss stronger to make the player train more before facing him.
        if hero.lvl < 20:
            leveldif = 21 - hero.lvl
    elif boss_defeat[3] == False:
        boss_level = 6
        # If the hero is not level 25 yet then make the boss stronger to make the player train more before facing him.
        if hero.lvl < 25:
            leveldif = 26 - hero.lvl
    elif boss_defeat[4] == False:
        boss_level = 7
        # If the hero is not level 30 yet then make the boss stronger to make the player train more before facing him.
        if hero.lvl < 30:
            leveldif = 40 - hero.lvl
        # We create the boss
    minion = spawnminion(hero.attack + leveldif ,hero.defense + leveldif, hero.speed + leveldif, hero.critchance + leveldif , hero.maxhealth + leveldif, boss_level)
    match boss_level:
        case 4:
            print("\nYou face the first general of the Demon King army: {name}, embrace yourself!\n".format(name = minion.name))
        case 5:
            print("\nYou face the second general of the Demon King army: {name}, embrace yourself!\n".format(name = minion.name))
        case 6:
            print("\nYou face the third general of the Demon King army: {name}, embrace yourself!\n".format(name = minion.name))
        case 7:
            print("\nYou face the Demon King himself: {name}, embrace yourself!\n".format(name = minion.name))
    combat = True
    while combat == True:
        try:
            # We let the player know how much hp he has and how many potions he was at the beggining of this turn.
            print(f'{"HP:":7}  {"{health}/{maxhealth}"}'.format(health = hero.health, maxhealth = hero.maxhealth))
            print(f'{"Potions:":7}  {"{potions}"}'.format(potions = hero.potions))
            # We ask the player if he wants to attack or drink a potion.
            decision = int(input('\nIt\'s your turn {hero} what do you want to do?\n1. Attack\n2. Use potion\n'.format(hero = hero.name)))
            match decision:
                case 1:
                    clear()
                    # If the player chooses 1 then we start the combat by attacking the boss using the attack_enemy method.
                    combat = hero.attack_enemy(minion)
                    # If the boss has any HP left the attack enemy function will return True in which case it's the boss' turn
                    if combat == True:
                        # The minion attacks the player.
                        print("\nCarefull {enemy} is attacking now!\n".format(enemy = minion.name))
                        combat = minion.attack_hero(hero)
                    # If the boss does not have any HP left it means the player won the combat.
                    else:
                        match boss_level:
                            case 4:
                                boss_defeat[1] = True
                                # Give the player experience for winning the combat.
                                hero.exp += 11
                                # Give the player money for winning the combat.
                                hero.money += 10
                            case 5:
                                boss_defeat[2] = True
                                hero.exp += 21
                                hero.money += 15
                            case 6:
                                boss_defeat[3] = True
                                hero.exp += 31
                                hero.money += 20
                            case 7:
                                boss_defeat[4] = True
                                hero.exp += 41
                        # Reward the player with potions.
                        hero.potions += 3
                        # Inform the player of how much money he has now.
                        print ("You got {money}$ now.\n".format(money = hero.money))
                        if hero.potions > 10:
                            hero.potions = 10
                        # Check if the player leveled up and level him up.
                        if hero.exp >= 10:
                            hero.level_up()
                        input("\nPress Enter to go back to the Village\n")
                        clear()
                case 2:
                    clear()
                    # If the player choose to use a potion we call the use_potion method.
                    hero.use_potion() 
                case _:
                    # In case the player writes a number other than 1 or 2
                    print("Please type only 1 or 2 on your keyboard to choose an option.")
                    continue
        except ValueError:
            # In case the player writes a value that is not a number
            print("Sorry we didn't get that please try again.")
    # If the player has no more hp left then leave the combat logic.
    if hero.health == 0: 
        clear()
        return 0

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

village()

    
