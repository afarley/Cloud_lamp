#Lighting Cloud Mood Lamp By James Bruce
#View the full tutorial and build guide at http://www.makeuseof.com/
#
#Sound sampling code originally by Adafruit Industries.  Distributed under the BSD license.
#This paragraph must be included in any redistribution.

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import neopixel
from enum import Enum
#import numpy as np
###import analogio
import random

# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
#pixel_pin = board.NEOPIXEL

# On a Raspberry pi, use this instead, not all pins are supported
pixel_pin = board.D18
mic_pin = board.D16

# The number of NeoPixels
###num_pixels = 300
NUM_LEDS = 1500

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, NUM_LEDS, brightness=0.2, auto_write=False, pixel_order=ORDER)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
	if pos < 0 or pos > 255:
		r = g = b = 0
	elif pos < 85:
		r = int(pos * 3)
		g = int(255 - pos * 3)
		b = 0
	elif pos < 170:
		pos -= 85
		r = int(255 - pos * 3)
		g = 0
		b = int(pos * 3)
	else:
		pos -= 170
		r = 0
		g = int(pos * 3)
		b = int(255 - pos * 3)
	return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM_LEDS):
            pixel_index = (i * 256 // NUM_LEDS) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)



#include <Wire.h>
#include "FastLED.h"

#// How many leds in your strip?
###NUM_LEDS = 1200
#DATA_PIN = 6


#// Mode enumeration - if you want to add additional party or colour modes, add them here; you'll need to map some IR codes to them later;
#// and add the modes into the main switch loop
Mode = Enum('Mode', [ 'CLOUD', 'ACID', 'OFF', 'ON', 'RED', 'GREEN', 'BLUE', 'FADE' ])
###print(Mode)
mode = Mode.ON
lastMode = Mode.ON


###// Mic settings, shouldn't need to adjust these.
###MIC_PIN = 0  
#// Microphone is attached to this analog pin

DC_OFFSET = 0  
#// DC offset in mic signal - if unusure, leave 0

NOISE = 10  
#// Noise/hum/interference in mic signal

SAMPLES = 10  
#// Length of buffer for dynamic level adjustment

#byte
volCount  = 0      
#// Frame counter for storing past volume data

vol = []
vol = [0 for i in range(SAMPLES)]       
#vol = np.empty(SAMPLES, dtype=object) 
#// Collection of prior volume samples

n = 30
total = 30
average = 0.0

#// used to make basic mood lamp colour fading feature
#int fade_h;
fade_h = 0
fade_direction = 1


#// Define the array of leds
#CRGB leds[NUM_LEDS]
###leds=[]

#void setup() {
#  // this line sets the LED strip type - refer fastLED documeantion for more details https://github.com/FastLED/FastLED
#  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);
#  // starts the audio samples array at volume 15.
#  memset(vol, 15, sizeof(vol));
#  Serial.begin(115200);
#  Wire.begin(9);                // Start I2C Bus as a Slave (Device Number 9)
#  Wire.onReceive(receiveEvent); // register event
#}


def receiveEvent(received):
#  // Here, we set the mode based on the IR signal received. Check the debug log when you press a button on your remote, and
#  // add the hex code here (you need 0x prior to each command to indicate it's a hex value)
###	while(Wire.available():

# Temp dummy value for received
#	received = 1

	while True:
#      unsigned int received = Wire.read()
		print("Receiving IR hex: ")
### !!!!!Fix this!!!!!
###		print(received,HEX)
		lastMode = mode
		
#		switch(received):
		match received:
			case 0x3F:
				mode = Mode.ON
				break
			case 0xBF:
				mode = Mode.OFF
				break
			case 0x2F:
				mode = Mode.CLOUD
				break
			case 0xF:
				mode = Mode.ACID
				break
			case 0x37:
				mode = Mode.FADE
				break
			case 0x9F:
				mode = Mode.BLUE
				break
			case 0x5F:
				mode = Mode.GREEN 
				break
			case 0xDF:
				mode = Mode.RED
				break
			

#// Makes all the LEDs a single colour, see https://raw.githubusercontent.com/FastLED/FastLED/gh-pages/images/HSV-rainbow-with-desc.jpg for H values
def single_colour(H):
#  for (int i=0;i<NUM_LEDS;i++){
	for i in range(NUM_LEDS):
#    leds[i] = CHSV( H, 255, 255);
		pixels[i] = ( H, 255, 255)
#  //avoid flickr which occurs when FastLED.show() is called - only call if the colour changes
	if(lastMode != mode):
### Fix this?!?
#		FastLED.show()
		pixels.show()
		lastMode = mode

	time.sleep(0.050)


def colour_fade(fade_h, fade_direction):
#//mood mood lamp that cycles through colours
#  for (int i=0;i<NUM_LEDS;i++){
	for i in range(NUM_LEDS):
		pixels[i] = (fade_h, 255, 255)
		
	if(fade_h >254):
		fade_direction = -1
#		//reverse once we get to 254

	elif(fade_h < 0):
		fade_direction = 1

	fade_h += fade_direction;
### Fix This?!?
#	FastLED.show()
	pixels.show()
	time.sleep(0.1)


def detect_thunder():

	n = analogio.AnalogIn(mic_pin)
	print(n.value)
#	n   = analogRead(MIC_PIN)                        
#	// Raw reading from mic
	n   = abs(n - 512 - DC_OFFSET)
#	// Center on zero
### Check if this is the correct porting of ? ... a : b !!!!!!!!!!!!!
	n   = (n <= NOISE) if n==0 else n==(n - NOISE)
#	// Remove noise/hum
	vol[volCount] = n
#	// Save sample for dynamic leveling
	
	if(++volCount >= SAMPLES):
		volCount = 0 
#	// Advance/rollover sample counter

	total = 0;


#	for(int i=0; i<SAMPLES; i++) {
	for i in range(SAMPLES):
		total += vol[i]
		
#  // If you're having trouble getting the cloud to trigger, uncomment this block to output a ton of debug on current averages.
#  // Note that this WILL slow down the program and make it less sensitive due to lower sample rate.

#	for(int t=0; t<SAMPLES; t++) {
	for t in range(SAMPLES):
#    //initial data is zero. to avoid initial burst, we ignore zero and just add the current l
		print("Sample item ")
		print(t)
		print(":")
		print(vol[t])
		
	print("total")
	print(total)
	print("divided by sample size of ")
	print(SAMPLES)
	
	print("average:")
	print(average)
	
	print("current:")
	print(n)
	
	average = (total/SAMPLES)+2
	
	if(n>average):
		print("TRIGGERED")
		reset()
     
   
#    //I've programmed 3 types of lightning. Each cycle, we pick a random one.
	type = random.randint(1,3)

	match type:
#       //switch(3){
		
		case 1:
			thunderburst()
			time.sleep(random.uniform(0.010,0.500))
			print("Thunderburst")
#			break
			       
		case 2:
			rolling()
			print("Rolling")
#			break
			       
		case 3:
			crack()
			time.sleep(random.uniform(0.050,0.250))
			print("Crack")
#			break
			
			
#// utility function to turn all the lights off.  
def reset():
#  for (int i=0;i<NUM_LEDS;i++){
	for i in range(NUM_LEDS):
		pixels[i] = (0, 0, 0)

## Might need to fix this
######  FastLED.show();
	pixels.show()
   
   
def acid_cloud():
#    // a modification of the rolling lightning which adds random colour. trippy.
#    //iterate through every LED
#    for(int i=0;i<NUM_LEDS;i++){
	for i in range(NUM_LEDS):
		if(random.randint(0,100)>90):
			pixels[i] = (random.randint(0, 255), 255, 255)

		else:
			pixels[i] = (0,0,0)
# Fix this?!?
#    FastLED.show();
	pixels.show()
	time.sleep(random.uniform(0.005,0.100))
	reset()
   
 

def rolling():
#  // a simple method where we go through every LED with 1/10 chance
#  // of being turned on, up to 10 times, with a random delay wbetween each time
#  for(int r=0;r<random(2,10);r++){
	
	r = random.randint(2, 10)
	for i in range(r):
#    //iterate through every LED
#		for(int i=0;i<NUM_LEDS;i++){
		for i in range(NUM_LEDS):
			if(random.randint(0,100)>90):
				pixels[i] = (0, 0, 255)

			else:
#        //dont need reset as we're blacking out other LEDs her
				pixels[i] = (0,0,0)

# Fix this?!?
#	FastLED.show()
	pixels.show()
	time.sleep(random.uniform(0.005,0.100))
	reset()
   


def crack():
#   //turn everything white briefly
#   for(int i=0;i<NUM_LEDS;i++) {
	for i in range(NUM_LEDS):
		pixels[i] = (0, 0, 255)  
		
# Fix this?!?		
#	FastLED.show()
	pixels.show()
	time.sleep(random.uniform(0.010,0.100))
	reset()


def thunderburst():

#  // this thunder works by lighting two random lengths
#  // of the strand from 10-20 pixels.
	rs1 = random.randint(0,NUM_LEDS/2)
	rl1 = random.randint(10,20)
	rs2 = random.randint(rs1+rl1,NUM_LEDS)
	rl2 = random.randint(10,20)
	
#  //repeat this chosen strands a few times, adds a bit of realism
#for(int r = 0;r<random(3,6);r++){

	r = random.randint(3,6)
# Fix this	 
	for i in range(r):
	  
#    for(int i=0;i< rl1; i++){
		for j in range(rl1):
			pixels[j+rs1] = (0, 0, 255)
   
		if(rs2+rl2 < NUM_LEDS):
#      for(int i=0;i< rl2; i++){
			for j in range(rl2):
				pixels[j+rs2] = (0, 0, 255)
# Fix this?!?   
#    FastLED.show()
		pixels.show()
#    //stay illuminated for a set time
		time.sleep(random.uniform(0.010,0.050))
   
		reset()
		time.sleep(random.uniform(0.010,0.050))


#// basically just a debug mode to show off the lightning in all its glory, no sound reactivity.
def constant_lightning():
# 	switch(random.randint(1,10,1))
	type = random.randint(1,10)
	
	match type:
		case 1:
			thunderburst()
			time.sleep(random.uniform(0.010,0.500))
			print("Thunderburst")
#			break
       
		case 2:
			rolling()
			print("Rolling")
#			break
       
		case 3:
			crack()
			time.sleep(random.uniform(0.050,0.250))
			print("Crack")
#			break
       
   

while True:
	# Comment this line out if you have RGBW/GRBW NeoPixels
	print('Running')
	#pixels.fill((255, 0, 0))
	# Uncomment this line if you have RGBW/GRBW NeoPixels
	pixels.fill((255, 0, 0, 0))
	pixels.show()
	time.sleep(1)

	# Comment this line out if you have RGBW/GRBW NeoPixels
	#pixels.fill((0, 255, 0))
	# Uncomment this line if you have RGBW/GRBW NeoPixels
	pixels.fill((0, 255, 0, 0))
	pixels.show()
	time.sleep(1)

	# Comment this line out if you have RGBW/GRBW NeoPixels
	#pixels.fill((0, 0, 255))
	# Uncomment this line if you have RGBW/GRBW NeoPixels
	pixels.fill((0, 0, 255, 0))
	pixels.show()
	time.sleep(1)

	rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step

### !!!! This may need to be a while loop !!!!
###	received = 
###	receiveEvent(received)

#       // Maps mode names to code functions.
#       switch(mode):
#	rainbow_cycle(wait)
	match mode:
		case Mode.CLOUD:
			print('Cloud mode')
			detect_thunder()
			reset()
#                       break
		case Mode.ACID:
			print('Acid mode')
			acid_cloud()
			reset()
#                       break
		case Mode.OFF:
			print('Off')
			reset()
#                       break
		case Mode.ON:
			print('On')
			constant_lightning()
			reset()
#                       break
		case Mode.RED:
			print('Red mode')
			single_colour(0)
#                       break
		case Mode.BLUE:
			print('Blue mode')
			single_colour(160)
#                       break
		case Mode.GREEN:
			print('Green mode')
			single_colour(96)
#                       break
		case Mode.FADE:
			print('Fade mode')
			colour_fade(fade_h, fade_direction)
#                       break
