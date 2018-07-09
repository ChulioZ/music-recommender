import os
from os.path import abspath, dirname


PARS = ['loudness', 'hotttnesss', 'tempo', 'timeSig', 'songkey', 'mode']
CHOSEN_PARS_CLUSTER = ['loudness', 'tempo', 'timeSig', 'songkey', 'mode']
CHOSEN_PARS_RF = ['hotttnesss', 'timeSig', 'songkey', 'mode']
CP = ['timeSig', 'songkey', 'mode']
NCP = ['loudness', 'hotttnesss', 'tempo']
METHODS = ['get_loudness', 'get_song_hotttnesss',
           'get_tempo', 'get_time_signature', 'get_key', 'get_mode']

FILE_PATH = dirname(dirname(dirname(abspath(__file__))))
INITIAL_OUTPUT_FILE_PATH = FILE_PATH + '/test_data.txt'
MSD_DATA_PATH = os.path.join(FILE_PATH, 'msd', 'data')
MSD_DATA_FILE_PATH = FILE_PATH + '/msd_data.txt'
MSD_DATA_LABELED_FILE_PATH = FILE_PATH + '/msd_data_labeled.txt'
MSD_DATA_LABELED_PART_FILE_PATH = FILE_PATH + '/msd_data_labeled{}.txt'
USER_SONG_LISTEN_NUMBERS_FILE_PATH = FILE_PATH + \
    '/user_song_listen_numbers.txt'
SONG_LIST_FILE_PATH = FILE_PATH + '/song_list.txt'
RF_TEST_FILE_PATH = FILE_PATH + '/rf_test_results.txt'

WELCOMESTRING = '<font size="30">Welcome to the Music Recommender System!</font><br/><br/><br/> \
    To have the system make a recommendation for you, please visit <strong>http://127.0.0.1:5000/mrs</strong>.<br/> \
    You can specify the following parameters there after a "?" (They\'re all optional):<br/><br/> \
    <strong>rf</strong>: If you want to use Random Forest to calculate your recommendation, \
    enter rf=True. On default, kmeans++ clustering is used instead.<br/> \
    <strong>recamount</strong>: The amount of songs you want the system to recommend. Default is 10.<br/> \
    <strong>ent</strong>: The songs you want to enter into the Music Recommender System. You can specify as many as you like.<br/> \
    Start with ent1=(first song id), then ent2=(second song id) and so on.<br/> \
    Note that if you want to do a Random Forest recommendation, you have to enter at least one song that is eligible for a Random Forest recommendation.<br/> \
    To find out which songs are, do a song search as described below.<br/> \
    If you don\'t enter any songs, the system will randomly choose songs itself.<br/> \
    <strong>entamount</strong>: The amount of songs you want the system to randomly choose as entered songs.<br/> \
    Only relevant of course as long as you don\'t enter songs yourself.<br/><br/> \
    Example for a working MRS start:<br/><br/> \
    <strong>http://127.0.0.1:5000/mrs?rf=True&recamount=20&ent1=SOSJRJP12A6D4F826F</strong><br/><br/> \
    Depending on your PC, getting a recommendation might take a while, so please be patient.<br/><br/><br/><br/> \
    You can also visit <strong>http://127.0.0.1:5000/songs</strong> to get a list of all songs that meet specific seach criteria. There, the parameters to specify are:<br/><br/> \
    <strong>artist</strong>: artist of the song<br/> \
    <strong>title</strong>: title of the song<br/> \
    <strong>id</strong>: id of the song<br/> \
    <strong>elig</strong>: Random Forest eligibility of the song; elig=True if you want songs that are eligible for Random Forest recommendations, False otherwise.<br/><br/> \
    Example for a working song search:<br/><br/> \
    <strong>http://127.0.0.1:5000/songs?artist=Arctic Monkeys&elig=True</strong><br/><br/> \
    Have fun using the system and listening to the recommended songs!'

LIMIT_LIST = [8, 13]