import os
from PyPDF2 import PdfFileMerger, PdfFileReader
from os.path import expanduser
from typing import *


DEV_PDFS = "./pdfs"
DEV_MODE = True


def merge_pdfs(files: List[object], path_of_dir: str) -> bool:
    """
    Merges the PDFS together.
    Return true if the files were successfully merged, false otherwise.
    """
    choice = input("What order would you like to merge the files in? Please type the corresponding number of your choice:\n(1)Some or all in a custom order (ex. 132 (first, then third, then second)) \n(2)All PDFs in the way they appear in the directory\n(3)All PDFS from Oldest to newest(4)All PDFs Alphabetically\n(5)All PDFs from Newest to Oldest\n")
    merger = PdfFileMerger()
    
    if(choice.strip() in ['1', '(1)']):
        order = input("Specify an order to merge in: (for example, \"132\")")
        try:
            int(order)
        except:
            print("Error! Please try again")
            choice = input("What order would you like to merge the files in? Please type the corresponding number of your choice:\n(1)Some or all in a custom order (ex. 132 (first, then third, then second)) \n(2)All PDFs in the way they appear in the directory\n(3)All PDFS from Oldest to newest(4)All PDFs Alphabetically\n(5)All PDFs from Newest to Oldest\n")
        
        for char in order:
            if 1 <= int(char) <= len(files):
                merger.append(PdfFileReader(files[int(char) - 1], strict=False))
            else:
                print("Error! Please try again!")
                return False
            

        name = input("Success! Please choose a name for your new file: ")
        if not name.endswith(".pdf"):
            name += ".pdf"
        merger.write(path_of_dir + "/" + name)

        




 



if __name__ == "__main__":
    if(not DEV_MODE):
        path_of_dir = input("Input the path of the directory which contains the pdfs you would like to use: ")
    else:
        path_of_dir = DEV_PDFS
        home = expanduser("~")

        if "~" in path_of_dir:
            path_of_dir = path_of_dir.replace("~", home)

    print("Files found: ")
    # create the file objects
    pdf_files = []
    for filename in os.listdir(path_of_dir):
        if filename.endswith(".pdf"):
            try:
                print("\t" + filename)
                pdf_files.append(open(path_of_dir + "/" + filename, "rb"))
            except:
                print("Error creating file object for file " + filename)

    
    merge_pdfs(pdf_files, path_of_dir)

        


    

    

    






