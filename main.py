# Imports
import fileinput
import re
import os

# ----------------------------------------------------------------------------
# Input Variables

# Replacement pattern order must match the order of replacement text below
# Include all english characters and english special characters (without space)
# vehicleNamePattern = r'{"[a-zA-z0-9~@#$^*()_+=[\]{}|\\,.?:-]+"'
vehicleNamePattern = r'[a-zA-z0-9~@#$^*()_+=[\]|\\,.?:-]+'
outputFilePath = r'.\output.txt'

costPattern = r'cost [0-9]+'

commentTrigger = ';'

# ----------------------------------------------------------------------------
# Variables
# Sorting classes
sortClasses = {
    'lightmgcar': ["c(15)", "cp(3)", "b(v1)"],
    'heavymgcar': ["c(15)", "cp(5)", "b(v1)"],
    'transport': ["c(5)", "cp(2)", "b(v1)"],
    'logi': ["c(15)", "cp(2)", "b(v1)"],
    'emplacements': ["c(5)", "cp(5)", "b(v2)"],
    'hmg': ["c(5)", "cp(5)", "b(v2)"],
    'minigun': ["c(5)", "cp(5)", "b(v2)"],
    'gl': ["c(5)", "cp(5)", "b(v2)"],
    'field_artillery': ["c(5)", "cp(5)", "b(v2)"],
    'mortar': ["c(5)", "cp(5)", "b(v2)"],
    'aa_gun': ["c(5)", "cp(5)", "b(v2)"],
    'atgm': ["c(5)", "cp(5)", "b(v2)"],
    'at_gun': ["c(5)", "cp(5)", "b(v2)"],
    'light_mortar_spg': ["c(15)", "cp(10)"],
    'lightspgarty': ["c(20)", "cp(15)", "b(v2)"],
    'heavyspgarty': ["c(30)", "cp(20)", "b(v2)"],
    'lightrocketarty': ["c(30)", "cp(15)", "b(v2)"],
    'heavyrocketarty': ["c(30)", "cp(20)", "b(v2)"],
    'light_apc': ["c(5)", "cp(0)", "b(v3)"],
    'medium_wheeled_apc': ["c(10)", "cp(5)", "b(v3)"],
    'heavy_apc': ["c(20)", "cp(10)", "b(v3)"],
    'spg_aa': ["c(15)", "cp(10)", "b(v3)"],
    'medium_tank': ["c(15)", "cp(15)", "b(v4)"],
    'cold_war_tank': ["c(25)", "cp(15)", "b(v4)"],
    'heavy_cold_war_tank': ["c(30)", "cp(20)", "b(v4)"],
    'heavy_modern_war_tank': ["c(35)", "cp(25)", "b(v4)"],
    'very_heavy_modern_war_tank': ["c(40)", "cp(30)", "b(v4)"],
    'tank_destroyer': ["c(15)", "cp(10)", "b(v5)"],
    'aircraft': ["c(60)", "cp(20)", "b(special)"],
    'light_robot_mech': ["c(40)", "cp(10)", "b(v4)"],
}

# List of vehicles default
vehicleCostHashByUnit = {
}
# isCollecting trigger for enable line to be added to hash table. False by default
isCollecting = False
fileToSearchDirectory = r'.\FilesToSearch'

# ----------------------------------------------------------------------------
# Helpers
# Formatting Helper: Gets filePath from file Name and Directory


def getFilePath(fileDirectory, fileName):
    return r'{filePath}\{fileName}'.format(filePath=fileDirectory, fileName=fileName)

# Find vehicleNamePattern in currentLine and return it


def foundPatternInLine(text_to_search):
    # Find pattern in the current line
    stringPatternMatch = re.findall(text_to_search, line)
    # If pattern matches, return the matched name otherwise return nothing
    if stringPatternMatch:
        return stringPatternMatch
    else:
        return None

# Find Check to see if stringPatternMatch pattern is already in Hash table and add if it is not


def checkUpdateHash(stringPatternMatch, costValue):
    # Debugging
    print("stringPatternMatch", stringPatternMatch, "\n")
    # print("Type: ", type(stringPatternMatch), "\n\n")
    # print("vehicleCostHashByUnit", vehicleCostHashByUnit, "\n")
    # print("Type: ", type(vehicleCostHashByUnit), "\n\n")

    # If already in hash, do not add anything
    if stringPatternMatch in vehicleCostHashByUnit:
        print('Vehicle Already in Table')
    else:
        # Adds vehicle entry to hash table if not in table
        vehicleCostHashByUnit[stringPatternMatch] = costValue


# Formatted write resulting hashtable to output
def writeOutput(outputText):
    # Open output file
    d = open(outputFilePath, 'w')
    # Write start
    d.write("{\n")
    # Write formatted inner contents
    for entry in vehicleCostHashByUnit:
        # Format handling
        if type(vehicleCostHashByUnit[entry]) == list:
            rawCost = vehicleCostHashByUnit[entry][0]
            rawCost = re.findall(r'[0-9]+', rawCost)[0]
        else:
            rawCost = vehicleCostHashByUnit[entry]
        d.write('{}: {},\n'.format(entry, rawCost))
    # Write end
    d.write("}")


# Main Code
for sortClass in sortClasses:
    print('\n\ncurrent sortClass = ', sortClass)
    vehicleCostHashByUnit[sortClass] = {}
    print('\n\nInitialize subhash in vehicleCostHashByUnit = ',
          vehicleCostHashByUnit)
    for fileName in os.listdir(fileToSearchDirectory):
        # Get filePath for fileinput
        filePath = getFilePath(fileToSearchDirectory, fileName)
        with fileinput.FileInput(filePath) as file:
            for line in file:
                # If line starts with comment Trigger
                if line[0] == commentTrigger:
                    # If runs into the sortClass on that line
                    if re.findall(sortClass, line):
                        # Activate collecting mode to search lines
                        isCollecting = True
                        # continue off of the comment line to prevent search of comment line
                        continue
                    else:
                        # Turns off collection mode when it runs into another comment
                        isCollecting = False

                # isCollecting must be true AND line must not start with comment trigger to search and possibly list in hash
                if isCollecting == True and line[0] != commentTrigger:
                    # Get vehicle name from searching line helper
                    stringPatternMatch = foundPatternInLine(vehicleNamePattern)

                    # If vehicle name is found in that line exists
                    if stringPatternMatch:
                        # Get costValue
                        # Cost will always accompany string match
                        costPatternMatch = re.findall(costPattern, line)

                        # Check and maybe Update Hash table with info
                        checkUpdateHash(
                            stringPatternMatch[0], costPatternMatch)


# def getSortClassEntries():

# Print final resulting table
# print("EndResult = ", vehicleCostHashByUnit)
# writeOutput(vehicleCostHashByUnit)
