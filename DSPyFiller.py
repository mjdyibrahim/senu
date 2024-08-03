import dspy

class TeamSectionFiller(dspy.Signature):
    """A complete startup team section looks like the example below, 
        if level of completion is less than 50%, you need to ask user for a number of questions till you get as much information about the team as possible :
    
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
