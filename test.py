import pandas as pd

# Data for 30 students
data = {
    "Student Name": ["John Doe", "Jane Smith", "Emily Johnson", "Mark Thompson", "Sarah Brown",
                     "Brian Miller", "Angela Davis", "Thomas Wilson", "Olivia Moore", "Ethan Parker",
                     "Natalie Adams", "Daniel Turner", "Sophia Garcia", "Ryan Hernandez", "Emma White",
                     "Jake White", "Chloe Davis", "Mason Miller", "Lily Wilson", "Caleb Moore",
                     "Zoe Parker", "Isaac Adams", "Aria Turner", "Dylan Garcia", "Maya Hernandez",
                     "Aaron White", "Grace Davis", "Leo Miller"],
    "Campus": ["West Campus", "North Campus", "South Campus",
               "East Campus", "Main Campus", "Downtown Campus", "West Campus", "North Campus",
               "South Campus", "East Campus", "Main Campus", "Downtown Campus", "West Campus",
               "North Campus", "South Campus", "East Campus", "Main Campus", "Downtown Campus",
               "West Campus", "North Campus", "South Campus", "East Campus", "Main Campus",
               "Downtown Campus", "West Campus", "North Campus", "South Campus", "East Campus"],
    "Parent's Name": ["Mary Doe", "Robert Smith", "David Johnson", "Susan Thompson", "Michael Brown",
                      "Laura Miller", "Richard Davis", "Linda Wilson", "James Moore", "Patricia Parker",
                      "John Adams", "Carol Turner", "Kevin Garcia", "Lisa Hernandez", "Andrew White",
                      "Jessica White", "William Davis", "Karen Miller", "George Wilson", "Denise Moore",
                      "Charles Parker", "Pamela Adams", "Jonathan Turner", "Sophia Garcia", "Benjamin Hernandez",
                      "Rachel White", "Christopher Davis", "Margaret Miller"],
    "Parent's Contact": ["123-456-7890", "987-654-3210", "555-123-4567", "789-012-3456", "234-567-8901",
                         "876-543-2109", "321-654-0987", "987-123-4567", "555-987-6543", "111-222-3333",
                         "444-555-6666", "777-888-9999", "987-789-0123", "234-567-8901", "876-543-2109",
                         "555-987-6543", "321-654-0987", "789-012-3456", "555-123-4567", "123-456-7890",
                         "987-654-3210", "555-987-6543", "234-567-8901", "555-123-4567", "123-456-7890",
                         "321-654-0987", "789-012-3456", "555-987-6543"],
    "Group": ["Pre-Engineering", "Biology", "Pre-Engineering", "Computer-Science", "Biology",
              "Pre-Engineering", "Computer-Science", "Biology", "Pre-Engineering", "Computer-Science",
              "Biology", "Pre-Engineering", "Computer-Science", "Biology", "Pre-Engineering", "Computer-Science",
              "Biology", "Pre-Engineering", "Computer-Science", "Biology", "Pre-Engineering", "Computer-Science",
              "Biology", "Pre-Engineering", "Computer-Science", "Biology", "Pre-Engineering", "Computer-Science"],
    "Roll Number": [303, 404, 505, 606, 707, 808, 909, 1010, 1111, 1212, 1313, 1414, 1515, 1616, 1717, 1818, 1919, 2020, 2121, 2222, 2323, 2424, 2525, 2626, 2727, 2828, 2929, 3030],
    "Batch": ["2023-C", "2023-B", "2023-A", "2023-C", "2023-B", "2023-A", "2023-C",
              "2023-B", "2023-A", "2023-C", "2023-B", "2023-A", "2023-C", "2023-B", "2023-A", "2023-C", "2023-B",
              "2023-A", "2023-C", "2023-B", "2023-A", "2023-C", "2023-B", "2023-A", "2023-C", "2023-B", "2023-A", "2023-C"],
    "Joining Date": ["2023-02-02", "2023-03-10", "2023-01-20", "2023-02-15",
                     "2023-03-01", "2023-01-25", "2023-02-28", "2023-03-15", "2023-01-30",
                     "2023-02-10", "2023-03-20", "2023-02-05", "2023-03-05", "2023-04-01",
                     "2023-02-15", "2023-03-10", "2023-04-15", "2023-02-20", "2023-03-15",
                     "2023-04-20", "2023-02-25", "2023-03-20", "2023-05-01", "2023-03-01",
                     "2023-04-05", "2023-05-15", "2023-03-05", "2023-04-15"],
    "Reference": ["Jake White", "", "Emma White", "", "", "", "",
                  "Emma White", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    "Percentage (Last Class)": [85.5, 92.0, 78.8, 88.2, 95.0, 79.5, 91.3, 87.0, 76.4, 90.1, 94.2, 82.7, 89.8, 86.3, 77.9, 92.5, 88.7, 80.2, 93.7, 85.1, 78.6, 94.0, 89.4, 79.0, 91.8, 87.5, 76.8, 90.5],
}


# Create DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
df.to_excel('studentsd.xlsx', index=False)