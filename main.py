import time
import random
import threading
from math import floor
print("New in 0.5.7: coal, redstone, burn, seeds, smooth stone, iron ingots, fixed negative health glitch for animals\n")# farming, sand, super furnace
# levels
axeLevel = 4
pickLevel = 2
swordLevel = 1
shovelLevel = 2
hoeLevel = 2
shield = False
inventory = {'wood':0, 'stone':0, 'coal':0, 'iron':0, 'gold':0, 'redstone':0, 'emerald':0, 'diamond':0, 'obsidian':0, 'planks':0, 'wool':0, # blocks
             'leather':0, 'sticks':0, 'seeds':0, 'iron ingots':0, # simple items
             'bucket':0, 'water bucket':0, 'smooth stone':0, #advanced items
             'crafting table':0, 'furnace':0, 'smoker':0, 'blast furnace':0, # advanced blocks
             'raw mutton':0, 'cooked mutton':0, 'beef':0, 'steak':0, 'raw porkchop':0, 'cooked porkchop':0 # food
            }
# healths
hearts = 20
hunger = 20
# commands
t = 0
dead = False
night = False
bigTable = False

def timing():
    '''t stands for ticks'''
    while not dead:
        time.sleep(10)
        global t
        global night
        global hunger
        global hearts
        
        t += 1
        if 1 <= t <= 20:
            night = False
            if t == 1:
                print('It is now day\n')
        if 21 <= t <= 40:
            night = True
            if t == 21:
                print('It is now night\n')
        if t >= 41:
            t = 0

        if t % 5 == 0 and hunger > 0:
            hunger -= 1
            unover0()
            if hearts < 20:
                hearts += 1
                print(f'You healed 1 heart. You now have {hearts} health\n')
            print(f'You now have {floor(hunger)} hunger left\n')

def timing_hunger():
    global hearts
    if hunger <= 0:
        hearts -= 1
        print(f'You are starving. Eat something to heal. You have {hearts} health\n')
            
threading.Thread(target=timing).start()

def left123():
    global left1
    global left2
    global left3
    if left1 < 0:
        left1 = 0
    if left2 < 0:
        left2 = 0
    if left3 < 0:
        left3 = 0

def left12():
    global left1
    global left2
    if left1 < 0:
        left1 = 0
    if left2 < 0:
        left2 = 0

def furnace_sleeping(item):
    if (inventory['smoker'] > 0) and (item == 'raw mutton' or item == 'raw porkchop' or item == 'beef'):
        time.sleep(1)
    elif (inventory['blast furnace'] > 0) and (item == 'iron' or item == 'stone'):
        time.sleep(1)
    else:
        time.sleep(3)

def unover20():
    global hunger
    if hunger > 20:
        hunger = 20

def unover0():
    global hunger
    if hunger <= 0:
        hunger = 0

def Inventory():
    all_gotten = [element + ' x ' + str(inventory[element]) for element in inventory if inventory[element] > 0]
    return str(all_gotten).replace('[', '').replace(']', '').replace("'", "")

class Mob:
    def __init__(self, max_health, herd_behaviour, drops):
        self.max_health = max_health
        self.health = max_health
        self.herd_behaviour = herd_behaviour
        self.drops = drops
        self.population = 2

    def populate(self):
        min_groups = self.herd_behaviour[0]
        max_groups = self.herd_behaviour[1]
        min_size = self.herd_behaviour[2]
        max_size = self.herd_behaviour[3]
        
        self.population = random.randint(min_groups, max_groups) * random.randint(min_size, max_size)

    def kill(self):
        self.population -= 1
        self.health = self.max_health
        
        for item_index in range(0, len(self.drops)-1, 2): 
            inventory[self.drops[item_index]] += random.randint(self.drops[item_index+1][0], self.drops[item_index+1][1]) # self.drops[item_index+1] refers to the (1, 1) or (1, 2) part of drops array for sheep. self.drops[item_index] refers to the instance drop so 'wool' for sheep

    def hurt(self):
        self.health -= swordLevel
        if self.health < 0:
            self.health = 0


sheep = Mob( 8, (0, 1, 1, 4), ['wool', (1, 1), 'raw mutton', (1, 2)] )
cow = Mob( 10, (0, 2, 2, 3), ['leather', (0, 2), 'beef', (0, 2)] )
pig = Mob( 10, (0, 2, 4, 5), ['raw porkchop', (0, 1)] )

def change_chunk():
    sheep.populate()
    cow.populate()
    pig.populate()


