#Match 般配

APPID：7YeJC0HnWNMJNgQutHBj
APPKEY：vmuWqxU4IwlrKuai0ouWmG1KNu7DiN


## 账号相关

### 注册

    发送网站POST  xxx/account/register/
    {
        "username":
        "password":
        "gender": "0" / "1"   "0":man "1":female
    }
    file "avatar"

    返回
    {

        "result": 1
    }

### 登入

    发送网站POST  xxx/account/login/
    {
        "username":
        "password":
    }
    返回
    {
        "user_info": {
            "user": 12,  (id)
            "nickname": 
            "gender": 
            "avatar":
            "token":
            "lover": avatar of my lover 
        },
        "result": 1
    }

### 设置

    发送网站POST xxx/account/settings/
    {
        "nickname":
        "password_old":
        "password":
        "gender":

    }
    file "avatar" 
    
    返回
    {
        "result": 1,
        "match_users": [
            {
                "username": 
                "nickname": ""
                "avatar": "/media/account/avatar/173571467.jpg"
            },

            xxx, 
        ]
    }


### 匹配异性列表(一次返5个)

    发送网站GET  xxx/account/match_users/

    返回
    {
        "result": 1,
        "match_users": [
            {
                "username": 
                "nickname": ""
                "avatar": "/media/account/avatar/173571467.jpg"
            },

            xxx, 
        ]
    }

### 获取用户头像

    发送网站GET account/check_user/?check_username=zjindiss2
    
    返回
    {
        "result": 1,
        "avatar": "/media/account/avatar/2.jpg"
    }

### 获取通讯录好友

    发送网站POST account/get_phone_friends/
    {
        "phone_friends": ["188292xxx", "xxxx"]
    }
    返回
    {
        "result": 1,
    }

### 链接好友
    
    发送网站POST account/link_user/
    {
        "link_username":"xxx"
    }
    返回
    {
        "result": 1,
    }



## 随机匹配

### 随机获取5男5女列表 

    发送网站get  xxx/couple/random/list
    返回
    {
        "boys": [
            {
                "user": 2, 用户id
                "avatar": "/media/account/avatar/190131ro5oos1865m1zo96.png.thumb.jpg" 头像
             },
            {
                "user": 1,
                "avatar": "/media/account/avatar/185903tzhchyvycc0dvajl.png.thumb.jpg"
            },
            {
                "user": 4,
                "avatar": "/media/account/avatar/hanhan_.png"
            }
        ],
        "girls": [
            {
                "user": 5,
                "avatar": null
            },
            {
                "user": 6,
                "avatar": null
            },
            {
                "user": 7,
                "avatar": null
            }
        ],
        "result": 1
    }

### 提交般配名单

    发送网站POST xxx/couple/random/match/
    {
    "boy":1,"girl":男孩id，女孩id
    }
    
    返回
    {
        "vote": 
        "result": 1
    }


## 情侣秀

### 获取恩爱狗

    发送网站GET xxx/couple/love_show/get/

    返回
    {
        "lovers": [
            {
                "id": 
                "girl_avatar": 
                "boy_avatar": 
            }

            xxx  一次返回十个
        ],
        "result": 1
    }

### 给恩爱狗评价

    发送网站POST xxx/couple/love_show/judge/
    {
        'love_show_id':
        'judge': 0 / 1 (1点赞，0反对)
    }
    返回
    {

        "result": 1
    }