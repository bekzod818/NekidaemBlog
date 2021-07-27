from django.conf import settings
from django.core.mail import send_mail
from django_rq import job


@job
def email_notification_subscriber(email, blog_title, post_url):
    subject = 'New Post from %s' % blog_title
    message = f'''
        Blog from <{blog_title}> published a new post. 
        The post is available via direct link - {post_url} .
    '''
    email_from = settings.EMAIL_HOST_USER
    email_to = [email]
    send_mail(subject, message, email_from, email_to, fail_silently=False)