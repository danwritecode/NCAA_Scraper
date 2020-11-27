import json
import requests
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    print(event)

    bpiData = getBPIData()

    try:
        bpiData = getBPIData()
    except Exception as e:
        return({
                "statusCode": 500,
                "body": json.dumps("Uh Oh, looks like something went wrong.")
            })
    else:
        return({
            "statusCode": 200,
            "body": json.dumps(bpiData)
        })

def getBPIData():
    # Create list to hold the entire data set after all looping is completed
    fullDataSet = []

    for page in range(7):
        URL = 'https://www.espn.com/mens-college-basketball/bpi/_/view/bpi/page/{}'.format(page+1)
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        # Target the bpi table and then extract all rows from that table
        tableDiv = soup.find(class_='bpi__table')
        tableRows = tableDiv.find_all('tr')


        # Establish mapping dictionary to map column headers to table values
        tableHeaderIndexMapping = {
            0: 'Rank',
            1: 'Team',
            2: 'Conference',
            3: 'W-L',
            4: 'BPI OFF',
            5: 'BPI DEF',
            6: 'BPI',
            7: '7-Day Change Rank'
        }

        # Create an empty list to hold the team data
        teamData = []

        # loop through all able rows
        for row in tableRows:
            rowValue = row.find_all('td')
            # Create empty dict that we'll add to in the next loop
            teamDict = {}
            for index, value in enumerate(rowValue):
                header = tableHeaderIndexMapping[index]
                teamDict[header] = value.text
            #Append dict to teamData list
            teamData.append(teamDict)

        fullDataSet += teamData

    return(fullDataSet)



