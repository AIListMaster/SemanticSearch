import csv


def convert_csv_to_sentences(csv_file):
    sentences = []

    with open(csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            user_id = row['User ID']
            email = row['Email']
            name = row['Name']
            full_name = row['Full Name']
            city = row['City']
            designation = row['Designation']
            department = row['Department']
            career_highlights = row['Career Highlights']
            introduction = row['Introduction']
            skills = row['Skills']
            project_engagements = row['Project_Engagements']

            sentence = f"{full_name}, based in {city}, is a {designation} in the {department} department. You can reach them at {email}."

            if skills:
                skills_list = skills.split(', ')
                skill_sentence = " They have the following skills: " + ", ".join(skills_list) + "."
                sentence += skill_sentence

            if project_engagements:
                projects = project_engagements.split('\n')
                project_sentences = []
                for project in projects:
                    project_details = project.split('|')
                    if len(project_details) >= 4:
                        project_name, role, start_date, end_date, description = project_details
                        project_sentence = f" They worked on the {project_name} project as a {role} from {start_date} to {end_date}, where they {description.lower()}."
                        project_sentences.append(project_sentence)
                if project_sentences:
                    sentence += " ".join(project_sentences)

            sentences.append(sentence)

    return sentences


# Path to the CSV file
csv_file = 'data.csv'

# Convert CSV to sentences
sentences = convert_csv_to_sentences(csv_file)

# Display the sentences
for sentence in sentences:
    print(sentence)
