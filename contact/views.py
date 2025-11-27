from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

@login_required
def contact(request):
    user_email = request.user.email or settings.DEFAULT_FROM_EMAIL

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            body = (
                f"送信者: {request.user.username}\n"
                f"メール: {user_email}\n\n"
                f"件名: {subject}\n"
                f"内容:\n{message}"
            )
            try:
                send_mail(
                    subject=f"[お問い合わせ] {subject}",
                    message=body,
                    from_email=user_email,
                    recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                )
                return render(request, 'contact/thanks.html', {'name': request.user.username})
            except Exception as e:
                return render(request, 'contact/contact.html', {
                    'form': form,
                    'error': '送信に失敗しました。時間をおいて再度お試しください。'
                })
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})