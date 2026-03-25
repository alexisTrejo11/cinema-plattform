from enum import Enum


class EmploymentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ON_LEAVE = "ON_LEAVE"
    SUSPENDED = "SUSPENDED"
    TERMINATED = "TERMINATED"


class Department(str, Enum):
    OPERATIONS = "OPERATIONS"
    PROJECTION = "PROJECTION"
    CONCESSIONS = "CONCESSIONS"
    TICKETING = "TICKETING"
    SECURITY = "SECURITY"
    CLEANING = "CLEANING"
    MANAGEMENT = "MANAGEMENT"
    FINANCE = "FINANCE"
    HR = "HR"
    IT = "IT"


class EmployeeRole(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    SUPERVISOR = "SUPERVISOR"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"


class ContractType(str, Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    TEMPORARY = "TEMPORARY"
    INTERNSHIP = "INTERNSHIP"
