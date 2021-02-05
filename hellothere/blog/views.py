from django.shortcuts import render,redirect
from django.views import View
from django.views.generic.list import ListView

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
filehandler = logging.FileHandler('views(blog).log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(lineno)d:%(name)s:%(message)s')
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)


class TestIndex(View):
    def get(self,request):
        logger.info('yesssssssss-1')
        for key, value in request.session.items():
            logger.info('{} => {}'.format(key, value))

        # is_authenticated is i think checked from session cookie.
        if not request.user.is_authenticated:
            return redirect('login',permanent=True)
        logger.info('yesssssssss-2')
        return render(request,template_name='blog/index.html',context={})
        
    