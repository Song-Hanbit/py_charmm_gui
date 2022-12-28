from .main.charmm_gui.charmm_gui import CharmmGUI, Setting
from .main.charmm_gui import account
import os

acc = account.load_account()
setting = Setting(acc['email'], acc['password'], acc['working_dir'], acc['download_dir'])
cg = CharmmGUI(setting, True)
a = cg.run_ligandrm_using_smiles('CCO', 'ETOH')
a = cg.run_ligandrm_using_smiles('C1=CC(=CC=C1C2=COC3=C(C2=O)C=CC(=C3)O)O', 'DZN')
