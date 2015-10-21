#Match 般配

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
    "matchs":[{"boy":1,"girl":5},{"boy":"4","girl":"6"}] 男孩id，女孩id， json数组
    }
返回
    {
        "vote": [
            11,
            1
        ],
        "result": 1
    }