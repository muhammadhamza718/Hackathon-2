"""Input sanitization and security utilities for the Todo Chatbot"""
import re
from typing import Union, List, Dict, Any
from html import escape
import bleach
from urllib.parse import urlparse


class InputSanitizer:
    """Provides input sanitization and security measures for user inputs"""

    @staticmethod
    def sanitize_text(text: str, max_length: int = 500) -> str:
        """Sanitize text input by removing dangerous characters and limiting length"""
        if not isinstance(text, str):
            raise ValueError("Input must be a string")

        # Limit length
        text = text[:max_length]

        # Remove null bytes and other dangerous characters
        text = text.replace('\x00', '')  # Remove null bytes
        text = text.replace('\x01', '')  # Remove start of heading
        text = text.replace('\x02', '')  # Remove start of text

        # Basic HTML sanitization using bleach
        try:
            text = bleach.clean(text, strip=True, tags=[], attributes={})
        except:
            # If bleach fails, use basic HTML escaping
            text = escape(text)

        # Remove potential SQL injection patterns (basic check)
        sql_patterns = [
            r"(?i)(union\s+select)",
            r"(?i)(drop\s+table)",
            r"(?i)(delete\s+from)",
            r"(?i)(insert\s+into)",
            r"(?i)(update\s+\w+\s+set)",
            r"(?i)(exec\s*\()",
            r"(?i)(execute\s*\()",
            r"(?i)(sp_\w+)",
            r"(?i)(xp_\w+)"
        ]

        for pattern in sql_patterns:
            text = re.sub(pattern, "", text)

        # Remove potential command injection patterns
        cmd_patterns = [
            r"(?i)(\|\||\|\s)",
            r"(?i)(;\s*\w+)",
            r"(?i)(`.*`)",
            r"(?i)(\$\(.*)",
            r"(?i)(\$\{.*\})",
        ]

        for pattern in cmd_patterns:
            text = re.sub(pattern, "", text)

        return text.strip()

    @staticmethod
    def sanitize_todo_content(content: str) -> str:
        """Specific sanitization for todo content"""
        # Remove dangerous characters and limit length
        sanitized = InputSanitizer.sanitize_text(content, max_length=500)

        # Additional checks specific to todo content
        # Remove potential script tags
        sanitized = re.sub(r'(?i)<script[^>]*>.*?</script>', '', sanitized)
        sanitized = re.sub(r'(?i)<iframe[^>]*>.*?</iframe>', '', sanitized)
        sanitized = re.sub(r'(?i)<object[^>]*>.*?</object>', '', sanitized)
        sanitized = re.sub(r'(?i)<embed[^>]*>.*?</embed>', '', sanitized)

        # Remove javascript: and data: URIs
        sanitized = re.sub(r'(?i)javascript:', '', sanitized)
        sanitized = re.sub(r'(?i)data:', '', sanitized)
        sanitized = re.sub(r'(?i)vbscript:', '', sanitized)

        return sanitized.strip()

    @staticmethod
    def sanitize_json_input(data: Union[Dict, List]) -> Union[Dict, List]:
        """Sanitize JSON input recursively"""
        if isinstance(data, dict):
            sanitized = {}
            for key, value in data.items():
                # Sanitize the key
                safe_key = InputSanitizer.sanitize_text(str(key), max_length=100)
                # Sanitize the value
                if isinstance(value, (dict, list)):
                    sanitized[safe_key] = InputSanitizer.sanitize_json_input(value)
                elif isinstance(value, str):
                    sanitized[safe_key] = InputSanitizer.sanitize_text(value)
                else:
                    sanitized[safe_key] = value
            return sanitized
        elif isinstance(data, list):
            return [InputSanitizer.sanitize_json_input(item) if isinstance(item, (dict, list)) else InputSanitizer.sanitize_text(item) if isinstance(item, str) else item for item in data]
        else:
            return data

    @staticmethod
    def validate_todo_id(todo_id: Any) -> int:
        """Validate and sanitize todo ID"""
        try:
            # Convert to int and validate
            id_int = int(todo_id)
            if id_int <= 0:
                raise ValueError("Todo ID must be a positive integer")
            return id_int
        except (ValueError, TypeError):
            raise ValueError("Invalid todo ID format")

    @staticmethod
    def is_valid_date_format(date_str: str) -> bool:
        """Validate date format (ISO format)"""
        if not date_str:
            return True  # Allow None/empty dates

        # Check basic ISO format with regex
        iso_pattern = r'^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})?)?$'
        return bool(re.match(iso_pattern, date_str))

    @staticmethod
    def sanitize_user_message(message: str) -> str:
        """Sanitize user chat messages"""
        if not message or not isinstance(message, str):
            return ""

        # Basic sanitization
        sanitized = InputSanitizer.sanitize_text(message, max_length=2000)

        # Remove potential harmful patterns specific to chat
        # Prevent potential server-side request forgery by removing certain patterns
        sanitized = re.sub(r'(?i)(http[s]?://localhost[:\d]*)', '', sanitized)
        sanitized = re.sub(r'(?i)(http[s]?://127\.0\.0\.1[:\d]*)', '', sanitized)
        sanitized = re.sub(r'(?i)(http[s]?://0\.0\.0\.0[:\d]*)', '', sanitized)

        # Remove potential path traversal
        sanitized = sanitized.replace('../', '').replace('..\\', '').replace('/..', '').replace('\\..', '')

        return sanitized.strip()

    @staticmethod
    def escape_special_characters(text: str) -> str:
        """Escape special characters that might be used in injection attacks"""
        if not isinstance(text, str):
            return str(text) if text is not None else ""

        # Escape special regex characters
        special_chars = ['\\', '.', '^', '$', '*', '+', '?', '{', '}', '[', ']', '|', '(', ')']
        for char in special_chars:
            text = text.replace(char, '\\' + char)

        return text

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False