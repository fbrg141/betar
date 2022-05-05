from fuzzywuzzy import fuzz
import numpy as np
from datetime import datetime


def make_dct(odds, lenght, match, dct):

    #function used for making dictionary from match objects

    if len(odds) == lenght:
        dct[
                str(
                    match.get_teams_str() + "-" + str(match.get_bet()) + "*" + str(match.get_time())
                )
            ] = odds
        

def fuzz_match(s1, t1, s2, t2):
    
    #string are made as uniform as possible but there is not any standar 
    #among betting sites so for matching we used fuzzywuzzy library
    #based on Levenshtein distance
    
    if len(s1.split(" ")) < 2 or len(s2.split(" ")) < 2:
        return False
    h1 = s1.split(" ")[0]
    h2 = s1.split(" ")[1].split("-")[0]
    a1 = s2.split(" ")[0]
    a2 = s2.split(" ")[1].split("-")[0]
    if fuzz.partial_ratio(h1, a1) > 50 and fuzz.partial_ratio(h2, a2) > 60: 
        if t1 == t2:
            return True
    else:
        return False
    #THIS FUNCTION SHOULD BE BETTER BECAUSE SOME MATCHES ARE NOT MATCHED
    #IT IS BECAUSE THERE IS NOT STANDARDS FOR NAMING TEAMS


def list_separator(dct):
    l
    #function used for separating dictionary into list of lists
    #for easier calculation of arb
      
    list_of_list_of_pairs = []
    l1 = []
    tmp = sorted(dct.items())[0]

    #first we sort our big list of pairs by names of teams
    #target is to make list of lists where smaler list contains
    #same matches but from different bookmakers

    for d in sorted(dct.items()):

        #going trough dictionary and populating l1 list with same matches
        #from different bookmakers

        teams = d[0].split("-")[0]
        time = datetime.strptime(d[0].split("-")[1].split("*")[1], "%d/%m/%Y %H:%M")
        teams_tmp = tmp[0].split("-")[0]
        time_tmp = datetime.strptime(
            tmp[0].split("-")[1].split("*")[1], "%d/%m/%Y %H:%M"
        )

        if fuzz_match(teams, time, teams_tmp, time_tmp):
            l1.append(d)

            #we use team name and time to check if we have same match
            #if matches are same we add it to l1 list

        elif len(l1) == 1:
            l1 = []
            l1.append(d)
        else:
            
            #whe we have different match we add l1 list to list of lists
            #and empty l1 list, for new match

            list_of_list_of_pairs.append(l1)
            l1 = []
            l1.append(d)
        tmp = d
    return list_of_list_of_pairs


def find_max_od_2(list_of_list_of_pairs):

    #function used for finding max odds from small list 

    max_od_list = []
    bet_list = []
    for list_of_pairs in list_of_list_of_pairs:
        if len(list_of_pairs) == 1:
            continue

        bet_index_02 = list((map(lambda x: x[0], list_of_pairs)))[
            np.argmax((list(map(lambda x: x[1], list_of_pairs))), axis=0)[0]
        ]

        bet_index_3 = list((map(lambda x: x[0], list_of_pairs)))[
            np.argmax((list(map(lambda x: x[1], list_of_pairs))), axis=0)[1]
        ]

        for l in list_of_pairs:
            if l[0] == bet_index_02:
                max_od_02 = l[1][0]
            if l[0] == bet_index_3:
                max_od_3 = l[1][1]

        bet_list.append(
            [
                bet_index_02.split("-")[1].split("*")[0],
                bet_index_3.split("-")[1].split("*")[0],
            ]
        )
        max_od_list.append([max_od_02, max_od_3])
    return bet_list, max_od_list


def find_max_od_3(list_of_list_of_pairs):

    #same as above function but for 3 odds

    max_od_list = []
    bet_list = []
    for list_of_pairs in list_of_list_of_pairs:
        if len(list_of_pairs) == 1:
            continue
        bet_index_1 = list((map(lambda x: x[0], list_of_pairs)))[
            np.argmax((list(map(lambda x: x[1], list_of_pairs))), axis=0)[0]
        ]

        bet_index_x = list((map(lambda x: x[0], list_of_pairs)))[
            np.argmax((list(map(lambda x: x[1], list_of_pairs))), axis=0)[1]
        ]

        bet_index_2 = list((map(lambda x: x[0], list_of_pairs)))[
            np.argmax((list(map(lambda x: x[1], list_of_pairs))), axis=0)[2]
        ]
        for l in list_of_pairs:
            if l[0] == bet_index_1:
                max_od_1 = l[1][0]
            if l[0] == bet_index_x:
                max_od_x = l[1][1]
            if l[0] == bet_index_2:
                max_od_2 = l[1][2]
        bet_list.append(
            [
                bet_index_1.split("-")[1].split("*")[0],
                bet_index_x.split("-")[1].split("*")[0],
                bet_index_2.split("-")[1].split("*")[0],
            ]
        )
        max_od_list.append([max_od_1, max_od_x, max_od_2])
    return bet_list, max_od_list


def arb_calculator(od, invest):

    #function used for calculating arbitrage profite

    od = list(map(lambda x: float(x), od))
    if 0 in od:
        return 0, 0
    arb_ind = list(map(lambda x: (1 / x) * 100, od))
    arb = sum(arb_ind)
    if arb >= 100:
        return [0, 0, 0], -1
    profit = invest / (arb / 100) - invest
    bet_ind = list(map(lambda x: round(invest * (x / 100) / (arb / 100)), arb_ind))
    return bet_ind, profit


def print_profit2(dct, str1, str2):

    #printing arbitrage profit (if higher than 0) in readable format

    lolop = list_separator(dct)
    bet_list, max_od_list = find_max_od_2(lolop)

    for i in range(len(lolop)):
        bet_ind, profit = arb_calculator(max_od_list[i], 100)
        if profit < 0:
             continue
        print("_____________________")
        print(*lolop[i], sep='\n')
        print(
            lolop[i][0][0].split("-")[0].upper(), lolop[i][0][0].split("*")[1]
        )
        print("---")
        print(
            "{:<20} {:>5} {:>5}".format(
                bet_list[i][0], str1, max_od_list[i][0], bet_ind[0]
            )
        )
        print(
            "{:<20} {:>5} {:>5}".format(
                bet_list[i][1], str2, max_od_list[i][1], bet_ind[1]
            )
        )
        print("---")
        print(profit)
        print("_____________________")

def print_profit3(dct, str1, str2, str3):

    #with 3 odds

    lolop = list_separator(dct)
    bet_list, max_od_list = find_max_od_3(lolop)
    print(len(bet_list), len(lolop))
    for i in range(len(bet_list)):
        bet_ind, profit = arb_calculator(max_od_list[i], 100)
        if profit < 0:
            continue
        print("_____________________")
        print(*lolop[i], sep="\n")
        print(
            lolop[i][0][0].split("-")[0].upper(), lolop[i][0][0].split("*")[1]
        )
        print("---")
        print(
            "{:<20} {:>5} {:>5}".format(
                bet_list[i][0], str1, max_od_list[i][0], bet_ind[0]
            )
        )
        print(
            "{:<20} {:>5} {:>5}".format(
                bet_list[i][1], str2, max_od_list[i][1], bet_ind[1]
            )
        )
        print(
            "{:<20} {:>5} {:>5}".format(
                bet_list[i][2], str3, max_od_list[i][2], bet_ind[2]
            )
        )
        print("---")
        print(profit)
        print("_____________________")
    