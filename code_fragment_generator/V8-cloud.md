
### 1.1 登录

请求方法：POST

请求路径：/public/login

请求内容：

	{
    	"loginName": string,           // 账号，必填
    	"password": string,            // 密码，必填
		"captchaToken": string,        // 验证码token，无需必填
		"captchaValue": string,        // 验证码value，无需必填
		"source": "CastServer",        // 登录源，必填，CastServer：飞屏盒子，Web：浏览器，App：移动端，Wechat：微信端
		"role": ["teacher"],           // 允许登录的账号角色，teacher：老师，student：学生，admin：学校管理员，无需必填
		"deviceId": string,            // 设备唯一标识 ，可以为设备的SN或GUID或MAC...无需必填
		"softwareId": string,          // 设备运行的极域软件ID，无需必填
		"softwareVer": string          // 设备运行的极域软件版本号，无需必填
	}

请求返回：

	{
		"errCode": int,
		"errMsg": string,
		"data": {
    		"loginToken": string,       // 教育云登录token
    		"name": string,             // 用户姓名
    		"eduUuid": string,          // uuid
    		"user": {                   // 教育云账户信息
				"eduMail": string,      // 邮箱
				"eduMobile": string,    // 电话
				"eduName": string,      // 用户名
				"eduPhoto": "string",   // 头像
				"userId": string        // 教育云账号id      --- CastServer 需保存该ID 后期使用
    		}
		}
	}

>1. 当账号某段时间内登录失败次数太多时，系统返回错误码4200，要求用户输入验证码。此时客户端需要调用获取验证码接口。
>2. 目前只能是老师登录，学生和学校管理员无权限登录。

### 1.2 获取登录验证码

请求方法：GET

请求路径：/public/login/captcha

请求返回：

	{
		"errCode": int,
		"errMsg": string,
		"data": {
			"captchaToken": string,     // 验证码令牌
			"imageContent": string,     // 验证码图片，base64
			"imageType": "image/jpeg"   // 验证码图片类型
		}
	}


### 1.3 获取当前老师已加入的学校列表

请求方法：GET

请求路径：/profile/joinedSchools

请求头authorization: loginToken

请求返回：

	{
		"errCode": int,
        "errMsg": string,
        "data": [
			{
				"schoolId": string,    // 学校id
				"schoolName": string   // 学校名称
			}
			...
		]
	}

### 1.4 根据极域云账号登陆Token获取绑定的教育云账号

请求方法：POST

请求路径：/public/findEduAcctListByMythwareIdToken

请求内容类型：application/json

请求内容：

	{
    	"mythwareidLoginToken": string,   // mythwareid登陆token，必填
		"source": "CastServer",           // 登录源，必填
		"role": ["teacher"]               // 返回指定角色的教育云账号
	}

请求返回：

	{
		"errCode": int,
        "errMsg": string,
        "data": {
			"teachers": [                    // Mythware ID绑定的教育云老师列表
				{
					"userId": string，       // 教育云账号id --- CastServer 需保存改ID 后期使用
					"eduMail": string,       // 邮箱
					"eduMobile": string,     // 电话
					"eduName": string,       // 用户名
					"eduPhoto": "string",    // 头像
					"schools":[              // 账户已加入的学校列表
						{
							"schoolId": string,   // 学校id
							"schoolName": string  // 学校名称
						}
						...
					]
				}
				...
			],
			"students": [                    // Mythware ID绑定的教育云学生列表，后期使用
				{
					"userId": string，       // 教育云账号id
					"eduMail": string,       // 邮箱
					"eduMobile": string,     // 电话
					"eduName": string,       // 用户名
					"eduPhoto": "string",    // 头像
					"schools":[              // 账户已加入的学校列表
						{
							"schoolId": string,   // 学校id
							"schoolName": string  // 学校名称
						}
					]
				}
				...
			],
			"admins": [                      // Mythware ID绑定的教育云管理员列表，后期使用
				{
					"userId": string，       // 教育云账号id
					"eduMail": string,       // 邮箱
					"eduMobile": string,     // 电话
					"eduName": string,       // 用户名
					"eduPhoto": "string",    // 头像
					"schools":[              // 账户已加入的学校列表
						{
							"schoolId": string,   // 学校id
							"schoolName": string  // 学校名称
						}
					]
				}
				...
			]
		}
	}


### 1.5 根据极域云账号登陆token生成教育云账号登陆token

请求方法：POST

请求路径：/public/createLoginTokenByMythwareIdToken

