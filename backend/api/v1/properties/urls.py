from django.urls import path 

from apps.properties.views import (GetProperties,
                                   AddProperty,
                                   PropertyDetail,
                                   UpdateProperty,
                                   DeleteProperty,AddToFavoriteView,
                                   RemoveFromFavoriteView,
                                   ActivatePropertyView,
                                   DeactivatePropertyView,
                                   SearchPropertiesView,
                                   FilterPropertiesView
                                   )

urlpatterns = [
    path('',GetProperties.as_view(),name='get-properties'),
    path('add/',AddProperty.as_view(),name='add-property'),
    path('<int:pk>/',PropertyDetail.as_view(),name='property-detail'),
    path('<int:pk>/update/',UpdateProperty.as_view(),name='update-property'),
    path('<int:pk>/delete/',DeleteProperty.as_view(),name='delete-property'),
    
    path('search/', SearchPropertiesView.as_view(), name='property-search'),
    path('filter/', FilterPropertiesView.as_view(), name='property-filter'),
    # path('filter/', PropertyFilterView.as_view(), name='property-filter'),
    # path('featured/', FeaturedPropertiesView.as_view(), name='featured-properties'),
    # path('nearby/', NearbyPropertiesView.as_view(), name='nearby-properties'),
    # path('user/<int:user_id>/', UserPropertiesView.as_view(), name='user-properties'),
    # path('category/<int:category_id>/', PropertiesByCategoryView.as_view(), name='properties-by-category'),
    
    # # Action endpoints
    path('<int:pk>/activate/', ActivatePropertyView.as_view(), name='property-activate'),
    path('<int:pk>/deactivate/', DeactivatePropertyView.as_view(), name='property-deactivate'),
    path('<int:pk>/favorite/', AddToFavoriteView.as_view(), name='property-favorite'),
    path('<int:pk>/unfavorite/', RemoveFromFavoriteView.as_view(), name='property-unfavorite'),
    # path('<int:pk>/bookmark/', PropertyBookmarkView.as_view(), name='property-bookmark'),
    
]
