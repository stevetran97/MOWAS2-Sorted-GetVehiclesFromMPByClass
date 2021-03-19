# Imports
import fileinput
import re
import os

# ----------------------------------------------------------------------------
# Input Variables

# Replacement pattern order must match the order of replacement text below
# Include all english characters and english special characters (without space)
# vehicleNamePattern = r'{"[a-zA-z0-9~@#$^*()_+=[\]{}|\\,.?:-]+"'
vehicleNamePattern = r'\"[a-zA-z0-9~@#$^*()_+=[\]|\\,.?:-]+\"'
print("vehicleNamePattern = ", vehicleNamePattern)
outputFilePath = r'.\vehicleList.txt'

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
    print("Checking stringPatternMatch = ", stringPatternMatch, "\n")

    # If already in subhash, do not add anything
    if stringPatternMatch in vehicleCostHashByUnit[sortClass]:
        print('Vehicle Already in Table: {}'.format(stringPatternMatch))
    else:
        # Adds vehicle entry to hash table if not in table
        vehicleCostHashByUnit[sortClass][stringPatternMatch] = costValue


# Formatted write resulting hashtable to output
def writeOutput(outputText):
    # Open output file
    d = open(outputFilePath, 'w')
    # Sort all values in all subhashes
    for sortClass in vehicleCostHashByUnit:
        vehicleCostHashByUnit[sortClass] = sortHashAlphab(
            vehicleCostHashByUnit[sortClass])

    # Write from each sortClass
    for sortClass in vehicleCostHashByUnit:
        d.write('\n#{}\n'.format(sortClass))
        # Write from subhash
        for entry in vehicleCostHashByUnit[sortClass]:
            # Format handling
            if type(vehicleCostHashByUnit[sortClass][entry]) == list:
                rawCost = vehicleCostHashByUnit[sortClass][entry][0]
                rawCost = re.findall(r'[0-9]+', rawCost)[0]
            else:
                rawCost = vehicleCostHashByUnit[sortClass][entry]
            d.write('{}: {},\n'.format(entry, rawCost))

# Sorts any hashTable alphabetically and returns sorted hash table


def sortHashAlphab(hashTable):
    sortedKeys = sorted(hashTable)
    newSortedHash = {}
    for key in sortedKeys:
        newSortedHash[key] = hashTable[key]
    return newSortedHash


# ----------------------------------------------------------------------------
# Main Code/ Algorithm
for sortClass in sortClasses:

    vehicleCostHashByUnit[sortClass] = {}
    print('\n\nInitialize subhash in {} = '.format(sortClass),
          vehicleCostHashByUnit[sortClass])
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
                        # format to integer and remove string parts
                        formattedCost = int(re.findall(
                            r'[0-9]+', costPatternMatch[0])[0])

                        # Check and maybe Update Hash table with info
                        checkUpdateHash(
                            stringPatternMatch[0], formattedCost)


# Print final resulting table
writeOutput(vehicleCostHashByUnit)


# print('\n\nInitialize mainhash in vehicleCostHashByUnit = ',
#       vehicleCostHashByUnit)
# print("Type: ", type(stringPatternMatch), "\n\n")
# print("vehicleCostHashByUnit", vehicleCostHashByUnit, "\n")
# print("Type: ", type(vehicleCostHashByUnit), "\n\n")
# print('\n\ncurrent sortClass = ', sortClass)
# print("EndResult = ", vehicleCostHashByUnit)
# print('\n\nFinal mainhash in = ',
#       vehicleCostHashByUnit)

# print('\n\nFinal subhash in {} = '.format(sortClass),
#         vehicleCostHashByUnit[sortClass])

# print("Unsorted lightmgcar Hash = ",
#       vehicleCostHashByUnit["lightmgcar"])
# print("Sorted lightmgcar Hash = ", sorted(
#     vehicleCostHashByUnit["lightmgcar"]))
# print("sortHashAlphab Function = ", )
