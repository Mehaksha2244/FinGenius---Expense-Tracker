"""
OCR Receipt Processing Module
Handles receipt image processing and text extraction using pytesseract or easyocr
"""

import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
from typing import Dict, List, Optional, Tuple
import logging

# Try to import easyocr
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReceiptProcessor:
    def __init__(self):
        """Initialize the receipt processor"""
        # Configure tesseract path (adjust for your system)
        # For Windows, you might need to set the path to tesseract.exe
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # For Linux/Mac, tesseract should be in PATH
        
        # Initialize easyocr reader if available
        self.easyocr_reader = None
        if EASYOCR_AVAILABLE:
            try:
                self.easyocr_reader = easyocr.Reader(['en'])
            except Exception as e:
                logger.warning(f"Could not initialize easyocr: {e}")
                self.easyocr_reader = None

    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess the receipt image for better OCR accuracy
        
        Args:
            image_path: Path to the receipt image
            
        Returns:
            Preprocessed image as numpy array
        """
        try:
            # Read the image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image from {image_path}")
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Morphological operations to clean up the image
            kernel = np.ones((1, 1), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            return cleaned
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            raise
    
    def extract_text(self, image_path: str) -> str:
        """
        Extract text from receipt image using OCR
        
        Args:
            image_path: Path to the receipt image
            
        Returns:
            Extracted text as string
        """
        try:
            # Try easyocr first if available
            if self.easyocr_reader:
                try:
                    results = self.easyocr_reader.readtext(image_path)
                    text = "\n".join([result[1] for result in results])
                    logger.info(f"Extracted text using easyocr: {len(text)} characters")
                    return text.strip()
                except Exception as e:
                    logger.warning(f"EasyOCR failed, falling back to pytesseract: {e}")
            
            # Preprocess the image
            processed_image = self.preprocess_image(image_path)
            
            # Try multiple OCR configurations for better accuracy
            configs = [
                r'--oem 3 --psm 6',  # Default
                r'--oem 1 --psm 6',  # LSTM only
                r'--oem 3 --psm 4',  # Assume a single column of text of variable sizes
                r'--oem 3 --psm 3',  # Fully automatic page segmentation, but no OSD
            ]
            
            best_text = ""
            best_length = 0
            
            for config in configs:
                try:
                    text = pytesseract.image_to_string(processed_image, config=config)
                    if len(text.strip()) > best_length:
                        best_text = text.strip()
                        best_length = len(text.strip())
                except Exception as e:
                    logger.warning(f"OCR config failed: {config} - {e}")
                    continue
            
            return best_text
            
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            raise
    
    def extract_amount(self, text: str) -> Optional[float]:
        """
        Extract monetary amount from OCR text
        
        Args:
            text: OCR extracted text
            
        Returns:
            Extracted amount as float, or None if not found
        """
        try:
            # Split text into lines for better pattern matching
            lines = text.split('\n')
            
            # Common currency symbols and patterns
            currency_patterns = [
                r'[Tt][Oo][Tt][Aa][Ll][:\s]*[\$€£¥₹]?\s*(\d+[,.]?\d*)',  # Total amount (case insensitive)
                r'[Aa][Mm][Oo][Uu][Nn][Tt][:\s]*[\$€£¥₹]?\s*(\d+[,.]?\d*)',  # Amount field (case insensitive)
                r'[\$€£¥₹]\s*(\d+[,.]?\d*)',  # Currency symbol followed by amount
                r'(\d+[,.]\d{2})\s*[\$€£¥₹]',  # Amount followed by currency symbol
                r'(\d+\.\d{2})',  # Standard decimal format
                r'(\d+,\d{2})',   # Comma decimal format
                r'\b(\d{1,3}[,.]\d{2,3}[,.]\d{2,3}[,.]\d{2})\b',  # Large amounts with commas/spaces
                r'\b(\d+\.\d{2})\b',  # Standalone amounts with decimal
            ]
            
            amounts = []
            
            # Check each line separately for better accuracy
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                for pattern in currency_patterns:
                    matches = re.findall(pattern, line, re.IGNORECASE)
                    for match in matches:
                        try:
                            # Clean the match
                            clean_amount = match.replace(',', '').replace(' ', '')
                            # Handle European decimal format
                            if ',' in clean_amount and '.' not in clean_amount:
                                clean_amount = clean_amount.replace(',', '.')
                            amount = float(clean_amount)
                            
                            # Reasonable amount range (0.01 to 999999.99)
                            if 0.01 <= amount <= 999999.99:
                                amounts.append(amount)
                        except ValueError:
                            continue
            
            if amounts:
                # Sort by frequency and then by value
                from collections import Counter
                amount_counts = Counter(amounts)
                most_common = amount_counts.most_common()
                
                # If we have a clear winner (appears more than once), use it
                if most_common and most_common[0][1] > 1:
                    return most_common[0][0]
                
                # Otherwise, look for amounts near "TOTAL" or "AMOUNT" keywords
                total_line_indices = []
                for i, line in enumerate(lines):
                    if re.search(r'[Tt][Oo][Tt][Aa][Ll]|[Aa][Mm][Oo][Uu][Nn][Tt]', line):
                        total_line_indices.append(i)
                
                if total_line_indices and amounts:
                    # Prefer amounts found on or near total lines
                    for idx in total_line_indices:
                        # Check the total line and surrounding lines
                        for i in range(max(0, idx-2), min(len(lines), idx+3)):
                            line = lines[i]
                            for amount in amounts:
                                if str(amount) in line or str(int(amount)) in line:
                                    return amount
                
                # Return the largest reasonable amount as fallback
                return max(amounts)
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting amount: {e}")
            return None
    
    def extract_merchant(self, text: str) -> Optional[str]:
        """
        Extract merchant name from OCR text
        
        Args:
            text: OCR extracted text
            
        Returns:
            Merchant name or None if not found
        """
        try:
            lines = text.split('\n')
            
            # Common merchant indicators
            merchant_indicators = [
                'store', 'shop', 'mart', 'center', 'plaza', 'mall', 'outlet',
                'supermarket', 'grocery', 'restaurant', 'cafe', 'coffee',
                'corp', 'inc', 'llc', 'ltd', 'company', 'enterprise'
            ]
            
            # Look for common merchant patterns
            merchant_patterns = [
                r'^[A-Z][A-Z\s&]+$',  # All caps with spaces and &
                r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$',  # Title case words
                r'^[A-Z][A-Za-z\s&.,-]+(?:Inc|LLC|Ltd|Corp)\.?$',  # Company names
            ]
            
            # First, look for lines that contain merchant indicators
            for line in lines[:15]:  # Check first 15 lines
                line = line.strip()
                if len(line) > 3 and len(line) < 60:  # Reasonable length
                    line_lower = line.lower()
                    # Check if line contains merchant indicators
                    if any(indicator in line_lower for indicator in merchant_indicators):
                        # Clean the line - remove extra spaces and special characters at ends
                        clean_line = re.sub(r'^[^A-Za-z0-9]+|[^A-Za-z0-9]+$', '', line)
                        if len(clean_line) > 2:
                            return clean_line
                    
                    # Check pattern matches
                    for pattern in merchant_patterns:
                        if re.match(pattern, line):
                            return line
            
            # If no pattern matches, look for the most prominent line
            # (longest line without too many numbers)
            best_candidate = None
            best_score = 0
            
            for line in lines[:10]:
                line = line.strip()
                if len(line) > 5 and len(line) < 60:  # Reasonable length
                    # Score based on length and letter-to-digit ratio
                    letter_count = len(re.findall(r'[A-Za-z]', line))
                    digit_count = len(re.findall(r'\d', line))
                    
                    # Prefer lines with more letters than digits
                    if letter_count > digit_count:
                        score = len(line) * (letter_count / max(digit_count, 1))
                        if score > best_score:
                            best_score = score
                            best_candidate = line
            
            if best_candidate:
                return best_candidate
            
            # Last resort: return the first substantial line without numbers
            for line in lines[:8]:
                line = line.strip()
                if len(line) > 5 and len(line) < 50 and not re.search(r'\d', line):
                    return line
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting merchant: {e}")
            return None
    
    def extract_date(self, text: str) -> Optional[str]:
        """
        Extract date from OCR text
        
        Args:
            text: OCR extracted text
            
        Returns:
            Date in YYYY-MM-DD format or None if not found
        """
        try:
            # Split text into lines for better processing
            lines = text.split('\n')
            
            # Common date patterns with more variations
            date_patterns = [
                r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',  # MM/DD/YYYY or DD/MM/YYYY
                r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',  # YYYY/MM/DD
                r'(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*,?\s*(\d{4})',  # DD Mon YYYY
                r'(\d{1,2})[/-](\d{1,2})[/-](\d{2})',  # MM/DD/YY or DD/MM/YY
                r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2})[a-z]*,?\s*(\d{4})',  # Mon DD YYYY
                r'(\d{8})',  # YYYYMMDD
            ]
            
            month_names = {
                'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
            }
            
            # Check each line separately for better accuracy
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                for pattern in date_patterns:
                    matches = re.findall(pattern, line, re.IGNORECASE)
                    for match in matches:
                        try:
                            if len(match) == 3:
                                if pattern == date_patterns[2] or pattern == date_patterns[4]:  # Text month formats
                                    if pattern == date_patterns[2]:  # DD Mon YYYY
                                        day, month, year = match
                                    else:  # Mon DD YYYY
                                        month, day, year = match
                                    month_num = month_names.get(month.lower()[:3])
                                    if month_num:
                                        # Validate year
                                        year = int(year)
                                        if year < 100:
                                            year += 2000 if year < 50 else 1900
                                        return f"{year}-{month_num}-{day.zfill(2)}"
                                else:  # Numeric formats
                                    if len(match[2]) == 4 or len(match[0]) == 4:  # YYYY format
                                        if len(match[0]) == 4:
                                            year, month, day = match
                                        else:
                                            year, month, day = match[2], match[1], match[0]
                                    else:  # Assume MM/DD/YY or DD/MM/YY
                                        month, day, year = match
                                        # Handle 2-digit years
                                        year = int(year)
                                        year += 2000 if year < 50 else 1900
                                    
                                    # Validate date components
                                    year, month, day = int(year), int(month), int(day)
                                    if 1 <= month <= 12 and 1 <= day <= 31:
                                        return f"{year}-{month:02d}-{day:02d}"
                            elif len(match) == 1 and pattern == date_patterns[5]:  # YYYYMMDD
                                date_str = match[0]
                                if len(date_str) == 8:
                                    year, month, day = int(date_str[:4]), int(date_str[4:6]), int(date_str[6:8])
                                    if 1 <= month <= 12 and 1 <= day <= 31:
                                        return f"{year}-{month:02d}-{day:02d}"
                        except (ValueError, IndexError):
                            continue
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting date: {e}")
            return None
    
    def categorize_expense(self, text: str, merchant: str = None) -> str:
        """
        Categorize expense based on text content and merchant
        
        Args:
            text: OCR extracted text
            merchant: Merchant name if available
            
        Returns:
            Expense category
        """
        try:
            text_lower = text.lower()
            merchant_lower = (merchant or "").lower()
            
            # Enhanced category keywords with more specific terms
            categories = {
                'Food & Dining': [
                    'restaurant', 'cafe', 'coffee', 'food', 'dining', 'pizza', 'burger', 'subway', 
                    'mcdonalds', 'kfc', 'dominos', 'taco bell', 'starbucks', 'wendy', 'burger king',
                    'chipotle', 'panera', 'dunkin', 'mexico', 'italian', 'chinese', 'indian',
                    'sushi', 'steak', 'grill', 'pub', 'bar', 'wine', 'beer'
                ],
                'Transportation': [
                    'uber', 'lyft', 'taxi', 'gas', 'fuel', 'parking', 'metro', 'bus', 'train', 
                    'flight', 'airline', 'car', 'vehicle', 'auto', 'petrol', 'diesel', 'toll',
                    'rental', 'uber eats', 'doordash', 'grubhub'
                ],
                'Shopping': [
                    'store', 'shop', 'mall', 'amazon', 'walmart', 'target', 'clothing', 'fashion', 
                    'electronics', 'best buy', 'costco', 'ikea', 'home depot', 'lowes', 'macys',
                    'nike', 'adidas', 'zara', 'uniqlo', 'h&m', 'gap', 'books', 'toys', 'gift'
                ],
                'Entertainment': [
                    'movie', 'cinema', 'theater', 'netflix', 'spotify', 'game', 'entertainment', 
                    'concert', 'ticket', 'disney', 'hulu', 'youtube', 'prime video', 'hbo',
                    'playstation', 'xbox', 'nintendo', 'steam', 'apple music', 'tidal'
                ],
                'Healthcare': [
                    'pharmacy', 'drug', 'medical', 'doctor', 'hospital', 'clinic', 'cvs', 'walgreens',
                    'cvs pharmacy', 'rite aid', 'dentist', 'optometrist', 'therapy', 'prescription',
                    'vitamin', 'supplement', 'insurance'
                ],
                'Bills & Utilities': [
                    'electric', 'water', 'internet', 'phone', 'cable', 'utility', 'bill', 'payment',
                    'verizon', 'at&t', 'comcast', 'xfinity', 'spectrum', 'duke energy', 'pg&e',
                    'rent', 'mortgage', 'subscription', 'membership', 'fee'
                ],
                'Education': [
                    'school', 'university', 'college', 'book', 'tuition', 'education', 'course',
                    'student', 'loan', 'textbook', 'software', 'udemy', 'coursera', 'skillshare',
                    'khan academy', 'harvard', 'mit', 'stanford'
                ],
                'Groceries': [
                    'grocery', 'market', 'supermarket', 'whole foods', 'trader joe', 'aldi', 'kroger',
                    'safeway', 'publix', 'winn-dixie', 'food lion', 'fresh market', 'produce', 'vegetable'
                ],
                'Others': []
            }
            
            # Check merchant first with fuzzy matching
            if merchant_lower:
                for category, keywords in categories.items():
                    # Direct match
                    if any(keyword in merchant_lower for keyword in keywords):
                        return category
                    
                    # Partial match with higher threshold
                    for keyword in keywords:
                        if len(keyword) > 4 and keyword in merchant_lower:
                            return category
            
            # Check text content with scoring
            category_scores = {}
            lines = text_lower.split('\n')
            
            for category, keywords in categories.items():
                score = 0
                # Check each line for keywords
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                        
                    # Weight keywords in lines with "total" or "amount" higher
                    weight = 2 if any(word in line for word in ['total', 'amount', 'subtotal']) else 1
                    
                    for keyword in keywords:
                        if keyword in line:
                            score += weight
                        elif len(keyword) > 4 and keyword in line:
                            score += weight * 0.5  # Partial match
                
                if score > 0:
                    category_scores[category] = score
            
            # Return category with highest score
            if category_scores:
                return max(category_scores, key=category_scores.get)
            
            return 'Others'
            
        except Exception as e:
            logger.error(f"Error categorizing expense: {e}")
            return 'Others'
    
    def process_receipt(self, image_path: str) -> Dict:
        """
        Process a receipt image and extract structured data
        
        Args:
            image_path: Path to the receipt image
            
        Returns:
            Dictionary containing extracted data
        """
        try:
            logger.info(f"Processing receipt: {image_path}")
            
            # Extract text
            text = self.extract_text(image_path)
            logger.info(f"Extracted text length: {len(text)}")
            
            # Extract structured data
            amount = self.extract_amount(text)
            merchant = self.extract_merchant(text)
            date = self.extract_date(text)
            category = self.categorize_expense(text, merchant)
            
            result = {
                'success': True,
                'raw_text': text,
                'amount': amount,
                'merchant': merchant,
                'date': date,
                'category': category,
                'confidence': self.calculate_confidence(text, amount, merchant, date)
            }
            
            logger.info(f"Processing result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing receipt: {e}")
            return {
                'success': False,
                'error': str(e),
                'raw_text': '',
                'amount': None,
                'merchant': None,
                'date': None,
                'category': 'Others',
                'confidence': 0
            }
    
    def calculate_confidence(self, text: str, amount: float, merchant: str, date: str) -> float:
        """
        Calculate confidence score for the extracted data
        
        Args:
            text: Raw OCR text
            amount: Extracted amount
            merchant: Extracted merchant
            date: Extracted date
            
        Returns:
            Confidence score between 0 and 1
        """
        try:
            score = 0.0
            
            # Text quality (length and character diversity)
            if len(text) > 50:
                score += 0.15
            if len(set(text)) > 20:  # Character diversity
                score += 0.1
            
            # Amount extraction
            if amount is not None:
                score += 0.3
                # Higher confidence for reasonable amount range
                if 1.00 <= amount <= 10000:  # More realistic range
                    score += 0.15
                elif 0.01 <= amount <= 100000:  # Still acceptable
                    score += 0.1
            
            # Merchant extraction
            if merchant is not None and len(merchant) > 2:
                score += 0.2
                # Higher confidence for longer, more descriptive merchant names
                if len(merchant) > 5:
                    score += 0.1
            
            # Date extraction
            if date is not None:
                score += 0.15
                # Validate date format
                try:
                    from datetime import datetime
                    datetime.strptime(date, '%Y-%m-%d')
                    score += 0.1  # Bonus for valid date format
                except:
                    pass
            
            # Bonus for having all key pieces of information
            key_fields = [amount, merchant, date]
            filled_fields = sum(1 for field in key_fields if field is not None)
            if filled_fields >= 2:
                score += 0.1 * filled_fields
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.0

# Example usage and testing
if __name__ == "__main__":
    processor = ReceiptProcessor()
    
    # Test with a sample image
    test_image = "sample_receipt.jpg"
    if os.path.exists(test_image):
        result = processor.process_receipt(test_image)
        print("Processing Result:")
        print(f"Success: {result['success']}")
        print(f"Amount: {result['amount']}")
        print(f"Merchant: {result['merchant']}")
        print(f"Date: {result['date']}")
        print(f"Category: {result['category']}")
        print(f"Confidence: {result['confidence']:.2f}")
    else:
        print("Test image not found. Please provide a sample receipt image.")
