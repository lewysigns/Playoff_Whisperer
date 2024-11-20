from ._anvil_designer import Form1Template
from anvil import *

import anvil.http


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.match_ups = {}
    self.users = {}
    self.rosters = {}

  def button_run_click(self, **event_args):
    """This method is called when the component is clicked."""
    if not self.text_box_league_id.text:
      alert("Need to enter your league id first!")
      return

    match_up_data = anvil.http.request(f"https://api.sleeper.app/v1/league/{self.text_box_league_id.text}/matchups/11",json=True)
    users_data = anvil.http.request(f"https://api.sleeper.app/v1/league/{self.text_box_league_id.text}/users",json=True)
    roster_data = anvil.http.request(f"https://api.sleeper.app/v1/league/{self.text_box_league_id.text}/rosters",json=True)
    # for data in match_up_data:
    #   self.match_ups[data['matchup_id']] = data
    
    for data in users_data:
      self.users[data['user_id']] = data
      
    for data in roster_data:
      self.rosters[data['roster_id']] = data

    matchup_map = []
    for match_up in match_up_data:
      matchup_map.append(
        {
        'team':self.users[self.rosters[match_up['roster_id']]['owner_id']]['metadata']['team_name'],
        'matchup':match_up['matchup_id'],
        }
      )
    self.repeating_panel_1.items = matchup_map
