# Codezvous by team AncientSE of USTC(古代软剑)

第二次更新：

当前网站结构

学生端：

主页---页面一：查看课程---页面二：选课（待实现）
                  |         
                  |进入课程子页---页面一：作业提交与查看（待实现）
		  
教师端

主页---页面一：查看课程---页面二：发布课程（待实现）
                  |         
                  |进入课程子页---页面一：作业发布（待实现）---页面二：作业批改（待实现）

进行中的任务：

1. 注册和登录端的优化

2. 作业的提交和显示

3. 服务器的部署

4. 选课以及发布课程

将要进行的任务：

1. 前端页面的优化

2. 作业的批改



第一次更新：

Blogs: www.cnblogs.com/ustc-rjgc

Github: https://github.com/AncientSE/Codezvous

初步实现教师和学生的注册和登录框架
当前Model里面的表

	·学生表S(系统表)
	
	·老师表T(系统表)
	
	·身份表Identity(name, identity)
	
	·课程表ClassTable(class_number, teacher, class_name, class_content)
	
	·选课表ClassChoose(class_number, student)
	
	·作业表Homework(class_number, homework_number, homework_content, deadline)
	
	·作业提交表Submit(student, class_number, homework_number, submit_content, submit_date)
	
操作方法：

   ·将该文件拷贝到本地：

      ·git clone https://github.com/AncientSE/Codezvous.git 
  
   ·如果已经安装了python3以及Django库，那么进入Codezvous文件夹
  
      ·python manage.py migrate
      
      ·python manage.py runserver
      
   ·在浏览器打开127.0.0.1：8000就可以看到首页
      
      
实现之后的效果应该是rickyim.pythonanywhere.com这样



