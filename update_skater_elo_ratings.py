try:
    from timemachines.skatertools.data.live import random_residual_data, random_elo_data
    from timemachines.skatertools.data.long import random_long_data
except ImportError:
    raise('pip install microprediction')

from pprint import pprint
import json
import os
import random
import time

CAN_BLOW_AWAY = False



ELIMINATE = ['constant_skater','darts_ARIMA_skater','darts_AutoARIMA_skater','darts_FFT_skater',
             'darts_FourTheta_skater','darts_Prophet_skater','darts_ExponentialSmoothing_skater']
AVOID_KEYS = ['evaluator']

ALWAYS_SKATERS = ['tsa_p2_d0_q1','quick_aggressive_ema_ensemble','thinking_slow_and_fast']


def ensure_ratings_are_clean(d, index_key='name', avoid_keys=None):
    """ Eliminate duplicate entries, and cleans out crud """
    if avoid_keys is None:
        avoid_keys = AVOID_KEYS
    kys = d.keys()
    unique_kys = set()
    valid = list()
    from copy import deepcopy
    d_copy = deepcopy(d)
    for j,ky in enumerate(d[index_key]):
        if ky not in unique_kys and not any([ elim in ky for elim in ELIMINATE]):
            valid.append(j)
            unique_kys.add(ky)
    for ky in kys:
        if ky not in avoid_keys:
            try:
                d[ky] = [d_copy[ky][v] for v in valid]
            except IndexError:
                pass
                raise ValueError('Ratings were corrupted, somehow')
    return d

import random


def update_skater_elo_ratings_for_five_minutes_or_more(max_min=5, max_count=10):
    the_start_time = time.time()
    elapsed = 0
    count = 0
    while elapsed<max_min*60 and count<max_count:
        update_skater_elo_ratings_once()
        elapsed = time.time()-the_start_time
        if False:
            print('Elapsed= '+str(elapsed))
        count += 1
        
    print('Done updating Elo ratings')   


def update_skater_elo_ratings_once(regular_data_source=random_elo_data, residual_data_source=random_residual_data, special_data_source=random_long_data):
    from timemachines.skatertools.comparison.skaterelo import skater_elo_multi_update

    category = random.choice(['residual-k_', 'univariate-k_','special-k_','special-k_','special-k_','special-k_','special-k_'])
    if 'residual' in category:
        data_source = residual_data_source
    elif 'special' in category:
        data_source = special_data_source
    else:
        data_source = regular_data_source

    print(category)
    k = random.choice([1,1,1,1,2,2,2,3,3,5,8,13,21,34])
    print('k='+str(k))
    ELO_PATH = os.path.dirname(os.path.realpath(__file__))+os.path.sep+'ratings'
    LEADERBOARD_PATH = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'leaderboards_json'

    try:
        os.makedirs(ELO_PATH)
    except FileExistsError:
        pass
    ELO_FILE = ELO_PATH + os.path.sep + category+str(k).zfill(3)+'.json'

    # Try to resume
    try:
        with open(ELO_FILE,'rt') as fp:
            elo = json.load(fp)
    except:
        if CAN_BLOW_AWAY or 'special' in category:
            elo = {}
        else:
            raise RuntimeError()

    # Dedup
    if True:
        elo = ensure_ratings_are_clean(elo, index_key='name')

    elo = skater_elo_multi_update(elo=elo,k=k,data_source=data_source, always_skaters=ALWAYS_SKATERS)
    if False:
        pprint(sorted(list(zip(elo['rating'],elo['name'])))[-3:])
    print('',flush=True)

    # Try to save
    with open(ELO_FILE, 'wt') as fp:
        json.dump(elo,fp)

    # Write individual files so that the directory serves as a leaderboard
    LEADERBOARD_DIR = LEADERBOARD_PATH +os.path.sep+category+ str(k).zfill(3)
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
    for rating, name, count,active, traceback, pypi, scnds in sorted(list(zip(elo['rating'],elo['name'],elo['count'],elo['active'],elo['traceback'], elo['pypi'], elo['seconds'])),reverse=True):

        SCORE_FILE = LEADERBOARD_DIR + os.path.sep +str(pos).zfill(3)+'-'+str(int(rating)).zfill(4)+'-'+name+'-'+str(count)
        pos+=1
        if not active:
            SCORE_FILE += '_inactive'
        elif len(traceback)>100:
            SCORE_FILE += '_FAILING'
        SCORE_FILE+='.json'
        with open(SCORE_FILE, 'wt') as fp:
            json.dump(obj={'name':name,'pypi':pypi,'seconds':scnds,'traceback':traceback,'rating':rating}, fp=fp)


def running_locally():
    import sys
    print(sys.platform)
    return 'darwin' in sys.platform


if __name__=='__main__':
    if running_locally():
       update_skater_elo_ratings_for_five_minutes_or_more(max_min=100000, max_count=200000000)
    else:
       if False:
          # disabled while ratings are bootstrapped locally (new models included)
          update_skater_elo_ratings_for_five_minutes(max_min=5, max_count=10)
