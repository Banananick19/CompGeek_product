from .models import PrimaryCategory, SecondaryCategory


def context_processor(request):
    context = {}
    context['primary_categories'] = PrimaryCategory.objects.all()
    context['secondary_categories'] = SecondaryCategory.objects.all()

    return context
