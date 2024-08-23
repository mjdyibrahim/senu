import requests
import json
import os
import datetime
import logging
from openai import OpenAI
import app.models
import dspy
from app.services.aimlapi import AIMLAPI
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.openai import OpenAIInstrumentor

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print("Script started")
logging.info("Initializing...")

# Load environment variables
load_dotenv()
print("Environment variables loaded")

# Set up OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
print("OpenTelemetry tracer set up")

# Set up the OTLP exporter
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)
print("OTLP exporter set up")

# Initialize OpenAI instrumentation
OpenAIInstrumentor().instrument()
print("OpenAI instrumentation initialized")

# Initialize OpenAI client
client = OpenAI()
print("OpenAI client initialized")

# Set your API key and endpoint
AIML_API_KEY = os.getenv("AIML_API_KEY")
ENDPOINT_URL = 'https://api.aimlapi.com/chat/completions'

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

meta_model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
openai_model ="openai/gpt-4o"

# Define your JSON template for generating data
template = {
    "Info": {
        "Startup Name": "<STARTUP_NAME>",
        "Date Started": "<DATE_STARTED>",
        "Registration Type": "<REGISTRATION_TYPE>",
        "Registration Country": "<REGISTRATION_COUNTRY>",
        "Contact Info": "<CONTACT_INFO>"
    },
    "Team": {
        "Number of Team Members": "<NUMBER_OF_TEAM_MEMBERS>",
        "Team Members": {
            "Name": "<TEAM_MEMBER_NAME>",
            "Title": "<TEAM_MEMBER_TITLE>",
            "Availability Per Week": "<AVAILABILITY_PER_WEEK>",
            "Involved Since": "<INVOLVED_SINCE>",
            "Equity %": "<EQUITY_PERCENTAGE>",
            "Salary %": "<SALARY_PERCENTAGE>",
            "Years of Experience": "<YEARS_OF_EXPERIENCE>",
            "Academic Degree": {
                "Undergraduate": "<UNDERGRADUATE_DEGREE>",
                "Graduate Degree": "<GRADUATE_DEGREE>",
                "Masters": "<MASTERS_DEGREE>",
                "PhD or More": "<PHD_OR_MORE>"
            },
            "Startup Experience": {
                "Has Been Part of a Startup Team": "<HAS_BEEN_PART_OF_STARTUP_TEAM>",
                "Has Been the Founder of a Startup": "<HAS_BEEN_FOUNDER_OF_STARTUP>",
                "Has Previous C-Level Position": "<HAS_PREVIOUS_CLEVEL_POSITION>",
                "Has Been Part of a Successful Exit": "<HAS_SUCCESSFUL_EXIT>"
            },
            "Role": "<TEAM_MEMBER_ROLE>"
        },
        "Team Overview": "<TEAM_OVERVIEW>",
        "Team Assessment": "<TEAM_ASSESSMENT>"
    },
    "Fundraising": {
        "Current Amount Being Raised": "<CURRENT_AMOUNT_BEING_RAISED>",
        "Amount Raised So Far": "<AMOUNT_RAISED_SO_FAR>",
        "Sources of Funds": {
            "Founders": "<FOUNDERS>",
            "Friends and Family": "<FRIENDS_AND_FAMILY>",
            "Crowdfunding": "<CROWDFUNDING>",
            "Accelerator": "<ACCELERATOR>",
            "Angel Investor": "<ANGEL_INVESTOR>",
            "VC": "<VC>"
        },
        "Spending Allocation": {
            "Product": "<SPENDING_ON_PRODUCT>",
            "Marketing": "<SPENDING_ON_MARKETING>",
            "Team": "<SPENDING_ON_TEAM>",
            "Operations": "<SPENDING_ON_OPERATIONS>"
        },
        "Received Patents": "<RECEIVED_PATENTS>",
        "Significant Achievements": "<SIGNIFICANT_ACHIEVEMENTS>",
        "Pitch Deck Ready": "<PITCH_DECK_READY>"
    },
    "Market": {
        "Consumer Payment": "<CONSUMER_PAYMENT>",
        "Market Size": "<MARKET_SIZE>",
        "Market Share in 3 Years": "<MARKET_SHARE_IN_3_YEARS>"
    },
    "Business Model": {
        "Primary Industry": "<PRIMARY_INDUSTRY>",
        "Charges": {
            "Capital": "<CHARGES_CAPITAL>",
            "Content": "<CHARGES_CONTENT>",
            "Data / Information": "<CHARGES_DATA_INFORMATION>",
            "Goods / Widgets (Resellers)": "<CHARGES_GOODS_RESELLERS>",
            "Goods / Widgets (Producers)": "<CHARGES_GOODS_PRODUCERS>",
            "Hard Science": "<CHARGES_HARD_SCIENCE>",
            "Network or Community": "<CHARGES_NETWORK_COMMUNITY>",
            "Non-Physical Direct to Consumer": "<CHARGES_NON_PHYSICAL_DIRECT_CONSUMER>",
            "Physical Direct to Consumer": "<CHARGES_PHYSICAL_DIRECT_CONSUMER>",
            "Services": "<CHARGES_SERVICES>",
            "Technology / Platform": "<CHARGES_TECHNOLOGY_PLATFORM>",
            "Other": "<CHARGES_OTHER>"
        },
        "Revenue Model": {
            "Advertising": "<REVENUE_MODEL_ADVERTISING>",
            "Pay Per Unit": "<REVENUE_MODEL_PAY_PER_UNIT>",
            "Pay Per Project": "<REVENUE_MODEL_PAY_PER_PROJECT>",
            "Brokerage or Marketplace": {
                "Consumer to Consumer": "<BROKERAGE_C2C>",
                "Enterprise to Enterprise": "<BROKERAGE_E2E>",
                "Enterprise to Consumer": "<BROKERAGE_E2C>"
            },
            "Recurring": "<REVENUE_MODEL_RECURRING>",
            "Other": "<REVENUE_MODEL_OTHER>"
        },
        "Customer Acquisition Method": {
            "Online Advertising": "<ACQUISITION_ONLINE_ADVERTISING>",
            "Strategic Partnership": "<ACQUISITION_STRATEGIC_PARTNERSHIP>",
            "Affiliate Marketing": "<ACQUISITION_AFFILIATE_MARKETING>",
            "Conferences & Exhibitions": "<ACQUISITION_CONFERENCES_EXHIBITIONS>",
            "Virtual / Word of Mouth": "<ACQUISITION_VIRTUAL_WORD_OF_MOUTH>"
        },
        "Customer Acquisition Cost": {
            "10": "<COST_10>",
            "20": "<COST_20>",
            "30": "<COST_30>"
        },
        "User Base": {
            "Everyone": "<USER_BASE_EVERYONE>",
            "Niche": "<USER_BASE_NICHE>"
        }
    },
    "Product": {
        "Product Stage": {
            "Idea": "<PRODUCT_STAGE_IDEA>",
            "Prototype": "<PRODUCT_STAGE_PROTOTYPE>",
            "Beta": "<PRODUCT_STAGE_BETA>",
            "Live": "<PRODUCT_STAGE_LIVE>"
        },
        "Prospective Customers Interviewed": "<PROSPECTIVE_CUSTOMERS_INTERVIEWED>",
        "Percentage of Purchase Intent": "<PERCENTAGE_PURCHASE_INTENT>"
    },
    "Traction": {
        "Sales and Revenues Started": "<SALES_REVENUES_STARTED>",
        "Revenue Past 12 Months": "<REVENUE_PAST_12_MONTHS>",
        "Revenue Past 3 Months": "<REVENUE_PAST_3_MONTHS>",
        "Number of Leads Resulting in Sales": "<NUMBER_LEADS_RESULTING_IN_SALES>"
    }
}

