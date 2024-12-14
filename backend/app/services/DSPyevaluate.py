import dspy
from dspy.functional import TypedPredictor
from typing import List
from pydantic import BaseModel

#specify class for Feedback item
class Feedback(BaseModel):
    feedback_item: str

class FeedbackItems(BaseModel):
    feedback_items: List[Feedback]


class EvaluateTeamSection(dspy.Signature):
    """
    Analyze provided content and score the strength of the team section only from 1-10 based on available information and provide feedback on possible improvements.

    Optimal conditions for the team include:
    - 2-3 cofounders, with near equal equity
    - Specialized academic degrees and/or expertise in their areas
    - Half-time or more commitment to the startup
    - Previous startup experience and successful exits
    - Team working together for a significant period
    - Presence of mentors with substantial experience

    Example of team_feedback output format:

    "team_feedback": {
    "feedback_1": "The team has strong experience and a clear vision, but they need more diversity in skills.",
    "feedback_2": "The team's track record is impressive, but they lack experience in scaling businesses.",
    "feedback_3": "There is a strong leadership team, but more emphasis on technical skills is needed.",
    "feedback_4": "The team has a clear vision but needs better execution plans.",
    "feedback_5": "The team should work on improving communication strategies within the group."
}

    """
    team_content = dspy.InputField(desc="Content of the pitch deck.")
    team_score: int = dspy.OutputField(desc="Score from 1-10 indicating the strength of the team section.")
    team_feedback: list[str] = dspy.OutputField(desc="list containing 5 items each must start with *, specifying feedback for the startup to improve its team score. If any information is missing, recommend for it to be included.")

class EvaluateFundraisingSection(dspy.Signature):
    """
    Analyze provided content and score the strength of the fundraising section only from 1-10 based on available information and provide feedback on possible improvements.
    Optimal conditions for fundraising include:
    - A clear and feasible plan for raising funds in the next 12-18 months
    - Secured initial funding or demonstrated progress in fundraising
    - Identified potential sources of funding such as venture capital, angel investors, or grants
    - Detailed and realistic financial projection
    - A strong pitch deck and business plan that have been refined and tested with investors

    Example of fundraising_feedback output format:

    "fundraising_feedback": {
    "score": 7,
    "feedback_1": "The startup has secured initial funding but needs to outline a clearer path for future rounds.",
    "feedback_2": "Funding sources are diversified, but there is a need for more detailed financial projections.",
    "feedback_3": "The pitch to investors is strong but needs better risk management strategies.",
    "feedback_4": "Current funding is sufficient for initial growth but not for scaling.",
    "feedback_5": "Consider exploring alternative funding options like grants or strategic partnerships."
    }

    """
    fundraising_content = dspy.InputField(desc="Content of the pitch deck.")
    fundraising_score: int = dspy.OutputField(desc="Score from 1-10 indicating the strength of the fundraising section.")
    fundraising_feedback: list[str] = dspy.OutputField(desc="list containing 5 items each must start with *, specifying feedback for the startup to improve its fundraising score. If any information is missing, recommend for it to be included.")

class EvaluateMarketSection(dspy.Signature):
    """
    Score the strength of the market section from 1-10 based on available information and provide feedback on any possible improvements.
    Optimal conditions for the market include:
    - Clear understanding of the market size and growth potential
    - Defined target market and a plan to capture a significant market share
    - Detailed information on market dynamics, customer needs, and competitive landscape
    - Evidence of market validation, such as customer interviews or pilot studies
    - Strategy for market entry and scaling

    """
    market_content = dspy.InputField(desc="Content of the pitch deck.")
    market_score: int = dspy.OutputField(desc="Score from 1-10 indicating the strength of the market section.")
    market_feedback: list[str] = dspy.OutputField(desc="list containing 5 items each must start with *, specifying feedback for the startup to improve its market score. If any information is missing, recommend for it to be included, don't add '\nUser:' at the end.")

class EvaluateBusinessModelSection(dspy.Signature):
    """
    Score the strength of the business model section from 1-10 based on available information and provide feedback on possible improvements.
    Optimal conditions for the business model include:
    - Clear revenue model showing how the business will make money
    - Identified who will pay for the service and a strategy for acquiring customers
    - Defined pricing strategy and detailed plan for scaling revenue
    - Identified and planned for key metrics like customer acquisition cost and lifetime value
    - Validated business model with proof of concept or early traction

    """
    business_model_content = dspy.InputField(desc="Content of the pitch deck.")
    business_model_score: int = dspy.OutputField(desc="Score from 1-10 indicating the strength of the business model section.")
    business_model_feedback: list[str] = dspy.OutputField(desc="list containing 5 items each must start with *, specifying feedback for the startup to improve its business model score. If any information is missing, recommend for it to be included, don't add '\nUser:' at the end.")

