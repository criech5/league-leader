class Player:
    def __init__(self, data):
        # data comes in dict form, received from leader pages and comes in format:
        # {
        #   'lastname': 'Longoria',
        #   'firstname': 'Evan',
        #   'url': 'https://www.baseball-reference.com/players/l/longoev01.shtml',
        #   'leads': [
        #               {
        #                   'category': 'Games Played',
        #                   'value': 162,
        #                   'year': 2014,
        #                   'team': 'TBR'
        #               },
        #                  ...
        #            ]
        # }
        self.last = data['lastname']
        self.first = data['firstname']
        # many players will have the same name, so url can probably stand-in as a player id of sorts
        self.url = data['url']
        self.leads = data['leads']