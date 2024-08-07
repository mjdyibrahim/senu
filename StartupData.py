from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union

class AcademicDegree(BaseModel):
    Undergraduate: bool
    Graduate_Degree: bool
    Masters: bool
    PhD_or_More: bool

class StartupExperience(BaseModel):
    Has_Been_Part_of_a_Startup_Team: bool
    Has_Been_the_Founder_of_a_Startup: bool
    Has_Previous_C_Level_Position: bool
    Has_Been_Part_of_a_Successful_Exit: bool

class Role(BaseModel):
    Marketing: bool
    Sales: bool
    Product: bool
    Creative: bool
    Technical: bool
    Operation: bool
    Other: Optional[str]

class TeamMember(BaseModel):
    Name: str
    Title: str
    Availability_Per_Week: int
    Involved_Since: str  # or date
    Equity_Percent: float
    Salary_Percent: float
    Years_of_Experience: int
    Academic_Degree: AcademicDegree
    Startup_Experience: StartupExperience
    Role: Role

class Team(BaseModel):
    Number_of_Team_Members: int
    Team_Members: List[TeamMember]
    Team_Overview: str
    Team_Assessment: str

class SourcesOfFunds(BaseModel):
    Founders: bool
    Friends_and_Family: bool
    Crowdfunding: bool
    Accelerator: bool
    Angel_Investor: bool
    VC: bool

class SpendingAllocation(BaseModel):
    Product: bool
    Marketing: bool
    Team: bool
    Operations: bool

class Fundraising(BaseModel):
    Current_Amount_Being_Raised: float
    Amount_Raised_So_Far: float
    Sources_of_Funds: SourcesOfFunds
    Spending_Allocation: SpendingAllocation
    Received_Patents: bool
    Significant_Achievements: bool
    Pitch_Deck_Ready: bool

class Market(BaseModel):
    Consumer_Payment: float
    Market_Size: float
    Market_Share_in_3_Years: float

class Charges(BaseModel):
    Capital: bool
    Content: bool
    Data_Information: bool
    Goods_Widgets_Resellers: bool
    Goods_Widgets_Producers: bool
    Hard_Science: bool
    Network_or_Community: bool
    Non_Physical_Direct_to_Consumer: bool
    Physical_Direct_to_Consumer: bool
    Services: bool
    Technology_Platform: bool
    Other: Optional[str]

class RevenueModel(BaseModel):
    Advertising: bool
    Pay_Per_Unit: bool
    Pay_Per_Project: bool
    Brokerage_or_Marketplace: Dict[str, bool]
    Recurring: bool
    Other: Optional[str]

class CustomerAcquisitionMethod(BaseModel):
    Online_Advertising: bool
    Strategic_Partnership: bool
    Affiliate_Marketing: bool
    Conferences_Exhibitions: bool
    Virtual_Word_of_Mouth: bool

class CustomerAcquisitionCost(BaseModel):
    Ten: bool
    Twenty: bool
    Thirty: bool

class UserBase(BaseModel):
    Everyone: bool
    Niche: bool

class BusinessModel(BaseModel):
    Primary_Industry: str
    Charges: Charges
    Revenue_Model: RevenueModel
    Customer_Acquisition_Method: CustomerAcquisitionMethod
    Customer_Acquisition_Cost: CustomerAcquisitionCost
    User_Base: UserBase

class ProductStage(BaseModel):
    Idea: bool
    Prototype: bool
    Beta: bool
    Live: bool

class Product(BaseModel):
    Product_Stage: ProductStage
    Prospective_Customers_Interviewed: int
    Percentage_of_Purchase_Intent: float

class Traction(BaseModel):
    Sales_and_Revenues_Started: bool
    Revenue_Past_12_Months: float
    Revenue_Past_3_Months: float
    Number_of_Leads_Resulting_in_Sales: int

class Info(BaseModel):
    Startup_Name: str
    Date_Started: str  # or date
    Registration_Type: str
    Registration_Country: str
    Contact_Info: str

class DataFields(BaseModel):
    Info: Info
    Team: Team
    Fundraising: Fundraising
    Market: Market
    Business_Model: BusinessModel
    Product: Product
    Traction: Traction

# Define a class that holds the entire structure
class StartupProfile(BaseModel):
    Info: Info
    Team: Team
    Fundraising: Fundraising
    Market: Market
    Business_Model: BusinessModel
    Product: Product
    Traction: Traction
