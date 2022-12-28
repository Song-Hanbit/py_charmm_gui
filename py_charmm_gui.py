from main.charmm_gui.charmm_gui import CharmmGUI, Setting
from main.charmm_gui import account
import json
import argparse

parser = argparse.ArgumentParser(description=
                'Download psf, pdb, prm files from charmm-gui.org.\
                    Either -s & -l options or -j option must pass.\
                    Files will be sent to -st option if -st option\
                    passed or they will be sent to download dir.\
                    -r option will reset account history.')
parser.add_argument('-s', '--smiles', dest='smiles', help=
                'isomeric(preferred)/canonical smiles string')
parser.add_argument('-l', '--ligand', dest='ligand', help=
                'ligand name (3~6 letters)')
parser.add_argument('-j', '--json', dest='json', help=
                'json file which is a dict of {ligand_name:smiles}')              
parser.add_argument('-st', '--sendto', dest='sendto', help=
                'send files to this dir (default: download dir)')
parser.add_argument('-r', '--reset', default=False, dest='r',
                    action='store_true', help='reset account history')
args = parser.parse_args()

if args.r: account.set_account()
account_set = account.load_account()
setting = Setting(  account_set['email'],
                    account_set['password'],
                    account_set['working_dir'],
                    account_set['download_dir'])
cg = CharmmGUI(setting)
if args.smiles and args.ligand:
    if args.json: 
        raise RuntimeError('3 options must not pass at the same time')
    cg.run_ligandrm_using_smiles(   args.smiles, args.ligand, 
                                    args.sendto)
elif args.json:
    with open(args.json, 'r') as file: j = json.load(file)
    for ligand_name in j:
        cg.run_ligandrm_using_smiles(   j[ligand_name], 
                                        ligand_name, args.sendto)
elif args.r: print('Account info reset')
else:
    raise RuntimeError('Either -s & -l options or -j option must pass')

exit()