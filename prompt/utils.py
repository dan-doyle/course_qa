import re

def extract_course_request_pairs(html_string):
    course_pattern = re.compile(r'<course>(.*?)</course>')
    request_pattern = re.compile(r'<request>(.*?)</request>')
    
    course_contents = course_pattern.findall(html_string)
    request_contents = request_pattern.findall(html_string)
    
    return list(zip(course_contents, request_contents))