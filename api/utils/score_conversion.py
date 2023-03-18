

def get_grade(score):
    
    if score <= 100 and score >= 70:
        return 'A'
    elif score < 70 and score >= 60:
        return 'B'
    elif score < 60 and score >= 50:
        return 'C'
    elif score < 50 and score >= 45:
        return 'D'
    elif score < 45 and score >= 40:
        return 'E' 
    else:
        return 'F'


def grade_to_gpa(grade):
   
    if grade == 'A':
        return 4.0
    elif grade == 'B':
        return 3.3
    elif grade == 'C':
        return 2.3
    elif grade == 'D':
        return 1.3
    else:
        return 0.0
