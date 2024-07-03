import pandas as pd
from app.util import preprocess_text

def convert_csv_to_sentences(csv_file, output_file):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Create an empty list to store the sentences
    sentences = []

    for _, row in df.iterrows():
        email = row['Email']
        full_name = row['Full Name']
        city = row['City']
        designation = row['Designation']
        department = row['Department']
        skills = row['Skills']
        certifications = row['Certification']
        project_engagements = row['Project_Engagements']

        sentence = f"{full_name}, based in {city}, is a {designation} in the {department} department. You can reach him/her at {email}."

        if pd.notna(skills):
            skills_list = skills.split(', ')
            skill_sentence = " He has the following skills: " + ", ".join(skills_list) + "."
            sentence += skill_sentence

        if pd.notna(certifications):
            certifications_list = certifications.split(', ')
            certifications_sentence = " He has completed the following certifications: " + ", ".join(certifications_list) + "."
            sentence += certifications_sentence

        if pd.notna(project_engagements):
            project_engagements_list = project_engagements.split(', ')
            project_sentence = " He worked on the " + ", ".join(project_engagements_list) + "."
            sentence += project_sentence

        sentences.append(preprocess_text(sentence))

    # Add the sentences as a new column in the DataFrame
    df['combined_text'] = sentences

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)


# Path to the input and output CSV files
input_csv_file = 'merged_tables_live.csv'
output_csv_file = 'merged_tables_live.csv'

# Convert CSV to sentences and save the updated DataFrame
convert_csv_to_sentences(input_csv_file, output_csv_file)
