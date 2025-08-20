import toons as c

print("Welcome to SuperMagic101's Future Fight Teambuilding Guide! You can select a gamemode, input your damage dealer, and this program will recommend good leaders and supports for that gamemode. PLEASE NOTE: All characters are assumed to have their most recent uniforms equipped until such a time that I decide to put in the info for the other 300-something. Thanks!")

##*********DO UNIFORMS (eventually)***********
##*****Adjust Thor's code to include the leadership if they have the artifact***

#lead/support skill setup
offensive_effects = ["all attack", "physical", "energy", "lightning", "fire", "mind", "poison", "cold", "hero", "villain", "damage to boss", "damage to non-boss", "ignore dodge", "ignore defense", "debuff effect increase", "all elem", "crit damage", "crit rate", "damage to universal", "damage to combat", "damage to speed", "damage to blast", "skill damage bonus damage", "chain hit", "guaranteed crit rate", "neutral", "male", "female", "no gender", "human", "alien", "creature", "mutant", "inhuman", "other", "summon illusion", "damage to cleansed"]
defensive_effects = ["debuff cleanse", "better debuff cleanse", "lightning resist", "fire resist", "mind resist", "poison resist", "cold resist", "dr", "dodge", "all defense", "dr hero", "dr villain", "hp", "super armor", "incapacitation immunity", "all resist", "dr universal", "dr speed", "dr combat", "dr blast", "heal when hit", "recovery rate", "reflect all", "reflect physical", "reflect energy", "decrease chain hit", "ignore damage inc/dec effect", "heal when debuffed", "guard break immunity", "decrease all reflect", "decrease phys reflect", "decrease energy reflect", "mind immunity", "emergency heal", "TIFBD"] #TIFBD = Temporary Immunity Followed By Death
damage_types = ["physical", "energy", "hp"]
damage_elem = ["lightning", "mind", "cold", "poison", "fire"]
damage_targets = ["hero", "villain", "neutral", "damage to boss", "damage to non-boss", "male", "female", "no gender", "human", "alien", "creature", "mutant", "inhuman", "other"]

#gamemode setup
#**********DO THESE DAMN GAMEMODES BEFORE THE GAME DIES**************
gamemodes_dict = {0:"story, dimension mission, dimension rift, epic quest, and/or heroic quest",
                  1:"the big bunch",
                  2:"dispatch mission",
                  3:"world boss",
                  4:"shadowland",
                  5:"alliance battle"}

effdict = {}

print("\n\n1: Story, Dimension Mission, Dimension Rift, Epic Quest, and/or Heroic Quest\n2: Dispatch Mission   3: World Boss\n4: Shadowland   5: Alliance Battle")
gamemode = gamemodes_dict[int(input("Select the number that corresponds to the gamemode you would like to play: "))]

