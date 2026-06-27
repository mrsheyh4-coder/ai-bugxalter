from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, JSON, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    ACCOUNTANT = "accountant"
    DIRECTOR = "director"
    OPERATOR = "operator"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default=UserRole.OPERATOR)
    is_active = Column(Boolean, default=True)
    telegram_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    companies = relationship("UserCompanyAccess", back_populates="user")

class CompanyType(str, enum.Enum):
    MCHJ = "mchj"
    YATT = "yatt"
    OILAVIY = "oilaviy"
    QOSHMA = "qoshma"

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    stir = Column(String, unique=True, index=True, nullable=False) # Tax ID (INN)
    type = Column(String, nullable=False)
    address = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    users = relationship("UserCompanyAccess", back_populates="company")
    reports = relationship("Report", back_populates="company")

class UserCompanyAccess(Base):
    __tablename__ = "user_company_access"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), primary_key=True)
    access_level = Column(String) # For fine-grained control if needed
    
    user = relationship("User", back_populates="companies")
    company = relationship("Company", back_populates="users")

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    type = Column(String, nullable=False) # e.g., "QQS", "Foyda"
    period = Column(String, nullable=False) # e.g., "2024-Q1"
    status = Column(String, default="draft") # draft, signed, submitted, error
    file_path = Column(String)
    metadata_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    company = relationship("Company", back_populates="reports")

class TaxRule(Base):
    __tablename__ = "tax_rules"
    id = Column(Integer, primary_key=True, index=True)
    tax_type = Column(String, nullable=False) # renta, zargarlik, ecommerce, etc.
    taxpayer_type = Column(String) # MCHJ, YATT, Self-Employed
    rate = Column(Float) # percentage rate
    fixed_amount = Column(Float) # absolute value (e.g., 2000 per gram)
    unit = Column(String) # gramm, litr, etc.
    effective_from = Column(DateTime)
    effective_to = Column(DateTime)
    region = Column(String) # Toshkent 1-zona, etc.
    formula = Column(String) # dynamic formula string
    legal_reference = Column(String)
    automation_level = Column(Integer, default=1)
    meta_data = Column(JSON) # For extra params like sugar content
