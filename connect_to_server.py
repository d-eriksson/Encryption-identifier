from BackupConnector import BackupConnector
from HiddenConfig import HiddenConfig
from create_RSA import create_RSA, RSA_toString
import tensorflow as tf
from ML import (prepare_data,
                train_model,
                load_latest_model,
                is_encrypted,
                print_fig)

from kivy.app import App
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.settings import SettingsWithTabbedPanel

from settings import (settings_backup,settings_ML)
# importing the requests library 
import requests 

URL = "http://localhost:5000/"

Builder.load_string('''
<Interface>:
    rows:3
    id: layout
    FloatLayout:
        Button:
            text: 'Settings'
            font_size: 15
            on_release: app.open_settings()
            size: 75, 50
            size_hint: None, None
            right:layout.right-10
            top: layout.top-10
    FloatLayout:
        Button:
            text: 'Restore'
            font_size: 15
            on_release: app.restore()
            size: 75, 50
            size_hint: None, None
            center: layout.right/3, 50
            
    FloatLayout:
        Button:
            text: 'Backup'
            font_size: 15
            on_release: app.backup()
            size: 75, 50
            size_hint: None, None
            center: layout.right/3*2, 50
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        Label:
            text:"SOME TEXT GOES HERE"
''')

class Interface(AnchorLayout):
    pass   

class BackupApp(App):

    def build(self):
        self.settings_cls = SettingsWithTabbedPanel
        self.use_kivy_settings = False
        rootpath = self.config.get('backup', 'rootpath')
        self.load()
        self.hiddenConfig = HiddenConfig("hidden.ini")
        self.id = self.hiddenConfig.get_parameter("id")
        if not self.id:
            self.id = self.hiddenConfig.set_parameter("id", "1234")
        self.keyPath = self.hiddenConfig.get_parameter("key_path")
        if not self.keyPath:
            self.keyPath = self.hiddenConfig.set_parameter("key_path", create_RSA())
            PARAMS = {'id':self.id, 'key':RSA_toString()} 
            r = requests.post(url = URL, params = PARAMS) 
            data = r.json()
            print(data.status)
        PARAMS = {'id': self.id}
        print(URL+"StartServer")
        try: 
            r = requests.post(url = URL+ "StartServer", params = PARAMS,timeout=0.0000000001)
        except requests.exceptions.ReadTimeout: 
            pass
        print("hej")
    
        self.bc = BackupConnector(self.keyPath,rootpath, self.model)
        
        return Interface()

    def build_config(self, config):
        config.setdefaults('backup', {
            'rootpath': './ClientRoot'})
        config.setdefaults('ML', {
            'test_dir': './Test'})
        config.setdefaults('ML', {
            'training_dir': './Training'})
        config.setdefaults('ML', {
            'og_dir': './OriginalFiles'})

    def build_settings(self, settings):
        settings.add_json_panel('Backup',
                                self.config,
                                data=settings_backup)
        settings.add_json_panel('ML',
                                self.config,
                                data=settings_ML)
                                

    def on_config_change(self, config, section,
                         key, value):
        print (config, section, key, value)
    def backup(self):
        print('Initialize backup')
        self.bc.backup_to_server()
    def restore(self):
        print('Initialize restore')
        self.bc.revert_from_backup()
    def train(self):
        activationLayers = ["hard_sigmoid","sigmoid","sigmoid","sigmoid"]
        opti = 'RMSprop' # Best Performance
        lss = tf.keras.losses.BinaryCrossentropy() # Best Performance
        layers = [64,8,8,1]
        self.model = train_model(layers,activationLayers,opti,lss)
        self.bc.model = self.model
    def load(self):
        self.model = load_latest_model()


if __name__ == '__main__':
    BackupApp().run()