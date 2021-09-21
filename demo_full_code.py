"""
 * Copyright (C) Mathstronauts. All rights reserved.
 * This information is confidential and proprietary to Mathstronauts and may not be used, modified, copied or distributed.
"""
import pygame  # pygame library for graphics
import requests  # library to extract APIs
import json  # library to read JSON files
from datetime import *
import mathstropy

# define some colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# define Earth weather text display variables:
weather_var = {
    "show_current_temp": "",
    "show_current_temp_units": "",
    "show_forecast": "",
    "show_update_time": "",
    "show_date": "",
    "show_high": "",
    "show_low": "",
    "show_sunrise_time": "",
    "show_sunset_time": "",
    "show_uvi": "",
    "show_pressure": "",
    "show_humidity": "",
    "show_windspeed": "",
}

# ====== API Data ========
# user input city location
textinput = mathstropy.TextInput(initial_string="Toronto", font_size=30)  # initial string will be our example city

# API URLs
API_KEY = "bc93af7ec21317a25fa7d755f7391e39"

# One Call Weather API
weather_URL = "https://api.openweathermap.org/data/2.5/onecall?"

# Geocoding API
geo_URL = "http://api.openweathermap.org/geo/1.0/direct?"

def getLocation():
    # get city location from user input
    city_name = textinput.get_text()

    # Extract Coordinates using Geocoding API
    geo_parameters = {
        "q": city_name,
        "appid": API_KEY
    }
    geo_response = requests.get(geo_URL, params=geo_parameters)
    print("Geocode API Status:", geo_response.status_code)
    geo_coord = geo_response.json()
    geo_first = geo_coord[0]  # get first item in list of possible cities (most popular)
    lat = float(geo_first["lat"])  # north is positive, south is negative
    lon = float(geo_first["lon"])  # east is positive, west is negative
    return [lat, lon]

def getWeather():
    global background, backgroundRect, font_col
    global weather_var

    # get update time
    update_time = datetime.now()  # get the current time
    weather_var['show_update_time'] = mathstropy.time_format(update_time)

    # get city location from user input
    # latlon = textinput.get_text()
    # lat = latlon.split(", ")[0]
    # lon = latlon.split(", ")[1]
    # print(lat, " ", lon)

    # get location variables using getLocation() function
    lat = getLocation()[0]
    lon = getLocation()[1]

    # Extract City Weather using One Call Weather API
    weather_parameters = {
      "lat": lat,
      "lon": lon,
      "appid": API_KEY,
      "units": "metric"
    }

    weather_response = requests.get(weather_URL, params=weather_parameters)
    print("One Call Weather API Status:", weather_response.status_code)
    weather_data = weather_response.json()
    current_weather = weather_data["current"]
    mathstropy.jprint(current_weather)  # print the weather data being extracted from the API
    daily_weather = (weather_data["daily"])[0]["temp"]

    # calculate cloud base height
    current_temp = round(current_weather["temp"])  # current temperature
    current_forecast = (current_weather["weather"])[0]["main"]  # current weather forecast
    dew_point = current_weather["dew_point"]  # current dew point temperature

    if current_forecast != "Clear":
        cloud_bh = round(mathstropy.cloud_base_height(current_temp, dew_point))
    else:
        cloud_bh = "- -"

    # format date and time variables
    weather_var['show_date'] = mathstropy.date_format(current_weather["dt"])
    weather_var['show_sunrise_time'] = mathstropy.time_format(current_weather["sunrise"])
    weather_var['show_sunset_time'] = mathstropy.time_format(current_weather["sunset"])

    # text to display on app screen
    weather_var['show_forecast'] = current_forecast  # current weather forecast
    weather_var['show_current_temp'] = current_temp  # current temperature
    weather_var['show_current_temp_units'] = chr(176) + "C"
    weather_var['show_high'] = "High: " + str(round(daily_weather["max"], 1)) + chr(176)
    weather_var['show_low'] = "Low: " + str(round(daily_weather["min"], 1)) + chr(176)

    # text under Show More
    weather_var['show_uvi'] = current_weather["uvi"]
    weather_var['show_humidity'] = str(current_weather["humidity"]) + " %"
    weather_var['show_pressure'] = str(current_weather["pressure"]) + " hPa"

    # text in bottom left corner
    weather_var['show_windspeed'] = str(round((current_weather["wind_speed"]) * 3.6)) + " km/h"
    weather_var['show_cloud_bh'] = str(cloud_bh) + " m"

    weather_var = mathstropy.dict_str(weather_var)  # convert all dictionary items to string

# ======================== GRAPHICS ==========================
# screen setup
WIDTH = 800
HEIGHT = 600
FPS = 30

# initialize pygame
pygame.init()

# create window and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Earth Weather App")

# Background Weather Image
font_col = BLACK
background_file = "images/bkgd_beach2.png"
background = pygame.image.load(background_file)
backgroundRect = background.get_rect()

