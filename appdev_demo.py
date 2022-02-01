"""
 * Copyright (C) Mathstronauts. All rights reserved.
 * This information is confidential and proprietary to Mathstronauts and may not be used, modified, copied or distributed.
"""
import pygame  # pygame library for graphics
from mathstropy import *
import requests
import json

# API DATA
API_KEY = "bc93af7ec21317a25fa7d755f7391e39"

# Geocoding API URL
geo_URL = "http://api.openweathermap.org/geo/1.0/direct?"

# user input city location
textinput = TextInput(initial_string="Toronto", font_size=30)

def getLocation():
    # Get city location
    city_name = textinput.get_text()

    # Extract Coordinates using Geocoding API
    geo_parameters = {"q": city_name, "appid": API_KEY}
    geo_response = requests.get(geo_URL, params=geo_parameters)
    geo_status = geo_response.status_code
    print("Geocode API Status:", geo_status)

    geo_data = geo_response.json()
    # jprint(geo_data)

    geo_first = geo_data[0]
    lat = float(geo_first["lat"])
    lon = float(geo_first["lon"])
    return [lat, lon]

# One Call Weather API
weather_URL = "https://api.openweathermap.org/data/2.5/onecall?"

# Store weather data in a dictionary
earth_var = {}

# weather data functions
# determine cloud base height
def cloud_base_height(temp, dew):
    cloud_base = (temp - dew) / 2.5 * 1000 / 3.28
    print("The height of clouds is", round(cloud_base), "metres")
    return cloud_base

# determine cloud type
def cloud_type(height, forecast):
    if height < 2000 and forecast == "Rain":
        cloud = "nimbus"
    elif height < 2000 and forecast == "Fog":
        cloud = "stratus"
    elif height < 2000:
        cloud = "cumulus"
    elif 2000 <= height < 7000:
        cloud = "alto"
    elif height >= 7000:
        cloud = "cirrus"
    return cloud

def getWeather():
    global earth_var
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
    # jprint(current_weather)  # print the weather data being extracted from the API
    daily_weather = (weather_data["daily"])[0]["temp"]

    # calculate cloud base height
    current_temp = round(current_weather["temp"])  # current temperature
    current_forecast = (current_weather["weather"])[0]["main"]  # current weather forecast
    dew_point = current_weather["dew_point"]  # current dew point temperature

    # format date and time variables
    earth_var['show_date'] = date_format(current_weather["dt"])
    earth_var['show_sunrise'] = time_format(current_weather["sunrise"])
    earth_var['show_sunset'] = time_format(current_weather["sunset"])

    # text to display on app screen
    earth_var['show_forecast'] = current_forecast  # current weather forecast
    earth_var['show_current_temp'] = current_temp  # current temperature
    earth_var['show_current_temp_units'] = chr(176) + "C"
    earth_var['show_high'] = "High: " + str(round(daily_weather["max"], 1)) + chr(176)
    earth_var['show_low'] = "Low: " + str(round(daily_weather["min"], 1)) + chr(176)

    # text under Show More
    earth_var['show_uvi'] = current_weather["uvi"]
    earth_var['show_humidity'] = str(current_weather["humidity"]) + " %"
    earth_var['show_pressure'] = str(current_weather["pressure"]) + " hPa"

    # Text in text box
    if earth_var['show_forecast'] == "Clear":
        cloud_bh = "- -"
        cloud_t = "None"
    else:
        cloud_bh = round(cloud_base_height(current_temp, dew_point))
        cloud_t = cloud_type(cloud_bh, current_forecast)

    # display text
    earth_var['show_cloud_bh'] = str(cloud_bh) + " m"
    earth_var['show_cloud_type'] = cloud_t

    # get the current time
    update_time = datetime.now()

    # format date and time variables
    earth_var['show_update_time'] = time_format(update_time)
    earth_var['show_date'] = date_format(current_weather["dt"])
    earth_var['show_sunrise'] = time_format(current_weather["sunrise"])
    earth_var['show_sunset'] = time_format(current_weather["sunset"])

    # convert all dictionary items to string
    earth_var = dict_str(earth_var)

