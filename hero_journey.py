#Author: Nicolas Agudelo.



from os import system
from time import sleep

clear = lambda: system('cls')
stat_points = 0
def main():
    menu()

def menu():
    #Printing a welcome message for the player:
    welcome_message()
    clear()
    #We create our player:
    create_player()
    print("I will put the village here.")

def create_player():
    print("""
You will now start your adventure to defeat the Demon King and his three generals, they have started a war against humanity and seek to exterminate them. 
The Hero is the only one capable of stopping them. 
You will have to train, face enemies, level up and gather resources before taking on to the generals and finally the Demon King.
    """, flush=True)
    input("Press any key to continue:")
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
                    input("Press any key to continue")
                    continue
                # In case they write anything else.
                case _: 
                    print("Please type Y for yes, or, N for no. Other answers are not supported.")
                    input("Press any key to continue")
                    continue
        # In case an ValueError happens.
        except ValueError :
            print("Sorry we didn\'t get that, please try again\n")
            input("Press any key to continue")
            continue
    clear()
    print("Sir {name} then, the outcome of your battles and how well you prepare yourself to face this challenge will forever change the destiny of humanity and the world.\n".format(name = name))
    input("Press any key to continue")
     
    stat_points = 10
    clear()
    print("""
Now is the time to distribute your initial stats you will receive {stat_points} for the start of your adventure. You will be able to distribute them in four different categories:
>  Attack: Determines how much damage you will deal to your enemies.
>  Defense: Determines how much damage reduction you will have against enemies.
>  Speed: Determines the chance of avoiding damage from an attack.
>  Crit Chance: Determines the chance of dealing extra damage when you attack an enemie.
    """.format(stat_points = stat_points))
    input("Press any key to continue")
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
                    input("Press any key to continue")
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
                    input("Press any key to continue")
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
                    input("Press any key to continue")
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
                    input("Press any key to continue")
                    continue
                else:
                    stat_points -= crit_points
                break       
        except ValueError:
            print("Please use only numbers to select your stats\n")
            input("Press any key to continue")
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
                    input("Press any key to continue")
                    break
                # In case they write anything else.
                case _: 
                    print("Please type Y for yes, or, N for no. Other answers are not supported.") 
                    continue
        if answer == 'N': continue
        clear()
        print("Thanks Hero, your adventure will now start, your will be transported to the village where you will be able to choose what to do next. if you have any unused stat points left you will be able to use them there too.\nI wish you the best of luck in your journey!")
        break

    # Create player once we have all his information collected:
    # I will create the hero here.
    return("Hero was created ;)")
    
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

    input("Press any button to continue:")    

main()

    
