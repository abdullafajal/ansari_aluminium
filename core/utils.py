from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.mixins import UserPassesTestMixin
from weasyprint import HTML, CSS

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and getattr(self.request.user, 'is_admin', False)

def render_to_pdf(template_src, context_dict={}, request=None, filename="document.pdf"):
    """
    Render a Django template to PDF using WeasyPrint.
    """
    template = get_template(template_src)
    html_string = template.render(context_dict)
    
    # Base URL is required for loading static files (css, images)
    # If request is provided, use it to build absolute URI
    base_url = request.build_absolute_uri('/') if request else None

    # Create HTML object
    html = HTML(string=html_string, base_url=base_url)
    
    # Generate PDF
    pdf_file = html.write_pdf()
    
    # Create HTTP response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

def pdf_preview(template_src, context_dict={}, request=None):
    """
    Render a Django template to PDF and return as inline preview (browser viewer).
    """
    template = get_template(template_src)
    html_string = template.render(context_dict)
    base_url = request.build_absolute_uri('/') if request else None

    html = HTML(string=html_string, base_url=base_url)
    pdf_file = html.write_pdf()
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="preview.pdf"'
    
    return response


import threading
from django.core.mail import EmailMessage

class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html_message):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html_message = html_message
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.body, self.from_email, self.recipient_list)
        if self.html_message:
            msg.content_subtype = "html"
            msg.body = self.html_message
        try:
            msg.send(fail_silently=self.fail_silently)
        except Exception as e:
            print(f"Error sending background email: {e}")

def send_background_email(subject, message, from_email, recipient_list, fail_silently=False, html_message=None):
    """
    Send email in a background thread.
    Use this instead of send_mail to avoid blocking the request.
    """
    EmailThread(subject, message, from_email, recipient_list, fail_silently, html_message).start()
