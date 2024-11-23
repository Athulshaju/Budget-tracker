from django.core.mail import send_mail


def send_alert(user, category, exceeded=False, total=False):
    subject = f"{'Exceeded' if exceeded else 'Nearing'} Budget Alert"
    body = f"You have {'exceeded' if exceeded else 'neared'} your {'total' if total else category.name} budget"
    print(f"Preparing to send email to {user.email} with subject: {subject}")  # De
    send_mail(subject, body, 'athulshaju42069@gmail.com', [user.email])