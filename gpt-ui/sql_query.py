# sql_query.py
import pyodbc
 
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'  
    'SERVER=localhost;'                        
    'DATABASE=SampleDB;'                       
    'UID=sa;'                                  
    'PWD=your_password;'                       
)
 
def read(conn):
    print("Read")
    cursor = conn.cursor()
    cursor.execute("select * from Disease")
    for row in cursor:
        print(f'row = {row}')
    print()
 
read(conn)

# Your list of symptoms
A = ['Abstraction', 'Flexibility', 'Matching Skill']

def query_match_rates(syptom_list):
    # Iterate over each diagnosis and calculate match rate
    match_rates = []

    cursor = conn.cursor()

    # Fetch distinct diagnoses from the database
    cursor.execute("SELECT DISTINCT Diagnosis FROM Disease")
    diagnoses = cursor.fetchall()

    for diagnosis in diagnoses:
        diagnosis = diagnosis[0]  # Extract the diagnosis from the tuple

        # Fetch symptoms for the current diagnosis
        cursor.execute("SELECT Symptoms FROM Disease WHERE Diagnosis=?", (diagnosis,))
        db_symptoms = cursor.fetchone()

        if db_symptoms:
            db_symptoms = db_symptoms[0].split(',')  # Assuming symptoms are stored as comma-separated values

            # Calculate match rate
            common_symptoms = set(A) & set(db_symptoms)
            match_rate = len(common_symptoms) / len(set(A))

            match_rates.append({'Diagnosis': diagnosis, 'match_rate': match_rate})

    # Print the match rates
    for match in match_rates:
        print(f"Diagnosis: {match['Diagnosis']}, Match Rate: {match['match_rate']}")

    print(match_rates)

    return match_rates

query_match_rates(A)

conn.close()