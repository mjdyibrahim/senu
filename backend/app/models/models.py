from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from database import Base

# User models
class UserBase(BaseModel):
    username: str
    email: EmailStr

    model_config = {
        "populate_by_name": True
    }

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    model_config = {
        "populate_by_name": True
    }

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    startups = relationship("StartupDB", back_populates="user")

# Startup models
class StartupBase(BaseModel):
    name: str
    tagline: Optional[str] = None
    description: Optional[str] = None
    date_started: Optional[date] = None
    registration_type: Optional[str] = None
    registration_country: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    owner: Optional[str] = None

    model_config = {
        "populate_by_name": True
    }

class StartupCreate(StartupBase):
    pass

class Startup(StartupBase):
    id: int
    user_id: int
    date_added: datetime

    model_config = {
        "populate_by_name": True
    }

class StartupDB(Base):
    __tablename__ = "startups"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date_added = Column(DateTime, default=datetime.utcnow)
    name = Column(String, index=True)
    tagline = Column(String, nullable=True)
    description = Column(String, nullable=True)
    date_started = Column(Date, nullable=True)
    registration_type = Column(String, nullable=True)
    registration_country = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    owner = Column(String, nullable=True)

    user = relationship("UserDB", back_populates="startups")
    pitches = relationship("PitchDB", back_populates="startup")

# Pitch models
class PitchBase(BaseModel):
    name: str
    tagline: Optional[str] = None
    description: Optional[str] = None

    model_config = {
        "populate_by_name": True
    }

class PitchCreate(PitchBase):
    startup_id: int

class Pitch(PitchBase):
    id: int
    startup_id: int
    date_added: datetime
    dashboard_id: Optional[int] = None
    team_id: Optional[int] = None
    team_member_id: Optional[int] = None
    fundraising_id: Optional[int] = None
    market_id: Optional[int] = None
    business_model_id: Optional[int] = None
    product_id: Optional[int] = None
    traction_id: Optional[int] = None

    model_config = {
        "populate_by_name": True
    }

