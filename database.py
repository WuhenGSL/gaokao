from models import db, User, School


class UserDBManager:
    def add_user(self, name, email, gender, rank, score, password, subject1, subject2, subject3):
        # 添加用户到 User 数据库
        new_user = User(name=name, email=email, gender=gender, rank=rank, score=score,
                        password=password, subject1=subject1, subject2=subject2, subject3=subject3)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_user_by_id(self, user_id):
        # 根据用户 ID 查询用户
        return User.query.get_or_404(user_id)

    def get_user_by_email(self, email):
        # 根据邮箱查询用户
        return User.query.filter_by(email=email).first()

    def update_user(self, user_id, name=None, email=None, gender=None, rank=None, preference=None, password=None):
        # 更新用户信息
        user = self.get_user_by_id(user_id)
        if user:
            if name is not None:
                user.name = name
            if email is not None:
                user.email = email
            if gender is not None:
                user.gender = gender
            if rank is not None:
                user.rank = rank
            if preference is not None:
                user.preference = preference
            if password is not None:
                user.set_password(password)
            db.session.commit()
            return True
        return False

    def delete_user(self, user_id):
        # 删除用户
        user = self.get_user_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False


class SchoolDBManager:
    def add_school(self, name, location, description):
        # 添加学校到 School 数据库
        new_school = School(name=name, location=location, description=description)
        db.session.add(new_school)
        db.session.commit()
        return new_school

    def get_school_by_id(self, school_id):
        # 根据学校 ID 查询学校
        return School.query.get(school_id)

    def get_school_by_name(self, name):
        # 根据学校名称查询学校
        return School.query.filter_by(name=name).first()

    def update_school(self, school_id, name=None, location=None, description=None):
        # 更新学校信息
        school = self.get_school_by_id(school_id)
        if school:
            if name is not None:
                school.name = name
            if location is not None:
                school.location = location
            if description is not None:
                school.description = description
            db.session.commit()
            return True
        return False

    def delete_school(self, school_id):
        # 删除学校
        school = self.get_school_by_id(school_id)
        if school:
            db.session.delete(school)
            db.session.commit()
            return True
        return False
