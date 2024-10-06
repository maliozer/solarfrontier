import openai
from openai import OpenAI
import pyodbc
import os

# Set your OpenAI GPT API key
openai_api_key = os.getenv['YOURKEY']

def gpt_symptom_matching(user_input):
    # Generate a response using GPT-3.5
    client = OpenAI(api_key = openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {
                    "role": "system",
                    "content": """The Space Mission Advisor is an AI-powered assistant designed to optimize 
                     astronauts' performance during missions and ensure successful completion of their tasks. 
                     Its responsibilities include analyzing astronauts' characteristics, offering suggestions 
                     to improve memory, attention, and flexibility, and providing performance-enhancing guidance. 
                     The advisor addresses challenges astronauts face by offering solutions and contributing to 
                     their personal development. Additionally, it identifies weaknesses during missions and 
                     presents strategies to strengthen the astronauts' abilities. 
                     The advisor serves as a guide, understanding astronauts' psychological 
                     and cognitive needs to boost success and efficiency, while offering solutions 
                     to overcome challenges specific to space conditions."""
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
        max_tokens=100
    )
    
    # Extract symptoms from GPT-3.5 response

    print(response)

    if response.choices[0].message.content.lower() == 'Out of Context'.lower():
        print("Just nasa app challenge organization..!")
        return False
    
    gpt_symptoms = response.choices[0].message.content.split(', ')

    if len(set(gpt_symptoms)) < 3:
        return False
    return set(gpt_symptoms)

def gpt_symptom_analysis(diag_info):
    client = OpenAI(api_key = openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {
                    "role": "system",
                    "content": """The Space Mission Advisor is an AI-powered assistant designed to 
                     optimize astronauts' performance during missions and ensure successful completion 
                     of their tasks. Its responsibilities include analyzing astronauts' characteristics, 
                     offering suggestions to improve memory, attention, and flexibility, and providing 
                     performance-enhancing guidance. The advisor addresses challenges astronauts face 
                     by offering solutions and contributing to their personal development. 
                     Additionally, it identifies weaknesses during missions and presents strategies 
                     to strengthen the astronauts' abilities.he advisor serves as a guide, 
                     understanding astronauts' psychological and cognitive needs to boost success and 
                     efficiency, while offering solutions to overcome challenges specific to space conditions.' """
                },
                {
                    "role": "user",
                    "content": diag_info
                }
            ],
        max_tokens=1000
    )

    print(response.choices[0].message.content)

def get_diag_info(diagnosis,cursor):
    cursor.execute("SELECT TOP (1000) game_id, game_name, game_typeFROM nasaGame.dbo.game;", diagnosis)
    results = cursor.fetchall()

    print('diag analysis:\n')

    print(results)

    for row in results:
        print(f"Examination: {row.Examination}")
        print(f"DiagnosisDetails: {row.DiagnosisDetails}")
        print(f"Note: {row.Note}")
        print(f"Comment: {row.Comment}")
        print("\n")
    
    str = f"Diagnosis: {row.Diagnosis}, Examination: {row.Examination}, DiagnosisDetails: {row.DiagnosisDetails}, Note: {row.Note}, Comment: {row.Comment}"

    gpt_symptom_analysis(str)

def get_matching_diseases(user_symptoms, cursor):
    matching_diseases = []
    max_intersection = 0

    # Fetch diseases from the database
    cursor.execute("SELECT TOP (1000) game_id, game_name, game_typ FROM nasaGame.dbo.game;")
    diseases = cursor.fetchall()

    # Compare user symptoms with each disease in the database
    for disease in diseases:
        disease_id = disease[0]
        db_symptoms = set(disease[1].split(', '))
        intersection_count = len(user_symptoms.intersection(db_symptoms))

        print('debug intersection:',user_symptoms.intersection(db_symptoms))

        if intersection_count > max_intersection:
            max_intersection = intersection_count
            matching_diseases = [disease_id]
        elif intersection_count == max_intersection:
            matching_diseases.append(disease_id)

    return matching_diseases

def get_gpt_response(user_input):
    # Connect to the SQL Server database
     connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'  # ODBC Driver versiyonu
    'SERVER=localhost;'                        # Sunucu adı (örneğin localhost ya da bir IP adresi)
    'DATABASE=SampleDB;'                       # Veritabanı adı (örneğin SampleDB)
    'UID=sa;'                                  # Kullanıcı adı (örneğin SQL Server'ın 'sa' kullanıcı adı)
    'PWD=your_password;'                       # Şifre ('sa' kullanıcısının şifresi)
)
    cursor = conn.cursor()

    # Get symptoms from the user using GPT-3.5
    gpt_symptoms = gpt_symptom_matching(user_input)

    while(gpt_symptoms == False):
        user_input = input("Please describe your symtomps with at least 3 different sypmtoms:")
        gpt_symptoms = gpt_symptom_matching(user_input)

    # Get matching diseases
    matching_diseases = get_matching_diseases(gpt_symptoms, cursor)

    print('matches:', matching_diseases)

    # Display the results
    if matching_diseases:
        print("Possible diseases based on your symptoms:")
        for disease_id in matching_diseases:
            cursor.execute("SELECT TOP (1000) game_id, game_name, game_typ FROM nasaGame.dbo.game; = ?", disease_id)
            disease_data = cursor.fetchone()
            print(f"DiseaseID: {disease_data[0]}, Diagnosis: {disease_data[5]}, Symptoms: {disease_data[1]}")
            get_diag_info(disease_data[0],cursor)
    else:
        print("No matching diseases found for the provided symptoms.")

    # Close the database connection
    cursor.close()
    conn.close()

def main():
    user_input = input("can you introduce yourself: ")
    get_gpt_response(user_input)

if __name__ == "__main__":
    main()