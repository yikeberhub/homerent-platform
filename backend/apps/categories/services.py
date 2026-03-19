from apps.categories.models import Category

class CategoryService:
    @staticmethod
    def add_category(values):
        name = values['name']
        if Category.objects.filter(name=name).exists():
            return None 
        category = Category.objects.create(**values)
        return category 
    
    @staticmethod
    def update_category(id, values):
        name = values['name']
        if Category.objects.filter(name=name).exclude(id=id).exists():
            return None 

        try:
            category = Category.objects.get(id=id)
            for key, value in values.items():
                setattr(category, key, value)
            category.save()
            return category
        except Category.DoesNotExist:
            return None
