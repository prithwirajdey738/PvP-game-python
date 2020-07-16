from classes.game import bcolors, Person
from classes.magic import Spell
from classes.Inventory import Item
import random

# Black Magic
fire = Spell("Fire", 10, 100, "Black")
thunder = Spell("Thunder", 10, 100, "Black")
blizzard = Spell("Blizzard", 10, 100, "Black")
meteor = Spell("Meteor", 20, 200, "Black")
quake = Spell("Quake", 14, 140, "Black")

# White Magic
cure = Spell("Cure", 12, 700, "White")
cura = Spell("Cura", 18, 1500, "White")
curaga = Spell("Curaga", 50, 6000, "White")
# Create some items
potion = Item("Potion", "Potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "Potion", "Heals 100 HP", 100)
superpotion = Item('Super Potion', "Potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "Elixer", "Fully restores HP/MP of one party member", 9999)
megaelixer = Item("Mega Elixer", "Elixer", "Fully restores HP/MP of entire party", 9999)
grenade = Item("Grenade", "Attack", "Deals 500 damage", 500)

enemy_magic = [fire, meteor, curaga]
player_magic = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5},
                {"item": megaelixer, "quantity": 2},
                {"item": grenade, "quantity": 5}]
# Instantiate People, names are 5 characters long
player1 = Person("Prith", 7000, 400, 160, 34, player_magic, player_items)
player2 = Person("Jyoti", 7000, 400, 160, 34, player_magic, player_items)
player3 = Person("Tariq", 7000, 400, 160, 34, player_magic, player_items)
players = [player1, player2, player3]

enemy1 = Person("Amrit", 10000, 701, 350, 25, enemy_magic, [])
enemy2 = Person("Bibas", 10000, 560, 300, 25, enemy_magic, [])
enemy3 = Person("Hasan", 10000, 560, 300, 25, enemy_magic, [])
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!!!" + bcolors.ENDC)

while running:
    print("\n========================\n\n")
    print("NAME              HP                                 MP")

    # Print player stats
    for player in players:
        print("\n")
        player.get_stats()

    # Print enemy stats
    for enemy in enemies:
        print("\n")
        enemy.get_enemy_stats()

    # Player's turn
    for player in players:
        player.choose_action()
        choice = input('Choose action:')
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()

            # Choosing enemy
            enemy = player.choose_target(enemies)
            enemies[enemy].take_dmg(dmg)
            print(bcolors.OKBLUE + "Damage inflicted on " + enemies[enemy].name + " :" + str(dmg) + bcolors.ENDC)

            # Removing dead enemies
            if enemies[enemy].get_hp() == 0:
                print(bcolors.OKGREEN + enemies[enemy].name + " has been killed!!!" + bcolors.ENDC)
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose your spell:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_dmg()
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNOT ENOUGH MAGIC POINTS!!!" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.typ == "White":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals your " + str(magic_dmg) + " HP by " + bcolors.ENDC)
            elif spell.typ == "Black":

                # Choosing enemy
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals damage to " + enemies[enemy].name + " by " +
                      str(magic_dmg) + " HP" + bcolors.ENDC)

                # Removing dead enemies
                if enemies[enemy].get_hp() == 0:
                    print(bcolors.OKGREEN + enemies[enemy].name + " has been killed!!!" + bcolors.ENDC)
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose your item:")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL, "None left!!!", bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.typ == "Potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + item.name + " heals for" + str(item.prop) + "HP" + bcolors.ENDC)
            elif item.typ == "Elixer":
                if item.name == "Mega Elixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp

                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + "Fully restored HP and MP" + bcolors.ENDC)
            elif item.typ == "Attack":

                # Choosing enemy
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(item.prop)
                print(bcolors.OKBLUE + item.name + "deals" + str(item.prop) + "damage to " +
                      enemies[enemy].name + bcolors.ENDC)

                # Removing dead enemies
                if enemies[enemy].get_hp() == 0:
                    print(bcolors.OKGREEN + enemies[enemy].name + " has been killed!!!" + bcolors.ENDC)
                    del enemies[enemy]

    # Checking if player has won
    defeated_enemies = 0
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1
    if defeated_enemies == 3:
        print(bcolors.OKGREEN + "WINNER WINNER CHICKEN DINNER!!!" + bcolors.ENDC)
        running = False

    # Enemy's turn
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)
        if enemy_choice == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()
            players[target].take_dmg(enemy_dmg)
            print(bcolors.FAIL + "Damage inflicted on " + players[target].name + " by " + enemy.name + " is " +
                  str(enemy_dmg) + bcolors.ENDC)

            # Removing dead players
            if players[target].get_hp() == 0:
                print(bcolors.OKGREEN + players[target].name + " has been killed!!!" + bcolors.ENDC)
                del players[target]

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            if spell.typ == "White":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals " + enemy.name + "'s HP by " +
                      str(magic_dmg) + bcolors.ENDC)
            elif spell.typ == "Black":
                # Choosing enemy
                target = random.randrange(0, 3)
                players[target].take_dmg(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals damage to " + players[target].name + " by " +
                      str(magic_dmg) + " HP" + bcolors.ENDC)

                # Removing dead players
                if players[target].get_hp() == 0:
                    print(bcolors.OKGREEN + players[target].name + " has been killed!!!" + bcolors.ENDC)
                    del players[target]

        print("========================\n")

    # Checking if enemy has won
    defeated_players = 0
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1
    if defeated_players == 3:
        print(bcolors.FAIL + "YOU'RE TOAST BRO!!!" + bcolors.ENDC)
        running = False
