# 🎓 Job Portal System with Student & Company Login
# Now includes: View Applied Jobs (Student) + View Applicants (Company)

class Job:
    def __init__(self, title, required_skills, description, company):
        self.title = title
        self.required_skills = required_skills
        self.description = description
        self.company = company
        self.applicants = []  # students who applied

    def __str__(self):
        return f"Job Title: {self.title}\nSkills Required: {', '.join(self.required_skills)}\nDescription: {self.description}\n"


class Company:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.jobs = []
        self.logged_in = False

    def login(self, password):
        if self.password == password:
            self.logged_in = True
            print(f"🔓 Company {self.name} logged in successfully!")
        else:
            print("❌ Incorrect password!")

    def post_job(self, job):
        if self.logged_in:
            self.jobs.append(job)
            print(f"✅ {self.name} posted a new job: {job.title}")
        else:
            print("❌ Please login first!")

    def view_applicants(self):
        if not self.logged_in:
            print("❌ Please login first!")
            return
        print(f"\n📋 Applicants for {self.name}:")
        if not self.jobs:
            print("📭 No jobs posted yet.")
            return
        for job in self.jobs:
            print(f"\n📝 Job: {job.title}")
            if not job.applicants:
                print("   No applicants yet.")
            else:
                for student in job.applicants:
                    print(f"   - {student.name} (Skills: {', '.join(student.skills)})")


class Student:
    def __init__(self, name, password, skills):
        self.name = name
        self.password = password
        self.skills = skills
        self.applied_jobs = []  # store (job, company)
        self.logged_in = False

    def login(self, password):
        if self.password == password:
            self.logged_in = True
            print(f"🔓 Student {self.name} logged in successfully!")
        else:
            print("❌ Incorrect password!")

    def add_skill(self, skill):
        if self.logged_in:
            self.skills.append(skill)
            print(f"🆕 {self.name} learned a new skill: {skill}")
        else:
            print("❌ Please login first!")

    def apply_job(self, job):
        if not self.logged_in:
            print("❌ Please login first!")
            return

        if all(skill in self.skills for skill in job.required_skills):
            self.applied_jobs.append((job, job.company))
            job.applicants.append(self)  # add student to job applicants
            print(f"🎉 {self.name} successfully applied for {job.title} at {job.company.name}")
        else:
            print(f"❌ {self.name} does not match skills for {job.title}")

    def view_applied_jobs(self):
        if not self.logged_in:
            print("❌ Please login first!")
            return
        if not self.applied_jobs:
            print(f"📭 {self.name} has not applied for any jobs yet.")
        else:
            print(f"\n📌 {self.name}'s Applied Jobs:")
            for job, company in self.applied_jobs:
                print(f"- {job.title} at {company.name}")


class JobPortal:
    def __init__(self):
        self.students = []
        self.companies = []

    def add_student(self, student):
        self.students.append(student)

    def add_company(self, company):
        self.companies.append(company)

    def show_all_jobs(self):
        print("\n📌 Available Jobs in Portal:")
        for company in self.companies:
            for idx, job in enumerate(company.jobs, start=1):
                print(f"[{idx}] 🏢 {company.name} → {job}")


# ------------------ MENU SYSTEM ------------------

def main():
    portal = JobPortal()

    while True:
        print("\n========== JOB PORTAL ==========")
        print("1. Register Student")
        print("2. Register Company")
        print("3. Student Login")
        print("4. Company Login")
        print("5. Post Job (Company)")
        print("6. Show All Jobs")
        print("7. Student Apply for Job")
        print("8. Add Skill to Student")
        print("9. View Applied Jobs (Student)")
        print("10. View Applicants (Company)")
        print("0. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter student name: ")
            password = input("Set password: ")
            skills = input("Enter skills (comma separated): ").split(",")
            student = Student(name, password, [s.strip() for s in skills])
            portal.add_student(student)
            print(f"✅ Student {name} registered successfully!")

        elif choice == "2":
            name = input("Enter company name: ")
            password = input("Set password: ")
            company = Company(name, password)
            portal.add_company(company)
            print(f"✅ Company {name} registered successfully!")

        elif choice == "3":
            sname = input("Enter student name: ")
            password = input("Enter password: ")
            student = next((s for s in portal.students if s.name == sname), None)
            if student:
                student.login(password)
            else:
                print("❌ Student not found!")

        elif choice == "4":
            cname = input("Enter company name: ")
            password = input("Enter password: ")
            company = next((c for c in portal.companies if c.name == cname), None)
            if company:
                company.login(password)
            else:
                print("❌ Company not found!")

        elif choice == "5":
            cname = input("Enter company name: ")
            company = next((c for c in portal.companies if c.name == cname), None)
            if company:
                if company.logged_in:
                    title = input("Enter job title: ")
                    skills = input("Enter required skills (comma separated): ").split(",")
                    desc = input("Enter job description: ")
                    job = Job(title, [s.strip() for s in skills], desc, company)
                    company.post_job(job)
                else:
                    print("❌ Please login first!")
            else:
                print("❌ Company not found!")

        elif choice == "6":
            portal.show_all_jobs()

        elif choice == "7":
            sname = input("Enter student name: ")
            student = next((s for s in portal.students if s.name == sname), None)
            if not student:
                print("❌ Student not found!")
                continue

            cname = input("Enter company name: ")
            company = next((c for c in portal.companies if c.name == cname), None)
            if not company:
                print("❌ Company not found!")
                continue

            for idx, job in enumerate(company.jobs, start=1):
                print(f"{idx}. {job.title} (Skills: {', '.join(job.required_skills)})")
            job_choice = int(input("Enter job number to apply: "))
            if 1 <= job_choice <= len(company.jobs):
                student.apply_job(company.jobs[job_choice - 1])
            else:
                print("❌ Invalid job selection!")

        elif choice == "8":
            sname = input("Enter student name: ")
            student = next((s for s in portal.students if s.name == sname), None)
            if student:
                skill = input("Enter new skill: ")
                student.add_skill(skill)
            else:
                print("❌ Student not found!")

        elif choice == "9":
            sname = input("Enter student name: ")
            student = next((s for s in portal.students if s.name == sname), None)
            if student:
                student.view_applied_jobs()
            else:
                print("❌ Student not found!")

        elif choice == "10":
            cname = input("Enter company name: ")
            company = next((c for c in portal.companies if c.name == cname), None)
            if company:
                company.view_applicants()
            else:
                print("❌ Company not found!")

        elif choice == "0":
            print("👋 Exiting Job Portal. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Try again.")


# Run the program
if __name__ == "__main__":
    main()