class PitchDB(Base):
    __tablename__ = "pitches"

    id = Column(Integer, primary_key=True, index=True)
    startup_id = Column(Integer, ForeignKey("startups.id"))
    date_added = Column(DateTime, default=datetime.utcnow)
    name = Column(String, index=True)
    tagline = Column(String, nullable=True)
    description = Column(String, nullable=True)
    dashboard_id = Column(Integer, ForeignKey("dashboards.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    team_member_id = Column(Integer, ForeignKey("team_members.id"), nullable=True)
    fundraising_id = Column(Integer, ForeignKey("fundraising.id"), nullable=True)
    market_id = Column(Integer, ForeignKey("markets.id"), nullable=True)
    business_model_id = Column(Integer, ForeignKey("business_models.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    traction_id = Column(Integer, ForeignKey("traction.id"), nullable=True)

    startup = relationship("StartupDB", back_populates="pitches")
    dashboard = relationship("DashboardDB", back_populates="pitch")
    team = relationship("TeamDB", back_populates="pitch")
    fundraising = relationship("FundraisingDB", back_populates="pitch")
    market = relationship("MarketDB", back_populates="pitch")
    business_model = relationship("BusinessModelDB", back_populates="pitch")
    product = relationship("ProductDB", back_populates="pitch")
    traction = relationship("TractionDB", back_populates="pitch")

# Dashboard models
class DashboardBase(BaseModel):
    burn_rate: Optional[Decimal] = None
    customer_acquisition_cost: Optional[Decimal] = None
    customer_lifetime_value: Optional[Decimal] = None
    exit_potential: Optional[Decimal] = None
    valuation: Optional[Decimal] = None
    mojo: Optional[Decimal] = None

    model_config = {
        "populate_by_name": True
    }

class DashboardCreate(DashboardBase):
    user_id: int
    startup_id: int

class Dashboard(DashboardBase):
    id: int
    user_id: int
    startup_id: int
    date_added: datetime

    model_config = {
        "populate_by_name": True
    }

class DashboardDB(Base):
    __tablename__ = "dashboards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    startup_id = Column(Integer, ForeignKey("startups.id"))
    date_added = Column(DateTime, default=datetime.utcnow)
    burn_rate = Column(Numeric, nullable=True)
    customer_acquisition_cost = Column(Numeric, nullable=True)
    customer_lifetime_value = Column(Numeric, nullable=True)
    exit_potential = Column(Numeric, nullable=True)
    valuation = Column(Numeric, nullable=True)
    mojo = Column(Numeric, nullable=True)

    pitch = relationship("PitchDB", back_populates="dashboard")

# Team models
class TeamBase(BaseModel):
    size: Optional[int] = None
    description: Optional[str] = None

    model_config = {
        "populate_by_name": True
    }

class TeamCreate(TeamBase):
    pitch_id: int

class Team(TeamBase):
    id: int
    pitch_id: int
    date_added: datetime

    model_config = {
        "populate_by_name": True
    }

class TeamDB(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"))
    date_added = Column(DateTime, default=datetime.utcnow)
    size = Column(Integer, nullable=True)
    description = Column(String, nullable=True)

    pitch = relationship("PitchDB", back_populates="team")

# TeamMember models
class TeamMemberBase(BaseModel):
    name: str
    role: Optional[str] = None
    bio: Optional[str] = None
    linkedin: Optional[str] = None

    model_config = {
        "populate_by_name": True
    }

class TeamMemberCreate(TeamMemberBase):
    team_id: int

class TeamMember(TeamMemberBase):
    id: int
    team_id: int
    date_added: datetime

    model_config = {
        "populate_by_name": True
    }

class TeamMemberDB(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    date_added = Column(DateTime, default=datetime.utcnow)
    name = Column(String)
    role = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)

    team = relationship("TeamDB", back_populates="team_members")

# Fundraising models
class FundraisingBase(BaseModel):
    amount_raised: Optional[Decimal] = None
    target_amount: Optional[Decimal] = None
    pre_money_valuation: Optional[Decimal] = None
    equity_offered: Optional[Decimal] = None
    funding_stage: Optional[str] = None

    model_config = {
        "populate_by_name": True
    }

class FundraisingCreate(FundraisingBase):
    pitch_id: int

class Fundraising(FundraisingBase):
    id: int
    pitch_id: int
    date_added: datetime

    model_config = {
        "populate_by_name": True
    }

class FundraisingDB(Base):
    __tablename__ = "fundraising"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"))
    date_added = Column(DateTime, default=datetime.utcnow)
    amount_raised = Column(Numeric, nullable=True)
    target_amount = Column(Numeric, nullable=True)
    pre_money_valuation = Column(Numeric, nullable=True)
    equity_offered = Column(Numeric, nullable=True)
    funding_stage = Column(String, nullable=True)

    pitch = relationship("PitchDB", back_populates="fundraising")

# Market models
class MarketBase(BaseModel):
    size: Optional[Decimal] = None
    growth_rate: Optional[Decimal] = None
    competitors: Optional[str] = None

    model_config = {
        "populate_by_name": True
    }

class MarketCreate(MarketBase):
    pitch_id: int

class Market(MarketBase):
    id: int
    pitch_id: int
    date_added: datetime

    model_config = {
        "populate_by_name": True
    }

class MarketDB(Base):
    __tablename__ = "markets"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"))
    date_added = Column(DateTime, default=datetime.utcnow)
    size = Column(Numeric, nullable=True)
    growth_rate = Column(Numeric, nullable=True)
    competitors = Column(String, nullable=True)

    pitch = relationship("PitchDB", back_populates="market")

# BusinessModel models
class BusinessModelBase(BaseModel):
    revenue_streams: Optional[str] = None
    cost_structure: Optional[str] = None
    channels: Optional[str] = None

    model_config = {
        "populate_by_name": True
    }

class BusinessModelCreate(BusinessModelBase):
    pitch_id: int

class BusinessModel(BusinessModelBase):
    id: int
    pitch_id: int
    date_added: datetime

    model_config = {
        "populate_by_name": True
    }

class BusinessModelDB(Base):
    __tablename__ = "business_models"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"))
    date_added = Column(DateTime, default=datetime.utcnow)
    revenue_streams = Column(String, nullable=True)
    cost_structure = Column(String, nullable=True)
    channels = Column(String, nullable=True)

    pitch = relationship("PitchDB", back_populates="business_model")

# Product models
class ProductBase(BaseModel):
    features: Optional[str] = None
    development_stage: Optional[str] = None
    intellectual_property: Optional[str] = None

    model_config = {
        "populate_by_name": True
    }

class ProductCreate(ProductBase):
    pitch_id: int

class Product(ProductBase):
    id: int
    pitch_id: int
    date_added: datetime

    model_config = {
        "populate_by_name": True
    }

class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"))
    date_added = Column(DateTime, default=datetime.utcnow)
    features = Column(String, nullable=True)
    development_stage = Column(String, nullable=True)
    intellectual_property = Column(String, nullable=True)

    pitch = relationship("PitchDB", back_populates="product")

# Traction models
class TractionBase(BaseModel):
    metrics: Optional[str] = None
    milestones: Optional[str] = None
    partnerships: Optional[str] = None

    model_config = {
        "populate_by_name": True
    }

class TractionCreate(TractionBase):
    pitch_id: int

class Traction(TractionBase):
    id: int
    pitch_id: int
    date_added: datetime

    model_config = {
        "populate_by_name": True
    }

class TractionDB(Base):
    __tablename__ = "traction"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"))
    date_added = Column(DateTime, default=datetime.utcnow)
    metrics = Column(String, nullable=True)
    milestones = Column(String, nullable=True)
    partnerships = Column(String, nullable=True)

    pitch = relationship("PitchDB", back_populates="traction")