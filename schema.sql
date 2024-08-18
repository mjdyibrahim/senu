-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS senu;

-- Use the created database
USE senu;


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255)   
 NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE   
 startups (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(100) NOT NULL,
    tagline TEXT,
    description TEXT,
    date_started DATE,
    registration_type VARCHAR(50),
    registration_country VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    owner VARCHAR(100)
);

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    name VARCHAR(100),
    description TEXT,
    -- Other team-related fields
);

CREATE TABLE team_members (
    id SERIAL PRIMARY KEY,
    team_id INTEGER REFERENCES teams(id),
    name VARCHAR(100),
    title VARCHAR(50),
    availability_per_week INTEGER,
    involved_since DATE,
    equity_percentage NUMERIC(5,2),
    salary_percentage NUMERIC(5,2),
    years_of_experience INTEGER,
    -- Academic degree fields
    undergraduate BOOLEAN,
    graduate_degree BOOLEAN,
    masters BOOLEAN,
    phd_or_more BOOLEAN,
    -- Startup experience fields
    startup_team_member BOOLEAN,
    startup_founder BOOLEAN,
    c_level_position BOOLEAN,
    successful_exit BOOLEAN,
    -- Role fields
    marketing BOOLEAN,
    sales BOOLEAN,
    product BOOLEAN,
    creative BOOLEAN,
    technical BOOLEAN,
    operation BOOLEAN,
    other_role TEXT
    -- Contact fields
    linkedin VARCHAR(255)
    email VARCHAR(255)
);

CREATE TABLE fundraising (
    id SERIAL PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    current_amount_raised NUMERIC(10,2),
    amount_raised_so_far NUMERIC(10,2),
    -- Sources of funds fields
    founders BOOLEAN,
    friends_and_family BOOLEAN,
    crowdfunding BOOLEAN,
    accelerator BOOLEAN,
    angel_investor BOOLEAN,
    vc BOOLEAN,
    -- Spending allocation fields
    product BOOLEAN,
    marketing BOOLEAN,
    team BOOLEAN,
    operations BOOLEAN,
    received_patents BOOLEAN,
    significant_achievements BOOLEAN,
    pitch_deck_ready BOOLEAN
);

CREATE TABLE market (
    id SERIAL PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    consumer_payment NUMERIC(10,2),
    market_size INTEGER,
    market_share_in_3_years NUMERIC(5,2)
);

CREATE TABLE business_model (
    id SERIAL PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    primary_industry VARCHAR(100),
    -- Charges fields
    capital BOOLEAN,
    content BOOLEAN,
    data_information BOOLEAN,
    goods_resellers BOOLEAN,
    goods_producers BOOLEAN,
    hard_science BOOLEAN,
    network_community BOOLEAN,
    non_physical_direct_to_consumer BOOLEAN,
    physical_direct_to_consumer BOOLEAN,
    services BOOLEAN,
    technology_platform BOOLEAN,
    other_charges TEXT,
    -- Revenue model fields
    advertising BOOLEAN,
    pay_per_unit BOOLEAN,
    pay_per_project BOOLEAN,
    consumer_to_consumer BOOLEAN,
    enterprise_to_enterprise BOOLEAN,
    enterprise_to_consumer BOOLEAN,
    recurring BOOLEAN,
    other_revenue_model TEXT,
    -- Customer acquisition method fields
    online_advertising BOOLEAN,
    strategic_partnership BOOLEAN,
    affiliate_marketing BOOLEAN,
    conferences_exhibitions BOOLEAN,
    virtual_word_of_mouth BOOLEAN,
    customer_acquisition_cost NUMERIC(5,2),
    user_base_type VARCHAR(50)
);

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    -- Product stage fields
    idea BOOLEAN,
    prototype BOOLEAN,
    beta BOOLEAN,
    live BOOLEAN,
    prospective_customers_interviewed INTEGER,
    purchase_intent_percentage NUMERIC(5,2)
);

CREATE TABLE traction (
    id SERIAL PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    sales_started BOOLEAN,
    revenue_past_12_months NUMERIC(10,2),
    revenue_past_3_months NUMERIC(10,2),
    leads_resulting_in_sales INTEGER
);