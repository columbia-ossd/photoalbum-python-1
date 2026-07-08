"""
Represents a photo album, i.e. a collection of photos
"""

from photo import Photo

class Album():
    def __init__(self, name):
        self.name = name
        self.photos = []

    def __iter__(self):
        # Returns an iterator for the photos list
        return iter(self.photos)

    def get_name(self):
        return self.name

    def add_photo(self, p):
        for photo in self.photos:
            if photo.get_description() == p.get_description() or photo.get_filename() == p.get_filename():
                return False
        self.photos.append(p)
        return True
    
    def remove_photo(self, p):
        for photo in self.photos:
            if photo.get_description() == p.get_description() or photo.get_filename() == p.get_filename():
                self.photos.remove(photo)
                return True    
        self.photos.pop(p)
        return True

    def get_photos(self):
        return self.photos
    
    def get_count(self):
        return len(self.photos)
    
    def get_tags(self):
        tags = []
        for photo in self.photos:
            for pt in photo.get_tags():
                if pt not in tags:
                    tags.append(pt)
        tags.sort()
        return tags 
    
    def __str__(self):
        res = "%s (%d photos) " % (self.name, self.get_count())
        for tag in self.get_tags():
            res = res + "#" + tag + " "
        return res
    

def main():
    album = Album("test album")
    album.add_photo(Photo("snoopy.gif", "Charlie Brown", "Snoopy", ["dog", "SNOOPY"]))
    album.add_photo(Photo("bluey.gif", "Bingo Heeler", "Bluey", ["dog", "bluey", "dancing"]))
    print(album)

    print(album.add_photo(Photo("snoopy2.gif", "Charlie Brown", "Snoopy", ["dog", "snoopy"])))
    print(album.add_photo(Photo("snoopy.gif", "Charlie Brown", "Snoopy2", ["dog", "snoopy"])))

if __name__ == "__main__":
    main()