请求内容：

	{
    	"mythwareidLoginToken": string,   // mythwareid登陆token，必填
    	"eduacctUserId": string           // 教育云账号id，必填
    	"source": "CastServer",           // 登录源，必填
    	"deviceId": string,               // 设备唯一标识 ，可以为设备的SN或GUID或MAC...必填
		"softwareId": string,             // 设备运行的极域软件ID，必填
		"softwareVer": string             // 设备运行的极域软件版本号，必填
	}

请求返回：

	{
		"errCode": int,
        "errMsg": string,
        "data": {
			"loginToken": string,    // 教育云账号登录token
			"name": string,          // 用户姓名
			"eduUuid": string        // uuid
		}
	}


### 1.6 同步当前老师的班级模型数据

请求方法：POST

请求路径：/profile/teachingRelationshipSync/school/{schoolId}

请求头authorization: loginToken

请求内容：

    [
        {
            "classId": string,            // 班级id
            "classInfo": {
                "verion": long
            },
            "studentInfo": {
                "verion": long
            },
            "subjectInfo": {
                "version": long         // 任教关系版本
            }
        }
    ]

请求返回：

	{
		"errCode": int,
        "errMsg": string,
        "data": [
            {
                "classId": string,         // 班级id
                "classInfo": {
                    "classId": string,      // 班级id
                    "className": int,       // 班级名称
                    "remark": string,       // 班级名称备注
                    "degreeId": string,     // 学段id
                    "gradeId": string,      // 年级id
                    "gradeName": string,    // 年级名称
                    "verion": long
                },
                "studentInfo": {
                    "verion": long,
                    "students": [
                    {
                        "studentId": string,           // 学生id
                        "studentName": string,         // 姓名
                        "schoolRollNumber": string,    // 学籍号，校内唯一
                        "classroll_number": string,    // 班内学号
                        "feedbackNo": string,          // 反馈器编号
                        "boardNo": string              // 手写板编号
                    },
                    ...
                    ]
                },
                "subjectInfo": {
                    "verion": long,
                    "subjects": [
	                    {
                            "subjectId": string,    // 科目id
                            "subjectName": string  // 科目名称
                        },
                        ...
                    ]
                }
            },
            ...
        ]
	}

> 1. 若第一次获取数据，则请求内容为空数组，服务器返回所有的任教数据。
> 2. 若本地已缓存班级模型数据，则请求内容为所有缓存的任教班级数据，格式参考上面文档。服务器返回所有的任教数据。若class的version未改变，则classInfo和students字段为空。

### 1.7 获取教育云账号详情

请求方法：GET

请求路径：/profile

请求头authorization: loginToken

请求返回：

	{
		"errCode": int,
        "errMsg": string,
        "data": {
			"userId": string,       // 教育云id
			"name": string,         // 姓名
			"eduName": string,      // 用户名
			"eduMail": string,      // 邮箱
			"eduMobile": string,    // 手机
			"eduPhoto": string,     // 头像base64
			"userType": int         // 账号类型，1：学校管理员，2：老师，3：学生
        }
	}


### 1.8 获取当前老师的任教关系

请求方法：GET

请求路径：/profile/teachingRelationshipGroupBySchool

请求头authorization: loginToken

请求返回：

	{
		"errCode": int,
		"errMsg": string,
		"data": [
		    {
		        "schoolId": string,                 // 学校id
		        "schoolName": string,               // 学校名称
		        "subjectClassList": [
		            {
		                "subjectId": string,        // 科目id
		                "subjectName": string,      // 科目名称
		                "degreeId": string,         // 学段id
		                "gradeId": string,          // 年级id
		                "gradeName": string,        // 年级名称
		                "classId": string,          // 班级id
		                "className": string,        // 班级名称
		                "classRemark": string       // 班级名称备注
		            },
		            ...
		        ]
		    },
		    ...
		]
	}
	
### 1.9 盒子端获取二维码登陆所需的信息

请求方法：POST

请求路径：/public/qrcodeToken

请求内容：
    
    {
        "sn": string,
        "pn": string,
        "spn": string
    }

请求返回：

	{
		"errCode": int,
		"errMsg": string,
		"data": {
    		"qrcodeToken": string       // 二维码令牌
		}
	}

### 1.10 获取二维码登陆的微信账号信息

请求方法：GET

请求路径：/public/qrcodeToken/{qrcodeToken}

请求参数：

| 参数名称 | 参数类型 | 是否必填 | 字段说明 
|---------------
| qrcodeToken | String | 是 | 二维码令牌  |