# Define your prompts based on the startup data schema
prompts = {
    "Info": {
        "Startup Name": "Generate a realistic startup name:",
        "Date Started": "Generate a startup founding date in YYYY-MM-DD format:",
        "Registration Type": "Generate a registration type (e.g., LLC, Corporation):",
        "Registration Country": "Generate a country for registration:",
        "Contact Info": "Generate generic contact information for the startup (e.g., email, phone number):"
    },
    "Team": {
        "Number of Team Members": "How many team members does the startup have?",
        "Team Members": {
            "Name": "Generate a realistic name for a team member:",
            "Title": "Generate a job title for this team member:",
            "Availability Per Week": "How many hours per week is this team member available?",
            "Involved Since": "Generate the date when this team member started being involved in YYYY-MM-DD format:",
            "Equity %": "Generate a realistic equity percentage for this team member:",
            "Salary %": "Generate a realistic salary percentage for this team member:",
            "Years of Experience": "How many years of experience does this team member have?",
            "Academic Degree": {
                "Undergraduate": "Does this team member have an undergraduate degree? (Yes/No)",
                "Graduate Degree": "Does this team member have a graduate degree? (Yes/No)",
                "Masters": "Does this team member have a master's degree? (Yes/No)",
                "PhD or More": "Does this team member have a PhD or higher degree? (Yes/No)"
            },
            "Startup Experience": {
                "Has Been Part of a Startup Team": "Has this team member been part of a startup team before? (Yes/No)",
                "Has Been the Founder of a Startup": "Has this team member been the founder of a startup? (Yes/No)",
                "Has Previous C-Level Position": "Has this team member held a previous C-level position? (Yes/No)",
                "Has Been Part of a Successful Exit": "Has this team member been part of a successful exit? (Yes/No)"
            },
            "Role": "Generate a primary role for this team member (e.g., Marketing, Sales, Product, Technical, etc.):"
        },
        "Team Overview": "Provide an overview of the team's qualifications and expertise:",
        "Team Assessment": "How would you assess the team's experience and ability to execute the business plan?"
    },
    "Fundraising": {
        "Current Amount Being Raised": "How much money is the startup currently raising (in USD)?",
        "Amount Raised So Far": "How much money has the startup raised so far (in USD)?",
        "Sources of Funds": {
            "Founders": "Are the funds from Founders? (Yes/No)",
            "Friends and Family": "Are the funds from Friends and Family? (Yes/No)",
            "Crowdfunding": "Are the funds from Crowdfunding? (Yes/No)",
            "Accelerator": "Are the funds from an Accelerator? (Yes/No)",
            "Angel Investor": "Are the funds from an Angel Investor? (Yes/No)",
            "VC": "Are the funds from a VC? (Yes/No)"
        },
        "Spending Allocation": {
            "Product": "Will the funds be spent on Product? (Yes/No)",
            "Marketing": "Will the funds be spent on Marketing? (Yes/No)",
            "Team": "Will the funds be spent on Team? (Yes/No)",
            "Operations": "Will the funds be spent on Operations? (Yes/No)"
        },
        "Received Patents": "Has the startup received any patents? (Yes/No)",
        "Significant Achievements": "Has the startup accomplished any significant achievements? (Yes/No)",
        "Pitch Deck Ready": "Is the startup's pitch deck ready? (Yes/No)"
    },
    "Market": {
        "Consumer Payment": "How much are consumers currently paying on an annual basis to resolve this problem (in USD)?",
        "Market Size": "How big is the market in numbers (e.g., total addressable market size)?",
        "Market Share in 3 Years": "What market share is the startup planning to acquire in the next 3 years (in percentage)?"
    },
    "Business Model": {
        "Primary Industry": "What is the startup's primary industry?",
        "Charges": {
            "Capital": "Is the startup charging for Capital (Real Estate or Cash)? (Yes/No)",
            "Content": "Is the startup charging for Content? (Yes/No)",
            "Data / Information": "Is the startup charging for Data / Information? (Yes/No)",
            "Goods / Widgets (Resellers)": "Is the startup charging for Goods / Widgets (Resellers)? (Yes/No)",
            "Goods / Widgets (Producers)": "Is the startup charging for Goods / Widgets (Producers)? (Yes/No)",
            "Hard Science": "Is the startup charging for Hard Science (BioTech, Pharma, AI, etc.)? (Yes/No)",
            "Network or Community": "Is the startup charging for Network or Community? (Yes/No)",
            "Non-Physical Direct to Consumer": "Is the startup charging for Non-Physical Direct to Consumer (in-app purchases, Freemium, etc.)? (Yes/No)",
            "Physical Direct to Consumer": "Is the startup charging for Physical Direct to Consumer (monthly deliveries, etc.)? (Yes/No)",
            "Services": "Is the startup charging for Services (health care, professional services, legal services, etc.)? (Yes/No)",
            "Technology / Platform": "Is the startup charging for Technology / Platform? (Yes/No)",
            "Other": "What other charges is the startup applying?"
        },
        "Revenue Model": {
            "Advertising": "Is the startup's revenue model based on Advertising? (Yes/No)",
            "Pay Per Unit": "Is the startup's revenue model based on Pay Per Unit? (Yes/No)",
            "Pay Per Project": "Is the startup's revenue model based on Pay Per Project? (Yes/No)",
            "Brokerage or Marketplace": {
                "Consumer to Consumer": "Is the startup's marketplace model Consumer to Consumer (e.g., Airbnb)? (Yes/No)",
                "Enterprise to Enterprise": "Is the startup's marketplace model Enterprise to Enterprise (e.g., NYSE)? (Yes/No)",
                "Enterprise to Consumer": "Is the startup's marketplace model Enterprise to Consumer (e.g., Amazon)? (Yes/No)"
            },
            "Recurring": "Is the startup's revenue model Recurring (Rental, Subscription, Premiums, etc.)? (Yes/No)",
            "Other": "What other revenue model is the startup using?"
        },
        "Customer Acquisition Method": {
            "Online Advertising": "Is the startup using Online Advertising? (Yes/No)",
            "Strategic Partnership": "Is the startup using Strategic Partnership? (Yes/No)",
            "Affiliate Marketing": "Is the startup using Affiliate Marketing? (Yes/No)",
            "Conferences & Exhibitions": "Is the startup using Conferences & Exhibitions? (Yes/No)",
            "Virtual / Word of Mouth": "Is the startup using Virtual / Word of Mouth? (Yes/No)"
        },
        "Customer Acquisition Cost": {
            "10": "Is the cost to acquire each customer 10% of the sale value? (Yes/No)",
            "20": "Is the cost to acquire each customer 20% of the sale value? (Yes/No)",
            "30": "Is the cost to acquire each customer 30% of the sale value? (Yes/No)"
        },
        "User Base": {
            "Everyone": "Is the startup's user base Everyone? (Yes/No)",
            "Niche": "Is the startup's user base Niche? (Yes/No)"
        }
    },
    "Product": {
        "Product Stage": {
            "Idea": "Is the product at the Idea stage? (Yes/No)",
            "Prototype": "Is the product at the Prototype stage? (Yes/No)",
            "Beta": "Is the product at the Beta stage? (Yes/No)",
            "Live": "Is the product at the Live stage? (Yes/No)"
        },
        "Prospective Customers Interviewed": "How many prospective customers has the startup interviewed in the past 3 months?",
        "Percentage of Purchase Intent": "What percentage of these prospects said they would purchase the product or service?"
    },
    "Traction": {
        "Sales and Revenues Started": "Has the startup already started making sales and generating revenues? (Yes/No)",
        "Revenue Past 12 Months": "How much revenue has the startup realized over the past twelve months (in USD)?",
        "Revenue Past 3 Months": "How much revenue has the startup realized over the past three months (in USD)?",
        "Number of Leads Resulting in Sales": "How many individual leads have resulted in these sales?"
    }
}

