from playwright.sync_api import sync_playwright
from playwright._impl._page import Page
import tarfile
import time, os, shutil

def click_and_wait(page:Page, click_sel:str, wait_sel:str=None):
    ''' execute: click selector and wait for loading of page or selector.
        click_sel := selector string for click
        wait_sel := None or selector string for wait'''
    page.query_selector(click_sel).click()
    if wait_sel: page.wait_for_selector(wait_sel)
    else: page.wait_for_load_state()  


class Setting:
    def __init__(self, EM:str, PW:str, WD:str, DD:str):
        ''' set: account and directory info and make directories, 
            EM: charmm-gui account e-mail,
            PW: charmm-gui account password,
            WD: working directory, 
            DD: download directory for raw files'''
        self.email = EM
        self.password = PW
        self.dirs = {   'working_dir':WD,
                        'download_dir':DD}
        for dir_ in self.dirs:
            if not os.path.isdir(self.dirs[dir_]): os.mkdir(self.dirs[dir_])


class CharmmGUI:
    def __init__(self, setting:Setting, debug=False):
        ''' Set: account & dir through Setting obj, and open & login ligandrm
                page of charmm-gui.org using playwright api. If a user has 
                already logged in, self.login() method will be ignored.'''
        self.setting = setting
        playwright = sync_playwright().start()
        context = playwright.chromium.launch_persistent_context(
                                self.setting.dirs['working_dir'], 
                                headless=not debug, channel='chrome')
        self.page = context.new_page()
        self.page.goto('https://www.charmm-gui.org/?doc=input/ligandrm')
        if self.page.query_selector('[id="title"]').inner_text() == \
            'User Account Login': self.login()

    def login(self):
        ''' Login at ligandrm page of charmm-gui.org. If user license agreement
            page appear, this method will automatically set to agree.'''
        self.page.fill('[placeholder="Email"]', self.setting.email)
        self.page.fill('[placeholder="Password"]', self.setting.password)
        click_and_wait(self.page, '[type="submit"]')
        if self.page.query_selector('[id="title"]').inner_text() == \
            'User License Agreement':
            print('User License Agreement')
            for sel in self.page.query_selector_all('[type="checkbox"]'):
                sel.click()
            click_and_wait(self.page, '[id="tos_confirm_button"]')

    def logout(self):
        ''' If logout button exists, it will be cilcked'''
        if self.page.query_selector(
            '[onclick="window.location.href=\'./?doc=sign&do=logout\'"]'):
            click_and_wait(self.page, 
                '[onclick="window.location.href=\'./?doc=sign&do=logout\'"]')

    def run_ligandrm_using_smiles(self, smiles:str, lig_name:str, send_to:str=None):
        ''' Send: smiles string and custom ligand name to ligandrm @ charmm-gui.org.
                In the ligand selection page, the option on the top will be chosen.
                (Generally, "Make CGenFF topology" @ "Exact". If a ligand already
                exist in CHARMM toppar, ligand name will be changed according to it.)
                raw files will be downloaded at download_dir.
            smiles := isomeric(preferred)/canonical smiles,
            lig_name := ligand name (3~6 letters), It will be automatically modified 
                when fully matched CHARMM toppar occurs.
            send_to := send psf, prm, pdb files to this dir, default: download_dir'''
        if send_to is None: send_to = self.setting.dirs['download_dir']
        #first step
        while True:
            if self.page.query_selector('[id="title"]').inner_text() == \
                'Ligand Reader & Modeler': break
            else: continue
        self.page.wait_for_load_state()
        self.page.fill('[id="smilesField"]', smiles)
        self.page.query_selector('[value="Load SMILES"]').click()
        time.sleep(2)
        click_and_wait(self.page, '[id="nextBtn"]', '[class="jobid"]')
        #second step
        print(  '=======================\n',
                jobid := self.page.query_selector('[class="jobid"]').inner_text(),
                '\n Ligand name:', lig_name)
        jobid = jobid.split(':')[-1].strip()
        (resi_sele := self.page.query_selector_all('[id="resi_sele"]')[0]).click()
        if (cgenname := self.page.query_selector_all('[id="cgenname"]')):
            cgenname[0].fill(lig_name)
        else: 
            print('set lig_name to:', lig_name := resi_sele.get_attribute('value'))
            prm_origin = resi_sele.query_selector('//../..'
                                ).query_selector_all('//child::td')[3].inner_text()
        click_and_wait(self.page, '[id="nextBtn"]', '[class="download"]')
        #third step
        with self.page.expect_download() as download:
            self.page.query_selector('[class="download"]').click()
            while (progress := self.page.query_selector('[class="download"]')\
                .inner_text()) != 'downloading':
                print(f'{progress:18s}', end='\r')
            print(f'{progress:18s}', end='\r')
        file_name = lig_name + '.tgz'
        file_dir = '/'.join([self.setting.dirs['download_dir'], file_name])
        download.value.save_as(file_dir)
        #file processing
        with tarfile.open(file_dir) as tar: 
            tar.extractall(self.setting.dirs['download_dir'])
        extracted_dir = self.setting.dirs['download_dir'] + '/charmm-gui-' + jobid
        files_to = {
            extracted_dir + '/ligandrm.pdb':'/'.join([send_to, lig_name + '.pdb']),
            extracted_dir + '/ligandrm.psf':'/'.join([send_to, lig_name + '.psf'])}
        if not os.path.isfile(prm   := extracted_dir + '/toppar/' 
                                    + lig_name.lower() + '.prm'):
            prm = extracted_dir + '/toppar/' + prm_origin
        files_to[prm] = '/'.join([send_to, lig_name.lower() + '.prm'])
        for file in files_to: shutil.copy(file, files_to[file])
        self.page.goto('https://www.charmm-gui.org/?doc=input/ligandrm')
        print('Files were sent to :', send_to)