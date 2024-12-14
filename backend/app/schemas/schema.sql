-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS senu;

-- Use the created database
USE senu;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE startups (
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

CREATE TABLE pitch (
    id SERIAL PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(100) NOT NULL,
    tagline TEXT,
    description TEXT,
    dashboard_id INTEGER REFERENCES dashboard(id),
    team_id INTEGER REFERENCES teams(id),
    team_member_id INTEGER REFERENCES team_members(id),
    fundraising_id INTEGER REFERENCES fundraising(id),
    market_id INTEGER REFERENCES market(id),
    business_model_id INTEGER REFERENCES business_model(id),
    product_id INTEGER REFERENCES product(id),
    traction_id INTEGER REFERENCES traction(id)
);

CREATE TABLE dashboard (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    startup_id INTEGER REFERENCES startups(id),
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    burn_rate NUMERIC(5,2), 
    customer_acquisition_cost NUMERIC(5,2), 
    customer_lifetime_value NUMERIC(5,2), 
    exit_potential NUMERIC(5,2),
    valuation NUMERIC(5,2), 
    mojo NUMERIC(5,2)
);

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    name VARCHAR(100),
    description TEXT
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
    other_role TEXT,
    -- Contact fields
    linkedin VARCHAR(255),
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

CREATE TABLE crunchbase_objects (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(50),
    entity_id VARCHAR(50),
    parent_id INTEGER REFERENCES objects(id),
    name VARCHAR(255),
    normalized_name VARCHAR(255),
    permalink VARCHAR(255),
    category_code VARCHAR(50),
    status VARCHAR(50),
    founded_at DATE,
    closed_at DATE,
    domain VARCHAR(255),
    homepage_url VARCHAR(255), 
    twitter_username VARCHAR(50),
    logo_url VARCHAR(255),
    logo_width INTEGER,
    logo_height INTEGER,
    short_description TEXT,
    description TEXT,
    overview TEXT,
    tag_list TEXT,
    country_code VARCHAR(2),
    state_code VARCHAR(2),
    city VARCHAR(255),
    region VARCHAR(255),
    first_investment_at DATE,
    last_investment_at DATE,
    investment_rounds INTEGER,
    invested_companies INTEGER,
    first_funding_at DATE,
    last_funding_at DATE,
    funding_rounds INTEGER,
    funding_total_usd NUMERIC(20,2),
    first_milestone_at DATE,
    last_milestone_at DATE,
    created_by VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE crunchbase_people (
    id SERIAL PRIMARY KEY,
    object_id INTEGER REFERENCES objects(id),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birthplace VARCHAR(255),
    affiliation_name VARCHAR(255)
);

CREATE TABLE crunchbase_offices (
    id SERIAL PRIMARY KEY,
    object_id INTEGER REFERENCES objects(id),
    office_id VARCHAR(50),
    description TEXT,
    region VARCHAR(255),
    address1 VARCHAR(255),
    address2 VARCHAR(255),
    city VARCHAR(255),
    zip_code VARCHAR(50),
    state_code VARCHAR(2),
    country_code VARCHAR(2),
    latitude NUMERIC(10,6),
    longitude NUMERIC(10,6),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE crunchbase_funds (
    id SERIAL PRIMARY KEY,
    object_id INTEGER REFERENCES objects(id),
    name VARCHAR(255),
    funded_at DATE,
    raised_amount NUMERIC(20,2),
    raised_currency_code VARCHAR(3),
    source_url VARCHAR(255),
    source_description TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE crunchbase_degrees (
    id SERIAL PRIMARY KEY,
    object_id INTEGER REFERENCES objects(id),
    degree_type VARCHAR(50),
    subject VARCHAR(255),
    institution VARCHAR(255),
    graduated_at DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE crunchbase_milestones (
    id SERIAL PRIMARY KEY,
    object_id INTEGER REFERENCES objects(id),
    milestone_at DATE,
    milestone_code VARCHAR(50),
    description TEXT,
    source_url VARCHAR(255),
    source_description TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
CREATE TABLE crunchbase_acquisitions (
    id SERIAL PRIMARY KEY,
    acquiring_object_id INTEGER REFERENCES objects(id),
    acquired_object_id INTEGER REFERENCES objects(id),
    term_code VARCHAR(50),
    price_amount NUMERIC(20,2),
    price_currency_code VARCHAR(3),
    acquired_at DATE,
    source_url VARCHAR(255),
    source_description TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE crunchbase_investments (
    id SERIAL PRIMARY KEY,
    funding_round_id INTEGER REFERENCES rounds(id),
    funded_object_id INTEGER REFERENCES objects(id),
    investor_object_id INTEGER REFERENCES objects(id),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE crunchbase_rounds (
    id SERIAL PRIMARY KEY,
    object_id INTEGER REFERENCES objects(id),
    funded_at DATE,
    funding_round_type VARCHAR(50),
    funding_round_code VARCHAR(10),
    raised_amount_usd NUMERIC(20,2),
    raised_amount NUMERIC(20,2),
    raised_currency_code VARCHAR(3),
    pre_money_valuation_usd NUMERIC(20,2),
    pre_money_valuation NUMERIC(20,2),
    pre_money_currency_code VARCHAR(3),
    post_money_valuation_usd NUMERIC(20,2),
    post_money_valuation NUMERIC(20,2),
    post_money_currency_code VARCHAR(3),
    participants TEXT,
    is_first_round BOOLEAN,
    is_last_round BOOLEAN,
    source_url VARCHAR(255),
    source_description TEXT,
    created_by VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE crunchbase_ipos (
    id SERIAL PRIMARY KEY,
    object_id INTEGER REFERENCES objects(id),
    valuation_amount NUMERIC(20,2),
    valuation_currency_code VARCHAR(3),
    raised_amount NUMERIC(20,2),
    raised_currency_code VARCHAR(3),
    public_at DATE,
    stock_symbol VARCHAR(50),
    source_url VARCHAR(255),
    source_description TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE crunchbase_relationships (
    id SERIAL PRIMARY KEY,
    person_object_id INTEGER REFERENCES objects(id),
    relationship_object_id INTEGER REFERENCES objects(id),
    start_at DATE,
    end_at DATE,
    is_past BOOLEAN,
    sequence INTEGER,
    title VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);