请求返回：

	{
		"errCode": int,
		"errMsg": string,
		"data": {
    		"loginType": int,            // 0:表示未设置，1：微信访客，2:教育云账号
    		"loginToken": string         // 教育云账号的登陆令牌。该字段为loginType == 2时有效
		}
	}
	
> 错误码4094表示二维码令牌无效。

### 1.11 根据当前登陆token获取盒子端登陆token

请求方法：POST

请求路径：/profile/screenboxLoginToken

请求头authorization: loginToken

请求内容：

	{
    	"sn": string
	}

请求返回：

	{
		"errCode": int,
        "errMsg": string,
        "data": {
			"loginToken": string    // 教育云账号登录token
		}
	}
	
### 1.12 根据当前登陆token获取APP端登陆token

请求方法：POST

请求路径：/profile/appLoginToken

请求头authorization: loginToken

请求返回：

	{
		"errCode": int,
        "errMsg": string,
        "data": {
			"loginToken": string    // 教育云账号登录token
		}
	}

### 1.13 创建访客登陆令牌

请求方法：POST

请求路径：/public/visitorToken

请求内容：
    
    {
        "sn": string,
        "pn": string,
        "spn": string
    }

请求返回：

	{
		"errCode": int,
		"errMsg": string,
		"data": {
    		"loginToken": string       // 登陆令牌
		}
	}
	
## 2. 极域云相关接口

API Base Url

	https://be.edu.mythware.net:8899/mythwareid

### 2.1 登陆

请求方法：POST

请求路径：/public/login

请求内容：

	{
    	"loginName": string,           // 账号，必填
    	"password": string,            // 密码，必填
		"captchaToken": string,        // 验证码token，无需必填
		"captchaValue": string,        // 验证码value，无需必填
		"source": string               // 登录源，必填，CastServer：飞屏盒子，Web：浏览器，App：移动端，Wechat：微信端
	}

请求返回：

	{
		"errCode": int,
		"errMsg": string,
		"data": {
    		"loginToken": string       // mythwareid登录token
		}
	}


### 2.2 获取登录验证码

请求方法：GET

请求路径：/public/login/captcha

请求返回：

	{
		"errCode": int,
		"errMsg": string,
		"data": {
			"captchaToken": string,     // 验证码令牌
			"imageContent": string,     // 验证码图片，base64
			"imageType": "image/jpeg"   // 验证码图片类型
		}
	}
	
### 2.3 获取个人账号信息

请求方法：GET

请求路径：/profile

请求头authorization: 极域云账号loginToken

请求返回：

	{
		"errCode": int,
		"errMsg": string,
		"data": {
			"mythwareId": string,     // 极域云id
			"name": string,           // 姓名
			"mail": string,           // 邮箱
			"mobile": string,         // 手机
			"photo": string           // 头像base64
		}
	}
	
### 2.4 获取绑定的教育云账号列表

请求方法：GET

请求路径：/edu/bindedEduAcct

请求头authorization: 极域云账号loginToken

请求返回：

	{
		"errCode": int,
		"errMsg": string,
		"data": [
			{
			    "userId": string,       // 教育云id
			    "eduName": string,      // 用户名
			    "eduMail": string,      // 邮箱
			    "eduMobile": string,    // 手机
			    "eduPhoto": string,     // 头像base64
			    "userType": int         // 账号类型，1：学校管理员，2：老师，3：学生
			},
			...
		]
	}

## 3. 微信个人中心相关接口

API Base Url

	https://be.edu.mythware.net:8899/wechat
	
### 3.0 获取loginToken

请求方法：GET

请求路径：/loginToken

请求参数：

| 参数名称 | 参数类型 | 是否必填 | 字段说明 
|---------------
| code | String | 是 |  |

请求返回：

	{
		"errCode": int,
        "errMsg": string,
        "data": {
            "loginToken": string
		}
	}




### 3.1 获取个人信息

请求方法：GET

请求路径：/profile

请求头authorization: loginToken

请求返回：

	{
		"errCode": int,
        "errMsg": string,
        "data": {
            "wechatId": string,        // 微信id
			"nickname": string,        // 昵称
			"headimgurl": string       // 头像url
		}
	}

### 3.2 更新个人信息

请求方法：POST

请求路径：/profile

请求头authorization: loginToken

请求内容：

	{
	    "nickname": string,        // 昵称
		"headimgurl": string       // 头像url
	}
	
> 只需要提交修改的字段。

请求返回：

	{
		"errCode": int,
        "errMsg": string
	}


### 3.3 获取已绑定的账号

请求方法：GET

请求路径：/profile/bindedAccount

