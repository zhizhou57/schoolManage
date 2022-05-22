# -*- coding=utf8 -*-
# 导入Flask库
from flask import Flask, flash, render_template
from flask import request, session, g, redirect, url_for, abort
# 导入MySQL库
import pymysql

app = Flask(__name__)
# 写好的数据库连接函数，
# 传入的是table，数据表的名称，
# 返回值是数据表中所有的数据，以元祖的格式返回
app.config['SECRET_KEY'] = '231655'
# or
app.secret_key = '231655'
# or
app.config.update(SECRET_KEY='231655')

def get_Table_Data(table):
    conn = pymysql.connect(
        host='localhost', port=3306,
        user='root', passwd='231655',
        db='csp', charset='utf8',
    )
    cur = conn.cursor()
    res = cur.execute("select * from " + table)
    res = cur.fetchmany(res)
    cur.close()
    conn.commit()
    conn.close()
    return res
def connect_db():
    """Connects to the specific database."""
    db = pymysql.connect(host = 'localhost',user = 'root',charset = 'utf8',passwd = '231655',db = 'csp')
    return db
# 启动服务器后运行的第一个函数，显示对应的网页内容
@app.route('/', methods=['GET', 'POST'])
def home():
    # return '<a href="/index"><h1 align="center">欢迎使用教务系统---点击进入</h1></a>'
    return render_template('login.html')

# 对登录的用户名和密码进行判断
@app.route('/login', methods=['GET','POST'])
def login():
    # 需要从request对象读取表单内容：
    error = None
    if request.method == 'POST':
        if request.form['classname'] == 'admin':
            db = connect_db()
            cur = db.cursor()
            cur.execute('select username, password from admin_login')
            pas = dict(cur.fetchall())
            db.close()
            if pas.get(request.form['username']) == None :
                flash("账号错误，请重新输入...")
                return render_template('login.html')
            elif request.form['password'] != pas[request.form['username']]:
                flash("密码错误，请重新输入...")
                return render_template('login.html')
            else:
                session['logged_admin'] = request.form['username']
                # db = connect_db()
                # cur = db.cursor()
                # sql = 'select username from admin_login where username=%s'
                # s=cur.execute(sql, (session['logged_th']))
                # z=cur.fetchmany(s)
                # db.commit()
                # db.close()
                # return render_template('admin_index.html', error=error,name=z[0][0])
                return render_template('admin_index.html', name=session['logged_admin'])
        if request.form['classname']=='teacher':
            db = connect_db()
            cur = db.cursor()
            # cur.execute('select name, password from teacher, teacher_login where teacher.id = teacher_login.id')
            cur.execute('select id, password from teacher_login')
            pas = dict(cur.fetchall())
            db.commit()
            db.close()
            if pas.get(int(request.form['username'])) == None :
                flash("账号错误，请重新输入...")
                return render_template('login.html')
            elif request.form['password'] != pas[int(request.form['username'])]:
                flash("密码错误，请重新输入...")
                return render_template('login.html')
            else:
                db = connect_db()
                cur = db.cursor()
                cur.execute('select name from teacher where id=%s', (request.form['username']))
                name = cur.fetchone()[0]
                session['logged_th'] = name
                session['logged_th_id'] = request.form['username']
                db.close()
                return render_template('teacher_index.html', name=session['logged_th'])
        if request.form['classname']=='student':
            db = connect_db()
            cur = db.cursor()
            sql = 'select id, password from student_login'
            # sql = 'select name,password from student, student_login where student.id=student_login.id'
            cur.execute(sql)
            pas=dict(cur.fetchall())
            db.commit()
            db.close()
            if pas.get(int(request.form['username'])) == None :
                flash("账号错误，请重新输入...")
                return render_template('login.html')
            if pas[int(request.form['username'])] != request.form['password']:
                flash("密码错误，请重新输入...")
                return render_template('login.html')
            else :
                db = connect_db()
                cur = db.cursor()
                cur.execute('select name from student where id=%s', (request.form['username']))
                name = cur.fetchone()[0]
                session['logged_st'] = name
                session['logged_st_id'] = request.form['username']
                # print(session['logged_st'])
                return render_template('student_index.html', name=session['logged_st'])
    return render_template('login.html')

