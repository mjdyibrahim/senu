import dspy
from dspy.functional import TypedPredictor
from typing import List
from pydantic import BaseModel


class TeamSectionExtractor(dspy.Signature):
  """
  Extracts specific data point about the team from the given pitch deck content.
  
  You should use the format below to extract these data points for example to extract "team_size" you ask yourself 
  "What is the size of the founding team based on the provided text?", and to extract   "market_size": 
  "What is the estimated size of the target market based on the text?",

  

  "team_size": "What is the size of the founding team based on the provided text?",
  "market_size": "What is the estimated size of the target market based on the text?",
  
          team_member =  {
             "name": "What is the name of the team member?",
             "title": "What is the title of the team member?",
             "availability_per_week": "How many hours per week is the team member available?",
             "involved_since": "Since when has the team member been involved?",
             "equity_percentage": "What is the equity percentage of the team member?",
             "salary_percentage": "What is the salary percentage of the team member?",
             "years_of_experience": "How many years of experience does the team member have?",
             "undergraduate": "Does the team member have an undergraduate degree?",
             "graduate_degree": "Does the team member have a graduate degree?",
             "masters": "Does the team member have a master's degree?",
             "phd_or_more": "Does the team member have a PhD or more?",
             "startup_team_member": "Has the team member been a part of a startup team?",
             "startup_founder": "Has the team member founded a startup?",
             "c_level_position": "Has the team member held a C-level position?",
             "successful_exit": "Has the team member had a successful exit?",
             "marketing": "Is the team member involved in marketing?",
             "sales": "Is the team member involved in sales?",
             "product": "Is the team member involved in product development?",
             "creative": "Is the team member involved in creative roles?",
             "technical": "Is the team member involved in technical roles?",
             "operation": "Is the team member involved in operations?",
             "other_role": "What other roles does the team member have?",
             "linkedin": "What is the LinkedIn profile of the team member?",
             "email": "What is the email of the team member?"
         }

  
  """
  pitchdeck_content = dspy.InputField(desc="Content of the pitch deck.")

  # Team size
  team_size: int = dspy.OutputField(desc="How many team members at the startup team?")
  # team_members: dict = dspy.OutputField(dec="Build a complete profile for each team member based on the given format")
  team_members = dspy.OutputField(desc="List of team members and their corresponding info in the provided Json format")
  market_size: int = dspy.OutputField(desc="What is the size of the market for the startup?")

  # # Team member details (using separate OutputFields for each detail)
  # team_member_1_name: str = dspy.OutputField(desc="Name of the first team member.")
  # team_member_1_name_prompt = "What is the name of the first team member mentioned in the text?"

  # team_member_1_role: str = dspy.OutputField(desc="Role of the first team member.")
  # team_member_1_role_prompt = "What is the role of the first team member mentioned in the text (e.g., Marketing, Technical)?"

  # team_member_1_title: str = dspy.OutputField(desc="Title of the first team member (e.g., CEO, CTO).")
  # team_member_1_title_prompt = "What is the title of the first team member mentioned in the text?"

  # team_member_1_experience: int = dspy.OutputField(desc="Years of experience of the first team member.")
  # team_member_1_experience_prompt = "How many years of experience does the first team member have?"

  # team_member_1_education: str = dspy.OutputField(desc="Highest education level of the first team member.")
  # team_member_1_education_prompt = "What is the highest education level of the first team member?"

  # team_member_1_startup_experience: str = dspy.OutputField(desc="Startup experience of the first team member.")
  # team_member_1_startup_experience_prompt = "Does the first team member have any startup experience? If yes, please describe it briefly."

  # team_member_1_equity: float = dspy.OutputField(desc="Equity percentage of the first team member.")
  # team_member_1_equity_prompt = "What is the equity percentage of the first team member?"

  # ... (Add similar OutputFields and prompts for other team members)

  # Team overview and assessment
  # team_feedback: str = dspy.OutputField(desc="Feedback on the team's qualifications and ability to execute the plan.")
  # team_feedback_prompt = "Can you provide an overview of the team's qualifications and expertise? How would you assess the team's experience and ability to execute the business plan?"