from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import os
import logging

logger = logging.getLogger(__name__)

def send_interpreter_welcome_email(user, interpreter):
    """
    Send a welcome email to the newly registered interpreter with attached documents.
    
    Parameters:
    user (User): The User object of the interpreter
    interpreter (Interpreter): The Interpreter profile object
    
    Returns:
    bool: True if email was sent successfully, False otherwise
    """
    try:
        logger.info(f"Preparing welcome email for interpreter: {user.email}")
        
        # Email subject
        subject = 'Welcome to CGSD Logistics - Interpreter Offer Letter'
        
        # Email context for template
        context = {
            'user': user,
            'interpreter': interpreter,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        
        # Render email HTML content from template
        email_html = render_to_string('notifmail/interpreter_mail.html', context)
        
        # Create email message
        email = EmailMessage(
            subject=subject,
            body=email_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.content_subtype = 'html'  # Set content type to HTML
        
        # Attach documents
        policy_path = os.path.join(settings.BASE_DIR, 'contract', 'CGSD_Logistics_Policy_2025.pdf')
        offer_letter_path = os.path.join(settings.BASE_DIR, 'contract', 'Offer_Letter_CGSD_logistics_2025_1.pdf')
        
        # Check if files exist before attaching
        if os.path.exists(policy_path):
            email.attach_file(policy_path)
            logger.debug(f"Attached policy document: {policy_path}")
        else:
            logger.error(f"Policy document not found at: {policy_path}")
        
        if os.path.exists(offer_letter_path):
            email.attach_file(offer_letter_path)
            logger.debug(f"Attached offer letter: {offer_letter_path}")
        else:
            logger.error(f"Offer letter not found at: {offer_letter_path}")
        
        # Send email
        email.send(fail_silently=False)
        logger.info(f"Welcome email sent successfully to: {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send welcome email to {user.email}: {str(e)}", exc_info=True)
        return False