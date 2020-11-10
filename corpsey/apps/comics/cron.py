from corpsey.apps.comics.models import *
from django.template import RequestContext
from django.core.mail import mail_admins,mail_managers
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import cronjobs

@cronjobs.register
def test_cron():
    contributions_expiring_tomorrow = Contribution.objects.filter(pending=True, deadline__lte=timezone.now()+timedelta(days=1))
    contributions_expired = Contribution.objects.filter(pending=True, deadline__lte=timezone.now())
    message = 'Contributions expiring tomorrow: '
    for c in contributions_expiring_tomorrow:
        message = message + " %s " % c
    message = message + ' ... Contributions expired: '
    for c in contributions_expired:
        message = message + " %s " % c
    print message

@cronjobs.register
def check_contributions():
    print 'Running contribution cron... '
    contributions_expiring_tomorrow = Contribution.objects.filter(pending=True, has_panels=False, deadline__lte=timezone.now()+timedelta(days=1))
    print 'Expiring tomorrow: '
    for c in contributions_expiring_tomorrow:
        print c
    contributions_expired = Contribution.objects.filter(pending=True, has_panels=False, deadline__lte=timezone.now())
    print 'Expired: '
    for c in contributions_expired:
        print c
    for contribution in contributions_expiring_tomorrow:
        message = send_html_email({
            'template' : 'contribution_expiring_tomorrow',
            'email_to' : contribution.email,
            'subject'  : 'Your Infinite Corpse reservation expires tomorrow',
            'context'  : { 'contribution': contribution, 'title': 'Your Infinite Corpse reservation expires tomorrow' },
            })
        print message

    for contribution in contributions_expired:
        contribution.pending = False
        contribution.save()
        message = send_html_email({
            'template' : 'contribution_expired',
            'email_to' : contribution.email,
            'subject'  : 'Your Infinite Corpse reservation has expired',
            'context'  : { 'contribution': contribution, 'title': 'Your Infinite Corpse reservation has expired' },
            })
        print message

def send_html_email(email_data):
    plaintext = get_template('emails/%s.txt' % email_data['template'])
    htmly     = get_template('emails/%s.html' % email_data['template'])
    subject = email_data['subject']
    from_email = 'corpsey@trubble.club'
    text_content = plaintext.render(email_data['context'])
    html_content = htmly.render(email_data['context'])
    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email_data['email_to']])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        message = 'Email sent to %s ok!' % email_data['email_to']
    except:
        message = 'There was an error sending a "%s" email to %s.' % (email_data['template'], email_data['email_to'])
    return message
