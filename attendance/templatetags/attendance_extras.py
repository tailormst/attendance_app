from django import template
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """Custom filter to lookup dictionary values"""
    return dictionary.get(key, '')

@register.filter
def indian_currency(value):
    """Format currency in Indian format"""
    if value is None:
        return "₹0"
    try:
        # Convert to float and format with commas
        amount = float(value)
        return f"₹{amount:,.0f}"
    except (ValueError, TypeError):
        return "₹0"

@register.filter
def indian_date(date_obj):
    """Format date in Indian format (DD/MM/YYYY)"""
    if date_obj is None:
        return ""
    try:
        if hasattr(date_obj, 'strftime'):
            return date_obj.strftime("%d/%m/%Y")
        return str(date_obj)
    except:
        return str(date_obj)

@register.filter
def indian_datetime(datetime_obj):
    """Format datetime in Indian format"""
    if datetime_obj is None:
        return ""
    try:
        if hasattr(datetime_obj, 'strftime'):
            return datetime_obj.strftime("%d/%m/%Y %I:%M %p")
        return str(datetime_obj)
    except:
        return str(datetime_obj)
