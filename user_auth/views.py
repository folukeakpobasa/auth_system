from django.shortcuts import render
from user_auth.models import CustomUser
from rest_framework import viewsets
from user_auth.serializers  import ManageUserSerializer


class ManageUserViewSet(viewsets.ModelViewSet):
    serializer_class = ManageUserSerializer
    queryset = User.objects.all()
    # permission_classes = [permissions.IsAdminUser,
    #                   IsOwnerOrReadOnly]
  
    def list(self, request):
        ''' Get All Users '''
        serializer = ManageUserSerializer(self.queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        '''Get User Basic Information'''
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = ManageUserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['post'], permission_classes=[IsOwnerOrReadOnly] )
    def update_user(self, request, pk=None):
        '''Update User Basic Information'''
        user = self.get_object()
        
        serializer = ManageUserSerializer(data=request.DATA)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        '''Delete User'''
        user = get_object_or_404(self.queryset, pk=pk)
        user.delete()
        return Response(
                    data={"Success": "users removed successfully"}, status=status.HTTP_204_NO_CONTENT
                )
