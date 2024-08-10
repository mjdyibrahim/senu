-- Create a database for your application
CREATE DATABASE IF NOT EXISTS startup_profile;
USE startup_profile;

-- Table for Info section
CREATE TABLE Info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Startup_Name VARCHAR(255) NOT NULL,
    Date_Started DATE NOT NULL,
    Registration_Type VARCHAR(255) NOT NULL,
    Registration_Country VARCHAR(255) NOT NULL,
    Contact_Info VARCHAR(255) NOT NULL
);

-- Table for Academic Degree
CREATE TABLE AcademicDegree (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Undergraduate BOOLEAN NOT NULL,
    Graduate_Degree BOOLEAN NOT NULL,
    Masters BOOLEAN NOT NULL,
    PhD_or_More BOOLEAN NOT NULL
);

-- Table for Startup Experience
CREATE TABLE StartupExperience (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Has_Been_Part_of_a_Startup_Team BOOLEAN NOT NULL,
    Has_Been_the_Founder_of_a_Startup BOOLEAN NOT NULL,
    Has_Previous_C_Level_Position BOOLEAN NOT NULL,
    Has_Been_Part_of_a_Successful_Exit BOOLEAN NOT NULL
);

-- Table for Role
CREATE TABLE Role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Marketing BOOLEAN NOT NULL,
    Sales BOOLEAN NOT NULL,
    Product BOOLEAN NOT NULL,
    Creative BOOLEAN NOT NULL,
    Technical BOOLEAN NOT NULL,
    Operation BOOLEAN NOT NULL,
    Other VARCHAR(255)
);

-- Table for Team Members
CREATE TABLE TeamMember (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Title VARCHAR(255) NOT NULL,
    Availability_Per_Week INT NOT NULL,
    Involved_Since DATE NOT NULL,
    Equity_Percent DECIMAL(5, 2) NOT NULL,
    Salary_Percent DECIMAL(5, 2) NOT NULL,
    Years_of_Experience INT NOT NULL,
    Academic_Degree_ID INT NOT NULL,
    Startup_Experience_ID INT NOT NULL,
    Role_ID INT NOT NULL,
    FOREIGN KEY (Academic_Degree_ID) REFERENCES AcademicDegree(id),
    FOREIGN KEY (Startup_Experience_ID) REFERENCES StartupExperience(id),
    FOREIGN KEY (Role_ID) REFERENCES Role(id)
);

-- Table for Team
CREATE TABLE Team (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Number_of_Team_Members INT NOT NULL,
    Team_Overview TEXT NOT NULL,
    Team_Assessment TEXT NOT NULL
);

-- Table for Fundraising
CREATE TABLE Fundraising (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Current_Amount_Being_Raised DECIMAL(15, 2) NOT NULL,
    Amount_Raised_So_Far DECIMAL(15, 2) NOT NULL,
    Sources_of_Funds_Founders BOOLEAN NOT NULL,
    Sources_of_Funds_Friends_and_Family BOOLEAN NOT NULL,
    Sources_of_Funds_Crowdfunding BOOLEAN NOT NULL,
    Sources_of_Funds_Accelerator BOOLEAN NOT NULL,
    Sources_of_Funds_Angel_Investor BOOLEAN NOT NULL,
    Sources_of_Funds_VC BOOLEAN NOT NULL,
    Spending_Allocation_Product BOOLEAN NOT NULL,
    Spending_Allocation_Marketing BOOLEAN NOT NULL,
    Spending_Allocation_Team BOOLEAN NOT NULL,
    Spending_Allocation_Operations BOOLEAN NOT NULL,
    Received_Patents BOOLEAN NOT NULL,
    Significant_Achievements BOOLEAN NOT NULL,
    Pitch_Deck_Ready BOOLEAN NOT NULL
);

-- Table for Market
CREATE TABLE Market (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Consumer_Payment DECIMAL(15, 2) NOT NULL,
    Market_Size DECIMAL(15, 2) NOT NULL,
    Market_Share_in_3_Years DECIMAL(5, 2) NOT NULL
);