data_schema = {
    "Info": {
        "Startup Name": "string",
        "Date Started": "date",
        "Registration Type": "string",
        "Registration Country": "string",
        "Contact Info": "string"
    },
    "Team": {
        "Number of Team Members": "integer",
        "Team Members": {
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
        },
        "Team Overview": "string",
        "Team Assessment": "string"
    },
    "Fundraising": {
        "Current Amount Being Raised": "number",
        "Amount Raised So Far": "number",
        "Sources of Funds": {
            "Founders": "boolean",
            "Friends and Family": "boolean",
            "Crowdfunding": "boolean",
            "Accelerator": "boolean",
            "Angel Investor": "boolean",
            "VC": "boolean"
        },
        "Spending Allocation": {
            "Product": "boolean",
            "Marketing": "boolean",
            "Team": "boolean",
            "Operations": "boolean"
        },
        "Received Patents": "boolean",
        "Significant Achievements": "boolean",
        "Pitch Deck Ready": "boolean"
    },
    "Market": {
        "Consumer Payment": "number",
        "Market Size": "number",
        "Market Share in 3 Years": "number"
    },
    "Business Model": {
        "Primary Industry": "string",
        "Charges": {
            "Capital": "boolean",
            "Content": "boolean",
            "Data / Information": "boolean",
            "Goods / Widgets (Resellers)": "boolean",
            "Goods / Widgets (Producers)": "boolean",
            "Hard Science": "boolean",
            "Network or Community": "boolean",
            "Non-Physical Direct to Consumer": "boolean",
            "Physical Direct to Consumer": "boolean",
            "Services": "boolean",
            "Technology / Platform": "boolean",
            "Other": "string"
        },
        "Revenue Model": {
            "Advertising": "boolean",
            "Pay Per Unit": "boolean",
            "Pay Per Project": "boolean",
            "Brokerage or Marketplace": {
                "Consumer to Consumer": "boolean",
                "Enterprise to Enterprise": "boolean",
                "Enterprise to Consumer": "boolean"
            },
            "Recurring": "boolean",
            "Other": "string"
        },
        "Customer Acquisition Method": {
            "Online Advertising": "boolean",
            "Strategic Partnership": "boolean",
            "Affiliate Marketing": "boolean",
            "Conferences & Exhibitions": "boolean",
            "Virtual / Word of Mouth": "boolean"
        },
        "Customer Acquisition Cost": {
            "10": "boolean",
            "20": "boolean",
            "30": "boolean"
        },
        "User Base": {
            "Everyone": "boolean",
            "Niche": "boolean"
        }
    },
    "Product": {
        "Product Stage": {
            "Idea": "boolean",
            "Prototype": "boolean",
            "Beta": "boolean",
            "Live": "boolean"
        },
        "Prospective Customers Interviewed": "integer",
        "Percentage of Purchase Intent": "number"
    },
    "Traction": {
        "Sales and Revenues Started": "boolean",
        "Revenue Past 12 Months": "number",
        "Revenue Past 3 Months": "number",
        "Number of Leads Resulting in Sales": "integer"
    }
}

