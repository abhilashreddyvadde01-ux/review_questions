#csv file opening and loading data into a list
file = open("courses.csv", "r")
content = file.readlines()
content.pop(0)
from datetime import datetime
#errorlog creation
errors = open("errors.txt", "w")
course_fee_report = open("course_fee_report.csv", 'w')
today = datetime.today().date()
rejected_count = 0
accepted_count = 0
#classes creation
class Course:
    def __init__(self, CourseID, CourseName, CourseType, BaseFee, CourseAdjustmentFee, OfferDiscountPercent, OfferEndDate, OfferStatus, OfferDiscountAmount, FinalFee):
        self.CourseID = CourseID
        self.CourseName = CourseName
        self.CourseType = CourseType
        self.BaseFee = BaseFee
        self.CourseAdjustmentFee = CourseAdjustmentFee
        self.OfferDiscountPercent = OfferDiscountPercent
        self.OfferEndDate = OfferEndDate
        self.OfferStatus = OfferStatus
        self.OfferDiscountAmount = OfferDiscountAmount
        self.FinalFee = FinalFee

    def common_fee(self):
        pass

class ClassroomCourse(Course):
    def __init__(self, CourseID, CourseName, CourseType, BaseFee, CourseAdjustmentFee, OfferDiscountPercent, OfferEndDate, OfferStatus, OfferDiscountAmount, FinalFee):
        super().__init__(CourseID, CourseName, CourseType, BaseFee, CourseAdjustmentFee, OfferDiscountPercent, OfferEndDate, OfferStatus, OfferDiscountAmount, FinalFee)

    def common_fee(self):
        self.CourseAdjustmentFee =  self.BaseFee + 2000

    def CalculateFinalFee(self):

        if today <= self.OfferEndDate:
            self.OfferStatus = 'WithOffer'
            self.OfferDiscountAmount = self.CourseAdjustmentFee * (self.OfferDiscountPercent/100)
            self.FinalFee = self.CourseAdjustmentFee - self.OfferDiscountAmount
    
        else:
            self.OfferStatus = 'WithoutOffer'
            self.OfferDiscountAmount = 0
            self.FinalFee = self.CourseAdjustmentFee

    def display_info(self):
        return f"CourseID = {self.CourseID}, CourseName = {self.CourseName}, CourseType = {self.CourseType}, BaseFee = {self.BaseFee}, CourseAdjustmentFee = {self.CourseAdjustmentFee}, OfferDiscountPercent = {self.OfferDiscountPercent}, OfferEndDate = {self.OfferEndDate}, OfferStatus = {self.OfferStatus}, OfferDiscountAmount = {self.OfferDiscountAmount}, FinalFee = {self.FinalFee}"
    
class OnlineCourse(Course):
    def __init__(self, CourseID, CourseName, CourseType, BaseFee, CourseAdjustmentFee, OfferDiscountPercent, OfferEndDate, OfferStatus, OfferDiscountAmount, FinalFee):
        super().__init__(CourseID, CourseName, CourseType, BaseFee, CourseAdjustmentFee, OfferDiscountPercent, OfferEndDate, OfferStatus, OfferDiscountAmount, FinalFee)
        

    def common_fee(self):
        self.CourseAdjustmentFee =  self.BaseFee * 0.9

    def CalculateFinalFee(self):
    
        if today <= self.OfferEndDate:
            self.OfferStatus = 'WithOffer'
            self.OfferDiscountAmount = self.CourseAdjustmentFee * (self.OfferDiscountPercent/100)
            self.FinalFee = self.CourseAdjustmentFee - self.OfferDiscountAmount

        else:
            self.OfferStatus = 'WithoutOffer'
            self.OfferDiscountAmount = 0
            self.FinalFee = self.CourseAdjustmentFee

    def display_info(self):
        return f"CourseID = {self.CourseID}, CourseName = {self.CourseName}, CourseType = {self.CourseType}, BaseFee = {self.BaseFee}, CourseAdjustmentFee = {self.CourseAdjustmentFee}, OfferDiscountPercent = {self.OfferDiscountPercent}, OfferEndDate = {self.OfferEndDate}, OfferStatus = {self.OfferStatus}, OfferDiscountAmount = {self.OfferDiscountAmount}, FinalFee = {self.FinalFee}"

#iterating content list to create objects and save them

courseIDs = []
courseList = []
for courses in content:
    course = courses.strip().split(',')

    try:
        if len(course) != 6:
            raise Exception("No sufficent fields are provided.")
        for item in course:
            if item == '':
                raise Exception("Something in the required fields is empty.")
        if course[0] in courseIDs:
            raise Exception("Cannot have same Course ID's for two courses")  
        if course[3].isdigit():
            if float(course[3]) < 0:
                raise Exception("Basefee cannot be negative.")
        else:
            raise Exception("Basefee cannot be non-numeric or negative.")
        if course[4].isdigit():
            if float(course[4]) < 0 or float(course[4]) > 100:
                raise Exception("Discount should be in range of 0 to 100.")
        else:
            raise Exception("Discount cannot be non-numeric or negative.")
        try:
            end_date = datetime.strptime(course[5], "%Y-%m-%d").date()
        except ValueError:
            raise Exception("OfferEndDate is not a valid date (expected YYYY-MM-DD).")

        if course[2] == 'Online':
            courseList.append(OnlineCourse(CourseID = course[0], CourseName = course[1], CourseType = course[2], BaseFee = float(course[3]), CourseAdjustmentFee = 0, OfferDiscountPercent = float(course[4]), OfferEndDate = end_date, OfferStatus = '', OfferDiscountAmount = 0, FinalFee = 0))
        elif course[2] == 'Classroom':
            courseList.append(ClassroomCourse(CourseID = course[0], CourseName = course[1], CourseType = course[2], BaseFee = float(course[3]), CourseAdjustmentFee = 0, OfferDiscountPercent = float(course[4]), OfferEndDate = end_date, OfferStatus = '', OfferDiscountAmount = 0, FinalFee = 0))
        else:
            raise Exception("Invalid mode of coursework.")
        courseIDs.append(course[0])
    except Exception as e:
        rejected_count += 1
        errors.write(",".join(course) + ' '  + str(e) + '\n')
    

#Calculating final price 
total = 0
for courseObj in courseList:
    courseObj.common_fee()
    courseObj.CalculateFinalFee()
    course_fee_report.write(courseObj.display_info() + '\n')
    total += courseObj.FinalFee
    accepted_count += 1
errors.close()
file.close()
course_fee_report.close()
print(f"The total number of accepted courses: {accepted_count}")
print(f"The total number of rejected courses; {rejected_count}")
print(f"The total final fee of all valid courses: {total}")