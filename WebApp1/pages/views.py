from django.shortcuts import render

def contact_view(request, *args, **kwargs):
    """Отображает страницу контактов с информацией о связи"""
    context = {
        "contact_text": "Остались вопросы?",
        "contact_number": "Свяжитесь с нами по телефону: +7 (999) 99-99-99",
        "contact_time": "Часы работы: с 9:00 до 18:00",
    }
    return render(request, "pages/contact.html", context)

def about_view(request, *args, **kwargs):
    """Отображает страницу с информацией о компании"""
    return render(request, "pages/about.html", {})

def social_view(request, *args, **kwargs):
    """Отображает страницу социальных сетей"""
    return render(request, "pages/social.html", {})