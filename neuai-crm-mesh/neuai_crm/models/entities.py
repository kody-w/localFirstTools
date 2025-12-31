"""
Entity models for CRM data.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Optional
from datetime import datetime

from neuai_crm.models.schemas import Platform, SCHEMA_MAPPINGS


@dataclass
class Contact:
    """Contact entity that can be translated between platforms."""

    id: str
    first_name: str
    last_name: str
    email: str
    phone: str = ""
    company_id: str = ""
    job_title: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @classmethod
    def from_platform(cls, data: Dict, platform: Platform) -> "Contact":
        """Create a Contact from platform-specific data."""
        if platform == Platform.LOCAL:
            return cls(
                id=data.get("id", ""),
                first_name=data.get("firstName", ""),
                last_name=data.get("lastName", ""),
                email=data.get("email", ""),
                phone=data.get("phone", ""),
                company_id=data.get("companyId", ""),
                job_title=data.get("jobTitle", ""),
                created_at=data.get("createdAt", "")
            )
        elif platform == Platform.SALESFORCE:
            return cls(
                id=data.get("Id", ""),
                first_name=data.get("FirstName", ""),
                last_name=data.get("LastName", ""),
                email=data.get("Email", ""),
                phone=data.get("Phone", ""),
                company_id=data.get("AccountId", ""),
                job_title=data.get("Title", ""),
                created_at=data.get("CreatedDate", "")
            )
        else:  # DYNAMICS365
            return cls(
                id=data.get("contactid", ""),
                first_name=data.get("firstname", ""),
                last_name=data.get("lastname", ""),
                email=data.get("emailaddress1", ""),
                phone=data.get("telephone1", ""),
                company_id=data.get("parentcustomerid", ""),
                job_title=data.get("jobtitle", ""),
                created_at=data.get("createdon", "")
            )

    def to_platform(self, platform: Platform) -> Dict:
        """Convert to platform-specific format."""
        if platform == Platform.LOCAL:
            return {
                "id": self.id,
                "firstName": self.first_name,
                "lastName": self.last_name,
                "email": self.email,
                "phone": self.phone,
                "companyId": self.company_id,
                "jobTitle": self.job_title,
                "createdAt": self.created_at
            }
        elif platform == Platform.SALESFORCE:
            return {
                "Id": self.id,
                "FirstName": self.first_name,
                "LastName": self.last_name,
                "Email": self.email,
                "Phone": self.phone,
                "AccountId": self.company_id,
                "Title": self.job_title,
                "CreatedDate": self.created_at
            }
        else:  # DYNAMICS365
            return {
                "contactid": self.id,
                "firstname": self.first_name,
                "lastname": self.last_name,
                "emailaddress1": self.email,
                "telephone1": self.phone,
                "parentcustomerid": self.company_id,
                "jobtitle": self.job_title,
                "createdon": self.created_at
            }

    @property
    def full_name(self) -> str:
        """Get the full name."""
        return f"{self.first_name} {self.last_name}".strip()


@dataclass
class Company:
    """Company/Account entity that can be translated between platforms."""

    id: str
    name: str
    industry: str = ""
    website: str = ""
    phone: str = ""
    address: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @classmethod
    def from_platform(cls, data: Dict, platform: Platform) -> "Company":
        """Create a Company from platform-specific data."""
        if platform == Platform.LOCAL:
            return cls(
                id=data.get("id", ""),
                name=data.get("name", ""),
                industry=data.get("industry", ""),
                website=data.get("website", ""),
                phone=data.get("phone", ""),
                address=data.get("address", ""),
                created_at=data.get("createdAt", "")
            )
        elif platform == Platform.SALESFORCE:
            return cls(
                id=data.get("Id", ""),
                name=data.get("Name", ""),
                industry=data.get("Industry", ""),
                website=data.get("Website", ""),
                phone=data.get("Phone", ""),
                address=data.get("BillingAddress", ""),
                created_at=data.get("CreatedDate", "")
            )
        else:  # DYNAMICS365
            return cls(
                id=data.get("accountid", ""),
                name=data.get("name", ""),
                industry=data.get("industrycode", ""),
                website=data.get("websiteurl", ""),
                phone=data.get("telephone1", ""),
                address=data.get("address1_composite", ""),
                created_at=data.get("createdon", "")
            )

    def to_platform(self, platform: Platform) -> Dict:
        """Convert to platform-specific format."""
        if platform == Platform.LOCAL:
            return {
                "id": self.id,
                "name": self.name,
                "industry": self.industry,
                "website": self.website,
                "phone": self.phone,
                "address": self.address,
                "createdAt": self.created_at
            }
        elif platform == Platform.SALESFORCE:
            return {
                "Id": self.id,
                "Name": self.name,
                "Industry": self.industry,
                "Website": self.website,
                "Phone": self.phone,
                "BillingAddress": self.address,
                "CreatedDate": self.created_at
            }
        else:  # DYNAMICS365
            return {
                "accountid": self.id,
                "name": self.name,
                "industrycode": self.industry,
                "websiteurl": self.website,
                "telephone1": self.phone,
                "address1_composite": self.address,
                "createdon": self.created_at
            }


@dataclass
class Deal:
    """Deal/Opportunity entity that can be translated between platforms."""

    id: str
    name: str
    value: float
    stage: str
    company_id: str = ""
    contact_id: str = ""
    probability: int = 0
    close_date: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @classmethod
    def from_platform(cls, data: Dict, platform: Platform) -> "Deal":
        """Create a Deal from platform-specific data."""
        if platform == Platform.LOCAL:
            return cls(
                id=data.get("id", ""),
                name=data.get("name", ""),
                value=float(data.get("value", 0)),
                stage=data.get("stage", "lead"),
                company_id=data.get("companyId", ""),
                contact_id=data.get("contactId", ""),
                probability=int(data.get("probability", 0)),
                close_date=data.get("closeDate", ""),
                created_at=data.get("createdAt", "")
            )
        elif platform == Platform.SALESFORCE:
            return cls(
                id=data.get("Id", ""),
                name=data.get("Name", ""),
                value=float(data.get("Amount", 0)),
                stage=data.get("StageName", "Prospecting"),
                company_id=data.get("AccountId", ""),
                contact_id=data.get("ContactId", ""),
                probability=int(data.get("Probability", 0)),
                close_date=data.get("CloseDate", ""),
                created_at=data.get("CreatedDate", "")
            )
        else:  # DYNAMICS365
            return cls(
                id=data.get("opportunityid", ""),
                name=data.get("name", ""),
                value=float(data.get("estimatedvalue", 0)),
                stage=data.get("stepname", "1 - Qualify"),
                company_id=data.get("parentaccountid", ""),
                contact_id=data.get("parentcontactid", ""),
                probability=int(data.get("closeprobability", 0)),
                close_date=data.get("estimatedclosedate", ""),
                created_at=data.get("createdon", "")
            )

    def to_platform(self, platform: Platform) -> Dict:
        """Convert to platform-specific format."""
        # Translate stage to target platform
        translated_stage = self._translate_stage(platform)

        if platform == Platform.LOCAL:
            return {
                "id": self.id,
                "name": self.name,
                "value": self.value,
                "stage": translated_stage,
                "companyId": self.company_id,
                "contactId": self.contact_id,
                "probability": self.probability,
                "closeDate": self.close_date,
                "createdAt": self.created_at
            }
        elif platform == Platform.SALESFORCE:
            return {
                "Id": self.id,
                "Name": self.name,
                "Amount": self.value,
                "StageName": translated_stage,
                "AccountId": self.company_id,
                "ContactId": self.contact_id,
                "Probability": self.probability,
                "CloseDate": self.close_date,
                "CreatedDate": self.created_at
            }
        else:  # DYNAMICS365
            return {
                "opportunityid": self.id,
                "name": self.name,
                "estimatedvalue": self.value,
                "stepname": translated_stage,
                "parentaccountid": self.company_id,
                "parentcontactid": self.contact_id,
                "closeprobability": self.probability,
                "estimatedclosedate": self.close_date,
                "createdon": self.created_at
            }

    def _translate_stage(self, target_platform: Platform) -> str:
        """Translate the stage to the target platform format."""
        # Find current stage in all platforms
        for platform_name, stages in SCHEMA_MAPPINGS["stages"].items():
            if self.stage in stages:
                idx = stages.index(self.stage)
                target_stages = SCHEMA_MAPPINGS["stages"][target_platform.value]
                return target_stages[idx] if idx < len(target_stages) else self.stage

        # If not found, return as-is
        return self.stage


@dataclass
class Activity:
    """Activity/Task entity that can be translated between platforms."""

    id: str
    type: str
    subject: str
    description: str = ""
    due_date: str = ""
    status: str = "pending"
    contact_id: str = ""
    deal_id: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @classmethod
    def from_platform(cls, data: Dict, platform: Platform) -> "Activity":
        """Create an Activity from platform-specific data."""
        if platform == Platform.LOCAL:
            return cls(
                id=data.get("id", ""),
                type=data.get("type", "task"),
                subject=data.get("subject", ""),
                description=data.get("description", ""),
                due_date=data.get("dueDate", ""),
                status=data.get("status", "pending"),
                contact_id=data.get("contactId", ""),
                deal_id=data.get("dealId", ""),
                created_at=data.get("createdAt", "")
            )
        elif platform == Platform.SALESFORCE:
            return cls(
                id=data.get("Id", ""),
                type=data.get("TaskSubtype", "Task"),
                subject=data.get("Subject", ""),
                description=data.get("Description", ""),
                due_date=data.get("ActivityDate", ""),
                status=data.get("Status", "Not Started"),
                contact_id=data.get("WhoId", ""),
                deal_id=data.get("WhatId", ""),
                created_at=data.get("CreatedDate", "")
            )
        else:  # DYNAMICS365
            statecode = data.get("statecode", 0)
            status = "pending" if statecode == 0 else "completed" if statecode == 2 else "in_progress"
            return cls(
                id=data.get("activityid", ""),
                type=data.get("activitytypecode", "task"),
                subject=data.get("subject", ""),
                description=data.get("description", ""),
                due_date=data.get("scheduledend", ""),
                status=status,
                contact_id=data.get("regardingobjectid", ""),
                deal_id="",
                created_at=data.get("createdon", "")
            )

    def to_platform(self, platform: Platform) -> Dict:
        """Convert to platform-specific format."""
        if platform == Platform.LOCAL:
            return {
                "id": self.id,
                "type": self.type,
                "subject": self.subject,
                "description": self.description,
                "dueDate": self.due_date,
                "status": self.status,
                "contactId": self.contact_id,
                "dealId": self.deal_id,
                "createdAt": self.created_at
            }
        elif platform == Platform.SALESFORCE:
            sf_status = {
                "pending": "Not Started",
                "in_progress": "In Progress",
                "completed": "Completed",
                "cancelled": "Deferred"
            }.get(self.status, self.status)

            return {
                "Id": self.id,
                "TaskSubtype": self.type,
                "Subject": self.subject,
                "Description": self.description,
                "ActivityDate": self.due_date,
                "Status": sf_status,
                "WhoId": self.contact_id,
                "WhatId": self.deal_id,
                "CreatedDate": self.created_at
            }
        else:  # DYNAMICS365
            statecode = {
                "pending": 0,
                "in_progress": 1,
                "completed": 2,
                "cancelled": 3
            }.get(self.status, 0)

            return {
                "activityid": self.id,
                "activitytypecode": self.type,
                "subject": self.subject,
                "description": self.description,
                "scheduledend": self.due_date,
                "statecode": statecode,
                "regardingobjectid": self.contact_id or self.deal_id,
                "createdon": self.created_at
            }