请求头authorization: loginToken

请求返回：

	{
		"errCode": int,
        "errMsg": string,
        "data": {
            "eduAcct": [
                {
			        "userId": string,       // 教育云id
			        "name": string,         // 姓名
			        "eduName": string,      // 用户名
			        "eduMail": string,      // 邮箱
			        "eduMobile": string,    // 手机
			        "eduPhoto": string,     // 头像base64
			        "userType": int         // 账号类型，1：学校管理员，2：老师，3：学生
			        "schools": [            // 已加入的学校
			            {
			                "schoolId": string,   // 学校id
			                "schoolName": string  // 学校名称
			            },
			            ...
			        ]
                },
                ...
            ],
            "mythwareId": [
                {
                    "mythwareId": string,     // 极域云id
			        "name": string,           // 姓名
			        "mail": string,           // 邮箱
			        "mobile": string,         // 手机
			        "photo": string           // 头像base64
                }
            ]
        }
	}
	
### 3.4 绑定教育云账号

请求方法：POST

请求路径：/eduAcct/bind

请求头authorization: loginToken

请求内容：

	{
    	"loginName": string,           // 账号，必填
    	"password": string             // 密码，必填
	}

请求返回：

	{
		"errCode": int,
        "errMsg": string
	}
	

### 3.5 获取教育云账号详情

请求方法：GET

请求路径：/eduAcct/{eduAcctId}/profile

请求头authorization: loginToken

请求返回：

	{
		"errCode": int,
        "errMsg": string,
        "data": {
			"userId": string,       // 教育云id
			"name": string,         // 姓名
			"eduName": string,      // 用户名
			"eduMail": string,      // 邮箱
			"eduMobile": string,    // 手机
			"eduPhoto": string,     // 头像base64
			"userType": int         // 账号类型，1：学校管理员，2：老师，3：学生
        }
	}

### 3.6 获取教育云老师已加入的学校列表

请求方法：GET

请求路径：/eduAcct/{eduAcctId}/joinedSchools

请求头authorization: loginToken

请求返回：

	{
		"errCode": int,
        "errMsg": string,
        "data": [
			{
				"schoolId": string,    // 学校id
				"schoolName": string   // 学校名称
			}
			...
		]
	}

### 3.7 获取教育云账号的任教关系

请求方法：GET

请求路径：/eduAcct/{eduAcctId}/teachingRelationship

请求头authorization: loginToken

请求参数：

    {
        "schoolId": string,  // 学校id，不是必填
    }

请求返回：

	{
		"errCode": int,
		"errMsg": string,
		"data": [
		    {
		        "schoolId": string,                 // 学校id
		        "schoolName": string,               // 学校名称
		        "subjectClassList": [
		            {
		                "subjectId": string,        // 科目id
		                "subjectName": string,      // 科目名称
		                "degreeId": string,         // 学段id
		                "gradeId": string,          // 年级id
		                "gradeName": string,        // 年级名称
		                "classId": string,          // 班级id
		                "className": string,        // 班级名称
		                "classRemark": string       // 班级名称备注
		            },
		            ...
		        ]
		    },
		    ...
		]
	}
	
### 3.8 解除教育云账号的绑定

请求方法：POST

请求路径：/eduAcct/{eduAcctId}/unbind

请求头authorization: loginToken

请求返回：

	{
		"errCode": int,
        "errMsg": string
	}
	
### 3.9 绑定极域云账号

请求方法：POST

请求路径：/mythwareId/bind

请求头authorization: loginToken

请求内容：

	{
    	"loginName": string,           // 账号，必填
    	"password": string             // 密码，必填
	}

请求返回：

	{
		"errCode": int,
        "errMsg": string
	}
	
	
### 3.10 获取极域云账号详情

请求方法：GET

请求路径：/mythwareId/{mythwareId}/profile

请求头authorization: loginToken

请求返回：

	{
		"errCode": int,
		"errMsg": string,
		"data": {
			"mythwareId": string,     // 极域云id
			"name": string,           // 姓名
			"mail": string,           // 邮箱
			"mobile": string,         // 手机
			"photo": string           // 头像base64
		}
	}
	
### 3.11 获取极域云绑定的教育云账号

请求方法：GET

请求路径：/mythwareid/{mythwareId}/bindedEduAcct

请求头authorization: loginToken

