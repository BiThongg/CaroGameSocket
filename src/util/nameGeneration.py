import uuid, json, random, string

def name_generation(length):
    characters = string.ascii_letters
    random_string = "".join(random.choices(characters, k=length))
    return random_string 
