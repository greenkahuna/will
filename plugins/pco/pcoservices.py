from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
from plugins.pco import song_info, authenticate, set_list, teams
from will.mixins.slackwhitelist import wl_chan_id

app = "services"


# I turned off credentials for this because it's not sensitive info.
class PcoServicesPlugin(WillPlugin):
    @respond_to("(?:do you |find |got |a )?(set list for |!setlist|setlist for |"
                "!sunday |songs for |order of service for )(?P<pco_date>.*?(?=(?:\'|\?)|$))")
    def pco_setlist_lookup(self, message, pco_date):
        if pco_date is "":
            pco_date = 'sunday'
        """set list for Sunday: tells you the set list for a certain date"""
        attachment = []
        self.reply("Let me get that for you. This might take a bit if you have a lot of services.")
        for x in set_list.get(pco_date):
            attachment += x.slack()
        if attachment:
            self.reply("", message=message, attachments=attachment)
        else:
            self.reply("Sorry I don't find any set lists scheduled on" + pco_date + " in Services.")

    @respond_to("(?:what is |show me |what's |a )?(song list for |!songlist|!checksongs|!setsongs|!songcheck)"
                "(?P<pco_date>.*?(?=(?:\'|\?)|$))")
    def pco_setlist_songs(self, message, pco_date):
        if pco_date is "":
            pco_date = 'sunday'
        self.reply("Let me get that song list for you.")
        song_list = set_list.get_set_songs(pco_date)
        attachment = []
        for result in song_list:
            attachment += result.slack()
        if attachment:
            self.reply("Here's the songs scheduled for " + pco_date, message=message, attachments=attachment)
        else:
            self.reply("Sorry I don't find any songs scheduled on " + pco_date + " in Services.")

    @respond_to("(?:what is |show me |what's |a )?(arrangement for |!song )(?P<pco_song>.*?(?=(?:\'|\?)|$))")
    def pco_song_lookup(self, message, pco_song):
        """arrangement for [song]: tells you the arrangement for a certain song"""
        self.reply("Let me get that song for you.")
        song = song_info.get(pco_song)
        attachment = []
        for result in song:
            attachment += result.slack()
        if attachment is None:
            self.reply("Sorry I don't find " + song + "in services.")
        self.reply("", message=message, attachments=attachment)

    @respond_to("(!teams|!team)(?P<pco_team>.*?(?=(?:\?)|$))")
    def pco_team_lookup(self, message, pco_team):
        pco_team = pco_team.strip()
        """Lookup a [team] and print it's members"""
        if not pco_team:
            self.reply("Hold on I'll look up the teams for you.")
        else:
            self.reply("Hold on I'll look up that team for you.")
        team_list = teams.get(pco_team)
        attachment = []
        for result in team_list:
            attachment += result.slack()
        if not attachment:
            self.say('Sorry I don\'t find a team named "' + pco_team + '" in services.', channel=wl_chan_id(self))
        else:
            self.say("", message=message, attachments=attachment, channel=wl_chan_id(self))


# Test your setup by running this file.
# If you add functions in this file please add a test below.


if __name__ == '__main__':
    date = "sunday"
    song_name = "Mighty to Save"
    team_name = "Audio/Visual"
    # print("Getting set list for ", date)
    # for x in set_list.get(date):
    #     print(x.txt())
    # print("Getting song info for ", song_name)
    # for x in song_info.get(song_name):
    #     print(x.txt())
    # print("Getting this weeks songs.")
    # for attachment in set_list.get_set_songs(date):
    #     print(attachment.txt())
    print("Getting the team list")
    for attachment in teams.get(team_name):
        print(attachment.txt())
