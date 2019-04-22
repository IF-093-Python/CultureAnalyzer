from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

__all__ = ['send_email_to_members', 'send_email_to_mentor', ]


def send_email_to_members(domain, members, schedule):
    """
    :param domain: domain this site
    :param members: a list of members of a particular group
    :param schedule: the schedule for the quiz that was assigned to this
    group
    :return: sends emails to all members of the group
    """
    email_from = settings.EMAIL_HOST_USER
    for member in members:
        msg_text = render_to_string(
            'groups/send_email_to_member.txt',
            {'member': member, 'schedule': schedule})
        msg_html = render_to_string(
            'groups/send_email_to_member.html',
            {'member': member, 'schedule': schedule, 'domain': domain,
             'email_from': email_from})
        msg = EmailMultiAlternatives(subject=schedule.quiz,
                                     from_email=email_from,
                                     to=[member.email, ],
                                     body=msg_text)
        msg.attach_alternative(msg_html, "text/html")
        msg.send()


def send_email_to_mentor(domain, mentors, group):
    """
    :param domain: domain this site
    :param mentors: a list of mentors of a particular group
    :param group: a group for which the appointed mentor
    :return: sends emails to all members of the group
    """
    email_from = settings.EMAIL_HOST_USER
    for mentor in mentors:
        msg_text = render_to_string(
            'groups/send_email_to_mentor.txt',
            {'mentor': mentor, 'group': group})
        msg_html = render_to_string(
            'groups/send_email_to_mentor.html',
            {'mentor': mentor, 'group': group, 'domain': domain,
             'email_from': email_from})
        msg = EmailMultiAlternatives(subject=group.name,
                                     from_email=email_from,
                                     to=[mentor.email, ],
                                     body=msg_text)
        msg.attach_alternative(msg_html, "text/html")
        msg.send()
