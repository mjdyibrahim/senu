import dspy

class TeamSectionCompleter(dspy.Signature):
    """A complete startup team section looks like the example below, 
        if level of completion is less than 50%, you need to ask user for a number of questions till you get as much information about the team as possible :
    
    Dataset:

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
      ],
      "dataFields": {
        "Number of Team Members": "integer",
        "Team Members": [
          {
            "Name": "string",
            "Title": "string",
            "Availability Per Week": "integer",
            "Involved Since": "date",
            "Equity %": "number",
            "Salary %": "number",
            "Years of Experience": "integer",
            "Academic Degree": {
              "Undergraduate": "boolean",
              "Graduate Degree": "boolean",
              "Masters": "boolean",
              "PhD or More": "boolean"
            },
            "Startup Experience": {
              "Has Been Part of a Startup Team": "boolean",
              "Has Been the Founder of a Startup": "boolean",
              "Has Previous C-Level Position": "boolean",
              "Has Been Part of a Successful Exit": "boolean"
            },
            "Role": "string"
          }
        ],
        "Team Overview": "string",
        "Team Assessment": "string"
      }
    }   

    Example:
            Startup has 3 Cofounders with near equal equity
            Abdo has 8 years of startup experience with 1 successful exit, Abdo works half time on the startup
            Jack has 7 years of AI experience, he has Masters from Harvard Unviersity and teaches part time, engaged full time with the startup
            Ahmed has 9 years of sales experience, has worked in Fortune 100 companies for the past 5 years
            the team met 3 months ago and had been working on startup since then
            team has 2 mentors in technology and business with 12+ years of experience

    Questions to be prioritized and sent to the user within context:
        How many co-founders are there in your startup, and how is the equity distributed among them?
        Can you provide detailed background information on each team member, including their previous startup experience, areas of expertise, and any significant achievements?
        What is the time commitment of each team member to the startup (e.g., part-time, full-time)?
        How long have the team members been working together, and what was the nature of their prior interactions (if any)?
        Do you have any mentors or advisors associated with the startup? If so, please provide details on their experience and how they are contributing to the startup.
    """

    team_content = dspy.InputField(desc="Content of the team section from the pitch deck.")
    team_q1 = dspy.OutputField(desc="Question with priority 1 to complete team section")
    team_q2 = dspy.OutputField(desc="Question with priority 2 to complete team section.")
    team_q3 = dspy.OutputField(desc="Question with priority 3 to complete team section.")
    team_q4 = dspy.OutputField(desc="Question with priority 4 to complete team section.")
    team_q5 = dspy.OutputField(desc="Question with priority 5 to complete team section.")
