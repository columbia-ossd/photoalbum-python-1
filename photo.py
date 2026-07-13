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

    global_filename = "dogs.txt"

    def edit_tags(self, new_tags_list):
        self.tags = []
        for tag in new_tags_list:
            self.tags.append(tag)
        else:
            with open(self.global_filename, "r") as input_file:
                lines = input_file.readlines()
                for index, line in enumerate(lines):
                    parts = line.split(",")
                    fname = parts[0]
                    if fname == self.filename: #Find the right line to edit
                        new_line = ""
                        for x in range(3): #Add all parts of line before tag as is
                            new_line += (parts[x] + ",")
                        for tags_index, tag in enumerate(new_tags_list):                            
                            if tags_index != len(new_tags_list) - 1: #If not the last tag in list, add tag + ","
                                new_line += (tag + ",")
                            else:
                                new_line += (tag + "\n") #If last tag, add tag and newline
                        lines[index] = new_line
                        break
            with open(self.global_filename, "w") as output_file: #Edit tags in input file                        
                output_file.writelines(lines)
        return
                                        

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