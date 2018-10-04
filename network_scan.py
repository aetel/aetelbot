#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import re
from data_loader import DataLoader
from logger import get_logger

settings = DataLoader()
logger = get_logger("network_scan")
logger.setLevel(0)

def scan_for_devices():
    try:
        scan = subprocess.check_output("echo \"" + settings.admin_password + "\" | sudo -S nmap -sP " + settings.network, shell=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    p = re.compile(ur'(?:[0-9a-fA-F]:?){12}')
    return re.findall(p, scan)


def room_members_parser(people):
    answer_string = ""
    for member in people:
        answer_string += "- " + member + "\n"
    if answer_string == "":
        answer_string = "No parece haber nadie :'("
    else:
        answer_string = "Presentes:\n" + answer_string
    return answer_string


def who_is_there():
    macs = scan_for_devices()
    who_are_there = []
    logger.debug("ENCONTRADOS: " + str(macs))
    for mac in scan_for_devices():
        if mac in list(settings.devices.keys()):
            who_are_there.append(settings.devices[mac])
    who_are_there = sorted(set(who_are_there))
    respuesta = room_members_parser(who_are_there)
    return respuesta, who_are_there


def is_someone_there():
    who = who_is_there()[1]
    return len(who) != 0

if __name__ == "__main__":
    print ("Bienvenido, se va a escanear la red.")
    print(scan_for_devices())
    print ("Adios")

