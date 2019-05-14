from django.shortcuts import render
import requests
from .models import APIRequest, Bets
import datetime
from django.views.generic import ListView



def boolTimeComp(str):

    # True Means Game Is Still Active
    # False Game Has completed

    hour_now = int(datetime.datetime.now().hour) # for hour
    minute_now = int(datetime.datetime.now().minute) # for minute

    hour = int(str[:2])
    minute = int(str[3:5])
    
    if hour > hour_now:
        return True
    elif hour == hour_now: 
        if minute > minute_now:
            return True
    return False 
    

def boolDateComp(str):
    year = int(str[:4])
    month = int(str[5:7])
    day = int(str[8:])

    year_now = int(datetime.datetime.now().year())
    month_now = int(datetime.datetime.now().month())
    day_now = int(datetime.datetime.now().day())

    if year > year_now:
        return {'result': 'true'}
    elif year == year_now: 
        if month > month_now:
            {'result': 'true'}
        elif month == month_now: 
            if day > day_now:
                {'result': 'true'}
            elif day == day_now:
                {'result': 'equal'}
    return {'result': 'false'} 





def getAllTeamEvents(eventList):

    
    activeEventList = []


    for eventsObj in eventList: 

            home_team  = eventsObj["strHomeTeam"]
            away_team = eventsObj["strAwayTeam"]
            date = eventsObj["dateEvent"]
            time = eventsObj["strTime"]
            idEvent =  eventsObj["idEvent"]

            activeEvent = boolDateComp(date)
            
            if activeEvent['result'] == 'true': #Active
                event = {' homeTeam': home_team, 'awayTeam': away_team, 'date':date, 'time':time, 'eventID':idEvent }
                activeEventList.append(event)
            elif activeEvent['result'] == 'equal': #Equal
                boolactiveEvent = boolTimeComp(time)
                if boolactiveEvent:
                    event = {' homeTeam': home_team, 'awayTeam': away_team, 'date':date, 'time':time, 'eventID':idEvent }
                    activeEventList.append(event)
    return activeEventList




'''When User Goes to thier bets that's when we 
check time stamps and see the results using the other api

'''

def getTimeStamp(homeTeam, awayTeam):

    # PROBLEM: Need to know what game in the series

    event_lookup_URL = 'https://www.thesportsdb.com/api/v1/json/1/searchevents.php?e='

    search_team_details_URL = 'https://www.thesportsdb.com/api/v1/json/1/searchteams.php?t='

    next_5_events_by_team_id_URL = 'https://www.thesportsdb.com/api/v1/json/1/eventsnext.php?id='

    # Try one a direct event lookup 
    eventStr =  homeTeam + '_vs_' + awayTeam

    r = requests.get(event_lookup_URL + eventStr)
    eventJ = r.json
    if eventJ["event"]:
        # Double Check the JSON MIGHT BE LAYERED
        # Calling a function to loop over all the games being played

        activeEvents = getAllTeamEvents(eventJ["event"])

    # Need to look up team names properly
    
    else: 
        # If one team doesn't work might need to try a different team. try the rugby dragons example 
        # Still need to identify the other team name properly 

        r1 = requests.get(search_team_details_URL + homeTeam)
        hometeamJ = r1.json
        r2 = requests.get(search_team_details_URL + awayTeam)
        awayteamJ = r2.json


        if hometeamJ["teams"] and awayteamJ['teams']:
            homeTeamsList = hometeamJ["teams"]
            home_team = homeTeamsList[0]['strTeam']
            awayTeamsList = awayteamJ["teams"]
            away_team = awayTeamsList[0]['strTeam']
            
            # Get Event Details
            eventStr =  home_team + '_vs_' + away_team
            r = requests.get(event_lookup_URL + eventStr)
            eventJ = r.json
            if eventJ["event"]:
                    activeEvents = getAllTeamEvents(eventJ["event"])
            else:
                return False
            
        else:
            return False
    
        # Return a List of these items
    return activeEvents

                
'''
def getResults(): 
    betObjects = Bet.objects.all()

    for betObj in betObjects:
        hour_now = int(datetime.datetime.now().hour) # for hour
        minute_now = int(datetime.datetime.now().minute) # for minute

        betHour = bet

        if betObj.gameDate
'''

class BettingsListView(ListView):
    template_name = 'templates/bet_list.html'
    queryset = Bets.objects.all()



