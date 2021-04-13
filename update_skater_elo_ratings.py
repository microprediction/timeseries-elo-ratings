from timemachines.skatertools.comparison.skaterelo import skater_elo_update
from pprint import pprint
import json
import os
import random
import time

CAN_BLOW_AWAY = False


def update_skater_elo_ratings_for_five_minutes():
    st = time.time()
    while time.time()-st<8*60:
        update_skater_elo_ratings_once()



def update_skater_elo_ratings_once():
    k = random.choice([1,2,3,5,8,13,21,34])
    ELO_PATH = os.path.dirname(os.path.realpath(__file__))+os.path.sep+'ratings'
    LEADERBOARD_PATH = os.path.dirname(os.path.realpath(__file__))+os.path.sep+'leaderboards_json'

    try:
        os.makedirs(ELO_PATH)
    except FileExistsError:
        pass
    ELO_FILE = ELO_PATH + os.path.sep + 'univariate-k_'+str(k).zfill(3)+'.json'

    # Try to resume
    try:
        with open(ELO_FILE,'rt') as fp:
            elo = json.load(fp)
    except:
        if CAN_BLOW_AWAY:
            elo = {}
        else:
            raise RuntimeError()

    # Update elo skater_elo_ratings
    elo = skater_elo_update(elo=elo,k=k)
    pprint(sorted(list(zip(elo['rating'],elo['name']))))

    # Try to save
    with open(ELO_FILE, 'wt') as fp:
        json.dump(elo,fp)

    # Write individual files so that the directory serves as a leaderboard
    LEADERBOARD_DIR = LEADERBOARD_PATH + os.path.sep+'univariate_'+ str(k).zfill(3)
    try:
        os.makedirs(LEADERBOARD_DIR)
    except FileExistsError:
        pass

    # Clean out the old
    import glob
    fileList = glob.glob(LEADERBOARD_DIR+ os.path.sep + '*.json')
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)

    pos = 1
    for rating, name, count,active, traceback in sorted(list(zip(elo['rating'],elo['name'],elo['count'],elo['active'],elo['traceback'])),reverse=True):
        package = name.split('_')[0]
        if package not in ['fbprophet', 'pmdarima', 'pydlm', 'flux', 'divinity']:
            package = 'timemachines'
        SCORE_FILE = LEADERBOARD_DIR + os.path.sep +str(pos).zfill(3)+'-'+str(int(rating)).zfill(4)+'-'+name+'-'+str(count)
        pos+=1
        if not active:
            SCORE_FILE += '_inactive'
        elif len(traceback)>100:
            SCORE_FILE += '_FAILING'
        SCORE_FILE+='.json'
        with open(SCORE_FILE, 'wt') as fp:
            json.dump(obj={'name':name,'package':package,'url':'https://pypi.org/project/'+package,
                           'traceback':traceback}, fp=fp)


if __name__=='__main__':
    update_skater_elo_ratings_for_five_minutes()
