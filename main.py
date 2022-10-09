#!/usr/local/bin/python3.9
import sys			
import random	
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
import webbrowser
from kivy.core.window import Window
import glob       
import time

class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class PassPhraseGeneratorApp(MDApp):
    words_number = StringProperty()   # Absolutely needed to pass self.words_number to kv file
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.info_dialog = None
        self.contact_dialog = None
        # Open file with the name of saved current language dictionary
        self.filename = open("data/currentlanguage")
        self.current_lang = self.filename.readline()
        self.dict_name = "data/dicts/"+self.current_lang.strip()
        self.filename.close()
        # Open the current language dictionary
        self.dict = open(self.dict_name, "r")
        # Get list of available files with dictionaries in alphabetical order
        self.file = sorted(glob.glob('data/dicts/*'))   
        self.draws = 1
        self.result = []
        self.specialchars = ["!", "#", "$", "%", "&", "'", "(", ")", "*", "+", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@"]
        self.min = 1
        self.max = 6
        self.switch01Value = False
        self.switch02Value = False
        self.k = 0    
        self.output = ""
        self.texts = []
        self.screen = Builder.load_file("passphrasegenerator.kv")
        self.screen.ids["drop_item"].text = self.current_lang.strip()
        # Load texts in the current language
        self.display_text(self.dict) 
    
        menu_items = [
            {
                "viewclass": "IconListItem",
                "text": f[11:],
                "on_release": lambda x=f[11:]: self.set_item(x),
            }for f in self.file 
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids["drop_item"],
            items=menu_items,
            position="bottom",
            width_mult=4,
        )
        self.menu.bind()
    # END OF INIT
    
    def build(self):
        self.title = "PassPhraseGenerator"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "800"
        return self.screen  
    # Creating list of choices (available languages). Event handler for MDDropDownItem. When you click menu itema method will be called.       
    def set_item(self, text_item):
        print(text_item)
        self.screen.ids["drop_item"].set_item(text_item)
        self.set_default_language(text_item)
        # Load texts in the selected language
        self.display_text(self.dict)
        self.menu.dismiss()

    def set_default_language(self,text_item):
	    self.filename = open(r"data/currentlanguage", "wt")
	    self.filename.write(text_item)
	    self.filename.close()
	    dict_name = "data/dicts/"+text_item
	    self.dict = open(dict_name, "r")
	    
    def set_text(self,dict):
        texts = []
        for line in dict:
             if "INFO" in line:
                 app_info = line[14:]
                 texts.append(app_info)
             if "CHOOSE_LANG" in line:
                 choose_lang = line[14:]
                 texts.append(choose_lang.strip())
             if "ADD_NUMBER" in line:
                 add_number = line[14:]
                 texts.append(add_number.strip())
             if "ADD_SPEC_CHAR" in line:
                 add_spec_char = line[14:]
                 texts.append(add_spec_char.strip())
             if "WORDS" in line:
                 words = line[14:]
                 texts.append(words.strip())
             if  "WORDS_NUMBER" in line:
                 words_number = line[14:]
                 texts.append(words_number)
        dict.seek(0)
        return texts
        
    def display_text(self, dict):
        self.texts = self.set_text(dict)
        self.screen.ids["choose_lang"].text = self.texts[1]
        self.screen.ids["add_number"].text = self.texts[2]
        self.screen.ids["add_spec_char"].text = self.texts[3]
        self.screen.ids["words"].text = self.texts[4]
        self.words_number = self.texts[5]
    # Called by numbersswitch in .kv                                
    def switch01_callback(self, switchObject, switchValue):
        # Switch value are True and False
        if(switchValue):
            print('Switch01 is ON:):):)')	# Test
            self.switch01Value = True
        else:
            print('Switch01 is OFF:(:(:(')	# Test
            self.switch01Value = False
    # Called by symbolswitch in .kv
    def switch02_callback(self, switchObject, switchValue):
        # Switch value are True and False
        if(switchValue):
            print('Switch02 is ON:):):)')	# Test
            self.switch02Value = True
        else:
            print('Switch02 is OFF:(:(:(')	# Test
            self.switch02Value = False
            
    def create_pass_phrase(self, value):
        drawsnum = value
        words = ""
        fourdigits = ""
        specialchar = ""
        # Roll dice
        while self.draws <= drawsnum:
            for count in range (1,6):
                n = random.randint(self.min, self.max)
                self.result.append(n)
            for count in range (0,5):
                self.output = self.output+str(self.result[count])
            for line in self.dict:
                if self.output in line:
                    words = words + line[6:]
            self.dict.seek(0)
            self.draws += 1
            self.output = ""
            self.result = []
        self.draws = 1 
        drawsnum = 0
        # End of roll dice
        
        # Add four digits number
        if self.switch01Value == True:
           fourdigits = self.pick_four_digits()
        
        # Add special character  
        if self.switch02Value == True:
           specialchar = self.pick_spec_char()
			
        print(words)		# T e s t
        self.screen.ids["mdlab"].text = words + str(fourdigits) + "\n" + specialchar
        
    def pick_spec_char(self):
        n = random.randint(0,19)
        specialchar = self.specialchars[n]
        return specialchar
        
    def pick_four_digits(self):
        n = random.randint(1000,9999)
        return n
    # Called by OneLineAvatarListItem         
    def show_app_info_dialog(self):  
        #if not self.info_dialog:
        self.info_dialog = MDDialog(
            title = "Info App",
            text = self.texts[0].strip(),
            auto_dismiss = True
            )
        self.info_dialog.open()    
    # Called by OneLineAvatarListItem       
    def open_youtube_channel(self):    
        webbrowser.open('https://www.youtube.com/user/balneaopto')


PassPhraseGeneratorApp().run()
