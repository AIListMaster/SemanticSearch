import pandas as pd

# Load the User and Skills data
users_df = pd.read_csv('user_table_live.csv')
skills_df = pd.read_csv('skill_table_live.csv')
project_eng_df = pd.read_csv('project_eng_table_live.csv')

# Fill NaN values in 'Skill Name' and 'Competence Level' with an empty string
skills_df['Skill Name'] = skills_df['Skill Name'].fillna('')
skills_df['Competence Level'] = skills_df['Competence Level'].fillna('')

# Merge skills into a single string per user
skills_df['Skill'] = skills_df['Skill Name'] + ' with competence level ' + skills_df['Competence Level']
skills_merged = skills_df.groupby('User ID')['Skill'].apply(lambda x: ', '.join(x)).reset_index()

# Fill NaN values with an empty string in project engagement table.
project_eng_df['End Date'] = project_eng_df['End Date'].fillna('')
project_eng_df['Start Date'] = project_eng_df['Start Date'].fillna('')
project_eng_df['Project Responsibilities'] = project_eng_df['Project Responsibilities'].fillna('')

# Merge text column to single column
project_eng_df['Project Name'] = (project_eng_df['Project Name'] + ' as ' +
                                  project_eng_df['Role Performed'] + ' from ' +
                                  project_eng_df['Start Date'] + ' to ' +
                                  project_eng_df['End Date'])
project_eng_merged = project_eng_df.groupby('User ID')['Project Name'].apply(lambda x: ', '.join(x)).reset_index()

# Merge the users data with the aggregated skills data
merged_df = pd.merge(users_df, skills_merged, on='User ID', how='left')
merged_df = pd.merge(merged_df, project_eng_merged, on='User ID', how='left')

# Fill NaN values in 'Skill' column with an empty string
merged_df['Skill'] = merged_df['Skill'].fillna('')

# Rename the 'Skill' column to 'Skills'
merged_df.rename(columns={'Skill': 'Skills'}, inplace=True)

# Rename the 'Project Name' column to 'Project_Engagements'
merged_df.rename(columns={'Project Name': 'Project_Engagements'}, inplace=True)

# Save the merged dataframe to a new CSV file
merged_df.to_csv('merged_tables_live.csv', index=False)

print("Merged CSV file created successfully.")
