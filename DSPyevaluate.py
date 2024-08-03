import dspy

class EvaluateTeamSection(dspy.Signature):
    """
    Score the strength of the team section from 1-10 based on available information and provide feedback on any possible improvements.
    Optimal conditions for the team include:
    - 2-3 cofounders, with near equal equity
    - Specialized academic degrees and/or expertise in their areas
    - Half-time or more commitment to the startup
    - Previous startup experience and successful exits
    - Team working together for a significant period
    - Presence of mentors with substantial experience
    """
    team_content = dspy.InputField(desc="Content of the team section from the pitch deck (all available information).")
    team_score = dspy.OutputField(desc="Score from 1-10 indicating the strength of the team section.")
    team_feedback = dspy.OutputField(desc="One paragraph with 5 numbered list items, specifying feedback for the team to improve its score based on the team_content only. If any information is missing, recommend for it to be included.")

class EvaluateFundraisingSection(dspy.Signature):
    """
    Score the strength of the fundraising section from 1-10 based on available information and provide feedback on any possible improvements.
    Optimal conditions for fundraising include:
    - A clear and feasible plan for raising funds in the next 12-18 months
    - Secured initial funding or demonstrated progress in fundraising
    - Identified potential sources of funding such as venture capital, angel investors, or grants
    - Detailed and realistic financial projection
    - A strong pitch deck and business plan that have been refined and tested with investors
    """
    fundraising_content = dspy.InputField(desc="Content of the fundraising section from the pitch deck.")
    fundraising_score = dspy.OutputField(desc="Score from 1-10 indicating the strength of the fundraising section.")
    fundraising_feedback = dspy.OutputField(desc="One paragraph with 5 numbered list items, specifying feedback for the fundraising to improve its score based on the fundraising_content only. If any information is missing, recommend for it to be included.")

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
    market_content = dspy.InputField(desc="Content of the market section from the pitch deck.")
    market_score = dspy.OutputField(desc="Score from 1-10 indicating the strength of the market section.")
    market_feedback = dspy.OutputField(desc="One paragraph with 5 numbered list items, specifying feedback for the market to improve its score based on the market_content only. If any information is missing, recommend for it to be included.")

class EvaluateBusinessModelSection(dspy.Signature):
    """
    Score the strength of the business model section from 1-10 based on available information and provide feedback on any possible improvements.
    Optimal conditions for the business model include:
    - Clear revenue model showing how the business will make money
    - Identified who will pay for the service and a strategy for acquiring customers
    - Defined pricing strategy and detailed plan for scaling revenue
    - Identified and planned for key metrics like customer acquisition cost and lifetime value
    - Validated business model with proof of concept or early traction
    """
    business_model_content = dspy.InputField(desc="Content of the business model section from the pitch deck.")
    business_model_score = dspy.OutputField(desc="Score from 1-10 indicating the strength of the business model section.")
    business_model_feedback = dspy.OutputField(desc="One paragraph with 5 numbered list items, specifying feedback for the business model to improve its score based on the business_model_content only. If any information is missing, recommend for it to be included.")

class EvaluateProductSection(dspy.Signature):
    """
    Score the strength of the product section from 1-10 based on available information and provide feedback on any possible improvements.
    Optimal conditions for the product include:
    - Product is functional and has been tested with users
    - Clear roadmap for product development and future features
    - Feedback from prospective customers indicating strong interest
    - Validated product-market fit or evidence of traction
    - Product solves a significant problem and has unique value propositions
    """
    product_content = dspy.InputField(desc="Content of the product section from the pitch deck.")
    product_score = dspy.OutputField(desc="Score from 1-10 indicating the strength of the product section.")
    product_feedback = dspy.OutputField(desc="One paragraph with 5 numbered list items, specifying feedback for the product to improve its score based on the product_content only. If any information is missing, recommend for it to be included.")

class EvaluateTractionSection(dspy.Signature):
    """
    Score the strength of the traction section from 1-10 based on available information and provide feedback on any possible improvements.
    Optimal conditions for traction include:
    - Demonstrated early sales and revenue growth
    - Clear track record of customer acquisition and retention
    - Metrics and KPIs showing growth and market validation
    - Testimonials or case studies from early customers
    - Clear evidence of traction, such as user growth or partnership agreements
    """
    traction_content = dspy.InputField(desc="Content of the traction section from the pitch deck.")
    traction_score = dspy.OutputField(desc="Score from 1-10 indicating the strength of the traction section.")
    traction_feedback = dspy.OutputField(desc="One paragraph with 5 numbered list items, specifying feedback for the traction to improve its score based on the traction_content only. If any information is missing, recommend for it to be included.")
