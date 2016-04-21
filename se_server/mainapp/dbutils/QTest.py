skills=["JavaScript","C#","PHP"]

class Question:
    def __init__(self,skill,question,choices,correct):
        self.skill=skill
        self.question=question
        self.choices=choices
        self.correct=correct
import csv
with open("mainapp/dbutils/questionnaire.csv",encoding="UTF-8",errors="ignore") as csvfile:
    reader=csv.reader(csvfile)
    next(reader)
    count=0
    questions=[]
    for row in reader:
        if(count==10):
            break
        if(row[0] in skills):
            questions.append(Question(row[0],row[1],[row[2],row[3],row[4],row[5]],row[6]))
            count+=1
