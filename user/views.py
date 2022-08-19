from re import A
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import logging
import user
from .models import User, Feed
from email.mime.text import MIMEText
import smtplib
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from .serializer import UserSerializer
import base64
import numpy as np
import cv2
import uuid
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
        nickname = request.data.get('nickname', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        logger = logging.getLogger('LOG')

        logger.info(f"회원가입 요청 nickname: {nickname}, email: {email}")

        try:
            User.objects.create_user(
                email=email, nickname=nickname, password=password)

            smtp = smtplib.SMTP('smtp.gmail.com', 587)

            smtp.ehlo()

            smtp.starttls()

            smtp.login('buddyAuthMail@gmail.com', 'wdtzdxijdkoivyay')

            msg = MIMEText(
                f'아래 링크를 눌러 인증해주세요.\n http://127.0.0.1:8000/user/create?email={email}')
            msg['Subject'] = '버디 인증 메일입니다.'

            smtp.sendmail('buddyAuthMail@gmail.com', email, msg.as_string())

            smtp.quit()
            logger.info(f"회원가입 완료 nickname: {nickname}, email: {email}")
            return Response(status=200)
        except IntegrityError as u:

            logger.warning(f"닉네임 중복 nickname: {nickname}, email: {email} {u}")
            return Response(status=501)
        except Exception as e:
            logger.error(f"회원가입 실패 nickname: {nickname}, email: {email}, {e}")
            return Response(status=500)


class Profile (APIView):
    def post(self, request):
        logger = logging.getLogger('LOG')
        token = request.data.get("token", None)
        try:
            user = Token.objects.filter(key=token).first()
            if not user:
                logger.warning(f"프로필 조회 실패, 토큰 없음")
                Response(status=400)
            user_id = user.user_id
            profile = User.objects.filter(id=user_id).first()
            if not profile:
                logger.warning(f"프로필 조회 실패, user 없음")
                Response(status=400)
            logger.info(f"프로필 조회 성공 user_id: {user_id}")
            return Response(status=200, data=UserSerializer(profile).data)
        except Exception as e:
            logger.error(f"프로필 조회 실패 , {e}")
            return Response(status=500)




class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        logger = logging.getLogger('LOG')

        try:
            user = User.objects.filter(email=email).first()
            if not user:
                logger.warning(f"로그인 실패 email: {email}, 이메일 없음")
                return Response(status=400)
            if not check_password(password, user.password):
                logger.warning(f"로그인 실패 email: {email}, 비밀번호 불일치")
                return Response(status=400)
            if not user.auth:
                logger.warning(f"로그인 실패 email: {email}, 인증 안됨")
                smtp = smtplib.SMTP('smtp.gmail.com', 587)

                smtp.ehlo()

                smtp.starttls()

                smtp.login('buddyAuthMail@gmail.com', 'wdtzdxijdkoivyay')

                msg = MIMEText(
                    f'아래 링크를 눌러 인증해주세요.\n http://127.0.0.1:8000/user/create?email={email}')
                msg['Subject'] = '버디 인증 메일입니다.'

                smtp.sendmail('buddyAuthMail@gmail.com',
                              email, msg.as_string())

                smtp.quit()
                logger.info(f"로그인 성공 email: {email}")
                return Response(status=401)
            token, created = Token.objects.get_or_create(user=user)

            return Response(status=200, data={"token": str(token)})
        except Exception as e:
            logger.error(f"로그인 실패 email: {email}, {e}")
            return Response(status=500)


class UploadProfile(APIView):
    def post(self, request):
        logger = logging.getLogger('LOG')
        token = request.data[0]['token']

        try:
            user = Token.objects.filter(key=token).first()
            if not user:
                logger.warning(f"유저 조회 실패, 토큰 없음")
                Response(status=400)
            user_id = user.user_id
            profile = User.objects.filter(id=user_id).first()
            if not profile:
                logger.warning(f"프로필 조회 실패, user 없음")
                Response(status=400)

            base64Image = request.data[0]['image']
            imageStr = base64.b64decode(base64Image)
            nparr = np.fromstring(imageStr, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            filename =  str(uuid.uuid1()) + '.png'

            if cv2.imwrite(r'./images/' +filename, img_np):
                profile.profile_image = filename
                profile.save()
            return Response(status=200)
        except Exception as e:
            logger.error(f"프로필 이미지 업로드 실패 , {e}")
            return Response(status=500)

class FeedUpload(APIView):

    def post(self, request):
        logger = logging.getLogger('LOG')
        token = request.data[0]['token']

        try:
            user = Token.objects.filter(key=token).first()
            if not user:
                logger.warning(f"유저 조회 실패, 토큰 없음")
                Response(status=400)
            user_id = user.user_id
            profile = User.objects.filter(id=user_id).first()
            if not profile:
                logger.warning(f"프로필 조회 실패, user 없음")
                Response(status=400)

            base64Image = request.data[0]['image']
            imageStr = base64.b64decode(base64Image)
            nparr = np.fromstring(imageStr, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            filename =  str(uuid.uuid1()) + '.png'

            if cv2.imwrite(r'./images/' +filename, img_np):
                Feed.objects.create(user=profile, image=filename)

            return Response(status=200)
        except Exception as e:
            logger.error(f"피드 이미지 업로드 실패 , {e}")
            return Response(status=500)

class FeedGet(APIView):

    def post(self, request):
        logger = logging.getLogger('LOG')
        token = request.data.get('token',None)

        try:
            user = Token.objects.filter(key=token).first()
            if not user:
                logger.warning(f"유저 조회 실패, 토큰 없음")
                Response(status=400)
            user_id = user.user_id
            profile = User.objects.filter(id=user_id).first()
            if not profile:
                logger.warning(f"프로필 조회 실패, user 없음")
                Response(status=400)

            feeds = Feed.objects.filter(user = profile).order_by('-id')
            images = []
            for feed in feeds:
                images.append(feed.image)


            return Response(status=200, data={'images':images})
        except Exception as e:
            logger.error(f"피드 이미지 조회 실패 , {e}")
            return Response(status=500)