from django.urls import path 

from apps.properties.views import GetProperties,AddProperty,PropertyDetail,UpdateProperty,DeleteProperty

urlpatterns = [
    path('',GetProperties.as_view(),name='get-properties'),
    path('add/',AddProperty.as_view(),name='add-property'),
    path('<int:pk>/',PropertyDetail.as_view(),name='property-detail'),
    path('<int:pk>/update/',UpdateProperty.as_view(),name='update-property'),
    path('<int:pk>/delete/',DeleteProperty.as_view(),name='delete-property'),
    
]
