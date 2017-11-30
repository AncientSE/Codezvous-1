# Codezvous by team AncientSE of USTC(古代软剑)
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

  ·git clone https://github.com/AncientSE/Codezvous.git 将该文件拷贝到本地
  
  ·如果已经安装了python3以及Django库，那么进入Codezvous文件夹
  
      ·python manage.py migrate
      
      ·python manage.py runserver
      
      ·在浏览器打开127.0.0.1：8000就可以看到首页
      
      
实现之后的效果应该是rickyim.pythonanywhere.com这个效果


Blogs: www.cnblogs.com/ustc-rjgc
Github: github.com/AncientSE/Codezvous
