import webbrowser

first = "Riya"
last = "Devaliya"
age = 21

subjects = {}
for i in range(3):
    subject = input(f"Enter subject {i+1} name: ")
    marks = input(f"Enter marks in {subject}: ")
    subjects[subject] = marks

html2 = """
<html>
  <body>
    <h2>Student Profile</h2>
    <p>First Name: {}</p>
    <p>Last Name: {}</p>
    <p>Age: {}</p>
    <ul>
      {}
    </ul>
  </body>
</html>
""".format(
    first,
    last,
    age,
    '\n'.join(['<li>{}: {}</li>'.format(sub, mark) for sub, mark in subjects.items()])
)

with open("student_profile.html", "w", encoding="utf-8") as f:
    f.write(html2)

webbrowser.open("student_profile.html")
