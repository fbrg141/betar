import funcs as f
import pickle


#script expexts input.txt to be populated with data of football(or other) matches
#gathered from betting sites in format:
#   -every line is a match (string) which contains:
#       "team1-team2 bet time odd_02:odd_3+ odd_home_win:odd_draw:odd_away_win  

#from every line we make match object, then matches are used to make dictionaries
#   "teams-bet*time":odds
#in this case its not necessary for object aproach, dictionaries could be made directly,
#but for easier understanding and possible further development we use objects

def main(ind):
    
    if(ind):
        with open("input.txt", "r") as input:
            lines = input.readlines()
            matchs = []
            for line in lines:
                match = f.Football(line)
                matchs.append(match)

        with open("tmp_big_list", "wb") as file:
            pickle.dump(big_list, file)
    
    #this part (above) of code is for testing, if back part of the code is to be tested
    #the input.txt file dont need to be updated, so if we call with main(1) that
    #will use  updated input.txt file and serialise it in tmp_big_list if main is
    #called with 0 it wont use updated input.txt

    with open("tmp_big_list", "rb") as file:
        big_list = pickle.load(file)

    dct_3 = {}
    dct_win= {}

    for l in big_list:
        f.make_dct(l.get_win(), 3,  l, dct_win)
        f.make_dct(l.get_g3(), 2, l, dct_3)
        
        #making dictionaries for every game


    f.print_profit3(dct_win, '1:', 'X:', '2:')
    f.print_profit2(dct_3, '3+', '0-2')

    #printing profit if there is one