import requests
import json
import os

def readFile(fileName):
    fileObj = open(fileName, "r")
    lines = fileObj.read().splitlines()
    fileObj.close()
    return lines

def writeFile(fileName, line):
    fileObj = open(fileName,"a")
    fileObj.write(line)
    fileObj.close()

## Its the name you see when you browse to the twitch url of the streamer
USER_ID = "ProfessorSexton"

## First setup your application on your dashboard.
## here: https://dev.twitch.tv/console
## then click "Register Your Application" on the right hand side.
## For the oauth 9redirect just write: http://localhost
## Make note of 8your Client ID
## Finvzvxcbv><}rst get a local access token. 
## Make note of your Client Secret 
CLIENT_ID = "bnma30adlewbo9q7fb7msokcgidxlz" 
SECRET = "bbf0qk25vnss8fm67xzith63e51slr"

## First get a local access token. 
secretKeyURL = "https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials".format(CLIENT_ID, SECRET)
responseA = requests.post(secretKeyURL)
accessTokenData = responseA.json()

## Then figure out the user id. 
userIDURL = "https://api.twitch.tv/helix/users?login=%s"%USER_ID
responseB = requests.get(userIDURL, headers={"Client-ID":CLIENT_ID,
                                                'Authorization': "Bearer "+accessTokenData["access_token"]})
userID = responseB.json()["data"][0]["id"]


## Now you can request the video clip data.
findVideoURL = "https://api.twitch.tv/helix/videos?user_id=%s"%userID
responseC= requests.get(findVideoURL, headers={"Client-ID":CLIENT_ID,
                                                'Authorization': "Bearer "+accessTokenData["access_token"]})
channelData = responseC.json()  

## Get a list of all of the urls on the channel and add them to an array
data = channelData.get('data')
videoUrls = [] 

for entry in data: videoUrls.append(entry.get("url"))

## Read a text document that saves the urls of the videos you've already downloaded

downloaded = readFile('downloadedvideos.txt')

## Finds the difference between what's on the channel and what you've downloaded 
#  Then downloads the difference if there is one. 

difference = list(set(videoUrls)-set(downloaded))

if len(difference) == 0: print("You have all of the videos downloaded")

else:
    print('Downloading: ' + len(difference) + ' videos')
    
    for video in difference:
        cmd  = 'youtube-dl '+ video
        os.system(cmd)
        writeFile('downloadedvideos.txt', video)
