import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
from datetime import datetime, timedelta
from urllib.parse import urlparse
import json
import math

folder = sys.argv[1]


def get_domain(url):
    return urlparse(url).netloc

def soft_add(dictionary, key, value):
    if key in dictionary:
        dictionary[key] += value
    else:
        dictionary[key] = value

def get_computer_usages():
    usages = {
            "Other": 0,
            "Firefox": {},
            "URxvt": {}
            }
    for line in open(folder + "/log", "r"):
        elements = line.strip().split(" ")
        if len(elements) == 1:
            usages["Other"] += 1.0 / 6.0            
        elif len(elements) >= 2:
            if elements[1] == "Firefox":
                if len(elements) == 2:
                    soft_add(usages["Firefox"], "Unknown", 1.0 / 6.0)
                else: 
                    domain = get_domain(elements[2])                
                    soft_add(usages["Firefox"], domain, 1.0 / 6.0)
            elif elements[1] == "URxvt":
                if len(elements) == 2:
                    soft_add(usages["URxvt"], "Unknown", 1.0 / 6.0)
                else:
                    working_directory = elements[2]
                    soft_add(usages["URxvt"], working_directory, 1.0 / 6.0)
            else:
                soft_add(usages, elements[1], 1.0 / 6.0)

    return usages

def get_usage_in_minutes(filename):
    return int(open(folder + "/" + filename, "r").read())

def get_sleeping_time():
    text_waking = open(folder + "/waking", "r").read().strip() + "AM"
    waking_time = datetime.strptime(text_waking, "%I:%M%p")

    text_sleeping = open(folder + "/sleeping", "r").read().strip() + "PM"
    sleeping_time = datetime.strptime(text_sleeping, "%I:%M%p")

    sleeping_minutes = ( (60 * 60 * 24) - (sleeping_time - waking_time).total_seconds()) / 60

    return sleeping_minutes

def get_depth(dictionary):
    max_depth = 0
    for key, value in dictionary.items():
        if type(value) is dict:
            max_depth = max(max_depth, get_depth(value))        
    return max_depth + 1

def sum_recursive_dictionary(dictionary):
    total = 0
    for key, value in dictionary.items():
        if type(value) is dict:
            total += sum_recursive_dictionary(value)
        else:
            total += value

    return total

def values_at_depth(dictionary, depth):
    result = {}
    if depth == 0:
        for key, value in dictionary.items():
            if type(value) is dict:
                result[key] = sum_recursive_dictionary(value)
            else:
                if value > 0:
                    result[key] = value
    else:
        for key, value in dictionary.items():
            if type(value) is dict:
                result.update(values_at_depth(value, depth - 1))
            else:
                if value > 0:
                    result[key] = value

    return result


def pi_chart_from_usages(usages):
    unaccounted = 60 * 24 - sum_recursive_dictionary(usages)
    
    usages["Unaccounted"] = unaccounted
    depth = get_depth(usages)
    wedge_width = 1 / (depth + 1)

    fig, ax = plt.subplots()

    colors = []

    total_patches = []
    total_texts = []

    def on_mouse_move(event):
        for patch in total_patches:
            index = total_patches.index(patch)
            if patch.contains_point((event.x, event.y)):
                total_texts[index].set_visible(True)
            else:
                total_texts[index].set_visible(False)
        plt.draw()
            



    for level in range(depth):
        chart_dictionary = values_at_depth(usages, level)
        labels = list(chart_dictionary.keys())
         
        values = list(chart_dictionary.values())
        npvalues = list(chart_dictionary.values())
        levels_colors = []
        for index in range(len(values)):
            color = matplotlib.colors.hsv_to_rgb((index / len(values), 1 - level / (depth + 1), 1))
            levels_colors.append(color)

        patches, texts = ax.pie(npvalues, labels=labels, colors=np.array(levels_colors), radius=1-level*wedge_width, wedgeprops=dict(width=wedge_width), textprops=dict(visible=False))
        total_patches.extend(patches)
        total_texts.extend(texts)

    ax.set(aspect="equal", title='Time allocations')
    fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)
    plt.show()


usages = {}

usages.update({
    "P": {
        **get_computer_usages(),
        "Teaching": {
            "Tutoring": get_usage_in_minutes("tutoring")
        },
        "Meetings": get_usage_in_minutes("meeting")
    }})
usages.update({
        "PC": {
                "Reading": {
                    "Audible": get_usage_in_minutes("audible"),
                    "Physical": get_usage_in_minutes("reading")
                },
                "Bathroom": {
                    "Shower": get_usage_in_minutes("shower"),
                    "Teeth": get_usage_in_minutes("brushing_teeth"),
                    "Shaving": get_usage_in_minutes("shaving")
                },
                "Cleaning": {
                    "Dishes": get_usage_in_minutes("dishes")
                },
                "Exercise": {
                    "Weightlifting": get_usage_in_minutes("weightlifting"),
                    "Running": get_usage_in_minutes("running"),
                    "Plank": get_usage_in_minutes("plank")
                },
                "Eating": {
                    "Breakfast": get_usage_in_minutes("breakfast"),
                    "Lunch": get_usage_in_minutes("lunch"),
                    "Dinner": get_usage_in_minutes("dinner")
                },
                "Driving": get_usage_in_minutes("driving"),
                "Music": get_usage_in_minutes("music"),
                "Meditation": get_usage_in_minutes("meditating")
        },
        "Sleeping": get_sleeping_time()
        })

print(json.dumps(usages))
pi_chart_from_usages(usages)
