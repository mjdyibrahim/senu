import dspy

class VerifyTeamSection(dspy.Signature):
    """
    Your job is to verify the accuracy and consistency of information provided by the user for their startup using available means
    """
    team_content = dspy.InputField(desc="Content of the team section from the pitch deck (all available information).")
    startup_json = dspy.InputField(desc="Json file with the Questions and answers for each startup.")
    team_accuracy = dspy.OutputField(desc="Score from 1-10 indicating the strength of the team section.")
    team_questions = dspy.OutputField(desc="One paragraph with 5 priority questions to verify of deny certain pieces of information")
