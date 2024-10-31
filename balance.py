import json
from jsonic import serialize, deserialize
import os
import random
import string

class Player:
    name = "None"
    hp = "0"
    dpt = "0" #damage per turn

class NPC:
    name = "None"
    hp = "0"
    dpt = "0"
    count = "0"

#commented out code blow only used to generate sample json of player script
'''
player1 = Player()
player1.name = "Name1"
player1.hp = "0"
player1.dpt = "0" #damage per turn

json_str = serialize(player1, string_output = True)

print(json_str)

#save as file
with open('example_player.json', 'w') as out_file:
    out_file.write(json_str)
'''

#for each sub-folder that does not contain .csv file
import os
rootdir = os.getcwd()

for subdir,dirs,files in os.walk(rootdir):
    #if not in root directory
    if "balance.py" not in files:
        
        csv_exist = False

        for file in files:
            if ".csv" in file:
                csv_exist = True   
        if (csv_exist == False) and ("NPCs" not in subdir):
            #pp = player power
            pp = [0,0] #hp, dpt
            #np = npc power
            np = [0,0] #hp, dpt
            for file in files:
                if (".json" in file):
                    if ("_player" in file):
                        with open(os.path.join(subdir, file),"r") as X:
                            json_str= X.read()

                            P = deserialize(json_str,string_input=True)

                            pp[0] += float(P.hp)
                            pp[1] += float(P.dpt)
                        

                    else:
                        
                        with open(os.path.join(subdir, file),"r") as X:
                            json_str= X.read()

                            N = deserialize(json_str,string_input=True)

                            np[0] += float(N.hp)*float(N.count)
                            np[1] += float(N.dpt)*float(N.count)


            #now for specific encounter initial balance was created

            print("Balancing encounter:"+subdir)
            print("Current balance is:")
            print("player total hp = "+str(pp[0]))
            print("player total dpt = "+str(pp[1]))
            print("NPCs total hp = "+str(np[0]))
            print("NPCs total dpt = "+str(np[1]))

            #TODO implement balancing options
                # turns to wipe (player hp vs npc dpt and reverse)
                # equal hp, equal dpt

            #parameters for balancing script

            # balance above 1 means monsters will have an edge, below 1 players will
            balance = 0.8
            #number of monsters to add
            nom = 5

            #TODO implement scenarios 
                #boss + minions
                #equal minions
                #random power levels (mix)

            # for now simply divide the remaining hp and dpt by (nom-monster_count) -- those are remaining monsters
            n_add = NPC()
            char_set = string.ascii_uppercase
            n_add.name = "".join(random.sample(char_set*6, 3))
            #Will be rounding to integers, so balancing not perfect, but better than fractions of hp
            n_add.hp = int((pp[0]*balance-np[0])/5)
            n_add.dpt = int((pp[1]*balance-np[1])/5) #damage per turn
            n_add.count = nom

            #save as file
            json_str = serialize(n_add, string_output = True)
            with open(subdir+"\\NPC_"+n_add.name+"_"+str(n_add.count)+".json", 'w') as out_file:
                out_file.write(json_str)

            #create a csv listing all mosnters and players
            with open(subdir+"\\balanced.csv", "w") as my_empty_csv:
            # now you have an empty file already
                #TODO check if required, might be practical to have a list
                pass  # or write something to it already