# Mars Curiosity Rover REMS API URL
mars_URL = "https://mars.nasa.gov/rss/api/?feed=weather&category=msl&feedtype=json"

# Dictionary to Store Mars Display Data
mars_var = {}

def getMarsWeather():
    global mars_var
    mars_response = requests.get(mars_URL)  
    print("REMS API Status:", mars_response.status_code)

    REMS_lib = mars_response.json()
    REMS_soles = REMS_lib["soles"]
    mars_weather = REMS_soles[0]
    # jprint(mars_weather)

    # In southern hemisphere (location of Curiosity Rover), seasons marked by the following months:
    mars_month = mars_weather["season"]
    if mars_month == "Month 1" or mars_month == "Month 2" or mars_month == "Month 3":
        mars_season = "Autumn"
    elif mars_month in ["Month 4", "Month 5", "Month 6"]:
        mars_season = "Winter"
    elif mars_month == "Month 7" or mars_month == "Month 9" or mars_month == "Month 9":
        mars_season = "Spring"
    elif mars_month == "Month 10" or mars_month == "Month 11" or mars_month == "Month 12":
        mars_season = "Summer"
    else:
        mars_season = "no data"
    print(mars_season)
    mars_var["show_mars_season"] = mars_season

    # text to display on screen
    temp_units = chr(176) + "C"
    mars_var["show_high"] = mars_weather["max_temp"] + temp_units
    mars_var["show_low"] = mars_weather["min_temp"] + temp_units
    mars_var["show_sol"] = mars_weather["sol"]  # show Mars date
    mars_var["show_earth_date"] = mars_weather["terrestrial_date"]
    mars_var["show_forecast"] = mars_weather["atmo_opacity"]  # can be Sunny, Cloudy, or Windy
    mars_var["show_high_grd"] = mars_weather["max_gts_temp"] + temp_units
    mars_var["show_low_grd"] = mars_weather["min_gts_temp"] + temp_units

    # Mars More information
    mars_var["show_sunrise"] = mars_weather["sunrise"]
    mars_var["show_sunset"] = mars_weather["sunset"]
    mars_var["show_uvi"] = mars_weather["local_uv_irradiance_index"]
    mars_var["show_pressure"] = mars_weather["pressure"] + " Pa"
    # note the pressure is so much lower we are using Pa instead of kPa

    # get time when data is retrieved
    update_time = datetime.now()  # get the current time
    mars_var['show_update_time'] = time_format(update_time)

# screen setup
WIDTH = 800
HEIGHT = 600

# initialize pygame
pygame.init()

# define some colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mars Earth Weather App")

# function to display text on screen
def display_text(size, text, colour, x, y):
    font = pygame.font.Font('freesansbold.ttf', size)  # specify the font and size
    textSurf = font.render(text, True, colour)  # create a surface for the text object
    textRect = textSurf.get_rect()  # get rect position of text on the screen
    textRect.topleft = (x, y)  # specify rect position of text on screen
    screen.blit(textSurf, textRect)  # show the text on the screen

# load background images to pygame
bkgd_menu = pygame.image.load("images/bkgd_menu.png")
bkgd_menuRect = bkgd_menu.get_rect(topleft=(0, 0))
bkgd_earth = pygame.image.load("images/bkgd_earth.png")
bkgd_earthRect = bkgd_earth.get_rect(topleft=(0, 0))
bkgd_mars = pygame.image.load("images/bkgd_mars.png")
bkgd_marsRect = bkgd_mars.get_rect(topleft=(0, 0))

# Load Button Images and Rect Position
main_menu_button = pygame.image.load("images/main_menu_button.png")
main_menu_buttonRect = main_menu_button.get_rect(topleft=(17, 550))

