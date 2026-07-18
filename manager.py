import os
import sys

from photo import Photo
from album import Album
from graphics import *

def get_value_between(prompt, low, high):
    while True:
        try:
            orig = input(prompt)
        except KeyboardInterrupt:
            print("\nInput interrupted. Please try again.")
            continue
        try:
            choice = int(orig)
        except ValueError:
            print("Invalid input. Please enter an integer.")
        else:
            if low <= choice <= high:
                return choice
            else:
                print("Please enter a value between %d and %d" % (low, high))


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
    print("3: Search photos by tag(s)")
    print("4: View a photo")
    print("5: Edit photo info")
    print("6: Remove a photo")
    print("7: Edit a photo's tags")
    print("8: Exit")

    choice = get_value_between("Choose an option: ", 1, 8)

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
    terms = input("Enter the tag(s) to search for, separated by spaces: ").lower().split()

    if len(terms) == 0:
        print("No tags entered")
        return

    matched_all = []
    matched_some = []
    for photo in album.get_photos():
        matches = 0
        for term in terms:
            if term in photo.get_tags():
                matches = matches + 1
        if matches == len(terms):
            matched_all.append(photo)
        elif matches > 0:
            matched_some.append(photo)

    if len(matched_all) == 0 and len(matched_some) == 0:
        print("No photos found for: " + " ".join(terms))
        return

    if len(matched_all) > 0:
        if len(terms) > 1:
            print("Here are the photos with all of those tags:")
        else:
            print("Here are the photos for that tag:")
        for photo in matched_all:
            print(str(photo))

    if len(matched_some) > 0:
        print("Here are the photos with some of those tags:")
        for photo in matched_some:
            print(str(photo))



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

def removePhoto(album, filename):
    """
    Allow the user to remove a photo from the album, then save the updated album.
    """
    photos = album.get_photos()

    if len(photos) == 0:
        print("There are no photos to remove.")
        return

    print()
    print("Remove Photo")

    for i in range(len(photos)):
        print("%d: %s" % (i + 1, photos[i].get_description()))

    choice = get_value_between(
        "Choose a photo to remove: ",
        1,
        len(photos)
    )

    photo = photos[choice - 1]

    confirm = input("Are you sure you want to delete %s? (y/n) "
                     % photo.get_description()).strip().lower()
    if confirm != "y":
        print("Cancelled. No photo was removed.")
        return

    if album.remove_photo(photo):
        save_album(album, filename)
        print("Photo successfully removed.\n")
        for photo in album.get_photos():
            print(str(photo))

    else:
        print("Could not remove photo from album.")

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

def editTagsAlbum(album, input_filename):
    """
    Function for Menu Option 5
    """
    print()
    photos = album.get_photos()
    for i in range(len(photos)):
        print("%d: %s"  % (i+1, photos[i].get_description()))
    choice = get_value_between("Choose a photo to edit tags: ", 1, len(photos))
    chosen_photo = photos[choice - 1]
    new_tag_set = input("Enter the new tags for this photo, separated by commas: ").lower()
    new_tag_list = new_tag_set.split(",")
    cleaned_new_tag_list = []
    for tag in new_tag_list:
        if tag.strip():
            cleaned_new_tag_list.append(tag)
    chosen_photo.edit_tags(cleaned_new_tag_list, input_filename)
    new_photo_tags = chosen_photo.get_tags()
    print("Tags edited!")
    print("New tags: ", new_photo_tags)


def main():
    if len(sys.argv) > 1:
        input_filename = sys.argv[1]
    else:
        input_filename = input("Enter the input file name: ")

    while True:
        try:
            album = initialize(
                input_filename,
                "cartoon dog photos"
            )
            break
        except OSError:
            print("The file could not be read.")
            input_filename = input("Enter the input file name: ")

    choice = -1

    while choice != 8:
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
        
        elif choice == 6: # remove a photo
            removePhoto(album, input_filename)

        elif choice == 7: # edit a photo's tags
            editTagsAlbum(album, input_filename)


    print("Good bye!")


if __name__ == "__main__":
    main()