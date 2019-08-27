from app import db

class EmployeeModel (db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    fullname= db.Column(db.String(), nullable=False)
    gender=db.Column(db.String(), nullable=False)
    email=db.Column(db.String(), nullable=False)
    phonenumber=db.Column(db.String(), nullable=False, unique=True)
    idnumber=db.Column(db.String(), nullable=False, unique=True)
    krapin=db.Column(db.String(), nullable=False)
    basicsalary=db.Column(db.Float(), nullable=False)
    benefits=db.Column(db.Float(), nullable=False)
    department=db.Column(db.Integer, db.ForeignKey('departments.id'))

# CREATE

    def create_record(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def check_idnumber_exists(cls,nid):
        record = cls.query.filter_by(idnumber=nid).first()

        if record:
            return True
        else:
       
            return False
     # fetch all employees
    @classmethod
    def fetch_all(cls):
        return  cls.query.all()

    #edit by id
    @classmethod
    def edit_employee_by_id (cls, id, fullname=None, gender=None,email=None, phonenumber=None,idnumber=None,krapin=None,department=None, basicsalary=None, benefits=None):
        record =cls.query.filter_by(id=id).first()

        if record:
            record.fullname=fullname
            record.gender=gender
            record.email=email
            record.phonenumber=phonenumber
            record.idnumber=idnumber
            record.krapin= krapin
            record.department= department
            record.basicsalary= basicsalary
            record.benefits= benefits
            db.session.commit()
            return True
        else:
            return False


#delete by id
    @classmethod
    def delete_by_id(cls, id):
        record = cls.query.filter_by(id=id)

        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False