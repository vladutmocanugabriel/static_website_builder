import os
from src.textnode import *
from src.htmlnode import *
from src.helpers import *

def main():
    root = os.getcwd()
    public_path = os.path.join(root, "public")
    static_path = os.path.join(root, "static")  
    clean_public(public_path)
    copy_to_public(static_path, public_path)

main()