refresh_button = pygame.image.load("images/refresh_button.png")
refresh_buttonRect = refresh_button.get_rect(topleft=(500,10))
search_button = pygame.image.load("images/search_location_button.png")
search_buttonRect = search_button.get_rect(topleft=(360,10))
show_more_button = pygame.image.load("images/show_more_button.png")
show_more_buttonRect = show_more_button.get_rect()  # placeholder
hide_button = pygame.image.load("images/hide_button.png")
hide_buttonRect = hide_button.get_rect()  # placeholder

# Load Icon Images
sunrise_i = pygame.image.load("images/sunrise_icon.png")
sunset_i = pygame.image.load("images/sunset_icon.png")
UVI_i = pygame.image.load("images/UVI_icon.png")
pressure_i = pygame.image.load("images/pressure_icon.png")
humidity_i = pygame.image.load("images/humidity_icon.png")

# CREATE PAGES
def main_menu():
    # draw backgrounds
    screen.fill(BLACK)
    screen.blit(bkgd_menu, bkgd_menuRect)

# display Earth weather page
def earth_weather_display():
    global show_more_buttonRect
    #draw background
    screen.fill(BLACK)
    screen.blit(bkgd_earth, bkgd_earthRect)

    # draw buttons
    screen.blit(main_menu_button, main_menu_buttonRect)
    screen.blit(refresh_button, refresh_buttonRect)
    screen.blit(search_button, search_buttonRect)

    show_more_buttonRect = show_more_button.get_rect(topleft=(600, 125))
    screen.blit(show_more_button, show_more_buttonRect)

    # display_text(size, text, colour, x, y)
    font_col = BLACK
    display_text(150, earth_var["show_current_temp"], font_col, 40, 55)
    display_text(40, earth_var["show_current_temp_units"], font_col, 205, 65)
    display_text(25, earth_var["show_forecast"], font_col, 45, 200)
    display_text(20, earth_var["show_high"], WHITE, 80, 400)
    display_text(20, earth_var["show_low"], WHITE, 80, 460)

    display_text(20, f"Last Updated: {earth_var['show_update_time']}", font_col, 550, 20)
    display_text(60, earth_var["show_date"], font_col, 550, 55)

    display_text(16, earth_var['show_cloud_bh'], font_col, 395, 550)
    display_text(16, earth_var['show_cloud_type'], font_col, 600, 550)

    # update display
    pygame.display.update()

# Earth Weather Show More
def showMore():
    global hide_buttonRect
    # draw hide button
    hide_buttonRect = hide_button.get_rect(topleft=(565, 130))
    screen.blit(hide_button, hide_buttonRect)

    # icon reference positions
    ref_x = 565
    ref_y = 180
    icon_height = sunrise_i.get_height() + 10
    icon_width = sunrise_i.get_width() + 10

    # icon y-position
    sunrise_y = ref_y
    sunset_y = ref_y + icon_height
    UVI_y = ref_y + 2 * (icon_height)
    pressure_y = ref_y + 3 * (icon_height)
    humidity_y = ref_y + 4 * (icon_height)

    # create icon rects
    sunrise_iRect = sunrise_i.get_rect(topleft=(ref_x, sunrise_y))
    sunset_iRect = sunset_i.get_rect(topleft=(ref_x, sunset_y))
    UVI_iRect = UVI_i.get_rect(topleft=(ref_x, UVI_y))
    pressure_iRect = pressure_i.get_rect(topleft=(ref_x, pressure_y))
    humidity_iRect = humidity_i.get_rect(topleft=(ref_x, humidity_y))

    # draw weather MORE info icons on screen
    screen.blit(sunrise_i, sunrise_iRect)
    screen.blit(sunset_i, sunset_iRect)
    screen.blit(UVI_i, UVI_iRect)
    screen.blit(pressure_i, pressure_iRect)
    screen.blit(humidity_i, humidity_iRect)

    # text positions
    text_x = ref_x + icon_width
    sunrise_text_y = sunrise_y + 5
    sunset_text_y = sunset_y + 5
    UVI_text_y = UVI_y + 5
    pressure_text_y = pressure_y + 5
    humidity_text_y = humidity_y + 5

    # draw weather info text
    font_col = BLACK
    font_size = 16
    display_text(font_size, f"Sunrise: {earth_var['show_sunrise']}", font_col, text_x, sunrise_text_y)
    display_text(font_size, f"Sunset: {earth_var['show_sunset']}", font_col, text_x, sunset_text_y)
    display_text(font_size, f"UV Index: {earth_var['show_uvi']}", font_col, text_x, UVI_text_y)
    display_text(font_size, f"Pressure: {earth_var['show_pressure']}", font_col, text_x, pressure_text_y)
    display_text(font_size, f"Humidity: {earth_var['show_humidity']}", font_col, text_x, humidity_text_y)

