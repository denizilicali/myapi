from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any, Optional
import re
import dns.resolver
import socket
from datetime import datetime

router = APIRouter()

class EmailValidationRequest(BaseModel):
    email: EmailStr
    check_deliverability: bool = True
    check_disposable: bool = True
    check_role: bool = True

class EmailValidationResponse(BaseModel):
    email: str
    is_valid: bool
    is_deliverable: bool
    is_disposable: bool
    is_role_account: bool
    domain_exists: bool
    mx_record_exists: bool
    confidence_score: float
    validation_details: Dict[str, Any]
    recommendations: List[str]

class BatchEmailValidationRequest(BaseModel):
    emails: List[EmailStr]
    check_deliverability: bool = True
    check_disposable: bool = True
    check_role: bool = True

# Disposable email domains (partial list)
DISPOSABLE_DOMAINS = {
    '10minutemail.com', 'guerrillamail.com', 'mailinator.com', 'tempmail.org',
    'throwaway.email', 'fakeinbox.com', 'sharklasers.com', 'getairmail.com',
    'yopmail.com', 'mailnesia.com', 'maildrop.cc', 'getnada.com',
    'mailmetrash.com', 'trashmail.com', 'mailnull.com', 'spam4.me',
    'bccto.me', 'chacuo.net', 'dispostable.com', 'mailnesia.com'
}

# Role account patterns
ROLE_ACCOUNTS = {
    'admin', 'administrator', 'info', 'contact', 'support', 'help',
    'sales', 'marketing', 'hr', 'human.resources', 'jobs', 'careers',
    'newsletter', 'noreply', 'no-reply', 'donotreply', 'do-not-reply',
    'webmaster', 'postmaster', 'abuse', 'security', 'billing', 'accounts',
    'service', 'customer.service', 'customerservice', 'feedback'
}

def validate_email_format(email: str) -> Dict[str, Any]:
    """Validate email format and basic structure"""
    # Basic regex pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid_format = bool(re.match(pattern, email))
    
    # Check for common issues
    issues = []
    if not is_valid_format:
        issues.append("invalid_format")
    
    if len(email) > 254:  # RFC 5321 limit
        issues.append("too_long")
    
    if email.count('@') != 1:
        issues.append("multiple_at_symbols")
    
    local_part, domain = email.split('@')
    if len(local_part) > 64:  # RFC 5321 limit
        issues.append("local_part_too_long")
    
    if len(domain) > 253:  # RFC 5321 limit
        issues.append("domain_too_long")
    
    return {
        "is_valid_format": is_valid_format,
        "issues": issues,
        "local_part": local_part,
        "domain": domain
    }

def check_domain_exists(domain: str) -> Dict[str, Any]:
    """Check if domain exists and has MX records"""
    try:
        # Check if domain resolves
        socket.gethostbyname(domain)
        domain_exists = True
    except socket.gaierror:
        domain_exists = False
    
    try:
        # Check for MX records
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_exists = len(mx_records) > 0
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        mx_exists = False
    
    return {
        "domain_exists": domain_exists,
        "mx_record_exists": mx_exists
    }

def check_disposable_email(domain: str) -> bool:
    """Check if email domain is disposable"""
    return domain.lower() in DISPOSABLE_DOMAINS

def check_role_account(local_part: str) -> bool:
    """Check if email is a role account"""
    return local_part.lower() in ROLE_ACCOUNTS

def calculate_confidence_score(validation_results: Dict[str, Any]) -> float:
    """Calculate confidence score based on validation results"""
    score = 0.0
    
    # Format validation (30%)
    if validation_results.get("format_valid", False):
        score += 0.3
    
    # Domain existence (25%)
    if validation_results.get("domain_exists", False):
        score += 0.25
    
    # MX records (25%)
    if validation_results.get("mx_record_exists", False):
        score += 0.25
    
    # Not disposable (10%)
    if not validation_results.get("is_disposable", False):
        score += 0.1
    
    # Not role account (10%)
    if not validation_results.get("is_role_account", False):
        score += 0.1
    
    return min(1.0, score)