# Function to generate data based on the provided template and prompts
def generate_data(section, fields, system_message):
    prompt = f"Generate data for the section: {section} with the following fields: {json.dumps(fields)}"
    
    data = {
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "model": openai_model,
        "max_tokens": 4000,
        "response_format": {"type": "json_object"}
    }
    
    try:
        response = client.chat.completions.create(
            model=data["model"],
            messages=data["messages"],
            max_tokens=data["max_tokens"],
            response_format=data["response_format"]
        )
        print(response)
        # Extracting the plain text content from the response
        content = response.choices[0].message.content
        
        if content:
            return content.strip()  # Return the raw LLM output as plain text
        else:
            logging.error("No content found in response.")
            return None
    except Exception as e:
        logging.error(f"Error parsing response: {str(e)}", exc_info=True)
        return None

def save_startup_data_to_file(startup_id, generated_data):
    # Directory to save the startup data
    output_dir = 'data/synthetic'
    os.makedirs(output_dir, exist_ok=True)
    
    # File name based on the startup ID (e.g., 00001.txt)
    output_file = os.path.join(output_dir, f'{startup_id:05d}.txt')
    
    # Save the accumulated data to a file
    with open(output_file, 'w') as f:
        f.write(generated_data)
    
    logging.info(f'Saved startup data to {output_file}')