# Load Button Images and Rect Positions
search_button = pygame.image.load("images/search_location_button.png")
search_buttonRect = search_button.get_rect(topleft=(360,10))
refresh_button = pygame.image.load("images/refresh_button.png")
refresh_buttonRect = refresh_button.get_rect(topleft=(500,10))
show_more_button = pygame.image.load("images/show_more_button.png")
show_more_buttonRect = show_more_button.get_rect(topleft=(600, 125))
hide_button = pygame.image.load("images/hide_button.png")
hide_buttonRect = hide_button.get_rect(topleft=(565,130))

# Load Icon Images
sunrise_i = pygame.image.load("images/sunrise_icon.png")
sunset_i = pygame.image.load("images/sunset_icon.png")
UVI_i = pygame.image.load("images/UVI_icon.png")
pressure_i = pygame.image.load("images/pressure_icon.png")
humidity_i = pygame.image.load("images/humidity_icon.png")

# function to display text on screen
def display_text(size, text, colour, x, y):
    font = pygame.font.Font('freesansbold.ttf', size)  # specify the font and size
    textSurf = font.render(text, True, colour)    # create a surface for the text object
    textRect = textSurf.get_rect()  # get rect position of text on the screen
    textRect.topleft = (x, y)  # specify rect position of text on screen
    screen.blit(textSurf, textRect)  # show the text on the screen

def showMore():
    global weather_var
    # create icon rects
    sunrise_iRect = sunrise_i.get_rect(topleft=(565, 180))
    sunset_iRect = sunset_i.get_rect(topleft=(565, 215))
    UVI_iRect = UVI_i.get_rect(topleft=(565, 250))
    pressure_iRect = pressure_i.get_rect(topleft=(565, 285))
    humidity_iRect = humidity_i.get_rect(topleft=(565, 320))

    # draw weather info text
    mathstropy.display_text(16, f"Sunrise: {weather_var['show_sunrise_time']}", font_col, 600, 185)
    mathstropy.display_text(16, f"Sunset: {weather_var['show_sunset_time']}", font_col, 600, 220)
    mathstropy.display_text(16, f"UV Index: {weather_var['show_uvi']}", font_col, 600, 255)
    mathstropy.display_text(16, f"Pressure: {weather_var['show_pressure']}", font_col, 600, 290)
    mathstropy.display_text(16, f"Humidity: {weather_var['show_humidity']}", font_col, 600, 325)

    # draw weather MORE info icons on screen
    screen.blit(sunrise_i, sunrise_iRect)
    screen.blit(sunset_i, sunset_iRect)
    screen.blit(UVI_i, UVI_iRect)
    screen.blit(pressure_i, pressure_iRect)
    screen.blit(humidity_i, humidity_iRect)

# App Conditions
running = True  # this means that app will run while this variable is true
show_more_click = False

# get location and weather data when app launches
getLocation()  # Get latitude and longitude for city location
getWeather()  # Initialize weather data

# ====================== APP DISPLAY LOOP =========================
while running:
  # process user input
  events = pygame.event.get()
  for event in events:
      mouse = pygame.mouse.get_pos()  # get mouse position (x, y)

      if event.type == pygame.QUIT:
          running = False  # stop game and quite

      if event.type == pygame.MOUSEBUTTONDOWN:
          print("Mouse click!")
          if pygame.Rect.collidepoint(refresh_buttonRect, mouse):  # if refresh button overlaps with mouse position
              print("REFRESH!")
              getWeather()
          elif pygame.Rect.collidepoint(search_buttonRect, mouse): # if new city button overlaps with mouse position
              print("NEW CITY")
              getLocation()
              getWeather()
          elif pygame.Rect.collidepoint(show_more_buttonRect, mouse): # if more button overlaps with mouse position
              print("SHOW MORE!!!")
              show_more_click = True
          elif pygame.Rect.collidepoint(hide_buttonRect, mouse):
              print("HIDE MENU")
              show_more_click = False

  # render/draw the screen
  screen.fill(BLACK)
  screen.blit(background, backgroundRect)

  # draw buttons
  screen.blit(refresh_button, refresh_buttonRect)
  screen.blit(search_button, search_buttonRect)
  screen.blit(show_more_button, show_more_buttonRect)

  # display_text(size, text, colour, x, y)
  mathstropy.display_text(150, weather_var['show_current_temp'], font_col, 40, 55)
  mathstropy.display_text(40, weather_var['show_current_temp_units'], font_col, 205, 65)
  mathstropy.display_text(25, weather_var['show_forecast'], font_col, 45, 200)
  mathstropy.display_text(20, f"Last Updated: {weather_var['show_update_time']}", font_col, 550, 20)
  mathstropy.display_text(60, weather_var['show_date'], font_col, 550, 55)
  mathstropy.display_text(20, weather_var['show_high'], font_col, 80, 400)
  mathstropy.display_text(20, weather_var['show_low'], font_col, 80, 460)
  # bottom bar text
  mathstropy.display_text(16, weather_var['show_windspeed'], BLACK, 70, 555)
  mathstropy.display_text(16, weather_var['show_cloud_bh'], BLACK, 250, 555)

  # show text input box on screen
  textinput.update(events)
  screen.blit(textinput.get_surface(), (25, 20))

  if show_more_click == True:
      showMore()
      screen.blit(hide_button, hide_buttonRect)

  # display all objects on the screen
  pygame.display.flip()

pygame.quit()
