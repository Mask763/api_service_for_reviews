from rest_framework import mixins, viewsets


class CreateRetrieveListViewSet(
        viewsets.GenericViewSet,
        mixins.CreateModelMixin,
        mixins.ListModelMixin
):
    pass