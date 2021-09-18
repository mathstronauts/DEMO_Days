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
    "show_location": "",
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
    "show_cloud_bh": "",
    "show_cloud_type": ""
}

# convert from epoch to standard time
def convert_time(time):
    standard_time = datetime.fromtimestamp(time)
    return standard_time

# =============================== API Data ======================================
# API URLs
API_KEY = "bc93af7ec21317a25fa7d755f7391e39"
weather_URL = "https://api.openweathermap.org/data/2.5/onecall?"
# use Toronto as an example:
lat = (43.7001)
lon = (-79.4163)

# determine cloud type
def cloud_base_height(temp, dew):
    cloud_base = (temp - dew) / 2.5 * 1000 / 3.280839895
    print("The height of clouds is", round(cloud_base), "metres")
    return cloud_base

def getWeather():
    global lat, lon
    global background, backgroundRect, font_col
    global weather_var

    # change city location
    global new_city_click
    if new_city_click == True:
      latlon = textinput.get_text()
      lat = latlon.split(", ")[0]
      lon = latlon.split(", ")[1]
      print(lat, " ", lon)
      new_city_click = False

    update_time = datetime.now() # get the current time
    weather_var['show_update_time'] = (f"{update_time.strftime('%I')}:" + f"{update_time.strftime('%M')}" + f" {update_time.strftime('%p')}")

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
    daily_weather = (weather_data["daily"])[0]["temp"]

    current_temp = round(current_weather["temp"])  # current temperature
    current_forecast = (current_weather["weather"])[0]["main"]  # current weather forecast
    pressure = current_weather["pressure"]  # current atmospheric pressure in hectopascals (hPa) which equals millibar (mb)
    dew_point = current_weather["dew_point"]  # current dew point temperature
    UVI = current_weather["uvi"]
    wind_speed = round((current_weather["wind_speed"]) * 3.6)  # current wind speed m/s, (x 3.6) to convert to km/h
    humidity = current_weather["humidity"]  # current humidity in %
    date = convert_time(current_weather["dt"])
    sunrise_time = convert_time(current_weather["sunrise"])
    sunset_time = convert_time(current_weather["sunset"])

    # format datetimes, .stftime() is a method to format the datetime object
    weather_var['show_date'] = date.strftime('%x')
    weather_var['show_sunrise_time'] = (
            f"{sunrise_time.strftime('%I')}:" + f"{sunrise_time.strftime('%M')}" + f" {sunrise_time.strftime('%p')}")
    weather_var['show_sunset_time'] = (
            f"{sunset_time.strftime('%I')}:" + f"{sunset_time.strftime('%M')}" + f" {sunset_time.strftime('%p')}")

    daily_max_temp = round(daily_weather["max"], 1)  # daily temperature high
    daily_min_temp = round(daily_weather["min"], 1)  # daily temperature low

    # text to display on app screen
    weather_var['show_forecast'] = str(current_forecast)
    weather_var['show_current_temp'] = str(current_temp)
    weather_var['show_current_temp_units'] = chr(176) + "C"
    weather_var['show_high'] = f"High: {daily_max_temp}" + chr(176)
    weather_var['show_low'] = f"Low: {daily_min_temp}" + chr(176)

    # text under Show More
    weather_var['show_uvi'] = str(UVI)
    weather_var['show_humidity'] = str(humidity) + " %"
    weather_var['show_pressure'] = str(pressure) + " hPa"

    # text in bottom left corner
    cloud_bh = "- -"
    if current_forecast != "Clear":
        cloud_bh = round(cloud_base_height(current_temp, dew_point))
    else:
        cloud_bh = "- -"

    weather_var['show_windspeed'] = str(wind_speed) + " km/h"
    weather_var['show_cloud_bh'] = str(cloud_bh) + " m"

    

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

# change our app icon image!
app_icon_file = "images/weather_icon_test4.png"
app_icon = pygame.image.load(app_icon_file)
pygame.display.set_icon(app_icon)

# Background Weather Image
font_col = BLACK
background_file = "images/bkgd_beach1.png"
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

# display text input box
textinput = mathstropy.TextInput(initial_string="43.7001, -79.4163", font_size=30)

def showMore():
    global weather_var
    # icon positions
    ref_x = 565
    ref_y = 180
    icon_height = sunrise_i.get_height() + 10
    icon_width = sunrise_i.get_width() + 10

    # icon y-position
    sunrise_y = ref_y
    sunset_y = ref_y + icon_height
    UVI_y = ref_y + 2*(icon_height)
    pressure_y = ref_y + 3*(icon_height)
    humidity_y = ref_y + 4*(icon_height)

    # create icon rects
    sunrise_iRect = sunrise_i.get_rect(topleft=(ref_x, sunrise_y))
    sunset_iRect = sunset_i.get_rect(topleft=(ref_x, sunset_y))
    UVI_iRect = UVI_i.get_rect(topleft=(ref_x, UVI_y))
    pressure_iRect = pressure_i.get_rect(topleft=(ref_x, pressure_y))
    humidity_iRect = humidity_i.get_rect(topleft=(ref_x, humidity_y))

    # draw weather info text
    display_text(16, f"Sunrise: {weather_var['show_sunrise_time']}", font_col, 625, 180)
    display_text(16, f"Sunset: {weather_var['show_sunset_time']}", font_col, 620, 210)
    display_text(16, f"UV Index: {weather_var['show_uvi']}", font_col, 600, 260)
    display_text(16, f"Pressure: {weather_var['show_pressure']}", font_col, 630, 300)
    display_text(16, f"Humidity: {weather_var['show_humidity']}", font_col, 650, 350)

    # draw weather MORE info icons on screen
    screen.blit(sunrise_i, sunrise_iRect)
    screen.blit(sunset_i, sunset_iRect)
    screen.blit(UVI_i, UVI_iRect)
    screen.blit(pressure_i, pressure_iRect)
    screen.blit(humidity_i, humidity_iRect)

# App Conditions
running = True  # this means that app will run while this variable is true
show_more_click = False
new_city_click = False

# get location and weather data when app launches
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
              new_city_click = True
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
  display_text(150, weather_var['show_current_temp'], font_col, 40, 55)
  display_text(40, weather_var['show_current_temp_units'], font_col, 205, 65)
  display_text(25, weather_var['show_forecast'], font_col, 45, 200)
  display_text(20, f"Last Updated: {weather_var['show_update_time']}", font_col, 550, 20)
  display_text(60, weather_var['show_date'], font_col, 550, 55)
  display_text(20, weather_var['show_high'], font_col, 80, 400)
  display_text(20, weather_var['show_low'], font_col, 80, 460)
  # bottom bar text
  display_text(16, weather_var['show_windspeed'], BLACK, 70, 555)
  display_text(16, weather_var['show_cloud_bh'], BLACK, 250, 555)

  # show text input box on screen
  textinput.update(events)
  screen.blit(textinput.get_surface(), (25, 20))

  if show_more_click == True:
      showMore()
      screen.blit(hide_button, hide_buttonRect)

  # display all objects on the screen
  pygame.display.flip()

pygame.quit()