@app.route('/pwd', methods=['GET','POST'])
def pwd():
    if not session.get('logged_st'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    if request.method=='POST':
        if request.form['pwd']==request.form['pwd1']:
            db = connect_db()
            cur = db.cursor()
            sql = 'update student_login set password=%s where number=%s'
            cur.execute(sql,(request.form['pwd'],session['logged_st_id']))
            db.commit()
            db.close()
            flash('修改密码成功，请重新登录')
            session.pop('logged_st',None)
            session.pop('logged_st_id',None)
            return render_template('login.html')
        else :
            flash('两次密码不相同，请重新输入')
            return render_template('pwd.html')
    return render_template('pwd.html')

@app.route('/pwdt', methods=['GET','POST'])
def pwdt():
    if not session.get('logged_th'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    if request.method=='POST':
        if request.form['pwd']==request.form['pwd1']:
            db = connect_db()
            cur = db.cursor()
            sql = 'update teacher_login set password=%s where username=%s'
            cur.execute(sql,(request.form['pwd'],session['logged_th_id']))
            db.commit()
            db.close()
            flash('修改密码成功，请重新登录')
            session.pop('logged_th',None)
            session.pop('logged_th_id',None)
            return render_template('login.html')
        else :
            flash('两次密码不相等，请重新输入')
            return render_template('pwdt.html')
    return render_template('pwdt.html')

@app.route('/pwda', methods=['GET','POST'])
def pwda():
    if not session.get('logged_admin'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    if request.method=='POST':
        if request.form['pwd']==request.form['pwd1']:
            db = connect_db()
            cur = db.cursor()
            sql = 'update admin_login set password=%s where username=%s'
            cur.execute(sql,(request.form['pwd'], session['logged_admin']))
            db.commit()
            db.close()
            flash('修改密码成功，请重新登录')
            session.pop('logged_admin',None)
            return render_template('login.html')
        else :
            flash('两次密码不相等，请重新输入')
            return render_template('pwda.html')
    return render_template('pwda.html')

@app.route('/loginout', methods=['GET','POST'])
def loginout():
    flash('登出成功！')
    session.pop('logged_th',None)
    session.pop('logged_th_id',None)
    return render_template('login.html')

@app.route('/loginout2', methods=['GET','POST'])
def loginout2():
    flash('登出成功！')
    session.pop('logged_st',None)
    session.pop('logged_st_id',None)
    return render_template('login.html')     

# 显示管理员首页的函数，可以显示首页里的信息
@app.route('/admin_index', methods=['GET'])
def admin_index():
    return render_template('admin_index.html', name=session['logged_admin'])

# 显示教师首页的函数，可以显示首页里的信息
@app.route('/teacher_index', methods=['GET'])
def teacher_index():
    return render_template('teacher_index.html', name=session['logged_th'])

# 显示学生首页的函数，可以显示首页里的信息
@app.route('/student_index', methods=['GET'])
def student_index():
    return render_template('student_index.html', name=session['logged_st'])


@app.route('/classroom_stu', methods=['GET','POST'])
def classroom_stu():
    if not session.get('logged_st'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    error = None
    # 调用数据库函数，获取数据
    db = connect_db()
    cur = db.cursor()

    id = session['logged_st_id']
    sql = 'select * from course_arrange where course_name in (select course_name from grade where student_id=%s)'
    cur.execute(sql, (id))
    data=cur.fetchall()
    db.commit()
    db.close()

    # 用列表的格式存放全部数据

    title={
        'a':'课程名称',
        'b':'上课地点',
        'c':'上课时间',
    }
    url='classroom'
    path="/classroom"
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        posts.append(dict_data)
    if request.method=='POST':
        if request.form['test']=='delete':
            db = connect_db()
            cur = db.cursor()
            sql = 'delete from course_arrange where coursename = %s'
            cur.execute(sql,(request.form['aaa']))
            db.commit()
            db.close()
            flash('删除成功！')
        # 搜索
        if request.form['test']=='search':
            db = connect_db()
            cur = db.cursor()
            sql='select * from course_arrange where course_name = %s'
            s = cur.execute(sql,(request.form['bbb']))
            if s != 0:
                z=cur.fetchmany(s)
                posts = []
                for value in data:
                    dict_data = {}
                    dict_data['a'] = value[0]
                    dict_data['b'] = value[1]
                    dict_data['c'] = value[2]
                    posts.append(dict_data)
            else:
                flash('未查询到...')
        return redirect(url_for('classroom'))

    return render_template('student.html', posts=posts,title=title,path=path,url=url)

# 显示课程的函数页面
@app.route('/course_stu', methods=['GET','POST'])
def course_stu():
    if not session.get('logged_st'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    url='course_stu'
    path="/course_stu"
    # 调用数据库函数，获取数据
    db = connect_db()
    cur = db.cursor()
    sql = 'select course.course_name, course_exam from course, grade where student_id = %s and course.course_name=grade.course_name'
    cur.execute(sql, (session['logged_st_id']))
    data = cur.fetchall()
    db.commit()
    db.close()

    title={
        'a':'课程名称',
        'b':'考核方式',
        # 'c':'考核方式',
    }
    # 用列表的格式存放全部数据
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        posts.append(dict_data)
    if request.method=='POST':
        # 搜索
        if request.form['test']=='search':
            db = connect_db()
            cur = db.cursor()
            sql='select * from course where course_name = %s'
            s = cur.execute(sql,(request.form['bbb']))
            if s != 0:
                z=cur.fetchmany(s)
                posts = []
                for value in data:
                    dict_data = {}
                    dict_data['a'] = value[0]
                    dict_data['b'] = value[1]
                    posts.append(dict_data)
            else:
                flash('未查询到...')
        return redirect(url_for('course'))
    # print posts
    return render_template('student.html', posts=posts,title=title, path=path, url=url)

# 学生成绩显示的界面
@app.route('/score', methods=['GET','POST'])
def score():
    if not session.get('logged_st'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    url='score'
    path="/score"
    # 调用数据库函数，获取数据
    db = connect_db()
    cur = db.cursor()
    sql = 'select id from student where name = %s'
    cur.execute(sql, (session['logged_st']))
    id = cur.fetchone()[0]
    print(id)
    sql = 'select course_name, student_score from grade where student_id=%s'
    cur.execute(sql, (id))
    data=cur.fetchall()
    print(data)
    db.commit()
    db.close()

    title={
        'a':'课程名称',
        'b':'学生姓名',
        'c':'考试成绩',
    }
    # 用列表的格式存放全部数据
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = session['logged_st']
        dict_data['c'] = value[1]
        posts.append(dict_data)
    if request.method=='POST':
        # 搜索
        if request.form['test']=='search':
            db = connect_db()
            cur = db.cursor()
            sql='select course_name, student_score from grade where course_name = %s'
            s = cur.execute(sql,(request.form['bbb']))
            if s != 0:
                z=cur.fetchmany(s)
                posts = []
                for value in data:
                    dict_data = {}
                    dict_data['a'] = value[0]
                    dict_data['b'] = session['logged_st']
                    dict_data['c'] = value[1]
                    posts.append(dict_data)
            else:
                flash('未查询到...')
        return redirect(url_for('score'))
    # print posts
    return render_template('student.html', posts=posts,title=title, path=path, url=url)

# 显示教室信息的函数，当有请求发生时，去数据库里查找对应的数据，
# 然后将数据的格式用for循环进行遍历，变成列表的格式，然后返回到页面中，
# 再由页面进行显示数据
@app.route('/classroom', methods=['GET','POST'])
def classroom():
    if not session.get('logged_th'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    error = None
    # 调用数据库函数，获取数据
    db = connect_db()
    cur = db.cursor()
    sql = 'select id from teacher where name = %s'
    cur.execute(sql, (session['logged_th']))
    id = cur.fetchone()[0]
    sql = 'select * from course_arrange where course_name in (select course_name from course where teacher_id=%s)'
    cur.execute(sql, (id))
    data=cur.fetchall()
    db.commit()
    db.close()

    # 用列表的格式存放全部数据

    title={
        'a':'课程名称',
        'b':'上课地点',
        'c':'上课时间',
    }
    url='classroom'
    path="/classroom"
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        posts.append(dict_data)
    if request.method=='POST':
        if request.form['test']=='delete':
            db = connect_db()
            cur = db.cursor()
            sql = 'delete from course_arrange where coursename = %s'
            cur.execute(sql,(request.form['aaa']))
            db.commit()
            db.close()
            flash('删除成功！')
        # 搜索
        if request.form['test']=='search':
            db = connect_db()
            cur = db.cursor()
            sql='select * from course_arrange where course_name = %s'
            s = cur.execute(sql,(request.form['bbb']))
            if s != 0:
                z=cur.fetchmany(s)
                posts = []
                for value in data:
                    dict_data = {}
                    dict_data['a'] = value[0]
                    dict_data['b'] = value[1]
                    dict_data['c'] = value[2]
                    posts.append(dict_data)
            else:
                flash('未查询到...')
        return redirect(url_for('classroom'))
    return render_template('teacher.html', posts=posts,title=title,path=path,url=url)

# 显示课程的函数页面
@app.route('/course', methods=['GET','POST'])
def course():
    if not session.get('logged_th'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    url='course'
    path="/course"
    # 调用数据库函数，获取数据
    db = connect_db()
    cur = db.cursor()
    sql = 'select id from teacher where name = %s'
    cur.execute(sql, (session['logged_th']))
    id = cur.fetchone()[0]
    sql = 'select course_name, course_exam from course where teacher_id=%s'
    cur.execute(sql, (id))
    data=cur.fetchall()
    db.commit()
    db.close()

    title={
        'a':'课程名称',
        'b':'任课老师',
        'c':'考核方式',
    }
    # 用列表的格式存放全部数据
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = session['logged_th']
        dict_data['c'] = value[1]
        posts.append(dict_data)
    if request.method=='POST':
        if request.form['test']=='delete':
            db = connect_db()
            cur = db.cursor()
            sql = 'delete from course_arrange where coursename = %s'
            cur.execute(sql,(request.form['aaa']))
            db.commit()
            db.close()
            flash('删除成功！')
        # 搜索
        if request.form['test']=='search':
            db = connect_db()
            cur = db.cursor()
            sql='select * from course_arrange where course_name = %s'
            s = cur.execute(sql,(request.form['bbb']))
            if s != 0:
                z=cur.fetchmany(s)
                posts = []
                for value in data:
                    dict_data = {}
                    dict_data['a'] = value[0]
                    dict_data['b'] = session['logged_th']
                    dict_data['c'] = value[1]
                    posts.append(dict_data)
            else:
                flash('未查询到...')
        return redirect(url_for('course'))
    # print posts
    return render_template('teacher.html', posts=posts,title=title, path=path, url=url)

# 显示管理班的函数页面
@app.route('/guanliban', methods=['GET','POST'])
def guanliban():
    if not session.get('logged_admin'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    # 调用数据库函数，获取数据
    data = get_Table_Data('class')
    # 用列表的格式存放全部数据
    title={
        'a':'班级编号',
        'b':'专业',
        'c':'年级',
        'd':'班级名称'
    }
    path="/guanliban"
    url="guanliban"
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        posts.append(dict_data)
    if request.method=='POST':
        if request.form['test']=='delete':
            db = connect_db()
            cur = db.cursor()
            sql = 'delete from class where id = %s '
            cur.execute(sql,(request.form['aaa']))
            db.commit()
            db.close()
            flash('删除成功！')
        if request.form['test']=='search':
            db = connect_db()
            cur = db.cursor()
            sql='select * from class where specialities = %s'
            s=cur.execute(sql,(request.form['bbb']))
            if s!=0:
                z=cur.fetchmany(s)
                print(z)
                posts = []
                for value in z:
                    dict_data = {}
                    dict_data['a'] = value[0]
                    dict_data['b'] = value[1]
                    dict_data['c'] = value[2]
                    dict_data['d'] = value[3]
                    posts.append(dict_data)
            else:
                flash('未查询到...')
        # return redirect(url_for('guanliban'))
    print(posts)
    return render_template('admin.html', posts=posts,title=title,path=path,url=url)

# 显示学生成绩页面
@app.route('/jxjh', methods=['GET','POST'])
def jxjh():
    if not session.get('logged_admin'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    # 调用数据库函数，获取数据
    db = connect_db()
    cur = db.cursor()
    sql='select course_name, name, course_exam from course, teacher where course.teacher_id = teacher.id'
    s=cur.execute(sql)
    data=cur.fetchmany(s)
    # 用列表的格式存放全部数据
    title={
        'a':'课程名称',
        'b':'任课老师',
        'c':'考核方式',
    }
    path="/jxjh"
    url="jxjh"
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        posts.append(dict_data)
    if request.method=='POST':
        db = connect_db()
        cur = db.cursor()
        sql='select course_name, name, course_exam from course, teacher where course.teacher_id = teacher.id and course_name = %s'
        s=cur.execute(sql,(request.form['bbb']))
        if s!=0:
            z=cur.fetchmany(s)
            posts = []
            for value in z:
                dict_data = {}
                dict_data['a'] = value[0]
                dict_data['b'] = value[1]
                dict_data['c'] = value[2]
                # dict_data['学生成绩'] = value[3]
                posts.append(dict_data)
        else:
            flash('未查询到...')
    # print posts
    return render_template('admin.html', posts=posts,title=title,path=path,url=url)

# 显示排课信息的函数页面
@app.route('/paike_js', methods=['GET','POST'])
def paike_js():
    if not session.get('logged_admin'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    # 调用数据库函数，获取数据
    data = get_Table_Data('course_arrange')
    # 用列表的格式存放全部数据
    title={
        'a':'课程名称',
        'b':'课程教室',
        'c':'课程时间'
    }
    path="/paike_js"
    url="paike_js"
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        posts.append(dict_data)
    if request.method=='POST':
        if request.form['test']=='delete':
            db = connect_db()
            cur = db.cursor()
            sql = 'delete from course_arrange where course_name = %s'
            cur.execute(sql,(request.form['aaa']))
            db.commit()
            db.close()
            flash('删除成功！')
        if request.form['test']=='search':
            db = connect_db()
            cur = db.cursor()
            sql='select * from course_arrange where course_name = %s'
            s=cur.execute(sql,(request.form['bbb']))
            if s !=0:
                z=cur.fetchmany(s)
                posts = []
                for value in z:
                    dict_data = {}
                    dict_data['a'] = value[0]
                    dict_data['b'] = value[1]
                    dict_data['c'] = value[2]
                    posts.append(dict_data)
            else:
                flash('未查询到...')
        return redirect(url_for('paike_js'))
    # print posts
    return render_template('admin.html', posts=posts,title=title,path=path,url=url)

# 显示学生成绩的页面，包括调用学生成绩数据表
@app.route('/xscj', methods=['GET','POST'])
def xscj():
    if not session.get('logged_admin'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    # 调用数据库函数，获取数据
    data = get_Table_Data('grade')
    # 用列表的格式存放全部数据
    title={
        'a':'学生学号',
        'b':'课程名称',
        'c':'学生成绩'
    }
    path="/xscj"
    url="xscj"
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        # dict_data['d'] = value[3]
        posts.append(dict_data)
    if request.method=='POST':
        if request.form['test']=='delete':
            db = connect_db()
            cur = db.cursor()
            sql = 'delete from grade where course_name = %s'
            cur.execute(sql,(request.form['aaa']))
            db.commit()
            db.close()
            flash('删除成功！')
        if request.form['test']=='search':
           db = connect_db()
           cur = db.cursor()
           sql='select * from grade where course_name = %s'
           s=cur.execute(sql,(request.form['bbb']))
           if s!=0:
               z=cur.fetchmany(s)
               posts1 = []
               for value in z:
                   dict_data = {}
                   dict_data['a'] = value[0]
                   # dict_data['学生姓名'] = value[1]
                   dict_data['b'] = value[1]
                   dict_data['c'] = value[2]
                   posts.append(dict_data)
           else:
               flash('未查询到...')
        return redirect(url_for('xscj'))
    # print posts
    return render_template('admin.html',posts=posts,title=title,path=path,url=url)

# 显示学生类别的页面，包括调用学生成绩数据表
@app.route('/xslb', methods=['GET','POST'])
def xslb():
    if not session.get('logged_admin'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    # 调用数据库函数，获取数据
    data = get_Table_Data('student')
    # 用列表的格式存放全部数据
    title={
        'a':'学生姓名',
        'b':'学生学号',
        # 'c':'学生专业',
        'c':'学生班级'
    }
    path="/xslb"
    url="xslb"
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        # dict_data['d'] = value[3]
        posts.append(dict_data)
    if request.method=='POST':
        if request.form['test']=='delete':
            db = connect_db()
            cur = db.cursor()
            sql = 'delete from student where name = %s'
            cur.execute(sql,(request.form['aaa']))
            db.commit()
            db.close()
            flash('删除成功！')
        if request.form['test']=='search':
          db = connect_db()
          cur = db.cursor()
          sql='select * from student where name = %s'
          s=cur.execute(sql,(request.form['bbb']))
          if s!=0:
              z=cur.fetchmany(s)
              posts = []
              for value in z:
                  dict_data = {}
                  dict_data['a'] = value[0]
                  dict_data['b'] = value[1]
                  # dict_data['学生专业'] = value[2]
                  dict_data['c'] = value[3]
                  posts.append(dict_data)
              flash(posts)
          else:
              flash('未查询到...')
        return redirect(url_for('xslb'))
    # print posts
    return render_template('admin.html', posts=posts,title=title,path=path,url=url)

@app.route('/add_jxjh', methods=['POST','GET'])
def add_jxjh():
    if not session.get('logged_admin'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    error = None
    titile={
        'a':'课程名称:',
        'b':'老师工号:',
        'c':'考核方式:',
        'add':'jxjh'
    }
    db = connect_db()
    cur = db.cursor()
    sql='insert into course(course_name,teacher_id,course_exam)VALUES(%s,%s,%s)'
    if request.method == 'POST':
        try:
            cur.execute(sql,(request.form['course_name'],request.form['teacher_id'],request.form['course_exam']))
        except pymysql.IntegrityError:
            flash("无该老师信息，请重新输入")
            redirect(url_for('jxjh'))
        db.commit()
        db.close()
        flash('添加成功！')
        redirect(url_for('jxjh'))

    return render_template('add.html',titile=titile)

@app.route('/add_guanliban', methods=['POST','GET'])
def add_guanliban():
    if not session.get('logged_admin'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    error = None
    titile={
        'a':'班级编号',
        'b':'专业:',
        'c':'年级:',
        'd':'班级名称:',
        'add':'guanliban'
    }
    db = connect_db()
    cur = db.cursor()
    sql='insert into class(id, specialities,grade,class)VALUES(%s,%s,%s,%s)'
    if request.method == 'POST':
        cur.execute(sql,(request.form['id'], request.form['specialities'],request.form['grade'],request.form['class']))
        db.commit()
        db.close()
        flash('添加成功！')
        redirect(url_for('guanliban'))

    return render_template('add.html',titile=titile)

@app.route('/add_paike_js', methods=['POST','GET'])
def add_paike_js():
    if not session.get('logged_admin'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    error = None
    titile={
        'a':'课程名称:',
        'b':'课程教室:',
        'c':'课时时间:',
        'add':'paike_js'
    }
    db = connect_db()
    cur = db.cursor()
    sql='insert into course_arrange(course_name,course_classroom,course_time)VALUES(%s,%s,%s)'
    if request.method == 'POST':
        try:
            cur.execute(sql,(request.form['course_name'],request.form['course_classroom'],request.form['course_time']))
        except pymysql.IntegrityError:
            flash("系统内无该课程，无法排课，请重新输入")
            redirect(url_for('paike_js'))
        db.commit()
        db.close()
        flash('添加成功！')
        redirect(url_for('paike_js'))

    return render_template('add.html',titile=titile)

@app.route('/add_xscj', methods=['POST','GET'])
def add_xscj():
    if not session.get('logged_admin'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    error = None
    titile={
        'a':'学生学号',
        'b':'课程名称',
        'c':'学生成绩',
        'add':'xscj'
    }
    db = connect_db()
    cur = db.cursor()
    sql='insert into grade(student_id, course_name, student_score)VALUES(%s,%s,%s)'
    if request.method == 'POST':
        try:
            cur.execute(sql,(request.form['student_id'],request.form['course_name'],request.form['student_score']))
        except pymysql.IntegrityError:
            flash("请确认课程、学生是否存在或成绩是否已添加")
            redirect(url_for('xscj'))
        db.commit()
        db.close()
        flash('添加成功！')
        redirect(url_for('xscj'))

    return render_template('add.html',titile=titile)

@app.route('/add_xslb', methods=['POST','GET'])
def add_xslb():
    if not session.get('logged_admin'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    error = None
    titile={
        'a':'学生姓名:',
        'b':'学生学号:',
        'c':'学生班级:',
        'add':'xslb'
    }
    db = connect_db()
    cur = db.cursor()
    sql='insert into student(name,id,class_id)VALUES(%s,%s,%s)'
    if request.method == 'POST':
        try:
            cur.execute(sql,(request.form['name'],request.form['id'],request.form['class_id'],request.form['class']))
        except pymysql.IntegrityError:
            flash("无该班级信息，请重新输入")
            redirect(url_for('xslb'))
        db.commit()
        db.close()
        flash('添加成功!')
        redirect(url_for('xslb'))

    return render_template('add.html',titile=titile)


# 主函数
if __name__ == '__main__':
    app.debug = True
    app.run()