def the_big_bunch():

    for i in c.toons:
        c.namedict[i.name] = i
        if "leader" in i.pos:
            c.leaders.append(i)
        if "support" in i.pos:
            c.supports.append(i)

    #potentially account for enemies with immunities, especially in story?
    def enterDealer():
        global dealer
        print("\nWho is your dealer? Please type in the exact name (Doctor Strange instead of Dr Strange, for example) unless it is something like Sharon Rogers because nobody likes typing in 'Captain America (Sharon Rogers)' but still please type in the character's first and last name in those cases")
        dealer = input("\n")
        if dealer.title() in c.namedict:
            dealer = c.namedict[dealer.title()]
        else:
            print("\n" + dealer + " was not found in the database.")
            dealer = input("\nWould you like to try typing the name in again? Y/N (N will end the program) ")
            if dealer == "n" or dealer == "N":
                quit()
            elif dealer == "y" or dealer == "Y":
                enterDealer()
            elif dealer.title() in c.namedict:
                dealer = c.namedict[dealer.title()]

        if dealer == c.Nicepool:
            c.leaders.remove(c.Deadpool)
        if dealer == c.Deadpool:
            synergy = input("\nPlease type 1 for Deadpool (Deadpool & Wolverine) or type 2 for Nicepool (Deadpool & Wolverine) ")
            if synergy == "1":
                dealer = c.Deadpool
                c.leaders.remove(c.Nicepool)
            elif synergy == "2":
                dealer = c.Nicepool
                c.leaders.remove(c.Deadpool)
    enterDealer()

    #leader setup
    offensive_leaders = []
    for i in c.leaders:
        for j in range(0, len(i.leadappliesto)):
            if i not in offensive_leaders:
                if i.leadappliesto[j] == "all allies" or i.leadappliesto[j] == dealer.typing or i.leadappliesto[j] == dealer.gender or i.leadappliesto[j] == dealer.allies or i.leadappliesto[j] == dealer.side or i.leadappliesto[j] == dealer.name:
                    offensive_leaders.append(i)
                for k in range(0, len(dealer.abilities)):
                    if i.leadappliesto[j] == dealer.abilities[k]:
                        offensive_leaders.append(i)
    defensive_leaders = offensive_leaders.copy()

    print("\n\nLeaders that provide offensive buffs are: ")
    blackball = []
    for i in offensive_leaders:
        leadapplies = False
        applied = []
        for j in range(0, len(i.leadappliesto)):
            if i.leadappliesto[j] == "all allies" or i.leadappliesto[j] == dealer.typing or i.leadappliesto[j] == dealer.gender or i.leadappliesto[j] == dealer.allies or i.leadappliesto[j] == dealer.side or i.leadappliesto[j] == dealer.name or i.leadappliesto[j] in dealer.abilities:
                for k in range(0, len(i.leadgives[j])):
                    if i.leadgives[j][k] in offensive_effects or (dealer == c.Hulk and i.leadgives[j][k] == "hp") or (dealer == c.Victorius and i.leadgives[j][k] == "hp"):
                        if i.leadgives[j][k] in damage_types:
                            if i.leadgives[j][k] == dealer.dmg_main:
                                leadapplies = True
                                applied.append(i.leadgives[j][k])
                        elif i.leadgives[j][k] == "all elem":
                            if dealer.dmg_elem != "none":
                                leadapplies = True
                                applied.append(i.leadgives[j][k])
                        elif i.leadgives[j][k] in damage_elem:
                            if i.leadgives[j][k] == dealer.dmg_elem:
                                leadapplies = True
                                applied.append(i.leadgives[j][k])
                            elif i.leadgives[j][k] in dealer.dmg_elem:
                                leadapplies = True
                                applied.append(i.leadgives[j][k])
                        elif i.leadgives[j][k] in damage_targets:
                            pass
                        elif i.leadgives[j][k] not in (damage_types or damage_elem or damage_targets):
                            leadapplies = True
                            applied.append(i.leadgives[j][k])
        if leadapplies == False:
            blackball.append(i)
        else:
            print(i.name + ": " + str(applied))
    for i in blackball:
        offensive_leaders.remove(i)
    if len(offensive_leaders) == 0:
        print("none")

    blackball = []       
    print("\nLeaders that provide defensive buffs are: ")
    for i in defensive_leaders:
        leadapplies = False
        applied = []
        for j in range(0, len(i.leadappliesto)):
            if i.leadappliesto[j] == "all allies" or i.leadappliesto[j] == dealer.typing or i.leadappliesto[j] == dealer.gender or i.leadappliesto[j] == dealer.allies or i.leadappliesto[j] == dealer.side or i.leadappliesto[j] == dealer.name or i.leadappliesto[j] in dealer.abilities:
                for k in range(0, len(i.leadgives[j])):
                    if i.leadgives[j][k] in defensive_effects:
                        if "dr" not in i.leadgives[j][k]:
                            leadapplies = True
                            applied.append(i.leadgives[j][k])
        if leadapplies == False:
            blackball.append(i)
        else:
            print(i.name + ": " + str(applied))
    for i in blackball:
        defensive_leaders.remove(i)
    if len(defensive_leaders) == 0:
        print("none")
            
    #support setup
    offensive_supports = []
    for i in c.supports:
        for j in range(0, len(i.suppappliesto)):
            if i not in offensive_supports:
                if i.suppappliesto[j] == "all allies" or i.suppappliesto[j] == dealer.typing or i.suppappliesto[j] == dealer.gender or i.suppappliesto[j] == dealer.allies or i.suppappliesto[j] == dealer.side or i.suppappliesto[j] == dealer.name:
                    offensive_supports.append(i)
                for k in range(0, len(dealer.abilities)):
                    if i.suppappliesto[j] == dealer.abilities[k]:
                        offensive_supports.append(i)
    defensive_supports = offensive_supports.copy()

    blackball = []
    print("\n\nSupport characters that provide offensive buffs are: ")
    for i in offensive_supports:
        supportapplies = False
        applied = []
        for j in range(0, len(i.suppappliesto)):
            if i.suppappliesto[j] == "all allies" or i.suppappliesto[j] == dealer.typing or i.suppappliesto[j] == dealer.gender or i.suppappliesto[j] == dealer.allies or i.suppappliesto[j] == dealer.side or i.suppappliesto[j] == dealer.name or i.suppappliesto[j] in dealer.abilities:
                for k in range(0, len(i.suppgives[j])):
                    if i.suppgives[j][k] in offensive_effects or (dealer == c.Hulk and i.suppgives[j][k] == "hp") or (dealer == c.Victorius and i.suppgives[j][k] == "hp"):
                        if i.suppgives[j][k] in damage_types:
                            if i.suppgives[j][k] == dealer.dmg_main:
                                supportapplies = True
                                applied.append(i.suppgives[j][k])
                        elif i.suppgives[j][k] == "all elem":
                            if dealer.dmg_elem != "none":
                                supportapplies = True
                                applied.append(i.suppgives[j][k])
                        elif i.suppgives[j][k] in damage_elem:
                            if i.suppgives[j][k] == dealer.dmg_elem:
                                supportapplies = True
                                applied.append(i.suppgives[j][k])
                            elif i.suppgives[j][k] in dealer.dmg_elem:
                                supportapplies = True
                                applied.append(i.suppgives[j][k])
                        elif i.suppgives[j][k] in damage_targets:
                            pass
                        elif i.suppgives[j][k] not in (damage_types or damage_elem or damage_targets):
                            supportapplies = True
                            applied.append(i.suppgives[j][k])
        if supportapplies == False:
            blackball.append(i)
        else:
            print(i.name + ": " + str(applied))
    for i in blackball:
        offensive_supports.remove(i)
    if len(offensive_supports) == 0:
        print("none")

    blackball = []   
    print("\nSupport characters that provide defensive buffs are: ")
    for i in defensive_supports:
        supportapplies = False
        applied = []
        for j in range(0, len(i.suppappliesto)):
            if i.suppappliesto[j] == "all allies" or i.suppappliesto[j] == dealer.typing or i.suppappliesto[j] == dealer.gender or i.suppappliesto[j] == dealer.allies or i.suppappliesto[j] == dealer.side or i.suppappliesto[j] == dealer.name or i.suppappliesto[j] in dealer.abilities:
                for k in range(0, len(i.suppgives[j])):
                    if i.suppgives[j][k] in defensive_effects:
                        if "dr" not in i.suppgives[j][k]:
                            supportapplies = True
                            applied.append(i.suppgives[j][k])
        if supportapplies == False:
            blackball.append(i)
        else:
            print(i.name + ": " + str(applied))

    for i in blackball:
        defensive_supports.remove(i)
    if len(defensive_supports) == 0:
        print("none")

    goagain = input("\nWould you like to try a different team? y/n ")
    if goagain.lower() == "y":
        the_big_bunch()
    else:
        quit()

    

