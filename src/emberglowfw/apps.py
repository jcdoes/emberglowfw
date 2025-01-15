import os
import json
from django.apps import AppConfig
from pathlib import Path


loaded_plugins = []

class EmberglowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emberglowfw'

    def ready(self):

        path = Path(__file__).resolve().parent.parent / 'plugins'
        file_list=os.listdir(path)

        # Start to parse plugin files.
        for plugin in file_list:
            with open(str(path / plugin), "r") as f:
                try:
                    json_text = json.loads(f.read()) 
                    loaded_plugins.append(json_text)

                except json.JSONDecodeError as e:
                    print('Plugin load error on: ' + plugin + ': ' + str(e))

        print("Finished loading plugins!")