# display Mars weather page
def mars_weather_display():
    global show_more_buttonRect
    #draw background
    screen.fill(BLACK)
    screen.blit(bkgd_mars, bkgd_marsRect)

    # draw buttons
    screen.blit(main_menu_button, main_menu_buttonRect)
    show_more_buttonRect = show_more_button.get_rect(topleft=(575, 195))
    screen.blit(show_more_button, show_more_buttonRect)

    # display_text(size, text, colour, x, y)
    font_col = WHITE
    display_text(18, "Latest Weather at", BLACK, 35, 20)
    display_text(50, "Gale Crater", BLACK, 30, 45)
    display_text(15, "The Curiosity Rover is collecting daily weather data", font_col, 30, 130)
    display_text(15, "at Gale Crater, located in the southern hemisphere", font_col, 30, 150)
    display_text(30, "Temperature", font_col, 30, 190)
    display_text(25, "AIR", font_col, 40, 250)
    display_text(20, f"High: {mars_var['show_high']}", font_col, 95, 310)
    display_text(20, f"Low: {mars_var['show_low']}", font_col, 95, 370)
    display_text(25, "GROUND", WHITE, 210, 250)
    display_text(20, f"High: {mars_var['show_high_grd']}", font_col, 295, 310)
    display_text(20, f"Low: {mars_var['show_low_grd']}", font_col, 295, 370)
    display_text(30, mars_var['show_forecast'], font_col, 40, 460)

    display_text(18, f"Last Updated: {mars_var['show_update_time']}", BLACK, 565, 20)
    display_text(65, f"Sol {mars_var['show_sol']}", font_col, 510, 55)
    display_text(20, f"Terrestrial Date: {mars_var['show_earth_date']}", font_col, 500, 130)
    display_text(20, f"Season: {mars_var['show_mars_season']}", font_col, 500, 160)

    # update display
    pygame.display.update()

# mars extra data
def marsMore():
    global hide_buttonRect
    # draw hide button
    hide_buttonRect = hide_button.get_rect(topleft=(530, 200))
    screen.blit(hide_button, hide_buttonRect)

    # icon reference positions
    ref_x = 530
    ref_y = 250
    icon_height = sunrise_i.get_height() + 10
    icon_width = sunrise_i.get_width() + 10

    # icon y-position
    sunrise_y = ref_y
    sunset_y = ref_y + icon_height
    UVI_y = ref_y + 2 * (icon_height)
    pressure_y = ref_y + 3 * (icon_height)

    # create icon rects
    sunrise_iRect = sunrise_i.get_rect(topleft=(ref_x, sunrise_y))
    sunset_iRect = sunset_i.get_rect(topleft=(ref_x, sunset_y))
    UVI_iRect = UVI_i.get_rect(topleft=(ref_x, UVI_y))
    pressure_iRect = pressure_i.get_rect(topleft=(ref_x, pressure_y))

    # draw weather MORE info icons on screen
    screen.blit(sunrise_i, sunrise_iRect)
    screen.blit(sunset_i, sunset_iRect)
    screen.blit(UVI_i, UVI_iRect)
    screen.blit(pressure_i, pressure_iRect)

    # text positions
    text_x = ref_x + icon_width
    sunrise_text_y = sunrise_y + 5
    sunset_text_y = sunset_y + 5
    UVI_text_y = UVI_y + 5
    pressure_text_y = pressure_y + 5

    # draw weather info text
    font_col = WHITE
    font_size = 18
    display_text(font_size, f"Sunrise: {mars_var['show_sunrise']}", font_col, text_x, sunrise_text_y)
    display_text(font_size, f"Sunset: {mars_var['show_sunset']}", font_col, text_x, sunset_text_y)
    display_text(font_size, f"UV Index: {mars_var['show_uvi']}", font_col, text_x, UVI_text_y)
    display_text(font_size, f"Pressure: {mars_var['show_pressure']}", font_col, text_x, pressure_text_y)

