# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Sum, Count
from calendar import month_name


class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        data = self.get_serializer(data=request.data)
        if data.is_valid(raise_exception=True):
            user = data.save()
            user_details = {
                # 'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
            }
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'message': 'User registered successfully', 'user': user_details, 'auth_token': token.key }, status=status.HTTP_201_CREATED)

        else:
            print(data.errors)  # Print the errors to the console
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignInView(generics.CreateAPIView):
    serializer_class = UserSigninSerializer
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(username=email, password=password)
        if user:
            user_details = {
                # 'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number
            }
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'message': 'User logged in successfully', 'user': user_details, 'auth_token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class AccountView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id=request.user.id)  # Set the user_id field to the authenticated user
            return Response({'message': 'Account created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Account with this account no already exists'}, status=status.HTTP_401_UNAUTHORIZED)
        
    
    def get(self, request):
        user_id = self.request.user.id
        account = Account.objects.filter(user_id=user_id)
        serializer = AccountSerializer(account, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_object(self):
        # Get the account object for the authenticated user
        return get_object_or_404(Account, user=self.request.user.id)

    def put(self, request, pk):
        # Update account details
        account = get_object_or_404(Account, account_no=pk)
        serializer = self.get_serializer(account, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        # Delete account
        account = get_object_or_404(Account, account_no=pk)
        account.delete()
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class TransactionView(generics.CreateAPIView):
    # queryset = FinancialTransaction.objects.all()
    serializer_class = FinancialTransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = request.user.id
        serializer.save(user_id=user_id)  # Set the user_id field to the authenticated user
        account = Account.objects.filter(user = user_id, account_no = int(request.data['account_no'])).first()
        if(request.data['transaction_type'] == 'expense'):
            balance = float(account.balance) - float(request.data['amount'])
            account.balance = balance
            account.save()
            print(balance)
        else:
            balance = float(account.balance) + float(request.data['amount'])
            account.balance = balance
            account.save()
            print(balance)
        
        return Response({'message': 'Transaction created successfully'}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        user_id = self.request.user.id
        account = FinancialTransaction.objects.filter(user_id=user_id)
        serializer = FinancialTransactionSerializer(account, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        # Update account details
        transaction = get_object_or_404(FinancialTransaction, id=pk)
        serializer = self.get_serializer(transaction, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        # Delete account
        transaction = get_object_or_404(FinancialTransaction, id=pk)
        amount = transaction.amount
        transaction_type = transaction.transaction_type
        # print(transaction.account_no.account_no)
        account = Account.objects.get(account_no=int(transaction.account_no.account_no))
        
        if transaction_type == 'expense':
            account.balance += amount 
        else:
            account.balance -= amount
        
        # Save the updated balance
        account.save()
        transaction.delete()
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class AnalyticsDataView(generics.CreateAPIView):
    serializer_class = FinancialTransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_id = self.request.user.id
        
        # Filter expense transactions
        expenses = FinancialTransaction.objects.filter(user_id=user_id, transaction_type="expense")
        
        # Annotate expense transactions with month and year
        expenses_by_month = expenses.annotate(
            month=ExtractMonth('timestamp'),
            year=ExtractYear('timestamp')
        )
        
        # Aggregate expense transactions by month and year
        grouped_expenses = expenses_by_month.values('year', 'month').annotate(
            total_amount=Sum('amount'),
            num_transactions=Count('id')
        )

        for expense in grouped_expenses:
            expense['month'] = month_name[expense['month']]

        # Filter income transactions
        incomes = FinancialTransaction.objects.filter(user_id=user_id, transaction_type="income")
        
        # Annotate income transactions with month and year
        incomes_by_month = incomes.annotate(
            month=ExtractMonth('timestamp'),
            year=ExtractYear('timestamp')
        )
        
        # Aggregate income transactions by month and year
        grouped_incomes = incomes_by_month.values('year', 'month').annotate(
            total_amount=Sum('amount'),
            num_transactions=Count('id')
        )

        for income in grouped_incomes:
            income['month'] = month_name[income['month']]

        return Response({
            'expenses': grouped_expenses,
            'incomes': grouped_incomes
        }, status=status.HTTP_200_OK)