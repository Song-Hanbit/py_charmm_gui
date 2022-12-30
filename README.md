# py_charmm_gui
Download psf, pdb and CHARMM parameter files from ligandrm of charmm-gui.org with Python.

## Dependency
Playwright (tested version: 1.29.0) for Python

## Structure of package

    ~/py_charmm_gui$ tree -L 3
    .
    ├── __init__.py
    ├── download
    ├── input.json
    ├── ipy_charmm_gui.py
    ├── main
    │   ├── __init__.py
    │   └── charmm_gui
    │       ├── __init__.py
    │       ├── account.py
    │       └── charmm_gui.py
    ├── py_charmm_gui.py
    └── test.py
    
## Usage
py_charmm_gui.py may directly executed at terminal

    ### example 1 ###
    $ python3 (your pkg dir)/py_charmm_gui.py -r -j (json file) -st (download dir)
    ### example 2 ###
    $ python3 (your pkg dir)/py_charmm_gui.py -l ETOH -s CCO
    ### example 3 ###
    $ python3 (your pkg dir)/py_charmm_gui.py -l ACR -s "CC(=O)OCC[N+](C)(C)C"
    
or ipy_charmm_gui.py may imported and executed line by line at ipython.

    from (your pkg dir) import ipy_charmm_gui
    ipy_charmm_gui.reset_account()
    ipy_charmm_gui.make_json_and_run_ligandrm({ "DZN": "C1=CC(=CC=C1C2=COC3=C(C2=O)C=CC(=C3)O)O", 
                                                "ETOH": "CCO"}, send_to=(download dir))
                                                
Top option at the "Search ligand" step will be automatically selected (generally, "Make CGenFF topology" @ "Exact").

## References:
* Charmm-gui ligand reader & modeller:  https://www.charmm-gui.org/?doc=input/ligandrm
* S. Jo, T. Kim, V.G. Iyer, and W. Im (2008) CHARMM-GUI: A Web-based Graphical User Interface for CHARMM.:
   J. Comput. Chem. 29:1859-1865
* S. Kim, J. Lee, S. Jo, C.L. Brooks III, H.S. Lee, and W. Im (2017) CHARMM-GUI Ligand Reader and Modeler for CHARMM Force Field Generation of Small Molecules.:
   J. Comput. Chem. 38:1879-1886
