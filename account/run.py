from account.models import User
from PIL import Image
import os

avatar_dir = os.walk('/home/z-kidy/pictures')
pro_dir = '/home/z-kidy/workspace/Match/media/account/avatar/'

for i in avatar_dir:
	a = i

images = a[2]

users = User.objects.all()

i = 0
for image in images:
	user = users[i]
	i += 1
	image_path = os.path.join(a[0], image)
	avatar = Image.open(image_path)
	avatar.save(pro_dir + str(i) + '.jpg')
	user.userinfo.avatar = 'account/avatar/' + str(i) + '.jpg' 
	user.userinfo.save()


@api_view(['POST'])
def settings(request):
    user = request.user
    receive = request.data
    form = SettingPasswordForm(receive)
    change_nickname = receive.get('new_nickname', None)
    change_gender = receive.get('gender', None)
    if not form.invalid():
    	return Response({
    		'result': 0,
    		'cause': form.errors
    		})

    if change_nickname:
        UserInfo.objects.filter(user=user).update(nickname=change_nickname)
    if change_gender and change_gender in ['0', '1']:
    	UserInfo.objects.filter(user=user).update(gender=change_gender)
    return Response({
        'result': 1,
        })