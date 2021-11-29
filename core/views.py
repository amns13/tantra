from rest_framework import generics


class CurrentUserListCreateApiView(generics.ListCreateAPIView):
    """Adds created_by and updated_by fields to ListCreateAPIView"""

    def perform_create(self, serializer):
        serializer.validated_data['created_by'] = self.request.user
        serializer.validated_data['updated_by'] = self.request.user
        return super(CurrentUserListCreateApiView,
                     self).perform_create(serializer)


class CurrentUserRetrieveUpdateDestroyAPIView(
        generics.RetrieveUpdateDestroyAPIView):
    """Adds created_by and updated_by fields to RetrieveUpdateDestroyAPIView"""

    def perform_update(self, serializer):
        serializer.validated_data['updated_by'] = self.request.user
        return super(CurrentUserRetrieveUpdateDestroyAPIView,
                     self).perform_update(serializer)

    def perform_destroy(self, instance):
        instance.updated_by = self.request.user
        return super(CurrentUserRetrieveUpdateDestroyAPIView,
                     self).perform_destroy(instance)
