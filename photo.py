"""
Represents a single photo in the album
"""

class Photo():
    def __init__(self, filename, creator, description, tags):
        self.filename = filename
        self.creator = creator
        self.description = description
        self.tags = []
        for tag in tags:
            self.tags.append(tag.lower())

    def get_filename(self):
        return self.filename
    
    def get_creator(self):
        return self.creator
    
    def get_description(self):
        return self.description
    
    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def get_tags(self):
        return self.tags


    def __str__(self):
        val = "%s, created by %s " % (self.description, self.creator)
        for tag in self.tags:
            val = val + " #" + tag
        return val
    
def main():
    p = Photo("snoopy.gif", "chris", "Snoopy", ["dog", "SNOOPY"])
    print(p)

if __name__ == "__main__":
    main()