Can be used to extract all unique vehicles (and properties) from a set of roster files.

## Use
  - Place all of the txt/set files that you want to search in the FilestoEdit Folder
  - The input takes a set of searched regular expression patterns (To be Replaced in set/txt files) 
    - searchPattern is used as a placeholder for the vehicle name
    - outputFilePath is the file to which the hash table of vehicles is written
    - costPattern is the pattern used to find the cost
    - commentTrigger is used to tell the code to ignore the line where this is the first character
  - Annotate the files in the FilestoEdit Folder with '\[commentTrigger]\[sortClass string]' to create sorting blocks
    - The algorithm will try to find each sortClass in each file and create subhashes for each sort Class.
    - all items listed directly below an initiating commentTrigger will fall into the sortClass corresponding to that comment trigger
  - run main.py to search all roster files and extract a hash table of unique vehicles


## Usecases
  - To consolidate all possible vehicle unit entries in one hashtable for balancing and later: redistribution to the roster files.

## Data Storage Organization
  - the sortClass stores a list of all different classes of vehicles and all sort blocks used in the editted set/txt files.
    - the sortClasses all translate directly to sub hash tables within a master hash table of vehicle costs
    - In this case, the searched entries are categorized by unit types
  - the retrieved data in this case is vehicle unit entries with associated costs
    - this data will be generated as a 2 level hash table.
      - First level = sortClass
      - Second level = vehicle info

## Algorithm
  - Loops through all sort classes in the sortClass table
    - Loops through each set (equivalent to txt) file in the Editting Folder
      - Loops through the current file which will return each line in a string format
        1. Checks if the first character in the line is the commentTrigger, the algorithm identifies the sort classes on that line and 'isCollecting' mode is enabled
          - isCollecting mode is used to further check/collect all lines as the algorithm continues looping through the lines. When the loop encounters another commentTrigger, it is either disabled or its state is changed to collect for another subhash.
        2. On every line, the algorithm checks to see if it isCollecting. If so, it tries to find the vehicleNamePattern in the current line.
        - If found, it retrieves the name and the vehicle cost on the same line.
          - A callback is used to check to see if the vehicleNamePattern is already in the current subhashtable 
            - If not, it adds an entry

## Current Intrinsic Issues/Assumptions
  - Assumes that all similar entries between roster files have the same cost. The hash table stores the first one it gets.