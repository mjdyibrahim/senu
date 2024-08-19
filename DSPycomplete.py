import dspy
from dspy.functional import TypedPredictor
from typing import List
from pydantic import BaseModel


class TeamSectionCompleter(dspy.Signature):
    """
    based on the given input text, extract the following items from the team section

    "Team": {
      "questions": [
        "How many team members do you have?",
        "List the team members with the following details:",
        {
          "Name": "What is the team member's name?",
          "Title": "What is the team member's title?",
          "Availability Per Week": "How many hours per week is the team member available?",
          "Involved Since": "Since when has the team member been involved?",
          "Equity %": "What percentage of equity does the team member hold?",
          "Salary %": "What percentage of salary does the team member receive?",
          "Years of Experience": "How many years of experience does the team member have?",
          "Academic Degree": {
            "Undergraduate": "Does the team member have an undergraduate degree?",
            "Graduate Degree": "Does the team member have a graduate degree?",
            "Masters": "Does the team member have a master's degree?",
            "PhD or More": "Does the team member have a PhD or higher degree?"
          },
          "Startup Experience": {
            "Has Been Part of a Startup Team": "Has the team member been part of a startup team?",
            "Has Been the Founder of a Startup": "Has the team member been the founder of a startup?",
            "Has Previous C-Level Position": "Has the team member held a previous C-level position?",
            "Has Been Part of a Successful Exit": "Has the team member been part of a successful exit?"
          },
          "Role": {
            "Marketing": "Is the team member's role in Marketing?",
            "Sales": "Is the team member's role in Sales?",
            "Product": "Is the team member's role in Product?",
            "Creative": "Is the team member's role in Creative?",
            "Technical": "Is the team member's role in Technical?",
            "Operation": "Is the team member's role in Operation?",
            "Other": "What other role does the team member have?"
          }
        },
        "Can you provide an overview of the team’s qualifications and expertise?",
        "How would you assess the team’s experience and ability to execute the business plan?"
}

    """
    team_content = dspy.InputField(desc="Content of the pitch deck.")
    team_count: int = dspy.OutputField(desc="How many team members does the startup have?")
    team_member_1_name: str = dspy.OutputField(des="")
    team_member_1_role: int = dspy.OutputField(desc="The role of the team member in the startup")
    team_feedback: list[str] = dspy.OutputField(desc="list containing 5 items each must start with *, specifying feedback for the startup to improve its team score. If any information is missing, recommend for it to be included.")
