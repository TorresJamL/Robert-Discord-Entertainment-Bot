### Goal: Implement a REALLY cursed version of fnaf ###
#? Nothing in this folder should be seen as a command available through -help
#   Not necessary to implement the above... low priority
#! Every place you can be should be a 'command' in the sense that typing "Cam1" will bring you to cam1
#* Cameras will print as gifs to discord... if movement of anykind is occuring cams should go static.
#   each camera can have MANY different states depending on animatronic movement and whos where at any point.
#   another folder will be necessary to store other folders pertaining to each camera / location. 
#   The folders should be organized as follows:
#       [folders]::FNAF <- LOCATIONS, ... <- CAMERA(1A-7), OFFICE <- ..., ... 
#* Animatronics should work as they normally do.
#* Power will need HEAVY adjusting in both amount and mechanic
#   possibly by making it that power will get wasted if you dont do some "cam down" command?..
#   regardless, time should definitely be imported for this.
#* Each night things will move faster and animatronics will become more active
#   how exactly this will work has to be thought through.
#   random animatronic movement might get complex.
#   especially considering how time for movement is more or less a range.
#   this should mean that theoretically... Freddy and Foxy are easier to make.
#   easier means nothing when i've barely started.
#TODO:
#   Before starting in discord, make it work through the terminal so testing goes faster.
#   An example of how cameras can be done is how I handled the menu in the cs115 proj
#   One primary function that has a dictionary that stores other functions (probably going to be cameras).
#       ?This primary function will likely end up as the discord async function.

import time
import random
import unittest

def cam1A(): #showstage
    return 'This is cam1A!'

def cam1B(): #partyarea
    return 'This is cam1B!'
    
def cam2A(): #easthall
    return 'This is cam2A!'

def cam2B(): #easthallcorner
    return 'This is cam2B!'
    
def cam3(): #closet
    return 'This is cam3!'
    
def cam4A(): #westhall
    return 'This is cam4A!'
    
def cam4B(): #westhallcorner
    return 'This is cam4B!'
    
def cam5(): #backstage
    return 'This is cam5!'
    
def cam6(): #kitchen
    return 'This is cam6!'
    
def cam7(): #bathrooms
    return 'This is cam7!'

def office(action): #office
    match action:
        case 'left':
            return 'Looking at left door'
        case 'right':
            return 'Looking at right door'
        case 'left door':
            return 'Closed left door'
        case 'right door':
            return 'Closed right door'
        case _:
            return 'Action not found'

#@commands.command(name = 'area')
def display_location(location, office_action = None):
    locations = {
        '1A' : cam1A,
        '1B' : cam1B,
        '2A' : cam2A,
        '2B' : cam2B,
        '3' : cam3,
        '4A' : cam4A,
        '4B' : cam4B,
        '5' : cam5,
        '6' : cam6,
        '7' : cam7,
        'office' : office
    }
    if location in locations:
        if location == 'office':
            return locations['office'](office_action)
        else:
            return locations[location]()
    else:
        return "Not a valid location... Try Again."

class FNAFTest(unittest.TestCase):
    def test_cams(self):
        self.assertEqual(display_location("1A"), "This is cam1A!")
        self.assertEqual(display_location("1B"), "This is cam1B!")
        self.assertEqual(display_location("2A"), "This is cam2A!")
        self.assertEqual(display_location("2B"), "This is cam2B!")
        self.assertEqual(display_location("3"), "This is cam3!")
        self.assertEqual(display_location("4A"), "This is cam4A!")
        self.assertEqual(display_location("4B"), "This is cam4B!")
        self.assertEqual(display_location("5"), "This is cam5!")
        self.assertEqual(display_location("6"), "This is cam6!")
        self.assertEqual(display_location("7"), "This is cam7!")
    
    def test_office(self):
        self.assertEqual(display_location("office", "left"), "Looking at left door")
        self.assertEqual(display_location("office", "right"), "Looking at right door")
        self.assertEqual(display_location("office", "left door"), "Closed left door")
        self.assertEqual(display_location("office", "right door"), "Closed right door")
        self.assertEqual(display_location("office", "somewhere man"), "Action not found")

if __name__ == "__main__":
    unittest.main()