-- Table for Charges
CREATE TABLE Charges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Capital BOOLEAN NOT NULL,
    Content BOOLEAN NOT NULL,
    Data_Information BOOLEAN NOT NULL,
    Goods_Widgets_Resellers BOOLEAN NOT NULL,
    Goods_Widgets_Producers BOOLEAN NOT NULL,
    Hard_Science BOOLEAN NOT NULL,
    Network_or_Community BOOLEAN NOT NULL,
    Non_Physical_Direct_to_Consumer BOOLEAN NOT NULL,
    Physical_Direct_to_Consumer BOOLEAN NOT NULL,
    Services BOOLEAN NOT NULL,
    Technology_Platform BOOLEAN NOT NULL,
    Other VARCHAR(255)
);

-- Table for Revenue Model
CREATE TABLE RevenueModel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Advertising BOOLEAN NOT NULL,
    Pay_Per_Unit BOOLEAN NOT NULL,
    Pay_Per_Project BOOLEAN NOT NULL,
    Brokerage_or_Marketplace_Consumer_to_Consumer BOOLEAN NOT NULL,
    Brokerage_or_Marketplace_Enterprise_to_Enterprise BOOLEAN NOT NULL,
    Brokerage_or_Marketplace_Enterprise_to_Consumer BOOLEAN NOT NULL,
    Recurring BOOLEAN NOT NULL,
    Other VARCHAR(255)
);

-- Table for Customer Acquisition Method
CREATE TABLE CustomerAcquisitionMethod (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Online_Advertising BOOLEAN NOT NULL,
    Strategic_Partnership BOOLEAN NOT NULL,
    Affiliate_Marketing BOOLEAN NOT NULL,
    Conferences_Exhibitions BOOLEAN NOT NULL,
    Virtual_Word_of_Mouth BOOLEAN NOT NULL
);

-- Table for Customer Acquisition Cost
CREATE TABLE CustomerAcquisitionCost (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Ten BOOLEAN NOT NULL,
    Twenty BOOLEAN NOT NULL,
    Thirty BOOLEAN NOT NULL
);

-- Table for User Base
CREATE TABLE UserBase (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Everyone BOOLEAN NOT NULL,
    Niche BOOLEAN NOT NULL
);

-- Table for Business Model
CREATE TABLE BusinessModel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Primary_Industry VARCHAR(255) NOT NULL,
    Charges_ID INT NOT NULL,
    Revenue_Model_ID INT NOT NULL,
    Customer_Acquisition_Method_ID INT NOT NULL,
    Customer_Acquisition_Cost_ID INT NOT NULL,
    User_Base_ID INT NOT NULL,
    FOREIGN KEY (Charges_ID) REFERENCES Charges(id),
    FOREIGN KEY (Revenue_Model_ID) REFERENCES RevenueModel(id),
    FOREIGN KEY (Customer_Acquisition_Method_ID) REFERENCES CustomerAcquisitionMethod(id),
    FOREIGN KEY (Customer_Acquisition_Cost_ID) REFERENCES CustomerAcquisitionCost(id),
    FOREIGN KEY (User_Base_ID) REFERENCES UserBase(id)
);

-- Table for Product Stage
CREATE TABLE ProductStage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Idea BOOLEAN NOT NULL,
    Prototype BOOLEAN NOT NULL,
    Beta BOOLEAN NOT NULL,
    Live BOOLEAN NOT NULL
);

-- Table for Product
CREATE TABLE Product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Product_Stage_ID INT NOT NULL,
    Prospective_Customers_Interviewed INT NOT NULL,
    Percentage_of_Purchase_Intent DECIMAL(5, 2) NOT NULL,
    FOREIGN KEY (Product_Stage_ID) REFERENCES ProductStage(id)
);

-- Table for Traction
CREATE TABLE Traction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Sales_and_Revenues_Started BOOLEAN NOT NULL,
    Revenue_Past_12_Months DECIMAL(15, 2) NOT NULL,
    Revenue_Past_3_Months DECIMAL(15, 2) NOT NULL,
    Number_of_Leads_Resulting_in_Sales INT NOT NULL
);
