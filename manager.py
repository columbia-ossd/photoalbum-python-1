import os

from photo import Photo
from album import Album
from graphics import *

def get_value_between(prompt, low, high):
    choice = int(input(prompt))
    while choice < low or choice > high:
        print("Please enter a value between %d and %d" % (low, high))
        choice = int(input(prompt))
    return choice


def initialize(filename, title):
    album = Album(title)

    fp = open(filename, "r")

    for line in fp:
        line = line.strip()
        parts = line.split(",")
        fname = parts[0]
        creator = parts[1]
        description = parts[2]
        tags = []
        for i in range(3, len(parts)):
            tags.append(parts[i])
        album.add_photo(Photo(fname, creator, description, tags))

    fp.close()

    return album

def save_album(album, filename):
    """
    Write all photo information in the album back to the input file.
    """
    with open(filename, "w") as fp:
        for photo in album.get_photos():
            values = [
                photo.get_filename(),
                photo.get_creator(),
                photo.get_description()
            ]
            values.extend(photo.get_tags())
            fp.write(",".join(values) + "\n")

def menu():
    print()
    print("1: List all photos")
    print("2: Add a photo")
    print("3: Search photos by tag")
    print("4: View a photo")
    print("5: Edit photo info")
    print("6: Exit")

    choice = get_value_between("Choose an option: ", 1, 6)

    return choice


def viewPhoto(album):
    """
    Function for Menu Option 4
    """
    print()
    photos = album.get_photos()
    for i in range(len(photos)):
        print("%d: %s"  % (i+1, photos[i].get_description()))
    choice = get_value_between("Choose a photo: ", 1, len(photos))
    
    name = photos[choice-1].get_filename()
    display_image(name)

def display_image(name):
    """
    Helper function that we provide
    """
    try:
        image = Image(Point(250, 250), name)
        win = GraphWin(name, image.getWidth(), image.getHeight())
        win.setCoords(0, 0, 500, 500)
        image.draw(win)
        try:
            win.getMouse()
            win.close()
        except:
            pass
    except:
        print("An error occurred trying to open %s" % name)


def searchByTag(album):
    """
    Function for Menu Option 3
    """
    print()
    tags = " ".join(album.get_tags())
    print("Here are the tags: " + tags)
    term = input("Enter the tag to search for: ").lower()
    found = []
    for photo in album.get_photos():
        if term in photo.get_tags():
            found.append(photo)
    if len(found) > 0:
        print("Here are the photos for that tag:")
        for photo in found:
            print(str(photo))
    else:
        print("No photos found for tag " + term)
    

def get_input(prompt):
    resp = ""
    while len(resp.strip()) == 0:
        resp = input(prompt)  
    return resp      


def addPhoto(album):
    """
    Function for Menu Option 2
    """
    print("Add Photo")
    fname = get_input("Enter the name of the file: ")
    creator = get_input("Enter the name of the creator: ")
    description = get_input("Enter the description: ")
    tagString = input("Enter all the tags, separated by spaces: ")
    tags = tagString.split(" ")
    #print(tags)
    if album.add_photo(Photo(fname, creator, description, tags)):
        print("Photo successfully added")
    else:
        print("Could not add photo to album")

def editPhoto(album, input_filename):
    """
    Allow the user to edit a photo's filename, creator,
    and description, then save the updated album.
    """
    photos = album.get_photos()

    if len(photos) == 0:
        print("There are no photos to edit.")
        return

    print()
    print("Edit Photo")

    for i in range(len(photos)):
        print("%d: %s" % (i + 1, photos[i].get_description()))

    choice = get_value_between(
        "Choose a photo to edit: ",
        1,
        len(photos)
    )

    photo = photos[choice - 1]

    print("Press Enter to keep the current value.")

    while True:
        new_filename = input(
            "Filename [%s]: " % photo.get_filename()
        ).strip()

        if new_filename == "":
            new_filename = photo.get_filename()

        if os.path.isfile(new_filename):
            break

        print("The photo file does not exist. Please enter a valid filename.")

    new_creator = input(
        "Creator [%s]: " % photo.get_creator()
    ).strip()

    if new_creator == "":
        new_creator = photo.get_creator()

    new_description = input(
        "Description [%s]: " % photo.get_description()
    ).strip()

    if new_description == "":
        new_description = photo.get_description()

    photo.set_filename(new_filename)
    photo.set_creator(new_creator)
    photo.set_description(new_description)

    save_album(album, input_filename)

    print("Photo information successfully updated.")


def main():
    input_filename = "dogs.txt"
    album = initialize(input_filename, "cartoon dog photos")

    choice = -1

    while choice != 6:
        choice = menu()

        if choice == 1:  # list all photos
            for photo in album.get_photos_sorted_by_description():
                print(str(photo))

        elif choice == 2:  # add a photo
            addPhoto(album)

        elif choice == 3:  # search by tag
            searchByTag(album)

        elif choice == 4:  # view a photo
            viewPhoto(album)

        elif choice == 5:  # edit photo info
            editPhoto(album, input_filename)

    print("Good bye!")


if __name__ == "__main__":
    main()