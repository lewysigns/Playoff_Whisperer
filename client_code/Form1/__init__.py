from ._anvil_designer import Form1Template
from anvil import *

from ..wizard import get_odds

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
    current_week = 12
    final_week = 14
    if not self.text_box_league_id.text:
      alert("Need to enter your league id first!")
      return

    get_odds(self.text_box_league_id.text,current_week,final_week)
    