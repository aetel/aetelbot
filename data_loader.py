#!/usr/bin/env python
# -*- coding: utf-8 -*-
from logger import get_logger
import json

logger = get_logger("data_loader")


class DataLoader:

    def __init__(self):
        global data_and_settings
        try:
            json_file = open('data-and-settings.json')
            data_and_settings = json.load(json_file, encoding="utf-8")
        except:
            logger.exception("Error al cargar el JSON de configuración")
        else:
            logger.info("JSON cargado con éxito")
            self.telegram_token = data_and_settings["telegram token"]
            self.help_string = data_and_settings["help"]
            self.start_message = data_and_settings["start message"]
            self.devices = data_and_settings["devices"]
            self.working_directory = data_and_settings["working directory"]
            self.pictures_directory = data_and_settings["pictures directory"]
            self.cam_url = data_and_settings["cam url"]
            self.network = data_and_settings["network"]
            self.node = data_and_settings["node"]
            self.admin_password = data_and_settings["admin password"]
            self.public_chatid = data_and_settings["public group chat id"]
            self.admin_chatid = data_and_settings["admin group chat id"]
            self.president_chatid = data_and_settings["president chat id"]

    @property
    def telegram_token(self):
        return self.telegram_token

    @property
    def president_chatid(self):
        return self.president_chatid

    @property
    def help_string(self):
        return self.help_string

    @property
    def start_message(self):
        return self.start_message

    @property
    def devices(self):
        return self.devices

    @property
    def working_directory(self):
        return self.working_directory

    @property
    def cam_url(self):
        return self.cam_url

    @property
    def network(self):
        return self.network

    @property
    def node(self):
        return self.node

    @property
    def admin_password(self):
        return self.admin_password

    @property
    def admin_chatid(self):
        return self.admin_chatid

    @property
    def public_chatid(self):
        return self.public_chatid

    @property
    def pictures_directory(self):
        return self.pictures_directory
