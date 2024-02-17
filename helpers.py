import pygame
from csv import reader
from os import walk

def import_csv_layout(path):
    """
    Import a CSV layout file and convert it into a list of lists representing the terrain map.

    Parameters:
    - path (str): The file path to the CSV layout file.

    Returns:
    - terrain_map (list): A list of lists representing the terrain map.
    """
    terrain_map = []
    with open(path) as level_map:
        #read the csv files and create a list of lists with the tile information
        layout = reader(level_map, delimiter = ",")
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map

def import_folder(path):
    """
    Import a folder containing images and return a list of surfaces.

    Parameters:
    - path (str): The folder path containing the images.

    Returns:
    - surface_list (list): A list of Pygame surfaces.
    """
    surface_list = []
    #returns the filepath, list of folders and list of files - need the files
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list