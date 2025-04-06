from .models import Category

def category_context(request):
    return {
        'categories': Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
    }