# App Display Loop Conditions
running = True
main_menu_page = True
earth_weather_page = False
mars_weather_page = False

# APP DISPLAY Loop
while running:
    # process user input
    events = pygame.event.get()  # creates a list of events detected in pygame
    for event in events:
        mouse = pygame.mouse.get_pos()  # get mouse position (x, y)

        if event.type == pygame.QUIT:
            running = False  # stop game and quite

        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse click!")
            menu_button_click = pygame.Rect.collidepoint(main_menu_buttonRect, mouse)
            more_button_click = pygame.Rect.collidepoint(show_more_buttonRect, mouse)
            hide_button_click = pygame.Rect.collidepoint(hide_buttonRect, mouse)

            # Main Menu Page
            if main_menu_page:
                # if mouse x position is between 0, 225, and mouse y position is between 77 and 523
                if 0 <= mouse[0] <= 225 and 77 <= mouse[1] <= 523:  # Earth Button
                    print("EARTH WEATHER")
                    main_menu_page = False
                    earth_weather_page = True
                    # get API Data
                    getLocation()
                    getWeather()
                    # draw earth weather page
                    earth_weather_display()

                elif 668 <= mouse[0] <= 800 and 169 <= mouse[1] <= 431:  # Mars button
                    print("MARS WEATHER")
                    main_menu_page = False
                    mars_weather_page = True
                    # get API Data
                    getMarsWeather()
                    # draw mars weather page
                    mars_weather_display()

            # Earth Page
            if earth_weather_page:
                search_button_click = pygame.Rect.collidepoint(search_buttonRect, mouse)
                refresh_button_click = pygame.Rect.collidepoint(refresh_buttonRect, mouse)
                if menu_button_click == True:  # main menu button overlaps with mouse pos
                    print("MAIN MENU, RETURN!!!")
                    earth_weather_page = False
                    main_menu_page = True
                elif search_button_click == True or refresh_button_click == True:
                    print("new city! or refresh!")
                    # retrieve new weather data
                    getLocation()
                    getWeather()
                    # print new weather data on screen
                    earth_weather_display()
                elif more_button_click == True:
                    print("Show more Earth weather")
                    showMore()
                elif hide_button_click == True:
                    print("Hide extra Earth info")
                    earth_weather_display()  

            # Mars Page
            if mars_weather_page:
                if menu_button_click == True:  # main menu button overlaps with mouse pos
                    print("MAIN MENU, RETURN!!!")
                    mars_weather_page = False
                    main_menu_page = True
                elif more_button_click == True:
                    print("Show more mars weather")
                    marsMore()
                elif hide_button_click == True:
                    print("Hide button clicked")
                    mars_weather_display()

    # draw the main menu
    if main_menu_page:
        main_menu()
    
    # draw the earth city search bar
    if earth_weather_page: 
        location_bar = pygame.Rect(20, 15, 330, 30)
        pygame.draw.rect(screen, WHITE, location_bar)
        textinput.update(events)
        screen.blit(textinput.get_surface(), (25, 20))
        pygame.display.update()

    # update display
    pygame.display.flip()

# quite pygame screen when we exit the app Loop
pygame.quit()