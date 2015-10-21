#encoding=utf-8
from django.db.models.fields.files import ImageField, ImageFieldFile
from PIL import Image
import os

def _add_thumb(s):
    """
    往图片文件名里添加'.thumb'
    """
    parts = s.split(".")
    parts.insert(-1, "thumb")
    return ".".join(parts)
def _add_mid(s):
    """
    往图片文件名里添加'.thumb'
    """
    parts = s.split(".")
    parts.insert(-1, "mid")
    return ".".join(parts)

def clipimage(size):
    '根据大小从中间切一个正方形'
    width = int(size[0])
    height = int(size[1])
    box = ()
    if (width > height):
        dx = width - height
        box = (dx / 2, 0, height + dx / 2,  height)
    else:
        dx = height - width
        box = (0, dx / 2, width, width + dx / 2)
    return box

class ThumbnailImageFieldFile(ImageFieldFile):
    def _get_thumb_path(self):
        return _add_thumb(self.path)
    thumb_path = property(_get_thumb_path)
    
    def _get_thumb_url(self):
        return _add_thumb(self.url)
    thumb_url = property(_get_thumb_url)

    def _get_mid_path(self):
        return _add_mid(self.path)
    mid_path = property(_get_mid_path)

    def _get_mid_url(self):
        return _add_mid(self.url)
    mid_url = property(_get_mid_url)


    def save(self, name, content, save=True):
        super(ThumbnailImageFieldFile, self).save(name, content, save)
        img = Image.open(self.path)

        img.thumbnail((self.field.mid_width, self.field.mid_height), Image.ANTIALIAS)
        img.save(self.mid_path) # 保存一个合适大小的图

        box = clipimage(img.size)
        img_thumb = img.crop(box)
        img_thumb.thumbnail((self.field.thumb_width, self.field.thumb_height), Image.ANTIALIAS)
        img_thumb.save(self.thumb_path) # 保存方形缩略图


    def delete(self, save=False):
        if os.path.exists(self.thumb_path):
            print self.thumb_path # remove the thumb img
            os.remove(self.thumb_path)       # remove the mid img  
        if os.path.exists(self.mid_path):
            print self.mid_path
            os.remove(self.mid_path)
        super(ThumbnailImageFieldFile, self).delete(save)


class ThumbnailImageField(ImageField):
    """
    接受两个可选参数，缩略图的宽和高，默认设置为100px；
    """
    attr_class = ThumbnailImageFieldFile

    def __init__(self, thumb_width=150, thumb_height=150, mid_width=400, mid_height=400, *args, **kwargs):
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        self.mid_width = mid_width
        self.mid_height = mid_height
        super(ThumbnailImageField, self).__init__(*args, **kwargs)