class EvaluateProductSection(dspy.Signature):
    """
    Score the strength of the product section from 1-10 based on available information and provide feedback on possible improvements.
    Optimal conditions for the product include:
    - Product is functional and has been tested with users
    - Clear roadmap for product development and future features
    - Feedback from prospective customers indicating strong interest
    - Validated product-market fit or evidence of traction
    - Product solves a significant problem and has unique value propositions
    
    """
    product_content = dspy.InputField(desc="Content of the pitch deck.")
    product_score: int = dspy.OutputField(desc="Score from 1-10 indicating the strength of the product section.")
    product_feedback: list[str] = dspy.OutputField(desc="list containing 5 items each must start with *, specifying feedback for the startup to improve its product score. If any information is missing, recommend for it to be included, don't add '\nUser:' at the end.")

class EvaluateTractionSection(dspy.Signature):
    """
    Score the strength of the traction section from 1-10 based on available information and provide feedback on possible improvements.
    Optimal conditions for traction include:
    - Demonstrated early sales and revenue growth
    - Clear track record of customer acquisition and retention
    - Metrics and KPIs showing growth and market validation
    - Testimonials or case studies from early customers
    - Clear evidence of traction, such as user growth or partnership agreements


    """
    traction_content = dspy.InputField(desc="Content of the pitch deck.")
    traction_score: int = dspy.OutputField(desc="Score from 1-10 indicating the strength of the traction section")
    traction_feedback: list[str] = dspy.OutputField(desc="list containing 5 items each must start with *, specifying feedback for the traction to improve its score. If any information is missing, recommend for it to be included, don't add '\nUser:' at the end.")

class EvaluatePitchDeck(dspy.Signature):
    """
    Evaluate the provided pitch deck content across all sections: Team, Fundraising, Market, Business Model, Product, and Traction.
    The output is a dictionary with each section containing a score (1-10) and a list of feedback items.

I need you to provide feedback in the following JSON format. Each section should include a score and five feedback items. The startup name should also be included in the JSON output. Below is an example of the format I need:

{
    "startup_name": "Example Startup",
    "team": {
        "score": 8,
        "feedback_1": "The team has strong experience and a clear vision, but they need more diversity in skills.",
        "feedback_2": "The team's track record is impressive, but they lack experience in scaling businesses.",
        "feedback_3": "There is a strong leadership team, but more emphasis on technical skills is needed.",
        "feedback_4": "The team has a clear vision but needs better execution plans.",
        "feedback_5": "The team should work on improving communication strategies within the group."
    },
    "fundraising": {
        "score": 7,
        "feedback_1": "The startup has secured initial funding but needs to outline a clearer path for future rounds.",
        "feedback_2": "Funding sources are diversified, but there is a need for more detailed financial projections.",
        "feedback_3": "The pitch to investors is strong but needs better risk management strategies.",
        "feedback_4": "Current funding is sufficient for initial growth but not for scaling.",
        "feedback_5": "Consider exploring alternative funding options like grants or strategic partnerships."
    },
    "business_model": {
        "score": 9,
        "feedback_1": "The business model is solid with clear revenue streams and customer acquisition strategies.",
        "feedback_2": "There is a well-defined value proposition and revenue model.",
        "feedback_3": "The model is scalable and has potential for high margins.",
        "feedback_4": "Consider refining the pricing strategy to maximize revenue.",
        "feedback_5": "The business model is competitive but should anticipate market changes."
    },
    "market": {
        "score": 6,
        "feedback_1": "The market size is promising but the startup should provide more data on target demographics.",
        "feedback_2": "Market research needs to be more comprehensive to support growth projections.",
        "feedback_3": "Competitive analysis is lacking; include more details on market positioning.",
        "feedback_4": "There is potential in the market, but customer needs need to be better defined.",
        "feedback_5": "Market entry strategy is good but should address potential barriers to entry."
    },
    "product": {
        "score": 8,
        "feedback_1": "The product is well-developed and addresses key customer needs, though some additional features would be beneficial.",
        "feedback_2": "Product design is strong, but user experience could be improved.",
        "feedback_3": "Consider adding more functionality based on customer feedback.",
        "feedback_4": "The product has good potential but needs a more robust testing phase.",
        "feedback_5": "Ensure the product is adaptable to future market trends."
    },
    "traction": {
        "score": 5,
        "feedback_1": "There is some initial traction, but significant growth is needed to prove the business's potential.",
        "feedback_2": "Customer acquisition numbers are low; focus on scaling marketing efforts.",
        "feedback_3": "Early results are promising but need to be sustained over a longer period.",
        "feedback_4": "Traction metrics should include more detailed customer feedback.",
        "feedback_5": "Consider strategies to accelerate growth and increase user engagement."
    }
}

Please format your feedback in this exact JSON structure, including five feedback items and a score for each section. Ensure that the 'startup_name' field is included at the top level of the JSON object.

    """
    pitchdeck_content = dspy.InputField(desc="Content of the startup pitch deck.")
    evaluation_results = dspy.OutputField(desc="A dictionary in the given Json format containing scores and feedback for each section of the pitch deck.")