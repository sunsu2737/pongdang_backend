from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response
import logging
from .models import User, UserManager
from email.mime.text import MIMEText
import smtplib
# Create your views here.


class UserCreate(APIView):

    def get(self, request):
        email = request.GET['email']
        logger = logging.getLogger('LOG')

        logger.info(f"이메일 인증 요청 {email}")

        try:
            user = User.objects.filter(email=email).first()
            print(user)
            if user.auth == True:
                logger.warning(f"이메일 인증 실패 - 이미 인증된 메일{email}")
                return render(request, 'auth/auth_again.html')
            user.auth = True
            user.save()
            logger.info(f"이메일 인증 완료 email: {email}")
            return render(request, 'auth/auth_page.html')
        except Exception as e:
            logger.error(f"이메일 인증 실패 {e} email: {email}")
            return render(request, 'auth/auth_fail.html')

    def post(self, request):
        nickname = request.data.get('nickname',None)
        email = request.data.get('email',None)
        password = request.data.get('password',None)

        logger = logging.getLogger('LOG')

        logger.info(f"회원가입 요청 nickname: {nickname}, email: {email}")
        

        try:
            User.objects.create_user(email=email, nickname=nickname, password=password)


            smtp = smtplib.SMTP('smtp.gmail.com', 587)

            smtp.ehlo()

            smtp.starttls()

            smtp.login('buddyAuthMail@gmail.com', 'wdtzdxijdkoivyay')

            msg = MIMEText(f'아래 링크를 눌러 인증해주세요.\n http://127.0.0.1:8000/user/create?email={email}')
            msg['Subject'] = '버디 인증 메일입니다.'

            smtp.sendmail('buddyAuthMail@gmail.com',email , msg.as_string())

            smtp.quit()
            logger.info(f"회원가입 완료 nickname: {nickname}, email: {email}")
            return Response(status=200)
        except IntegrityError as u:

            logger.warning(f"닉네임 중복 nickname: {nickname}, email: {email} {u}")
            return Response(status=501)
        except Exception as e:
            logger.error(f"회원가입 실패 nickname: {nickname}, email: {email}, {e}")
            return Response(status=500)
        

