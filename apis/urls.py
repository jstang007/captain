from django.urls import path, include
from apis import views
from .views import deployment
from .views import pod
from .views import pod_list

urlpatterns = [
    path('deployment', deployment.DeploymentView.as_view()),
    path('pod', pod.PodView.as_view()),
    path('podList', pod_list.PodListView.as_view())
]