def generate_recommendations(validation_results: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on validation results"""
    recommendations = []
    
    if validation_results.get("is_disposable", False):
        recommendations.append("This appears to be a disposable email address. Consider requiring a permanent email.")
    
    if validation_results.get("is_role_account", False):
        recommendations.append("This is a role account. Consider requiring a personal email address.")
    
    if not validation_results.get("domain_exists", False):
        recommendations.append("The domain does not exist. This email is likely invalid.")
    
    if not validation_results.get("mx_record_exists", False):
        recommendations.append("The domain has no mail servers. This email cannot receive messages.")
    
    if validation_results.get("confidence_score", 0) < 0.5:
        recommendations.append("Low confidence score. Manual verification recommended.")
    
    if not recommendations:
        recommendations.append("Email appears valid and deliverable.")
    
    return recommendations

@router.post("/validate", response_model=EmailValidationResponse)
async def validate_email(request: EmailValidationRequest):
    """
    Validate email address for format, deliverability, and quality.
    
    - **email**: Email address to validate
    - **check_deliverability**: Check if email can receive messages
    - **check_disposable**: Check if email is from disposable domain
    - **check_role**: Check if email is a role account
    """
    try:
        email = str(request.email)
        
        # Format validation
        format_validation = validate_email_format(email)
        local_part = format_validation["local_part"]
        domain = format_validation["domain"]
        
        # Domain and MX checks
        domain_check = check_domain_exists(domain)
        
        # Disposable email check
        is_disposable = check_disposable_email(domain) if request.check_disposable else False
        
        # Role account check
        is_role_account = check_role_account(local_part) if request.check_role else False
        
        # Determine deliverability
        is_deliverable = (
            format_validation["is_valid_format"] and
            domain_check["domain_exists"] and
            domain_check["mx_record_exists"] and
            not is_disposable
        )
        
        # Overall validity
        is_valid = format_validation["is_valid_format"] and domain_check["domain_exists"]
        
        # Compile validation results
        validation_results = {
            "format_valid": format_validation["is_valid_format"],
            "domain_exists": domain_check["domain_exists"],
            "mx_record_exists": domain_check["mx_record_exists"],
            "is_disposable": is_disposable,
            "is_role_account": is_role_account,
            "validation_issues": format_validation["issues"]
        }
        
        # Calculate confidence score
        confidence_score = calculate_confidence_score(validation_results)
        
        # Generate recommendations
        recommendations = generate_recommendations(validation_results)
        
        return EmailValidationResponse(
            email=email,
            is_valid=is_valid,
            is_deliverable=is_deliverable,
            is_disposable=is_disposable,
            is_role_account=is_role_account,
            domain_exists=domain_check["domain_exists"],
            mx_record_exists=domain_check["mx_record_exists"],
            confidence_score=confidence_score,
            validation_details=validation_results,
            recommendations=recommendations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email validation failed: {str(e)}")

@router.post("/batch-validate")
async def batch_validate_emails(request: BatchEmailValidationRequest):
    """
    Validate multiple email addresses at once for efficiency.
    """
    try:
        results = []
        for email in request.emails:
            try:
                validation_request = EmailValidationRequest(
                    email=email,
                    check_deliverability=request.check_deliverability,
                    check_disposable=request.check_disposable,
                    check_role=request.check_role
                )
                result = await validate_email(validation_request)
                results.append(result.dict())
            except Exception as e:
                results.append({
                    "email": str(email),
                    "error": str(e),
                    "is_valid": False
                })
        
        return {
            "results": results,
            "total_processed": len(request.emails),
            "valid_count": sum(1 for r in results if r.get("is_valid", False)),
            "deliverable_count": sum(1 for r in results if r.get("is_deliverable", False))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch validation failed: {str(e)}")

@router.get("/domain-info/{domain}")
async def get_domain_info(domain: str):
    """Get detailed information about an email domain"""
    try:
        domain_check = check_domain_exists(domain)
        is_disposable = check_disposable_email(domain)
        
        return {
            "domain": domain,
            "exists": domain_check["domain_exists"],
            "has_mx_records": domain_check["mx_record_exists"],
            "is_disposable": is_disposable,
            "deliverability_score": 1.0 if domain_check["mx_record_exists"] and not is_disposable else 0.0,
            "last_checked": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Domain info failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint for the email validation service"""
    return {"status": "healthy", "service": "email_validation"} 