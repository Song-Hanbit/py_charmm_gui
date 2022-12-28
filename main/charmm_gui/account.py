import json
import os

cur_dir = '/'.join(__file__.split('/')[:-1])
pkg_dir = '/'.join(__file__.split('/')[:-3])

def set_account():
    ''' Make: history.json that contains charmm-gui.org account e-mail 
        & password and automatically or manually set working & download
        directories by taking infomations from user through input().'''
    yes = ['y', 'yes']
    em = input('Your charmm-gui.org account E-mail:')
    pw = input('Your charmm-gui.org account password:')
    if (auto := input('Automatically set dirs to package? [y/n]'
        ).lower()) in yes:
        wd = pkg_dir
        dd = pkg_dir + '/download'
        if not os.path.isdir(dd): os.mkdir(dd)
    else:
        wd = input('working directory:')
        dd = input('download directory:')
    setting = { 'email':em, 'password':pw, 'working_dir':wd, 
                'download_dir':dd}
    with open(cur_dir + '/history.json', 'w') as file: 
        json.dump(setting, file)

def load_account() -> dict:
    ''' Load: history.json and check it. If some field is missing 
        set_account() will be executed and return None, else a dict
        that contains user informations will be returned.'''
    if not os.path.isfile(json_file := cur_dir + '/history.json'): 
        set_account()
    with open(json_file, 'r') as file: setting = json.load(file)
    setting_keys = ['email', 'password', 'working_dir', 'download_dir']
    missing = False
    for key in setting_keys:
        if key not in setting:
            set_account()
            missing = True
            break
        if not setting[key]:
            set_account()
            missing = True
            break
    if missing:
        print('please reload')
        return None
    else: return setting
    