请求返回：

	{
		"errCode": int,
		"errMsg": string,
		"data": [
			{
			    "userId": string,       // 教育云id
			    "name": string,         // 姓名
			    "eduName": string,      // 用户名
			    "eduMail": string,      // 邮箱
			    "eduMobile": string,    // 手机
			    "eduPhoto": string,     // 头像base64
			    "userType": int         // 账号类型，1：学校管理员，2：老师，3：学生
			},
			...
		]
	}
	
### 3.12 解除极域云账号的绑定

请求方法：POST

请求路径：/mythwareid/{mythwareId}/unbind

请求头authorization: loginToken

请求返回：

	{
		"errCode": int,
        "errMsg": string
	}
	
### 3.13 获取Qrcode Token信息

请求方法：GET

请求路径：/qrcodeToken/{qrcodeToken}

请求头authorization: loginToken

请求返回：

	{
		"errCode": int,
        "errMsg": string,
        "data": {
            "pn": string,
            "spn": string,
            "sn": string
        }
	}

> 如果qrcode token有效，则返回对应的设备信息。如果无效，则返回相关的错误码

### 3.14 设置Qrcode Token对应的登陆账号

请求方法：POST

请求路径：/qrcodeToken/{qrcodeToken}/loginAccount

请求头authorization: loginToken

请求内容：

    {
        "loginType": int,      // 1: 微信访客，2：教育云账号
        "eduAcctId": string,    // 教育云账号的id。该字段为loginType == 2时有效
        "schoolId": string
    }
    
请求返回：

	{
		"errCode": int,
        "errMsg": string
	}

### 3.15 获取教育云老师账号详情

请求方法：GET

请求路径：/eduAcct/{eduAcctId}/profile/teacherInfo

请求头authorization: loginToken

请求返回：

	{
		"errCode": int,
        "errMsg": string,
        "data": {
			"teacherId": string,       // 教育云id
			"teacherName": string
        }
	}

### 3.16 获取教育云学生账号详情

请求方法：GET

请求路径：/eduAcct/{eduAcctId}/profile/studentInfo

请求头authorization: loginToken

请求返回：

	{
		"errCode": int,
        "errMsg": string,
        "data": {
			"studentId": string,         // 学生id
			"studentName": string,       // 学生名称
			"schoolName": string,        // 学校名称
			"schoolRollNumber": string,  // 学籍号
			"classroll_number": string,  // 班内学号
			"className": int,            // 班级名称
			"classNameRemark": string,
			"gradeName": string
        }
	}

## 4 二维码生成规则

### 4.1 大屏端二维码登陆

二维码生成为一个url，规则为：

    https://screencast.wechat.mythware.net/qrcodeToken/{qrcodeToken}
    
操作流程：

    1. 盒子端调用接口1.9，创建qrcodeToken。根据上面的二维码生成规则，生成二维码供微信扫描。
    2. 盒子端调用接口1.10，查询微信。
        若loginType == 0，微信端尚未设置登陆账号。重新调用dia此接口。
        若loginType == 1，微信访客登陆。使用loginToken调用接口3.1，获取账号详情。
        若loginType == 2，教育云账号登陆。使用loginToken调用接口1.7，获取账号详情。
    3
    31. 微信端访问二维码中的url，在url对应的页面中调用接口3.13，检查qrcodeToken是否有效。若无效提示错误。若有效，执行步骤4。
    42. 微信端调用接口3.3，查询微信绑定的教育云账号和极域云账号。
    53. 如果步骤42中查询到当前微信绑定了极域云账号，调用接口3.11，查询极域云账号绑定的教育云账号。
    64. 获取步骤4和5中查询到的教育云账号，
        若教育云账号数量等于如果步骤2和3中，查询到当前绑定的教育云账号数量为0，则显示绑定账号界面。若绑定成功后，回到步骤43。也可以直接选择微信访客登陆，调用接口3.14。
        若如果步骤2和3中，查询到当前绑定的教育云账号数量大于不为0，则遍历教育云账号，调用接口3.6，显示老师任教的学校。，用户选择账号和学校后，调用接口3.14，设置qrcodeToken对应的教育云账号和学校。
    5. 


### 4.2 教师助手二维码

二维码生成为一个url，规则为：

    https://screencast.wechat.mythware.net/interactiveLesson/{interactiveLessonId}/join
    
操作流程：

    1. 微信端扫码，获取课堂id。
    2. 微信端根据课堂id，进入课堂详情。ddua端扫码
    
    
### 4.3 二维码签到

二维码生成为一个url，规则为：

    https://screencast.wechat.mythware.net/interactiveLesson/{interactiveLessonId}/signup
    
操作流程：
    1. 微信端扫码，获取课堂id。
    2. 微信根据课堂id，调用签到接口。