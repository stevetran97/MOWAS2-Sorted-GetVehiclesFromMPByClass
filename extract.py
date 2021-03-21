# Imports
import fileinput
import re
import os

# ----------------------------------------------------------------------------
# Input Variables

# Vehicle name pattern to identify vehicle unit on line
# Include all english characters and english special characters (without space)
vehicleNamePattern = r'\"[a-zA-z0-9~@#$^*()_+=[\]|\\,.?:-]+\"'
print("vehicleNamePattern = ", vehicleNamePattern)
outputFilePath = r'.\vehicleList.txt'

costPattern = r'cost [0-9]+'

# Group marker must start and end with comment trigger
commentTrigger = ';'

# ----------------------------------------------------------------------------
# Variables
# Sorting classes
sortClasses = {
    'lightmgcar',
    'heavymgcar',
    'transport',
    'logi',
    'emplacements',
    'hmg',
    'minigun',
    'gl',
    'field_artillery',
    'mortar',
    'aa_gun',
    'atgm',
    'at_gun',
    'light_mortar_spg',
    'lightspgarty',
    'heavyspgarty',
    'lightrocketarty',
    'heavyrocketarty',
    'light_apc',
    'medium_wheeled_apc',
    'heavy_apc',
    'spg_aa',
    'medium_tank',
    'cold_war_tank',
    'heavy_cold_war_tank',
    'heavy_modern_war_tank',
    'very_heavy_modern_war_tank',
    'tank_destroyer',
    'aircraft',
    'light_robot_mech'
}

# Instantiate List of vehicles
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
def findPatternInLine(text_to_search):
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
        print('Added Vehicle to Table: {}'.format(stringPatternMatch))


# Formatted write resulting hashtable to output
def writeOutput(outputText):
    # Open output file
    d = open(outputFilePath, 'w')
    # Sort all values in all subhashes and replace working main hash table
    for sortClass in vehicleCostHashByUnit:
        vehicleCostHashByUnit[sortClass] = sortHashAlphab(
            vehicleCostHashByUnit[sortClass])

    # Write from each sortClass
    for sortClass in vehicleCostHashByUnit:
        # Write python comment denoting vehicle Class
        d.write('\n#{}\n'.format(sortClass))
        # Write first half of vehicle Class hash table format
        d.write('"%s" : {\n' % (sortClass))

        # Write from subhash
        for entry in vehicleCostHashByUnit[sortClass]:
            # Format handling (Currently Redundant due to txt file preformatting)
            if type(vehicleCostHashByUnit[sortClass][entry]) == list:
                rawCost = vehicleCostHashByUnit[sortClass][entry][0]
                rawCost = re.findall(r'[0-9]+', rawCost)[0]
            else:
                rawCost = vehicleCostHashByUnit[sortClass][entry]
            d.write('\t{}: {},\n'.format(entry, rawCost))
        # Write second half of vehicle Class hash table format
        d.write('},')


# Sorts any hashTable alphabetically and returns sorted hash table
def sortHashAlphab(hashTable):
    sortedKeys = sorted(hashTable)
    newSortedHash = {}
    for key in sortedKeys:
        newSortedHash[key] = hashTable[key]
    return newSortedHash


# ----------------------------------------------------------------------------
# Main Code/ Algorithm
# Loops through all files multiple times (One sort class for one round)
for sortClass in sortClasses:
    # Initialize vehicle class subhash
    vehicleCostHashByUnit[sortClass] = {}
    # Loop through files in edit directory
    for fileName in os.listdir(fileToSearchDirectory):
        # Get filePath for fileinput
        filePath = getFilePath(fileToSearchDirectory, fileName)
        with fileinput.FileInput(filePath) as file:
            for line in file:
                # If line starts with comment Trigger
                if line[0] == commentTrigger:
                    # If loop runs into the sort Class on that line (Must start/end with comment trigger)
                    if re.findall(';{};'.format(sortClass), line):
                        # Activate collecting mode to search lines
                        isCollecting = True
                        # continue off of the comment line to prevent search of comment line
                        continue
                    else:
                        # Turns off collection mode when it runs into another comment without class
                        isCollecting = False

                # isCollecting must be true AND line must not start with comment trigger to search and possibly list in hash
                if isCollecting == True and line[0] != commentTrigger:
                    # Get vehicle name (in array) from pattern finding helper
                    stringPatternMatch = findPatternInLine(vehicleNamePattern)

                    # If vehicle name is found in that line exists
                    if stringPatternMatch:
                        # Get formatted cost parameter: Cost will always accompany string match in this case
                        costPatternMatch = re.findall(costPattern, line)
                        # Extract/ Format to integer and remove string parts
                        formattedCost = int(re.findall(
                            r'[0-9]+', costPatternMatch[0])[0])

                        # Check then Update Hash table with new entry
                        checkUpdateHash(
                            stringPatternMatch[0], formattedCost)
            # Reset isCollecting mode to default at end of file (Redundancy)
            isCollecting = False

# Print final resulting table
writeOutput(vehicleCostHashByUnit)