def get_last_startup_id():
    output_dir = 'data/synthetic'
    os.makedirs(output_dir, exist_ok=True)

    # Get the list of files in the output directory
    existing_files = os.listdir(output_dir)
    
    # Filter out files that match the pattern of our startup files (e.g., 00001.txt)
    startup_files = [f for f in existing_files if f.endswith('.txt') and f[:5].isdigit()]
    
    if startup_files:
        # Find the maximum ID from existing files
        last_id = max(int(f[:5]) for f in startup_files)
    else:
        last_id = 0  # If no files exist, start with ID 0
    
    return last_id

def main():
    print("Entering main function")
    # Get the last startup ID from existing files
    last_startup_id = get_last_startup_id()
    startup_id = last_startup_id + 1  # Start with the next ID
    
    system_message = "You are a system that generates synthetic data for a startup. Follow the provided data schema exactly and generate realistic data based on the prompts."

    while True:  # Loop to generate data for multiple startups
        startup_data = ""
        
        for section, fields in prompts.items():
            logging.info(f"Generating data for startup {startup_id:05d}, section {section}...")
            
            # Generate data for the section
            generated_text = generate_data(section, fields, system_message)
            
            if generated_text:
                # Accumulate the generated data for the startup
                startup_data += f"**{section}**\n{generated_text}\n\n"
            else:
                logging.error(f"Failed to generate data for {section} in startup {startup_id:05d}.")
        
        # Save the accumulated data for the startup into a single file
        save_startup_data_to_file(startup_id, startup_data)
        
        startup_id += 1  # Increment the startup ID for the next file

        # Here you can add a condition to break the loop, e.g., after a certain number of startups
        if startup_id > last_startup_id + 10:  # For example, generate data for 10 startups
            break

    print("Main function completed")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logging.error(f"Error details: {str(e)}", exc_info=True)

print("Script ended")