import openai
from openai import OpenAI

# Set your OpenAI GPT API key
openai_api_key = ''

# Define the disease database
disease_database = {
    1: {"Symptoms": {"excessive fatigue", "weakness", "pale skin", "cold hands and feet", "appetite loss", "ear discharge", "bad odor in the ear", "loss of balance", "vomiting"}},
    2: {"Symptoms": {"cough", "fever", "hoarse voice", "fatigue", "redness in eyes", "runny nose", "sore throat", "swelling in neck lymph nodes"}},
    3: {"Symptoms": {"fever", "high fever", "fatigue", "bloody/mucousy cough", "shortness of breath", "palpitations", "sweating", "chills", "tremors", "appetite loss", "chest pain when breathing", "cyanosis"}},
}

def gpt_symptom_matching(user_input):
    # Generate a response using GPT-3.5
    client = OpenAI(api_key = openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {
                    "role": "system",
                    "content": "You will be provided with a block of text, and your task is to extract a list of keywords from it. Keywords must be only medical symptoms. Content must be includes keywords only!."
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
    
    gpt_symptoms = response.choices[0].message.content.split(', ')

    if len(set(gpt_symptoms)) < 3:
        return False
    
    return set(gpt_symptoms)

def get_matching_diseases(user_symptoms):
    matching_diseases = []
    max_intersection = 0

    # Compare user symptoms with each disease in the database
    for disease_id, disease_data in disease_database.items():
        intersection_count = len(user_symptoms.intersection(disease_data["Symptoms"]))

        print('debug intersection:',user_symptoms.intersection(disease_data["Symptoms"]))
        
        if intersection_count > max_intersection:
            max_intersection = intersection_count
            matching_diseases = [disease_id]
        elif intersection_count == max_intersection:
            matching_diseases.append(disease_id)

    return matching_diseases

def get_gpt_suggestion(system_input):
    # Generate a response using GPT-3.5
    client = OpenAI(api_key = openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {
                    "role": "system",
                    "content": "You will be provided a diagnosis, and your task is make suggestion about this diagnosis or diagnosies."
                },
                {
                    "role": "user",
                    "content": system_input
                }
            ],
        max_tokens=100
    )
    
    print(response)

def main():
    # Get symptoms from the user using GPT-3.5
    user_input = input("Please describe your symptoms: ")
    gpt_symptoms = gpt_symptom_matching(user_input)

    while(gpt_symptoms == False):
        user_input = input("Please describe your symtomps with at least 3 different sypmtoms: ")
        gpt_symptoms = gpt_symptom_matching(user_input)

    print('symptoms:', gpt_symptoms)

    # Get matching diseases
    matching_diseases = get_matching_diseases(gpt_symptoms)
    print(matching_diseases)
    # Display the results
    if matching_diseases:
        print("Possible diseases based on your symptoms:")
        for disease_id in matching_diseases:
            print(f"DiseaseID: {disease_id}, Diagnosis: {disease_database[disease_id]}, Symptoms: {', '.join(disease_database[disease_id]['Symptoms'])}")
            if disease_id == 2:
                get_gpt_suggestion('Upper respiratory tract infection')
            elif disease_id == 3:
                get_gpt_suggestion('Pneumania')
            else:
                print("No suggestion yet....")
    else:
        print("No matching diseases found for the provided symptoms.")

if __name__ == "__main__":
    main()
