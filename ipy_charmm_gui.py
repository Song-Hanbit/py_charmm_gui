from .main.charmm_gui import account
import subprocess
import json

pkg_dir = '/'.join(__file__.split('/')[:-1])
account.load_account()

def run_ligandrm_using_smiles(smiles:str, lig_name:str, send_to:str=None):
    ''' Pass: smiles, lig_name and send_to args to py_charmm_gui.py using subprocess package.
        smiles := isomeric(preferred)/canonical smiles,
        lig_name := ligand name (3~6 letters), It will be automatically modified 
            when fully matched CHARMM toppar occurs.
        send_to := send psf, prm, pdb files to this dir, default: download_dir'''
    cmdline = [ 'python3', pkg_dir + '/py_charmm_gui.py', '-s', smiles,
                '-l', lig_name]
    if send_to: cmdline += ['-st', send_to]
    subprocess.run(cmdline)

def make_json_and_run_ligandrm(lig_dict:dict, send_to:str=None):
    ''' Make: input.json at pkg_dir using lig_dict and pass input.json and send_to
            args to py_charmm_gui.py using subprocess package.
        lig_dict := a dict of {ligand_name:smiles}
        send_to := send psf, prm, pdb files to this dir, default: download_dir'''
    with open(pkg_dir + '/input.json', 'w') as file: json.dump(lig_dict, file)
    cmdline = [ 'python3', pkg_dir + '/py_charmm_gui.py', '-j', 
                pkg_dir + '/input.json']
    if send_to: cmdline += ['-st', send_to]
    subprocess.run(cmdline)

def reset_account(): 
    '''Reset (pkg_dir)/main/charmm_gui/history.json'''
    account.set_account()