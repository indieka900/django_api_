from rest_framework.decorators import api_view,APIView
from django.http import Http404
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Job, Bookmark
from .serializers import CustomUserSerializer,JobSerializer
from django.db.models import Q

class UserRegistrationView(APIView):
    def post(self, request):
        data = request.data.copy()
        password = request.data.get('password')
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            if password:
                hashed_pass = make_password(password)
                serializer.validated_data['password'] = hashed_pass
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class UserDetail(APIView):
    def get_user(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:
            raise Http404()
        
    
    def put(self, request, pk):
        user =self.get_user(pk)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if 'password' in request.data:
                password = request.data['password']
                hashed_pass = make_password(password)
                serializer.validated_data['password'] = hashed_pass
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user = self.get_user(pk=pk)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=204)
    
class JobCreationView(APIView):
    # permission_classes = [IsAuthenticated]
    def get_user(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:
            raise Http404()
    def post(self, request, pk):
        user = self.get_user(pk)
        if user.isAdmin:
            job_data = request.data.copy()
            job_data['agent'] = user.pk
            serializer = JobSerializer(data=job_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=201)
            return Response(serializer.errors, status=400)
        return Response({"message":"Only admins are allowed.... "})
class FindBookmarkView(APIView):
    # permission_classes = [IsAuthenticated]
    def get_user(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:
            raise Http404()
    def get(self, request, pk):
        user = self.get_user(pk)
        bookmark = Bookmark.objects.filter(userid=user.pk)
        serializer = JobSerializer(bookmark)
        return Response(serializer.data,status=201)
        #return Response(serializer.errors, status=400)
    
class BookmarkView(APIView):
    # permission_classes = [IsAuthenticated]
    def get_user(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:
            raise Http404()
    def get_job(self, jobid):
        try:
            job = Job.objects.get(pk=jobid)
            return job
        except Job.DoesNotExist:
            raise Http404()
    def post(self, request, pk, jobid):
        user = self.get_user(jobid)
        job = self.get_job(pk)
        bookmark_data = request.data.copy()
        bookmark_data['job'] = job.pk
        bookmark_data['userid'] = user.pk
        serializer = JobSerializer(data=bookmark_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors, status=400)
    
class JobDetail(APIView):
    def get_job(self, pk):
        try:
            job = Job.objects.get(pk=pk)
            return job
        except Job.DoesNotExist:
            raise Http404()
        
    def get_user(self, user_pk):
        try:
            user = User.objects.get(pk=user_pk)
            return user
        except User.DoesNotExist:
            raise Http404()
    
    def put(self, request, pk, user_pk):
        user = self.get_user(user_pk)
        if user.isAdmin:
            job =self.get_job(pk)
            serializer = JobSerializer(job, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response({"message":"Only admins can create"})

    def delete(self, request, pk, user_pk):
        user = self.get_user(user_pk)
        if user.isAdmin:
            job = self.get_job(pk=pk)
            job.delete()
            return Response({'message': 'job deleted successfully'}, status=204)
        return Response({"message":"Only admins are allowed..."})

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Retrieve the user from the database based on the username or email
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'message': 'Invalid username'}, status=400)

        # Compare the entered password with the stored password
        if check_password(password, user.password):
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            serializer = CustomUserSerializer(user)
            response_data = {
                'token': access_token,
                'user': serializer.data
            }
            return Response(response_data, status=200)
        else:
            # Passwords do not match
            return Response({'message': 'Invalid password'}, status=400)

@api_view(['GET'])
def Job_list(request):
    job = Job.objects.all()
    serializer = JobSerializer(job, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_job(request,pk):
    job = Job.objects.get(pk=pk)
    serializer = JobSerializer(job,many=False)
    return Response(serializer.data)


@api_view(['GET'])
def delete_bookmark(request,pk):
    bookmark = Bookmark.objects.get(pk=pk)
    bookmark.delete()
    return Response({"message': 'bookmark deleted successfully"})

@api_view(['GET'])
def searchJob(request):
    query = request.GET.get('query')
    if query:
        results = Job.objects.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        )
        serialized_results = JobSerializer(results, many = True)
        return Response({'results': serialized_results.data})
    else:
        return Response({'error': 'No search query provided'}) 

# Create your views here.
