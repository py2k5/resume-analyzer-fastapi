import boto3
import os
from typing import Optional, Dict, Any
from botocore.exceptions import ClientError, NoCredentialsError
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class TextractService:
    def __init__(self):
        """
        Initialize AWS Textract service with proper credential handling
        """
        # Try to get region from environment, fallback to ap-southeast-2
        self.region = os.getenv('AWS_DEFAULT_REGION', 'ap-southeast-2')
        self.textract_client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """
        Initialize Textract client with proper error handling
        """
        try:
            # Try to create client with credentials from environment
            self.textract_client = boto3.client(
                'textract',
                region_name=self.region,
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                aws_session_token=os.getenv('AWS_SESSION_TOKEN')  # Optional for temporary credentials
            )
            
            # Test the connection
            self._test_connection()
            logger.info(f"Textract client initialized successfully in region: {self.region}")
            
        except NoCredentialsError:
            logger.error("AWS credentials not found. Please check your environment variables.")
            raise Exception("AWS credentials not configured. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        except ClientError as e:
            logger.error(f"AWS client error: {e}")
            raise Exception(f"AWS service error: {e}")
        except Exception as e:
            logger.error(f"Failed to initialize Textract client: {e}")
            raise Exception(f"Failed to initialize AWS Textract: {e}")
    
    def _test_connection(self):
        """
        Test the connection to AWS Textract
        """
        try:
            # Make a simple call to test credentials
            self.textract_client.list_document_analysis_jobs(MaxResults=1)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                logger.warning("AWS credentials are valid but may not have Textract permissions")
            else:
                logger.warning(f"AWS connection test failed: {error_code}")
    
    def extract_text_from_document(self, document_bytes: bytes) -> str:
        """
        Extract text from document using AWS Textract
        
        Args:
            document_bytes: Document content as bytes
            
        Returns:
            Extracted text as string
            
        Raises:
            Exception: If text extraction fails
        """
        try:
            # Use detect_document_text for synchronous processing
            response = self.textract_client.detect_document_text(
                Document={'Bytes': document_bytes}
            )
            
            # Extract text from response
            extracted_text = self._parse_textract_response(response)
            
            if not extracted_text.strip():
                raise Exception("No text could be extracted from the document")
            
            logger.info(f"Successfully extracted {len(extracted_text)} characters from document")
            return extracted_text
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            
            if error_code == 'InvalidParameterException':
                raise Exception(f"Invalid document format: {error_message}")
            elif error_code == 'AccessDeniedException':
                raise Exception("Access denied. Check your AWS permissions for Textract")
            elif error_code == 'ThrottlingException':
                raise Exception("Request throttled. Please try again later")
            elif error_code == 'LimitExceededException':
                raise Exception("Document size exceeds Textract limits")
            else:
                raise Exception(f"AWS Textract error: {error_message}")
                
        except Exception as e:
            logger.error(f"Text extraction failed: {e}")
            raise Exception(f"Failed to extract text: {e}")
    
    def _parse_textract_response(self, response: Dict[str, Any]) -> str:
        """
        Parse Textract response to extract text
        
        Args:
            response: Textract API response
            
        Returns:
            Extracted text
        """
        text_blocks = []
        
        # Extract text from blocks
        for block in response.get('Blocks', []):
            if block.get('BlockType') == 'LINE':
                text = block.get('Text', '')
                if text:
                    text_blocks.append(text)
        
        # Join text blocks with newlines
        extracted_text = '\n'.join(text_blocks)
        
        return extracted_text
    
    def get_document_info(self, document_bytes: bytes) -> Dict[str, Any]:
        """
        Get additional information about the document
        
        Args:
            document_bytes: Document content as bytes
            
        Returns:
            Document information dictionary
        """
        try:
            response = self.textract_client.detect_document_text(
                Document={'Bytes': document_bytes}
            )
            
            # Count different types of blocks
            block_counts = {}
            for block in response.get('Blocks', []):
                block_type = block.get('BlockType', 'UNKNOWN')
                block_counts[block_type] = block_counts.get(block_type, 0) + 1
            
            return {
                'total_blocks': len(response.get('Blocks', [])),
                'block_types': block_counts,
                'confidence_scores': self._get_confidence_scores(response),
                'document_metadata': response.get('DocumentMetadata', {})
            }
            
        except Exception as e:
            logger.warning(f"Failed to get document info: {e}")
            return {}
    
    def _get_confidence_scores(self, response: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract confidence scores from Textract response
        
        Args:
            response: Textract API response
            
        Returns:
            Dictionary of confidence scores
        """
        confidence_scores = []
        
        for block in response.get('Blocks', []):
            if 'Confidence' in block:
                confidence_scores.append(block['Confidence'])
        
        if confidence_scores:
            return {
                'average_confidence': sum(confidence_scores) / len(confidence_scores),
                'min_confidence': min(confidence_scores),
                'max_confidence': max(confidence_scores),
                'total_blocks_with_confidence': len(confidence_scores)
            }
        
        return {}
    
    def is_service_available(self) -> bool:
        """
        Check if Textract service is available
        
        Returns:
            True if service is available, False otherwise
        """
        try:
            self.textract_client.list_document_analysis_jobs(MaxResults=1)
            return True
        except Exception:
            return False

# Global instance
textract_service = None

def get_textract_service() -> TextractService:
    """
    Get or create Textract service instance
    
    Returns:
        TextractService instance
    """
    global textract_service
    if textract_service is None:
        textract_service = TextractService()
    return textract_service
