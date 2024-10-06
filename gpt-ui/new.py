import pyodbc
 
# Veritabanı bağlantısı kurma
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'  
    'SERVER=localhost;'                        
    'DATABASE=SampleDB;'                       
    'UID=sa;'                                  
    'PWD=your_password;'                       
)
 
# Veritabanı sorgusu
sql_query = "SELECT TOP (1000) game_id, game_name, game_typeFROM nasaGame.dbo.game;"
 
# Sorguyu çalıştırma
cursor = connection.cursor()
cursor.execute(sql_query)
 
# Sonuçları alıp işleme başlama
matching_diseases = []
A = ['Abstraction', 'Flexibility', 'Matching Skill']
 
for row in cursor.fetchall():
    disease_id, symptoms = row
    if any(symptom in symptoms for symptom in A):
        matching_diseases.append((disease_id, symptoms))
 
# Eşleşen hastalıkları yazdırma
for disease_id, symptoms in matching_diseases:
    print(f"DiseaseID: {disease_id}, Symptoms: {symptoms}")
 
# Bağlantıyı kapatma
connection.close()