def getBettingData(request):

    # Last Request Data
    api = APIRequest.load()
    hour_request = api.lastRequestHour
    minute_request = api.lastRequestMinute

    # Time Now
    hour_now = int(datetime.datetime.now().hour) # for hour
    minute_now = int(datetime.datetime.now().minute) # for minute

    # Checking if we should update data
    # Can add a check later if user is on free plan
    # Free Plan 5 hour waiting time 
    fiveHoursAgo = (hour_now - 5) % 24
    requestAPI = False
    if fiveHoursAgo > hour_request:
        requestAPI = True
    elif fiveHoursAgo == hour_request:
        if minute_now > minute_request:
            requestAPI = True

    
    if requestAPI: # Get New Data
    

        sportURL = 'api.the-odds-api.com/v3/sports/?apiKey='

        # URL
        r = requests.get(sportsURL + settings.BETTING_API_PASSWORD)
        sportsJ = r.json
        sportsH = r.headers

        # Assign Headers
        api.remainingRequests = sportsH['x-requests-remaining ']
        api.usedRequests = sportsH['x-requests-used']
        api.save()

        if api.remainingRequests > 0:

        
            ''' 
            sportsList = sportsJ['data']

            
            # Get all active sports keys and add any new groups and titles that do not exist 
            for sport in sportsList: 
                if sport['active']:
                    group = sport['group']
                    title = sport['title']
                    # details = sport['details']
                    # title = title + ": " + detail
                    key = sports['key']
                    

                    # Make Title and Group Object
                    if Title.objects.filter(title=title).count() == 0: # Title Does Not Exist

                        # Create Group or Find of already exists
                        if Group.objects.filter(group=group).count() == 0: # Group Does Not Exist
                            g = Group(group=group)
                            g.save()
                        else: # Group Exists
                            g = Group.objects.filter(group=group)

                        t = Title(title=title, group=g, key=key)
                        t.save()
                    else: # Title Exists 
                        g = Group.objects.filter(group=group)
                        t = Title.objects.filter(group=g, title=title, key=key)
            '''

            # Get Odds
            oddsURL = 'https://api.the-odds-api.com/v3/odds/?region=us&mkt=h2h&apiKey='
            # ALSO NEED TO GET RESULTS FOR USERS might be on this FIRST 
            # CHECK THIS BEFORE STORING TO SEE If USEFUL

            sport = '&sport='


            # Choose Active League
            epl = 'soccer_epl'
            bundesliga = 'soccer_germany_bundesliga'
            laLiga = 'soccer_spl'



            r = requests.get(oddsURL + settings.BETTING_API_PASSWORD + sport + epl) 
            oddsJ = r.json
            oddsH = r.headers
            ''' Need unique ID's specially for best out of 7 matches like NHL and NBA
            could have multiple same team matches test it out
            '''
            
            eventList = oddsJ['data']

            if not eventList:
                r = requests.get(oddsURL + settings.BETTING_API_PASSWORD + sport + bundesliga) 
                oddsJ = r.json
                oddsH = r.headers
                eventList = oddsJ['data']

                if not eventList:
                    r = requests.get(oddsURL + settings.BETTING_API_PASSWORD + sport + laLiga) 
                    oddsJ = r.json
                    oddsH = r.headers
                    eventList = oddsJ['data']

            if eventList:

                for event in eventList: 
                    
                    if event['sites']:  # Odds Exist
                        homeTeam = event['home_team']
                        teamsList = event['teams']    
                        oddsList = event['sites'][0]['odds']['h2h']
                        if teamList[0] == homeTeam: 
                            awayTeam = teamsList[1]
                            homeOdd = oddsList[0]
                            awayOdd = oddsList[1]
                        else: 
                            awayTeam = teamsList[0]
                            homeOdd = oddsList[1]
                            awayOdd = oddsList[0]
                        drawOdd = oddsList[2]
                        betType = 'h2h'
                        # eventDetails is a List incase multiple games are going to happen
                        eventDetails = getTimeStamp(homeTeam, awayTeam)

                        for event in eventDetails:
                            if event: 
                                gameTime = event['time']
                                gameDate = event['date']
                                eventID = event['eventID']

                                # According to sportsdb api
                                homeTeam = event['homeTeam']
                                awayTeam = event['awayTeam']
                        
                                # Check if Already exists
                                if Bet.objects.filter(eventID=eventID).count() != 0: 
                                    betEvent = Bet.objects.filter(eventID=eventID)
                                    # Add New Odds
                                    betEvent.homeOdds = homeOdd
                                    betEvent.awayOdds = awayOdd
                                    betEvent.drawOdds = drawOdd
                                    betEvent.save()
                                else:
                                    # Will Need a Title and Group
                                    b = Bets.objects.create(gameTime=gameTime, gameDate=gameDate, homeTeam=homeTeam, 
                                            awayTeam=awayTeam, betType=betType, eventID=eventID, homeOdds=homeOdd, 
                                            awayOdds=awayOdd, drawOdds=drawOdd)

        # Add Current Time
        # IF SUCCESSFUL CALL
        hour_now = int(datetime.datetime.now().hour) # for hour
        minute_now = int(datetime.datetime.now().minute) # for minute
        api.lastRequestHour = hour_now
        api.lastRequestMinute = minute_now
        api.remainingRequests = oddsH['x-requests-remaining']
        api.usedRequests = oddsH['x-requests-used']
        api.save()

        return BettingsListView.as_view()(request)
    

        