while not dead:    
    global command
    print('\nhearts:', hearts)
    print('hunger:', floor(hunger))
    print(Inventory())
    command = input('Type command: ').lower()

    threading.Thread(target=timing_hunger).start()

    
    mineWood = 'wood' in command and not 'axe' in command and not 'pick' in command and not 'sword' in command and not 'shovel' in command and not 'burn' in command
    mineStone = 'stone' in command and not 'axe' in command and not 'pick' in command and not 'sword' in command and not 'shovel' in command and not 'burn' in command and not 'smooth' in command
    mineIron = 'iron' in command and not 'axe' in command and not 'pick' in command and not 'sword' in command and not 'shovel' in command and not 'burn' in command and not 'ingot' in command
    mineGold = 'gold' in command and not 'axe' in command and not 'pick' in command and not 'sword' in command and not 'shovel' in command and not 'burn' in command
    mineEmerald = 'emerald' in command and not 'burn' in command
    mineDiamond = 'diamond' in command and not 'axe' in command and not 'pick' in command and not 'sword' in command and not 'shovel' in command and not 'burn' in command
    mineObsidian = 'obsidian' in command and not 'burn' in command
    mineCoal = 'coal' in command and not 'burn' in command
    mineRedstone = 'red' in command and 'stone' in command and 'mine' in command and not 'burn' in command
    mineGrass = 'grass' in command
    
    craftPlanks = 'plank' in command and not 'burn' in command and not 'burn' in command
    craftSticks = 'stick' in command and not 'burn' in command
    craftCraftingTable = 'crafting table' in command and not 'burn' in command
    craftFurnace = 'furnace' in command and not 'burn' in command
    craftSmoker = 'smoker' in command and not 'burn' in command
    craftBlastFurnace = 'blast' in command and 'furnace' in command and not 'burn' in command
    craftWoodenAxe = 'wood' in command and ' axe' in command and not 'burn' in command
    craftWoodenPick = 'wood' in command and 'pick' in command and not 'burn' in command
    craftWoodenSword = 'wood' in command and 'sword' in command and not 'burn' in command
    craftWoodenShovel = 'wood' in command and 'shovel' in command and not 'burn' in command
    craftWoodenHoe = 'wood' in command and 'hoe' in command and not 'burn' in command
    craftStoneAxe = 'stone' in command and ' axe' in command and not 'burn' in command
    craftStonePick = 'stone' in command and 'pick' in command and not 'burn' in command
    craftStoneSword = 'stone' in command and 'sword' in command and not 'burn' in command
    craftStoneShovel = 'stone' in command and 'shovel' in command and not 'burn' in command
    craftStoneHoe = 'stone' in command and 'hoe' in command and not 'burn' in command
    craftIronAxe = 'iron' in command and ' axe' in command and not 'burn' in command
    craftIronPick = 'iron' in command and 'pick' in command and not 'burn' in command
    craftIronSword = 'iron' in command and 'sword' in command and not 'burn' in command
    craftIronShovel = 'iron' in command and 'shovel' in command and not 'burn' in command
    craftIronHoe = 'iron' in command and 'hoe' in command and not 'burn' in command
    craftDiamondAxe = 'diamond' in command and ' axe' in command and not 'burn' in command
    craftDiamondPick = 'diamond' in command and 'pick' in command and not 'burn' in command
    craftDiamondSword = 'diamond' in command and 'sword' in command and not 'burn' in command
    craftDiamondShovel = 'diamond' in command and 'shovel' in command and not 'burn' in command
    craftDiamondHoe = 'diamond' in command and 'hoe' in command and not 'burn' in command
    craftShield = 'shield' in command and not 'burn' in command

    smeltSmoothStone = 'smooth' in command and 'stone' in command and not 'burn' in command
    smeltIronIngots = 'iron' in command and 'ingot' in command and not 'burn' in command
    
    cookRawMutton = 'raw mutton' in command and not 'eat' in command and not 'burn' in command
    cookRawBeef = 'beef' in command and not 'eat' in command and not 'burn' in command
    cookRawPorkchop = 'raw porkchop' in command and not 'eat' in command and not 'burn' in command
    
    
    eatRawMutton = 'eat' in command and 'raw' in command and 'mutton' in command and not 'burn' in command
    eatCookedMutton = 'eat' in command and 'cooked' in command and 'mutton' in command and not 'burn' in command
    eatRawBeef = 'eat' in command and 'beef' in command and not 'burn' in command
    eatSteak = 'eat' in command and 'steak' in command and not 'burn' in command
    eatRawPorkchop = 'eat' in command and 'raw porkchop' in command and not 'burn' in command
    eatCookedPorkchop = 'eat' in command and 'cooked porkchop' in command and not 'burn' in command
    
    killSheep = 'sheep' in command 
    killCow = 'cow' in command 
    killPig = 'pig' in command

    # extra commands

    if command == 'help':
        print('Start by breaking wood and go from there. Other commands are: inventory, walk, sprint, my food, changelog, tools, burn [item] [quantity] and burn all')

    if command == 'walk':
        print('walking to another chunk...')
        time.sleep(7)
        change_chunk()
        r = random.randint(1,10)
        if r == 1:
            hearts -= 1
            print(f'You took 1 heart of fall damage. You now have {hearts} health')
        hunger -= 2
        unover0()
        print(f"You walked to another chunk and lost 2 hunger. You now have {floor(hunger)} hunger")
        
    if command == 'sprint':
        print('sprinting to another chunk...')
        time.sleep(1)
        change_chunk()
        r = random.randint(1,10) # 
        if r == 1:
            r2 = random.randint(1,10)
            if r2 == 1:
                hearts = 0
                print("You fell of a cliff you didn't see")
                print(); print('you died'); print()
                dead = True
                break
            if r2 != 1:
                hearts -= 1
                print(f'You took 1 heart of fall damage. You now have {hearts} health')
        hunger -= 4; unover0()
        print(f"You sprinted to another chunk and lost 4 hunger. You now have {floor(hunger)} hunger")
        
    if command == 'my food':
        if inventory['raw mutton'] > 0:
            print(f'{inventory["raw mutton"]} raw mutton for 2 hunger each')
        if inventory['cooked mutton'] > 0:
            print(f'{inventory["cookedMutton"]} cooked mutton for 6 hunger each')
        if inventory['beef'] > 0:
            print(f'{inventory["beef"]} beef for 3 hunger each')
        if inventory['steak'] > 0:
            print(f'{inventory["steak"]} steak for 8 hunger each')

    if command == 'tools':
        if axeLevel == 4:
            print('no axe')
        elif axeLevel == 3:
            print('wooden axe')
        elif axeLevel == 1:
            print('stone axe')
        elif axeLevel == 0.5:
            print('iron axe')
        elif axeLevel == 0:
            print('diamond axe')

        if pickLevel == 2:
            print('no pickaxe')
        elif pickLevel == 1.5:
            print('wooden pickaxe')
        elif pickLevel == 1:
            print('stone pickaxe')
        elif pickLevel == 0.5:
            print('iron pickaxe')
        elif pickLevel == 0:
            print('diamond pickaxe')

        if swordLevel == 1:
            print('no sword')
        elif swordLevel == 2:
            print('wooden sword')
        elif swordLevel == 3:
            print('stone sword')
        elif swordLevel == 4:
            print('iron sword')
        elif swordLevel == 5:
            print('diamond sword')

        if shovelLevel == 2:
            print('no shovel')
        elif shovelLevel == 1.5:
            print('wooden shovel')
        elif shovelLevel == 1:
            print('stone shovel')
        elif shovelLevel == 0.5:
            print('iron shovel')
        elif shovelLevel == 0:
            print('diamond shovel')

        if hoeLevel == 2:
            print('no hoe')
        elif hoeLevel == 1.5:
            print('wooden hoe')
        elif hoeLevel == 1:
            print('stone hoe')
        elif hoeLevel == 0.5:
            print('iron hoe')
        elif hoeLevel == 0:
            print('diamond hoe')
        

    if command == 'changelog':
        print('0.5/0.5.1: everything')
        print('0.5.2: fixed problem of making wooden axe and mining at same time. Added sheep, food, all wood tools and chunks. Also intoduced extra commands like help and inventory')
        print('0.5.3: Better help command. Added sea pickle monster, stone tools, better crafting error, furnace, obsidian, hearts, hunger and a day night cycle. Furnaces, cooked food and you can eat it now')
        print("0.5.4: fixed bug of animals getting rarer and rarer the more you killed them! That took 3 days! I still don't know what's wrong! Iron and diamond tools, cows, shield, improved hunger")
        print("0.5.5: unchanged version of 0.5.4 bc I saved new one and lost motivation")
        print("0.5.6: deleted everything about sea pickles, added hearts and hunger to GUI, created inventory variable, added minimum pickaxe requirements, hoes, fixed mob code, deleted chunk class, made hunger float, pigs")
        print("0.5.7: coal, redstone, burn, seeds, smooth stone")

    if 'burn' in command and not 'all' in command:
        command = command.split(' ')
        item = command[1]
        number = int(command[2])
        
        if number > inventory[item]:
            number = inventory[item]
        
        inventory[item] -= int(number)

    if command == 'burn all':
        for i in inventory:
            inventory[i] = 0

    # mining stuff

    if mineWood == True:
        print('mining wood...')
        time.sleep(axeLevel * 1)
        inventory['wood'] += 1
        print(f'You now have {inventory["wood"]} wood')
    if mineStone == True:
        if pickLevel <= 1.5:
            print('mining stone...')
            time.sleep(pickLevel * 2)
            inventory['stone'] += 1
            print(f'You now have {inventory["stone"]} stone')
        else:
            print('You need a wooden pickaxe')
    if mineIron == True:
        if pickLevel <= 1:
            print('mining iron...')
            time.sleep(pickLevel * 3)
            inventory["iron"] += 1
            print(f'You now have {inventory["iron"]} iron')
        else:
            print('You need a stone pickaxe')
    if mineGold == True:
        if pickLevel <= 0.5:
            print('mining gold...')
            time.sleep(pickLevel * 2.5)
            inventory["gold"] += 1
            print(f'You now have {inventory["gold"]} gold')
        else:
            print('You need an iron pickaxe')
    if mineEmerald == True:
        if pickLevel <= 0.5:
            print('mining emerald...')
            time.sleep(pickLevel * 4)
            inventory["emerald"] += 1
            print(f'You now have {inventory["emerald"]} emerald')
        else:
            print('You need an iron pickaxe')
    if mineDiamond == True:
        if pickLevel <= 0.5:
            print('mining diamond...')
            time.sleep(pickLevel * 5)
            inventory["diamond"] += 1
            print(f'You now have {inventory["diamond"]} diamond')
        else:
            print('You need an iron pickaxe')
    if mineObsidian == True:
        if pickLevel <= 0:
            print('mining obsidian...')
            time.sleep(pickLevel * 6)
            inventory["obsidian"] += 1
            print(f'You now have {inventory["obsidian"]} obsidian')
        else:
            print('You need a diamond pickaxe')

    if mineCoal:
        if pickLevel <= 1:
            print('mining coal...')
            time.sleep(pickLevel * 2.5)
            inventory['coal'] += random.randint(3, 7)
            print(f'You now have {inventory["coal"]} coal')
        else:
            print('You need a stone pickaxe')

    if mineRedstone:
        if pickLevel <= 0.5:
            print('mining redstone...')
            time.sleep(pickLevel * 0.5)
            inventory['redstone'] += random.randint(3, 7)
            print(f'You now have {inventory["redstone"]} redstone')
        else:
            print('You need an iron pickaxe')

    if mineGrass:
        yeild = random.randint(0, 2) * random.randint(1, 2) # just a more complicated random
        inventory['seeds'] += yeild
        print(f"You have {yeild} more seeds")

    # making blocks and items

    if craftPlanks == True:
        if inventory['wood'] >= 1:
            inventory['wood'] -= 1
            inventory['planks'] += 4
            print(f'You now have {inventory["wood"]} wood and {inventory["planks"]} planks')
        else:
            left = 1 - inventory["wood"]
            print(f'You need {left} more wood')

    if craftSticks == True:
        if inventory["planks"] >= 2:
            inventory["planks"] -= 2
            inventory["sticks"] += 4
            print(f'You now have {inventory["planks"]} planks and {inventory["sticks"]} sticks')
        else:
            left = 2 - inventory["planks"]
            print(f'You need {left} more planks')

    if craftCraftingTable == True:
        if inventory["planks"] >= 4:
            inventory["planks"] -= 4
            inventory["crafting table"] += 1
            bigTable = True
            print(f'You now have {inventory["planks"]} planks and {inventory["crafting table"]} crafting tables')
        else:
            left = 4 - inventory["planks"]
            print(f'You need {left} more planks')

    if craftFurnace == True:
        if inventory["stone"] >= 8:
            if bigTable == True:
                inventory["stone"] -= 8
                inventory["furnace"] += 1
                print(f'You now have {inventory["furnace"]} furnace and {inventory["stone"]} stone')
            else:
                print('You need to make a crafting table')
        else:
            left = 8 - inventory["stone"]
            print(f'You need {left} more stone')

    if craftSmoker == True:
        if inventory["furnace"] > 0 and inventory["wood"] > 3:
            if bigTable == True:
                inventory["furnace"] -= 1
                inventory["wood"] -= 4
                inventory["smoker"] += 1
                print(f'You now have {inventory["smoker"]} smoker, {inventory["furnace"]} furnaces and {inventory["wood"]} wood')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 1 - inventory["furnace"]
            left2 = 4 - inventory["wood"]
            left12()
            print(f'You need {left1} more furnace and {left} more wood')

    # crafting tools
    
    if craftWoodenAxe == True:
        if inventory["sticks"] >= 2 and inventory["planks"] >= 3:
            if bigTable == True:
                inventory["planks"] -= 3
                inventory["sticks"] -=  2
                axeLevel = 3
                print(f'You now have a wooden axe, {inventory["planks"]} planks and {inventory["sticks"]} sticks')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 2 - inventory["sticks"]
            left2 = 3 - inventory["planks"]
            left12()
            print(f'You need {left1} more sticks and {left2} more planks')

    if craftWoodenPick == True:
        if inventory["sticks"] >= 2 and inventory["planks"] >= 3:
            if bigTable == True:
                inventory["planks"] -= 3
                inventory["sticks"] -= 2
                pickLevel = 1.5
                print(f'You now have a wooden pickaxe, {inventory["planks"]} planks and {inventory["sticks"]} sticks')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 2 - inventory["sticks"]
            left2 = 3 - inventory["planks"]
            left12()
            print(f'You need {left1} more sticks and {left2} more planks')

    if craftWoodenSword == True:
        if inventory["sticks"] >= 1 and inventory["planks"] >= 2:
            if bigTable == True:
                inventory["sticks"] -= 1
                inventory["planks"] -= 2
                swordLevel = 2
                print(f'You now have a wooden sword, {inventory["planks"]} planks and {inventory["sticks"]} sticks')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 1 - inventory["sticks"]
            left2 = 2 - inventory["planks"]
            left12()
            print(f'You need {left1} more sticks and {left2} more planks')

    if craftWoodenShovel == True:
        if inventory["sticks"] >= 2 and inventory["planks"] >= 1:
            if bigTable == True:
                inventory["sticks"] -= 2
                inventory["planks"] -= 1
                shovelLevel = 1.5
                print(f'You now have a wooden shovel, {inventory["planks"]} planks and {inventory["sticks"]} sticks')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 2 - inventory["sticks"]
            left2 = 1 - inventory["planks"]
            left12()
            print(f'You need {left1} more sticks and {left2} more planks')

    if craftWoodenHoe == True:
        if inventory['sticks'] >= 2 and inventory['planks'] >= 2:
            if bigTable == True:
                inventory['sticks'] -= 2
                inventory['planks'] -= 2
                hoeLevel = 1.5
                print(f'You now have a wooden hoe, {inventory["planks"]} planks and {inventory["sticks"]} sticks')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 2 - inventory['sticks']
            left2 = 2 - inventory['planks']
            left12()
            print(f'You need {left1} more sticks and {left2} more planks')

    if craftStoneAxe == True:
        if inventory["sticks"] >= 2 and inventory["stone"] >= 3:
            if bigTable == True:
                inventory["sticks"] -= 2
                inventory["stone"] -= 3
                axeLevel = 1
                print(f'You now have a stone axe, {inventory["sticks"]} sticks and {inventory["stone"]} stone')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 2 - inventory["sticks"]
            left2 = 3 - inventory["stone"]
            left12()
            print(f'You need {left1} more sticks and {left2} more stone')

    if craftStonePick == True:
        if inventory["sticks"] >= 2 and inventory["stone"] >= 3:
            if bigTable == True:
                inventory["sticks"] -= 2
                inventory["stone"] -= 3
                pickLevel = 1
                print(f'You now have a stone pickaxe, {inventory["sticks"]} sticks and {inventory["stone"]} stone')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 2 - inventory["sticks"]
            left2 = 3 - inventory["stone"]
            left12()
            print(f'You need {left1} more sticks and {left2} more stone')

    if craftStoneSword == True:
        if inventory["sticks"] >= 1 and inventory["stone"] >= 2:
            if bigTable == True:
                inventory['sticks'] -= 1
                inventory['stone'] -= 2
                swordLevel = 3
                print(f'You now have a stone sword, {inventory["sticks"]} sticks and {inventory["stone"]} stone')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 1 - inventory['sticks']
            left2 = 2 - inventory['stone']
            left12()
            print(f'You need {left1} more sticks and {left2} more stone')

    if craftStoneShovel == True:
        if inventory['sticks'] >= 2 and inventory['stone'] >= 1:
            if bigTable == True:
                inventory['sticks'] -= 2
                inventory['stone'] -= 1
                shovelLevel = 1
                print(f'You now have a stone shovel, {inventory["sticks"]} sticks and {inventory["stone"]} stone')
            else:
                print(f'You need to make a crafting table')
        else:
            left1 = 2 - inventory['sticks']
            left2 = 1 - inventory['stone']
            left12()
            print(f'You need {left1} more sticks and {left2} more stone')

    if craftStoneHoe == True:
        if inventory['sticks'] >= 2 and inventory['stone'] >= 2:
            if bigTable == True:
                inventory['sticks'] -= 2
                inventory['stone'] -= 2
                hoeLevel = 1
                print(f'You now have a stone hoe, {inventory["stone"]} stone and {inventory["sticks"]} sticks')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 2 - inventory['sticks']
            left2 = 2 - inventory['stone']
            left12()
            print(f'You need {left1} more sticks and {left2} more stone')

    if craftIronAxe == True:
        if inventory['sticks'] >= 2 and inventory['iron ingots'] >= 3:
            if bigTable == True:
                inventory['sticks'] -= 2
                inventory['iron ingots'] -= 3
                axeLevel = 0.5
                print(f'You now have an iron axe, {inventory["sticks"]} sticks and {inventory["iron ingots"]} iron ingots')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 2 - inventory['sticks']
            left2 = 3 - inventory['iron ingots']
            left12
            print(f'You need {left1} more sticks and {left2} more iron')

    if craftIronPick == True:
        if inventory['sticks'] >= 2 and inventory['iron ingots'] >= 3:
            if bigTable == True:
                inventory['sticks'] -= 2
                inventory['iron ingots'] -= 3
                pickLevel = 0.5
                print(f'You now have a iron pickaxe, {inventory["sticks"]} sticks and {inventory["iron ingots"]} iron ingots')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 2 - inventory['sticks']
            left2 = 3 - inventory['iron ingots']
            left12()
            print(f'You need {left1} more sticks and {left2} more iron ingots')
            
    if craftIronSword == True:
        if inventory['sticks'] >= 1 and inventory['iron ingots'] >= 2:
            if bigTable == True:
                inventory['sticks'] -= 1
                inventory['iron ingots'] -= 2
                swordLevel = 4
                print(f'You now have a iron sword, {inventory["sticks"]} sticks and {inventory["iron ingots"]} iron ingots')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 1 - inventory['sticks']
            left2 = 2 - inventory['iron ingots']
            left12()
            print(f'You need {left1} more sticks and {left2} more iron ingots')

    if craftIronShovel == True:
        if inventory['sticks'] >= 2 and inventory['iron ingots'] >= 1:
            if bigTable == True:
                inventory['sticks'] -= 2
                inventory['iron ingots'] -= 1
                shovelLevel = 0.5
                print(f'You now have a iron shovel, {inventory["sticks"]} sticks and {inventory["iron ingots"]} iron ingots')
            else:
                print(f'You need to make a crafting table')
        else:
            left1 = 2 - inventory['sticks']
            left2 = 1 - inventory['iron ingots']
            left12()
            print(f'You need {left1} more sticks and {left2} more iron ingots')

    if craftIronHoe == True:
        if inventory['sticks'] >= 2 and inventory['iron ingots'] >= 2:
            if bigTable == True:
                inventory['sticks'] -= 2
                inventory['iron ingots'] -= 2
                hoeLevel = 0.5
                print(f'You now have a iron hoe, {inventory["iron ingots"]} iron ingots and {inventory["sticks"]} sticks')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 2 - inventory['sticks']
            left2 = 2 - inventory['iron ingots']
            left12()
            print(f'You need {left1} more sticks and {left2} more iron ingots')

    if craftDiamondAxe == True:
        if inventory['sticks'] >= 2 and inventory['diamond'] >= 3:
            if bigTable == True:
                inventory['sticks'] -= 2
                inventory['diamond'] -= 3
                axeLevel = 0
                print(f'You now have an iron axe, {inventory["sticks"]} sticks and {inventory["diamond"]} diamond')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 2 - inventory['sticks']
            left2 = 3 - inventory['diamond']
            left12
            print(f'You need {left1} more sticks and {left2} more diamond')

    if craftDiamondPick == True:
        if inventory['sticks'] >= 2 and inventory['diamond'] >= 3:
            if bigTable == True:
                inventory['sticks'] -= 2
                inventory['diamond'] -= 3
                pickLevel = 0
                print(f'You now have a iron pickaxe, {inventory["sticks"]} sticks and {inventory["diamond"]} diamond')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 2 - inventory['sticks']
            left2 = 3 - inventory['diamond']
            left12()
            print(f'You need {left1} more sticks and {left2} more diamond')
            
    if craftDiamondSword == True:
        if inventory['sticks'] >= 1 and inventory['diamond'] >= 2:
            if bigTable == True:
                inventory['sticks'] -= 1
                inventory['diamond'] -= 2
                swordLevel = 5
                print(f'You now have a iron sword, {inventory["sticks"]} sticks and {inventory["diamond"]} diamond')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 1 - inventory['sticks']
            left2 = 2 - inventory['diamond']
            left12()
            print(f'You need {left1} more sticks and {left2} more diamond')

    if craftDiamondShovel == True:
        if inventory['sticks'] >= 2 and inventory['diamond'] >= 1:
            if bigTable == True:
                inventory['sticks'] -= 2
                inventory['diamond'] -= 1
                shovelLevel = 0
                print(f'You now have a iron shovel, {inventory["sticks"]} sticks and {inventory["diamond"]} diamond')
            else:
                print(f'You need to make a crafting table')
        else:
            left1 = 2 - inventory['sticks']
            left2 = 1 - inventory['diamond']
            left12()
            print(f'You need {left1} more sticks and {left2} more diamond')

    if craftDiamondHoe == True:
        if inventory['sticks'] >= 2 and inventory['diamond'] >= 2:
            if bigTable == True:
                inventory['sticks'] -= 2
                inventory['diamond'] -= 2
                hoeLevel = 1.5
                print(f'You now have a diamond hoe, {inventory["diamond"]} diamond and {inventory["sticks"]} sticks')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 2 - inventory['sticks']
            left2 = 2 - inventory['diamond']
            left12()
            print(f'You need {left1} more sticks and {left2} more diamond')

    if craftShield == True:
        if inventory['planks'] >= 6 and inventory['iron ingots'] >= 1:
            if bigTable == True:
                inventory['planks'] -= 6
                inventory['iron ingots'] -= 1
                shield = True
                print('You now have a shield')
            else:
                print('You need to make a crafting table')
        else:
            left1 = 6 - inventory['planks']
            left2 = 1 - inventory['iron ingots']
            left12
            print(f'You need {left1} more planks and {left2} more iron ingots')

    # furnacing and blast furnacing

    if smeltSmoothStone:
        if inventory['stone'] > 0:
            if inventory['furnace'] > 0 or inventory['blast furnace'] > 0:
                if inventory['coal'] > 0:
                    print('smelting...')
                    furnace_sleeping('stone')
                    inventory['coal'] -= 1
                    inventory['stone'] -= 1
                    inventory['smooth stone'] += 1
                    print(f"You now have {inventory['smooth stone']} smooth stone, {inventory['stone']} stone and {inventory['coal']} coal")
                else:
                    print('You need 1 more coal')
            else:
                print('You need to make a furnace')
        else:
            print('You need 1 more stone')

    if smeltIronIngots:
        if inventory['furnace'] or inventory['blast furnace'] > 0:
            if inventory['coal'] > 0:
                if inventory['iron'] > 0:
                    print('smelting...')
                    furnace_sleeping('iron')
                    inventory['coal'] -= 1
                    inventory['iron'] -= 1
                    inventory['iron ingots'] += 1
                    print(f"You now have {inventory['iron ingots']} iron ingots, {inventory['iron']} iron and {inventory['coal']} coal")
                else:
                    print('You need 1 more iron')
            else:
                print('You need 1 more coal')
        else:
            print('You need to make a furnace')

    # furnacing and eating

    if eatRawMutton == True:
        if inventory['raw mutton'] > 0:
            time.sleep(0.5)
            hunger += 2
            inventory['raw mutton'] -= 1
            unover20()
            print(f'gained 2 hunger. You now have {floor(hunger)} hunger and {inventory["raw mutton"]} raw mutton')
        else:
            print("You don't have any raw mutton")

    if cookRawMutton == True:
        if inventory['raw mutton'] > 0:
            if inventory['furnace'] > 0 or inventory['smoker'] > 0:
                if inventory['coal'] > 0:
                    print('cooking...')
                    furnace_sleeping('raw mutton')
                    inventory['coal'] -= 1
                    inventory['raw mutton'] -= 1
                    inventory['cooked mutton'] += 1
                    print(f'You now have {inventory["cooked mutton"]} cooked mutton, {inventory["raw mutton"]} raw mutton and {inventory["coal"]} coal')
                else:
                    print('You need 1 more coal')
            else:
                print('You need to make a furnace')
        else:
            print('You need 1 more raw mutton')

    if eatCookedMutton == True:
        if inventory['cooked mutton'] > 0:
            time.sleep(0.5)
            hunger += 6
            inventory['cooked mutton'] -= 1
            unover20()
            print(f'Gained 6 hunger. You now have {floor(hunger)} hunger and {inventory["cooked mutton"]} cooked mutton')
        else:
            if inventory['raw mutton'] > 0:
                print(f"You don't have any cooked mutton but {inventory['raw mutton']} raw mutton")
            else:
                print(f"You don't have any cooked mutton")

    if eatRawBeef == True:
        if inventory['beef'] > 0:
            time.sleep(0.5)
            hunger += 3
            inventory['beef'] -= 1
            unover20()
            print(f'Gained 3 hunger. You now have {floor(hunger)} hunger and {inventory["beef"]} beef')
        else:
            print("You don't have any beef")

    if cookRawBeef == True:
        if inventory['beef'] > 0:
            if inventory['furnace'] > 0 or inventory['smoker'] > 0:
                if inventory['coal'] > 0:
                    print('cooking...')
                    furnace_sleeping('raw beef')
                    inventory['coal'] -= 1
                    inventory['beef'] -= 1
                    inventory['steak'] += 1
                    print(f'You now have {inventory["steak"]} steak, {inventory["beef"]} beef and {inventory["coal"]} coal')
                else:
                    print('You need 1 more coal')
            else:
                print('You need to make a furnace')
        else:
            print('You need 1 more beef')

    if eatSteak == True:
        if inventory['steak'] > 0:
            time.sleep(0.5)
            hunger += 8
            inventory['steak'] -= 1
            unover20()
            print(f'Gained 8 hunger. You now have {floor(hunger)} hunger and {inventory["steak"]} steak')
        else:
            if inventory['beef'] > 0:
                print(f"You don't have any steak but {inventory['beef']} beef")
            else:
                print(f"You don't have any steak")

    if cookRawPorkchop == True:
        if inventory['raw porkchop'] > 0:
            if inventory['furnace'] > 0 or inventory['smoker'] > 0:
                if inventory['coal'] > 0:
                    print('cooking...')
                    furnace_sleeping('raw porkchop')
                    inventory['coal'] -= 1
                    inventory['raw porkchop'] -= 1
                    inventory['cooked porkchop'] += 1
                    print(f'You now have {inventory["cooked porkchop"]} cooked porkchops, {inventory["raw porkchop"]} raw porkchops and {inventory["coal"]} coal')
                else:
                    print('You need 1 more coal')
            else:
                print('You need to make a furnace')
        else:
            print('You need 1 more raw porkchop')

    if eatRawPorkchop == True:
        if inventory['raw porkchop'] > 0:
            time.sleep(0.5)
            hunger += 4
            inventory['raw porkchop'] -= 1
            unover20()
            print(f"Gained 3 hunger. You now have {floor(hunger)} hunger and {inventory['raw porkchop']} raw porkchops")
        else:
            print("You don't have any raw porkchops")

    if eatCookedPorkchop == True:
        if inventory['cooked porkchop'] > 0:
            time.sleep(0.5)
            hunger += 9
            inventory['cooked porkchop'] -= 1
            unover20()
            print(f"Gained 8 hunger. You now have {floor(hunger)} hunger and {inventory['cooked porkchop']} cooked porkchops")
        else:
            if inventory['raw porkchop'] > 0:
                print(f"You don't have any cooked porkchops but {inventory['raw porkchop']} raw porkchops")
            else:
                print("You don't have any cooked porkchops")
            
    # hunting
    
    if killSheep == True:
        if sheep.population > 0:
            hunger -= 0.2
            if random.randint(1, 10) > 2: # 80% chance of hitting
                sheep.hurt()
                print(f'the sheep now has {sheep.health} health')
            else:
                print('you missed')

            if sheep.health < 1:
                sheep.kill()
        else:
            print('there are no sheep here')

    if killCow:
        if cow.population > 0:
            hunger -= 0.2
            if random.randint(1, 10) > 2: # 80% chance of hitting
                cow.hurt()
                print(f'the cow now has {cow.health} health')
            else:
                print('you missed')

            if cow.health < 1:
                cow.kill()
        else:
            print('there are no cows here')

    if killPig:
        if pig.population > 0:
            hunger -= 0.2
            if random.randint(1, 10) > 2:
                pig.hurt()
                print(f'the pig now has {pig.health} health')
            else:
                print('you missed')

            if pig.health < 1:
                pig.kill()
        else:
            print('there are no pigs here')

    # death message
    
    if hearts <= 0:
        print()
        print('You died')
        print()
        dead = True
