#functions used for formatting string because we want strings to be uniform
#as possible

def team_fmt(team):
    team = (
        team.replace(" ", "")
        .replace("\n", "")
        .replace("-", "")
        .replace(".", "")
        .replace("/", "")
        .replace("(", "")
        .replace(")", "")
        .replace("\t", "")
        .replace("\r", "")
        .lower()
    )
    return team

def odds_fmt(odds):

    if odds == None or len(odds) != 2:
        odds = [1,1]
    if odds[0] == 0 or odds[0] == None:
        odds[0] = 1
    if odds[1] == 0 or odds[1] == None:
        odds[1] = 1
    return float(odds)