def dispatch():
    #simple teambuilding, work on stage filters
    pass

def world_boss():

    for i in c.toons:
        c.namedict[i.name] = i
        if "leader" in i.pos:
            c.leaders.append(i)
        if "support" in i.pos:
            c.supports.append(i)


    class Bosses:
        def __init__(self, bossside, bossallies, bossgender, bosstype, difficulty):
            self.bossside = bossside
            self.bossallies = bossallies
            self.bossgender = bossgender
            self.bosstype = bosstype
            self.difficulty = difficulty

    def enterBoss():
        global boss
        print("\n\nBosses:\nProxima Midnight, Black Dwarf, Corvus Glaive, Supergiant, Ebony Maw, Thanos,\nQuicksilver, Cable, Scarlet Witch, Apocalypse,\nKnull, Mephisto, Infinity Ultron, Gorr, Dark Phoenix, Kang, Black Swan")
        boss = input("\nWhich boss are you fighting? \n(Type the name EXACTLY as listed above and press enter) ")
        BossProxima = Bosses("villain", "alien", "female", "universal", "ultimate")
        BossBlack_Dwarf = Bosses("villain", "alien", "male", "universal", "ultimate")
        BossCorvus = Bosses("villain", "alien", "male", "universal", "ultimate")
        BossSupergiant = Bosses("villain", "alien", "female", "universal", "ultimate")
        BossEbony = Bosses("villain", "alien", "male", "universal", "ultimate")
        BossThanos = Bosses("villain", "alien", "male", "universal", "ultimate")
        BossQuicksilver = Bosses("hero", "other", "male", "speed", "ultimate")
        BossCable = Bosses("hero", "mutant", "male", "blast", "ultimate")
        BossScarlet = Bosses("hero", "other", "female", "blast", "ultimate")
        BossApocalypse = Bosses("villain", "mutant", "male", "combat", "ultimate")
        BossKnull = Bosses("villain", "alien", "male", "universal", "legend")
        BossMephisto = Bosses("villain", "other", "male", "blast", "legend")
        BossUltron = Bosses("villain", "other", "male", "universal", "legend")
        BossGorr = Bosses("villain", "alien", "male", "universal", "legend")
        BossJean = Bosses("villain", "mutant", "female", "universal", "legend")
        BossKang = Bosses("villain", "human", "male", "universal", "legend")
        BossBlack_Swan = Bosses("villain", "alien", "female", "speed", "legend+")
        boss_list = ["Proxima Midnight", "Black Dwarf", "Corvus Glaive", "Supergiant", "Ebony Maw", "Thanos", "Quicksilver", "Cable", "Scarlet Witch", "Apocalypse", "Knull", "Mephisto", "Infinity Ultron", "Gorr", "Dark Phoenix", "Kang", "Black Swan"]
        if boss.title() == "Proxima Midnight": boss = BossProxima
        elif boss.title() == "Black Dwarf": boss = BossBlack_Dwarf
        elif boss.title() == "Corvus Glaive": boss = BossCorvus
        elif boss.title() == "Supergiant": boss = BossSupergiant
        elif boss.title() == "Ebony Maw": boss = BossEbony
        elif boss.title() == "Thanos": boss = BossThanos
        elif boss.title() == "Quicksilver": boss = BossQuicksilver
        elif boss.title() == "Cable": boss = BossCable
        elif boss.title() == "Scarlet Witch": boss = BossScarlet
        elif boss.title() == "Apocalypse": boss = BossApocalypse
        elif boss.title() == "Knull": boss = BossKnull
        elif boss.title() == "Mephisto": boss = BossMephisto
        elif boss.title() == "Infinity Ultron": boss = BossUltron
        elif boss.title() == "Gorr": boss = BossGorr
        elif boss.title() == "Dark Phoenix": boss = BossJean
        elif boss.title() == "Kang": boss = BossKang
        elif boss.title() == "Black Swan": boss = BossBlack_Swan
        elif boss.title() not in boss_list:
            print("\nThe boss you entered is not on the list. Would you like to try again? ")
            tryagain = input("Y/N ")
            if tryagain == "Y" or "y":
                enterBoss()
            elif tryagain == "N" or "n":
                quit()
    enterBoss()

    #enter the stage, code stage requirements

    #also enter the leader and/or support
    #SORT LISTS INTO GREAT AND GOODISH LEAD/SUPPORTS
    #separate offensive/defensive, lead/support, and delineate good effects from great effects
    def enterDealer():
        global dealer
        print("\nWho is your dealer? Please type in the exact name (Doctor Strange instead of Dr Strange, for example) unless it is something like Sharon Rogers because nobody likes typing in 'Captain America (Sharon Rogers)' but still please type in the character's first and last name in those cases")
        dealer = input("\n")
        if dealer.title() in c.namedict:
            dealer = c.namedict[dealer.title()]
        else:
            print("\n" + dealer + " was not found in the database.")
            dealer = input("\nWould you like to try typing the name in again? Y/N (N will end the program) ")
            if dealer == "n" or dealer == "N":
                quit()
            elif dealer == "y" or dealer == "Y":
                enterDealer()
            elif dealer.title() in c.namedict:
                dealer = c.namedict[dealer.title()]

        if dealer in c.t2s and boss.difficulty == "legend" or dealer in c.t2s and boss.difficulty == "legend+" or dealer in c.t3s and boss.difficulty == "legend+":
            print("\nYour character is not eligible for this gamemode.")
            dealer = input("\nWould you like to try a different character? Y/N (N will end the program) ")
            if dealer == "n" or dealer == "N":
                quit()
            elif dealer == "y" or dealer == "Y":
                enterDealer()

        if dealer == c.Nicepool:
            c.leaders.remove(c.Deadpool)
        if dealer == c.Deadpool:
            synergy = input("\nPlease type 1 for Deadpool (Deadpool & Wolverine) or type 2 for Nicepool (Deadpool & Wolverine) ")
            if synergy == "1":
                dealer = c.Deadpool
                c.leaders.remove(c.Nicepool)
            elif synergy == "2":
                dealer = c.Nicepool
                c.leaders.remove(c.Deadpool)
    enterDealer()

    #leader setup
    offensive_leaders = []
    for i in c.leaders:
        if (boss.difficulty == "legend+" and i in c.t4s) or (boss.difficulty == "legend" and (i in c.t3s or i in c.t4s)) or boss.difficulty == "ultimate":
            for j in range(0, len(i.leadappliesto)):
                if i not in offensive_leaders:
                    if i.leadappliesto[j] == "all allies" or i.leadappliesto[j] == dealer.typing or i.leadappliesto[j] == dealer.gender or i.leadappliesto[j] == dealer.allies or i.leadappliesto[j] == dealer.side or i.leadappliesto[j] == dealer.name:
                        offensive_leaders.append(i)
                    for k in range(0, len(dealer.abilities)):
                        if i.leadappliesto[j] == dealer.abilities[k]:
                            offensive_leaders.append(i)
    defensive_leaders = offensive_leaders.copy()

    print("\n\nLeaders that provide offensive buffs are: ")
    blackball = []
    for i in offensive_leaders:
        leadapplies = False
        applied = []
        for j in range(0, len(i.leadappliesto)):
            if i.leadappliesto[j] == "all allies" or i.leadappliesto[j] == dealer.typing or i.leadappliesto[j] == dealer.gender or i.leadappliesto[j] == dealer.allies or i.leadappliesto[j] == dealer.side or i.leadappliesto[j] == dealer.name or i.leadappliesto[j] in dealer.abilities:
                for k in range(0, len(i.leadgives[j])):
                    if i.leadgives[j][k] in offensive_effects or (dealer == c.Hulk and i.leadgives[j][k] == "hp") or (dealer == c.Victorius and i.leadgives[j][k] == "hp"):
                        if i.leadgives[j][k] in damage_types:
                            if i.leadgives[j][k] == dealer.dmg_main:
                                leadapplies = True
                                applied.append(i.leadgives[j][k])
                        elif i.leadgives[j][k] == "all elem":
                            if dealer.dmg_elem != "none":
                                leadapplies = True
                                applied.append(i.leadgives[j][k])
                        elif i.leadgives[j][k] in damage_elem:
                            if i.leadgives[j][k] == dealer.dmg_elem:
                                leadapplies = True
                                applied.append(i.leadgives[j][k])
                            elif i.leadgives[j][k] in dealer.dmg_elem:
                                leadapplies = True
                                applied.append(i.leadgives[j][k])
                        elif i.leadgives[j][k] in damage_targets:
                            if i.leadgives[j][k] == boss.bossside or i.leadgives[j][k] == "damage to boss" or i.leadgives[j][k] == boss.bossgender or i.leadgives[j][k] == boss.bossallies:
                                leadapplies = True
                                applied.append(i.leadgives[j][k])
                        elif i.leadgives[j][k] not in (damage_types or damage_elem or damage_targets):
                            leadapplies = True
                            applied.append(i.leadgives[j][k])
                        elif i.leadgives[j][k] == "damage to %s" % boss.bosstype:
                            leadapplies = True
                            applied.append(i.leadgives[j][k])
        if leadapplies == False:
            blackball.append(i)
        else:
            print(i.name + ": " + str(applied))
    for i in blackball:
        offensive_leaders.remove(i)
    if len(offensive_leaders) == 0:
        print("none")

    blackball = []       
    print("\nLeaders that provide defensive buffs are: ")
    for i in defensive_leaders:
        leadapplies = False
        applied = []
        for j in range(0, len(i.leadappliesto)):
            if i.leadappliesto[j] == "all allies" or i.leadappliesto[j] == dealer.typing or i.leadappliesto[j] == dealer.gender or i.leadappliesto[j] == dealer.allies or i.leadappliesto[j] == dealer.side or i.leadappliesto[j] == dealer.name or i.leadappliesto[j] in dealer.abilities:
                for k in range(0, len(i.leadgives[j])):
                    if i.leadgives[j][k] in defensive_effects:
                        if (i.leadgives[j][k] == "dr hero" or i.leadgives[j][k] == "dr villain") and boss.bossside in i.leadgives[j][k]:
                            leadapplies = True
                            applied.append(i.leadgives[j][k])
                        elif i.leadgives[j][k] == "dr %s" % boss.bosstype or i.leadgives[j][k] == "dr %s" % boss.bossgender or i.leadgives[j][k] == "dr %s" % boss.bossallies:
                            leadapplies = True
                            applied.append(i.leadgives[j][k])
                        elif "dr" not in i.leadgives[j][k]:
                            leadapplies = True
                            applied.append(i.leadgives[j][k])
        if leadapplies == False:
            blackball.append(i)
        else:
            print(i.name + ": " + str(applied))
    for i in blackball:
        defensive_leaders.remove(i)
    if len(defensive_leaders) == 0:
        print("none")
            
    #support setup
    offensive_supports = []
    for i in c.supports:
        if (boss.difficulty == "legend+" and i in c.t4s) or (boss.difficulty == "legend" and (i in c.t3s or i in c.t4s)) or boss.difficulty == "ultimate":
            for j in range(0, len(i.suppappliesto)):
                if i not in offensive_supports:
                    if i.suppappliesto[j] == "all allies" or i.suppappliesto[j] == dealer.typing or i.suppappliesto[j] == dealer.gender or i.suppappliesto[j] == dealer.allies or i.suppappliesto[j] == dealer.side or i.suppappliesto[j] == dealer.name:
                        offensive_supports.append(i)
                    for k in range(0, len(dealer.abilities)):
                        if i.suppappliesto[j] == dealer.abilities[k]:
                            offensive_supports.append(i)
    defensive_supports = offensive_supports.copy()

    blackball = []
    print("\n\nSupport characters that provide offensive buffs are: ")
    for i in offensive_supports:
        supportapplies = False
        applied = []
        for j in range(0, len(i.suppappliesto)):
            if i.suppappliesto[j] == "all allies" or i.suppappliesto[j] == dealer.typing or i.suppappliesto[j] == dealer.gender or i.suppappliesto[j] == dealer.allies or i.suppappliesto[j] == dealer.side or i.suppappliesto[j] == dealer.name or i.suppappliesto[j] in dealer.abilities:
                for k in range(0, len(i.suppgives[j])):
                    if i.suppgives[j][k] in offensive_effects or (dealer == c.Hulk and i.suppgives[j][k] == "hp") or (dealer == c.Victorius and i.suppgives[j][k] == "hp"):
                        if i.suppgives[j][k] in damage_types:
                            if i.suppgives[j][k] == dealer.dmg_main:
                                supportapplies = True
                                applied.append(i.suppgives[j][k])
                        elif i.suppgives[j][k] == "all elem":
                            if dealer.dmg_elem != "none":
                                supportapplies = True
                                applied.append(i.suppgives[j][k])
                        elif i.suppgives[j][k] in damage_elem:
                            if i.suppgives[j][k] == dealer.dmg_elem:
                                supportapplies = True
                                applied.append(i.suppgives[j][k])
                            elif i.suppgives[j][k] in dealer.dmg_elem:
                                supportapplies = True
                                applied.append(i.suppgives[j][k])
                        elif i.suppgives[j][k] in damage_targets:
                            if i.suppgives[j][k] == boss.bossside or i.suppgives[j][k] == "damage to boss" or i.suppgives[j][k] == boss.bossgender or i.suppgives[j][k] == boss.bossallies:
                                supportapplies = True
                                applied.append(i.suppgives[j][k])
                        elif i.suppgives[j][k] not in (damage_types or damage_elem or damage_targets):
                            supportapplies = True
                            applied.append(i.suppgives[j][k])
                        elif i.suppgives[j][k] == "damage to %s" % boss.bosstype:
                            supportapplies = True
                            applied.append(i.suppgives[j][k])
        if supportapplies == False:
            blackball.append(i)
        else:
            print(i.name + ": " + str(applied))
    for i in blackball:
        offensive_supports.remove(i)
    if len(offensive_supports) == 0:
        print("none")

    blackball = []   
    print("\nSupport characters that provide defensive buffs are: ")
    for i in defensive_supports:
        supportapplies = False
        applied = []
        for j in range(0, len(i.suppappliesto)):
            if i.suppappliesto[j] == "all allies" or i.suppappliesto[j] == dealer.typing or i.suppappliesto[j] == dealer.gender or i.suppappliesto[j] == dealer.allies or i.suppappliesto[j] == dealer.side or i.suppappliesto[j] == dealer.name or i.suppappliesto[j] in dealer.abilities:
                for k in range(0, len(i.suppgives[j])):
                    if i.suppgives[j][k] in defensive_effects:
                        if (i.suppgives[j][k] == "dr hero" or i.suppgives[j][k] == "dr villain") and boss.bossside in i.suppgives[j][k]:
                            supportapplies = True
                            applied.append(i.suppgives[j][k])
                        elif i.suppgives[j][k] == "dr %s" % boss.bosstype or i.suppgives[j][k] == "dr %s" % boss.bossgender or i.suppgives[j][k] == "dr %s" % boss.bossallies:
                            supportapplies = True
                            applied.append(i.suppgives[j][k])
                        elif "dr" not in i.suppgives[j][k]:
                            supportapplies = True
                            applied.append(i.suppgives[j][k])
        if supportapplies == False:
            blackball.append(i)
        else:
            print(i.name + ": " + str(applied))

    for i in blackball:
        defensive_supports.remove(i)
    if len(defensive_supports) == 0:
        print("none")

    goagain = input("\nWould you like to try a different team? y/n ")
    if goagain.lower() == "y":
        world_boss()
    else:
        quit()


def shadowland():
    #this will be a lot of work, input all 35 stages + enemies for each option, only 1 character is needed, recommended typing should be an option
    pass

def alliance_battle():
    #each day has different restrictions, account for that
    pass

if gamemode == "the big bunch":
   the_big_bunch()
##elif gamemode == "dispatch mission":
##    dispatch()
elif gamemode == "world boss":
   world_boss()
##elif gamemode == "shadowland":
##    shadowland()
##elif gamemode == "alliance battle":
##    alliance_battle()
##else:
##    pass

