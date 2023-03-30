from .models import Category


def categories(request):
    """
    Provide all templates with category as context data
    """
    categories = Category.objects.all()
    return {"categories": categories}
