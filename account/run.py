from account.models import User
from PIL import Image
import os

avatar_dir = os.walk('/home/z-kidy/pictures')
pro_dir = '/home/z-kidy/Match/media/account/avatar/'

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


 