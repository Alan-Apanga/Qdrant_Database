# Qdrant_Database
Streamlit Demo App for Book Search 
The goal of this project is to create a Streamlit web application that allows users to capture and manage details of books. The application should provide a form where users can input the name, author, publication year, and short description of books. The collected data should be stored and displayed in a summary section. Additionally, the application should allow users to select a "Kind of Book" from a drop-down list, and if "Alien Invasion" is selected, the application should print a specific message.

## Implementation:
The project utilizes Streamlit, a Python library for creating interactive web applications with minimal code.
It uses the qdrant-client library to interact with the Qdrant vector search engine for similarity searches based on the short descriptions of books.
An encoder module is used to convert the short descriptions into vector representations, enabling similarity searches in the Qdrant index.
The application contains a form that captures the name, author, publication year, and short description of books. The "Kind of Book" drop-down list is provided to select a specific kind of book.
When users click the "Submit" button, the book details are appended to the books list.
A "Summary" section displays all the entered book details in a list format.
If the selected "Kind of Book" is "Alien Invasion," the application prints a specific message; otherwise, it displays the selected option.
A "Clear Input" button clears the text input fields in the form without affecting the stored book data in the books list.
Users can add multiple books before clicking the "Submit All Books" button, which uploads all the book details to the Qdrant database for later similarity searches.
A "Search" button allows users to perform searches based on the selected "Kind of Book" or a custom search term.

## Conclusion:
This Streamlit web application successfully allows users to capture and manage book details interactively. Users can input book data, including the name, author, publication year, short description, and the "Kind of Book" category. The application stores the entered book data in the books list and displays a summary of all the entered books. It also provides an option to search for "Alien Invasion" books or perform custom searches using the Qdrant vector search engine. The application is efficient, user-friendly, and enables seamless data entry and search functionalities for book details. With further enhancements and integration with a persistent Qdrant database, this application could be expanded into a fully functional book management system.
