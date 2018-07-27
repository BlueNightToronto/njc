import discord, csv, datetime
from discord.ext import commands
from cogs.utils import checks

from urllib.request import urlopen # Web library
from xml.dom import minidom # Library for parsing XML stuff
import os
import asyncio

class njc:
    """Bot for the NJC server!"""

def setup(bot):
    bot.add_cog(njc(bot))
 
 
class njc:
    """Components for NJC"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def langilles(self):
        data = discord.Embed(title="Langilles Scrap!")
        data.set_image(url="https://cdn.discordapp.com/attachments/369324229910593536/464974359417847828/b13212085e7fabe6719935f6ebac2c6f.png")
        await self.bot.say(embed=data)

    @commands.command()
    async def kirby(self):
        data = discord.Embed(title="Join NJC")
        data.set_image(url="https://i.imgur.com/CRugTWf.png")
        await self.bot.say(embed=data)

    @commands.command()
    async def blockinfo(self, day, runID):
        """Checks for interesting information about a run."""
        data = discord.Embed(title="Join NJC")
        data.set_image(url="https://i.imgur.com/CRugTWf.png")
        await self.bot.say(embed=data)


    @commands.command()
    # COMMAND FOR GETTING NEXT BUS <STOPID>
    async def ttcnext(self, stopID):
        """Obtains next vehicle predictions for TTC bus stop's SMS code. Enter a stopID, 'info', or 'alias'"""

        if stopID == 'info':
            data = discord.Embed(title="Next Vehicle Predictions for Toronto Transit Commission",description="This bot was developed by <@281750712805883904> and <@221493681075650560>. When you submit a valid stop ID, the bot fetches data and displays it here. This information is to let users find departures for a selected bus stop efficiently, without wasting much data.\n\nOne prediction typically looks like this:\n`7:07 - #8844 on 25_1_25A*, run 25_52_182`\n\nThis means vehicle `#8844` is coming to the stop in 7 minutes. This can help you find internal branches. `25_1_25A*` means it is on route `25` going `1` outbound on internal branch `25A*`.\n\nWith the run information, you can find interesting run interlines. The run `25_52_82` lets you know if it interlines, and when it services. This is run `8` on route `25`, which operates in the `2` afternoon. The runbox number `52` does not match run `8`. This happens if a route interlines, or if it shares the corridor with another route, to prevent confusion to operators. For possible values of runs, use the command `n!ttcnext runs`\n\nFor daytime routes that fully interline with another route for the whole day, like 130 Middlefield and 132 Milner, the runbox number will not differ from the route run number.\n\nPlease report any bugs to <@221493681075650560>.\n\nAll prediction data is copyright Toronto Transit Commission 2018.", colour=discord.Colour(value=13491480))
            data.set_thumbnail(url="http://ttc.ca/images/ttc-main-logo.gif")
            await self.bot.say(embed=data)
            return
        elif stopID == 'alias':
            data = discord.Embed(title="StopID Alias",description="You can also type these in to get their bus stop.", colour=discord.Colour(value=13491480))

            try:
                fleetlist = open("cogs/njc/ttcalias.csv")
                reader = csv.reader(fleetlist,delimiter=",")
                line = []
            except:
                await self.bot.say("No alias file found... <@221493681075650560>")
                stopID = stopID
            tosay = ""
            for row in reader:
                if True:
                    tosay=tosay + row[0]
                    await self.bot.say(tosay)
                else:
                    stopID = stopID
                    await self.bot.say("Test message 2")
            data.add_field(name='Alias',value=tosay, inline='false') # Alias
            data.set_thumbnail(url="http://ttc.ca/images/ttc-main-logo.gif")
            await self.bot.say(embed=data)
            return
        elif stopID == 'runs':
            data = discord.Embed(title="Runs Information",description="`<route>_<runbox>_<run><time>`, ex. `12_88_20`", colour=discord.Colour(value=13491480))
            data.add_field(name='Values for Routes:',value="The main route for the run. In the example, it is `12`.", inline='false') # Alias
            data.add_field(name='Values for Runbox:',value="Same as run, unless this run goes on more than one route, and/or the route operates very closely to another route. In the example, it is `88`.", inline='false') # Alias
            data.add_field(name='Values for Run:',value="The run number for the particular route. In the example, it is `2`.", inline='false') # Alias
            data.add_field(name='Values for Time:',value="`0` - Run operates all day.\n`1` - Run operates in the morning period only.\n`2` - Run starts to operate in the afternoon period.\nIn the example, it is `0`.", inline='false') # Alias
            data.set_thumbnail(url="http://ttc.ca/images/ttc-main-logo.gif")
            await self.bot.say(embed=data)
            return

        try:
            fleetlist = open("cogs/njc/ttcalias.csv")
            reader = csv.reader(fleetlist,delimiter=",")
            line = []
        except:
            await self.bot.say("No alias file found... <@221493681075650560>")
            stopID = stopID

        try:
            for row in reader:
                if str(row[0]) == stopID:
                    line = row
            fleetlist.close()
            stopID=line[1]
        except:
            stopID = stopID

        url = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=" + stopID
        raw = urlopen(url).read() # Get page and read data
        decoded = raw.decode("utf-8") # Decode from bytes object
        parsed = minidom.parseString(decoded) # Parse with minidom to get XML stuffses
    
        if len(parsed.getElementsByTagName('Error')) > 0: # Check whether the ID is valid
            data = discord.Embed(title=":x: Invalid Stop ID or Command: " + stopID,description="Type `n!ttcnext info` for help.",colour=discord.Colour(value=16467744))
            await self.bot.say(embed=data)
            return

        msg1 = "No predictions found for this route."
        data = discord.Embed(title="Next Vehicle Predictions",description="Stop ID: {}".format(stopID), colour=discord.Colour(value=11250603))
        routes = parsed.getElementsByTagName('predictions') # Get all tags called 'predictions'
        for i in routes: # Loop through these
            stopname = i.attributes['stopTitle'].value # GETS STOP NAME
            routename = i.attributes['routeTitle'].value # GETS ROUTE NAME
            predictions = i.getElementsByTagName('prediction') # Get all sub-tags called 'prediction'
            for i in predictions: # Loop through these
                try: #test
                    seconds = int(i.attributes['seconds'].value) # If the seconds value is blank, this will throw an error (dividing by 0) and trigger the exception handler, and this value needs to be an int later anyway
                    vehicle = i.attributes['vehicle'].value
                    if vehicle >= '1000' and vehicle <= '1149':
                        vehicle = vehicle + " VII Hybrid"                    
                    elif vehicle >= '1200' and vehicle <= '1423':
                        vehicle = vehicle + " VII NG Hybrid"                    
                    elif vehicle >= '1500' and vehicle <= '1689':
                        vehicle = vehicle + " VII NG Hybrid"                    
                    elif vehicle >= '1700' and vehicle <= '1829':
                        vehicle = vehicle + " VII NG Hybrid"                    
                    elif vehicle >= '3100' and vehicle <= '3369':
                        vehicle = vehicle + " LFS VISION"                    
                    elif vehicle >= '4000' and vehicle <= '4199':
                        vehicle = vehicle + " CLRV"                    
                    elif vehicle >= '4200' and vehicle <= '4251':
                        vehicle = vehicle + " ALRV"                    
                    elif vehicle >= '4400' and vehicle <= '4999':
                        vehicle = vehicle + " Flexity"                    
                    elif vehicle >= '7500' and vehicle <= '7883':
                        vehicle = vehicle + " VII"                    
                    elif vehicle >= '7900' and vehicle <= '7979':
                        vehicle = vehicle + " VII"                    
                    elif vehicle >= '8000' and vehicle <= '8011':
                        vehicle = vehicle + " VII-Airport"                    
                    elif vehicle >= '8012' and vehicle <= '8099':
                        vehicle = vehicle + " VII"                    
                    elif vehicle >= '8100' and vehicle <= '8219':
                        vehicle = vehicle + " VII NG"         
                    elif vehicle >= '8300' and vehicle <= '8396':
                        vehicle = vehicle + " VII 3G"         
                    elif vehicle >= '8400' and vehicle <= '8504':
                        vehicle = vehicle + " LFS"                    
                    elif vehicle >= '8510' and vehicle <= '8617':
                        vehicle = vehicle + " LFS"                    
                    elif vehicle >= '8620' and vehicle <= '8964':
                        vehicle = vehicle + " LFS"                    
                    elif vehicle >= '9000' and vehicle <= '9152':
                        vehicle = vehicle + " LFS-Artic"
                    elif vehicle >= '9200' and vehicle <= '9239':
                        vehicle = vehicle + " LFS"                    
                    else:
                        vehicle = vehicle + " UNKNOWN VEHICLE"

                    toSay = [vehicle,i.attributes['dirTag'].value,i.attributes['block'].value, seconds // 60, str(seconds % 60).zfill(2), seconds] # Get the time value, vehicle and route name from the first one
                    
                    toSay = [vehicle,i.attributes['dirTag'].value,i.attributes['block'].value, seconds // 60, str(seconds % 60).zfill(2)] # Get the time value, vehicle and route name from the first one
                    msg = "{3}:{4} - #{0} on `{1}`, Run `{2}`".format(*toSay if seconds > 60 else [*toSay[:-2], "**" + str(toSay[-2]), str(toSay[-1]) + "**"]) # Say various pieces of information
                
                    #Aah I hate how unclean this code is
                    if msg1[0] == "No predictions found for this route.":
                        msg1 = [msg]
                    else:
                        msg1.append(toSay)
                    toSay = [vehicle,i.attributes['dirTag'].value,i.attributes['block'].value, seconds // 60, str(seconds % 60).zfill(2)] # Get the time value, vehicle and route name from the first one
                    msg = "{3}:{4} - #{0} on `{1}`, Run `{2}`".format(*toSay if seconds > 60 else [*toSay[:-2], "**" + str(toSay[-2]), str(toSay[-1]) + "**"]) # Say various pieces of information
                
                    if msg1 == "No predictions found for this route.":
                        msg1 = msg
                    else:
                        msg1 = msg1 + "\n" + msg
                    # Did a nice sorting thingy
                        msg1.append(msg)
                   # Aah I hate how unclean this code is
                except:
                    try:
                        msg1 = "No predictions found for this route."
                        continue # And starting the next loop immediately
                    except:
                        msg1 = "Invalid Data recieved"
                        await self.bot.say("Invalid data recieved.") # Dunno how it'll look if there's no data, wrapping it in a try/except should cover all bases
            
            dirtyMessages = [i.split(" ") for i in msg1] # Complex and hacky code to sort everything, ignore it for now
            sortedDirtyMessages = sorted(dirtyMessages, key = lambda x:x[0])
            cleanMessages = [" ".join(i) for i in sortedDirtyMessages]
            string = "\n".join(cleanMessages)
            
            data.add_field(name=routename,value=string, inline='false') # Say message


            data.add_field(name=routename,value=str(msg1), inline='false') # Say message
            #Did a nice sorting thingy
            data.set_thumbnail(url="http://ttc.ca/images/ttc-main-logo.gif")
            data.set_footer(text="About this command, use n!ttcnext info.")
            msg1 = 'No predictions found for this route.'

        data.set_author(name=stopname, icon_url="http://ttc.ca/images/ttc-main-logo.gif")
        try:
            await self.bot.say(embed=data)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    #Gets info for fleet
    @commands.command()
    async def fleet(self, agency : str, number : int):
        """Gets information from a fleet. For more info, n!fleet info 0"""
        agencyname = 'null '
        curator = 'null'

        data = discord.Embed(title="Fleet Information",description="Vehicle not found.",colour=discord.Colour(value=12786604))

        if agency == "info":
            data = discord.Embed(title="Sources",description="Most fleet information is from the CPTDB wiki, with data curated by NJC staff.\nhttps://cptdb.ca/wiki/index.php/Main_Page.\n\nNOTE: When a vehicle status is `Inactive`, this means the vehicle is currently not used for revenue service. ",colour=discord.Colour(value=5))
            await self.bot.say(embed=data)
            return

        # AGENCY NAME
        if agency == 'go':
            agencyname = "GO Transit "
            curator = "BlueKnight17#3042"
        elif agency =='ttc':
            agencyname = "TTC "
            curator = "BlueKnight17#3042"
        elif agency =='yrt':
            agencyname = "YRT "
            curator = "Hexagonal10#4418"
        elif agency =='miway':
            agencyname = "MiWay "
            curator = "The Sauce Boss#1403"
        elif agency =='ddot':
            agencyname = "DDOT "
            curator = "TheYoshiState#3721"
        else:
            agencyname = ""

        try:
            fleetlist = open("cogs/njc/fleets/{}.csv".format(agency))
            reader = csv.reader(fleetlist,delimiter="	")
            line = []
        except Exception as e:
            data = discord.Embed(title="This agency is unsupported or invalid at this time.",description="You can help contribute to the fleet lists. Contact <@300473777047994371>\n\nError: `" + str(e) + "`",colour=discord.Colour(value=5))
            await self.bot.say(embed=data)
            return

        try:
            for row in reader:
                if row[-1] != "thumbnail" and int(row[0]) == number:
                    line = row
            fleetlist.close()
            data = discord.Embed( colour=discord.Colour(value=474494))
            data.add_field(name="Manufacturer", value=line[2])
            data.add_field(name="Model", value=line[3])
            data.add_field(name="Division/Category", value=line[4])
            data.add_field(name="Powertrain/Motor", value=line[5])
            data.add_field(name="Vehicle Group", value=line[1])
            data.add_field(name="Status", value=line[6])
            data.set_footer(text="Last updated " + line[8] + " - {} ".format(agencyname) + 'is maintained by @{}'.format(curator))

            if number < 1000:
                if agency == 'ttc':
                    number = str('W{}'.format(number))
                elif agency == 'miway':
                    number = str('0{}'.format(number))
            data.set_author(name="Fleet Information for {}".format(agencyname) + str(number), url=line[7])
            data.set_thumbnail(url=line[7])

        except Exception as e:
            data = discord.Embed(title="Vehicle {} was not found ".format(number) + "for {}".format(agencyname),description="Either you have entered a non-existent vehicle number, or that vehicle has not been added to our database yet! Vehicle groups that have been completely retired are removed from the database!\n\nError: `" + str(e) + "`",colour=discord.Colour(value=16467744))

        await self.bot.say(embed=data)


    # Allows users to edit file
    @commands.command()
    async def fleetedit(self, agency : str, number : int, field: str, newvalue: str):
        """Allows construction role and higher to edit information about fleet.\n\nAvailable values for field: vehicle, group, manufacturer, model, division, powertrain, status, thumbnail"""    
        
        try:
            reader = None
            fleetlist = open("cogs/njc/fleets/{}.csv".format(agency))
            reader = csv.reader(fleetlist,delimiter="	")
        except:
            data = discord.Embed(title="This agency is unsupported or invalid at this time.",description="You can help contribute to the fleet lists. Contact <@300473777047994371>",colour=discord.Colour(value=5))
            await self.bot.say(embed=data)
            return

    
        lineNum = None
        lines = []
        for row in reader:
            if row:
                lines.append(row)
                if len(lines) > 1 and int(row[0]) == number:
                    if not lineNum:
                        lineNum = len(lines) - 1
                    else:
                        await self.bot.say("More than one bus :3")
                        return
        fleetlist.close()
        if True:
            num = lines[0].index(field)
            if lineNum:
                lines[lineNum][num] = newvalue
                lines[lineNum][-1] = datetime.date.today().strftime("%d %B %Y").lstrip("0")
            else:
                await self.bot.say("Invalid number")
                return
        else:
            await self.bot.say("Invalid field")
            return
        writer = None
        with open("cogs/njc/fleets/{}.csv".format(agency), "w", newline='') as fleetlist:
            writer = csv.writer(fleetlist,delimiter="	")     
            for i in lines:
                writer.writerow(i)
        fleetlist.close()
        data = discord.Embed(title="'{}' has been updated for ".format(field) + agency + " " + str(number),description="New value for {}: ".format(field) + newvalue,colour=discord.Colour(value=34633))
        await self.bot.say(embed=data)


    # Gets schedules
    @commands.command()
    async def schedule(self, agency : str, line : int):
        """Gets a schedule for selected agency's line. Available agencies: [YRT, GO]"""

        if agency.lower() in ['yrt']:
            data = discord.Embed(colour=discord.Colour(value=2130939))
            data.add_field(name="YRT Route Navigator - Route {}".format(line), value=str("https://www.yrt.ca/en/schedules-and-maps/resources/{}.pdf".format(line)))
        # --- GO TRANSIT ---
        elif agency.lower() in ['go']:
            if line == 18: # REDIRCTS LINE 18 to 01
                line1 = "01"
            elif line == 30 or line == 32 : # REDIRECTS LINES 30 and 32 to 31
                line1 = "31"
            elif line == 40: # REDIRECTS TO ACTUAL TABLE PDF
                line1 = "40-Feb06"
            elif line == 45 or line == 47 or line == 48: # REDIRECTS LINES 45, 47 and 48 to 46
                line1 = "46"
            elif line == 51 or line == 54: # REDIRECTS LINES 51 and 54 to 52
                line1 = "52"
            elif line == 63 or line == 67 or line == 69: # REDIRECTS LINES 63, 67, and 69 to 65
                line1 = "65"
            elif line == 70: # REDIRECTS LINE 70 to LINE 71
                line1 = "71"
            elif line == 90 or line == 91: # REDIRECTS LINE 90 and 91 to 09
                line1 = "09"
            else:
                line1 = line
            data = discord.Embed(colour=discord.Colour(value=2130939))
            data.add_field(name="GO Transit Schedule - Route {}".format(line), value=str("https://www.gotransit.com/static_files/gotransit/assets/pdf/TripPlanning/FullSchedules/Table{}.pdf".format(line1)))

        # --- TORONTO TTC ---
        elif agency.lower() in ['ttc']:
            data = discord.Embed(colour=discord.Colour(value=2130939))
            data.add_field(name="TTC Route Information - Route {}".format(line), value=str("http://ttc.ca/Routes/{}/RouteDescription.jsp".format(line)))
        # --- INVALID AGENCY ---
        else:
            data = discord.Embed(title="This agency is unsupported or invalid at this time.",description="Schedules for this agency could not be fetched.",colour=discord.Colour(value=16467744))
        await self.bot.say(embed=data)

    # Gets map for a route.
    @commands.command(no_pm=False)
    async def map(self, agency : str, line : int):
        """Gets a map for agency's line. Available agencies: [TTC]"""

        maptitle = [agency , line]
        if agency.lower() in ['ttc']: # TTC
            data = discord.Embed(description="NJC Map Fetcher", title="Toronto Transit Commission - Route {1}".format(*maptitle), colour=discord.Colour(value=2130939))
            if line < 515:
                if line < 10:
                    line1 = str("00" + str(line))
                elif line < 100:
                    line1 = str("0" + str(line))
                else:
                    line1 = line
                data.set_image(url="http://ttc.ca/images/Route_maps/{}map.gif".format(line1))
            else:
                data.add_field(name="Error", value=str("Line too high"))
        else:
            data = discord.Embed(title="This agency is unsupported or invalid at this time.",description="Maps for this agency were not found.",colour=discord.Colour(value=16467744))
        await self.bot.say(embed=data)

    # Gets bylaw
    @commands.command()
    async def bylaw(self, agency : str):
        """Gets rules for an agency. Available agencies: [TTC, MiWay]"""

        if agency.lower() in ['ttc']: # ttc
            data = discord.Embed(colour=discord.Colour(value=5))
            data.add_field(name="TTC Bylaw No. 1", value=str("https://www.ttc.ca/Riding_the_TTC/TTC_Bylaws/index.jsp"))
            
        elif agency.lower() in ['miway']: # miway
            data = discord.Embed(colour=discord.Colour(value=5))
            data.add_field(name="THE CORPORATION OF THE CITY OF MISSISSAUGA TRANSIT BY-LAW", value=str("https://www7.mississauga.ca/documents/bylaws/TRANSIT_RULES_UPDATE.pdf"))
            
        else:
            data = discord.Embed(title="This agency is unsupported or invalid at this time.",description="The bylaw for this agency could not be found.",colour=discord.Colour(value=16467744))
        await self.bot.say(embed=data)

    # Gets profile for TTC route
    @commands.command()
    async def route1(self):
        """Gets information about TTC route"""
        data = discord.Embed(title="169 HUNTINGWOOD",description="169A DON MILLS STN to SCARBOROUGH CTR via VAN HORNE\n169B DON MILLS STN to SCARBOROUGH CTR",colour=discord.Colour(value=15801115))
        data.add_field(name="Division", value="Wilson, all trips, all days",inline='false')
        data.add_field(name="Operation", value="169A - Except weekday rush and late weekend evening\n169B - During weekday rush",inline='false')
        data.add_field(name="Interlines", value="None",inline='false')
        data.add_field(name="Internal Branches", value="169A - For 169A trips\n169B - For 169B trips\nMCDO - McCowan/Commander to Don Mills Stn, one trip only",inline='false')
        data.add_field(name="Signs", value="169A HUNTINGWOOD TO DON MILLS STN via VAN HORNE\n169A HUNTINGWOOD TO SCARBOROUGH CTR via VAN HORNE\n169B HUNTINGWOOD TO DON MILS STN\n169B HUNTINGWOOD TO SCARBOROUGH CTR",inline='false')
        data.set_footer(text="Page 1 of 2")
        await self.bot.say(embed=data)


    # Gets requirements
    @commands.command()
    async def requirements(self):
        """Sends requirements for downloads on NJC."""
        await self.bot.say("The latest version of New John City requires the following objects:\n\n**Chicago DLC:**\nhttps://store.steampowered.com/app/361290/OMSI_2_Addon_Chicago_Downtown/\n\n**Willshire Objects**\nhttp://www.vtransitcenter.com/index.php?action=downloads;sa=view;down=56\n\n**Simple Streets:**\nhttp://www.omnibussimulator.de/backup/index.php?page=Thread&threadID=2500\n\n**New Flyer Powertrain Mod:**\nhttp://www.vtransitcenter.com/index.php/topic,8.0.html")

    # Sends message you need logfile
    @commands.command()
    async def logfile(self):
        """Sends requirements for downloads on NJC."""
        await self.bot.say("For further support on your OMSI problem, you must **upload your logfile.txt**.\n\nYou can find **logfile.txt** in the OMSI folder. Upload the file to this channel so we can diagnose for the issue.\n\nhttps://i.imgur.com/DxclO7c.png")


    async def member_join(self, member):
        await self.bot.say('{0} joined at {0.joined_at}'.format(member))
