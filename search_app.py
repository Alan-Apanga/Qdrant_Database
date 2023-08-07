# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 18:07:47 2023

@author: alann
"""

"""     Build a semantic search engine for science fiction books

 After you set it up, you will ask the engine about an impending alien threat.
Your creation will recommend books as preparation for a potential space attack.

"""


# Process your data so that the search engine can work with it
# The [Sentence Transformers] framework gives you access to common 
# [Large Language Models] that turn raw data into embeddings.
# pip install -U sentence-transformers

# Once encoded, this data needs to be kept somewhere. 
# Qdrant lets you store data as embeddings.
# pip install qdrant-client

import streamlit as st

# Once the two main frameworks are defined, you need to specify the exact models this engine will use.
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer

#                   IMPORT THE MODELS                  
# The Sentence Transformers framework contains many embedding models.
encoder = SentenceTransformer('all-MiniLM-L6-v2') 




# =============================================================================
#                            ADD THE DATASET
# =============================================================================

# List to store the book details
# books = []

# DEFINE THE STORAGE LOCATION
# You need to tell Qdrant where to store embeddings
qdrant = QdrantClient(":memory:") 


def reset_input_fields():
    # Reset the input fields to their default values
    st.session_state.publication_year = 2023
    st.session_state.kind_of_book = ""
    
    # Reset only the text input fields to their default values
    st.session_state.name = ""
    st.session_state.author = ""
    st.session_state.short_description = ""




def book_form():
    # global book_count
    
    st.header("Book Details")
    
    # Session state to store input values
    if "books" not in st.session_state:
        st.session_state.books = []
    if "name" not in st.session_state:
        st.session_state.name = ""
    if "author" not in st.session_state:
        st.session_state.author = ""
    if "publication_year" not in st.session_state:
        st.session_state.publication_year = 2023
    if "short_description" not in st.session_state:
        st.session_state.short_description = ""
    if "kind_of_book" not in st.session_state:
        st.session_state.kind_of_book = ""
        
    
    # Input fields for the book data
    st.session_state.name = st.text_input("Name", st.session_state.name)
    st.session_state.author = st.text_input("Author", st.session_state.author)
    st.session_state.publication_year = st.number_input("Publication Year", min_value=1800, max_value=2100, value=st.session_state.publication_year, step=1)
    st.session_state.short_description = st.text_area("Short Description", st.session_state.short_description)
    

    
    
    # ADD BUTTON 1
    if st.button("Add Book"):
        # Append the book details to the list
        book_data = {
            "Name": st.session_state.name,
            "Author": st.session_state.author,
            "Publication Year": st.session_state.publication_year,
            "Short Description": st.session_state.short_description,
        }
        st.session_state.books.append(book_data)
        reset_input_fields()
        st.success("Book data added successfully!")
    
    
    # ADD BUTTON 2
    if st.button("Submit All Books"):
        # UPLOAD ALL THE BOOKS QDRANT DATABASE
        for idx, book in enumerate(st.session_state.books):
            qdrant.upload_records(
                collection_name="my_books",
                records=[
                    models.Record(
                        id=idx,
                        vector=encoder.encode(book["Short Description"]).tolist(),
                        payload=book
                        ) for idx, book in enumerate(st.session_state.books)
                    ]
            )
        st.success("All books submitted successfully!")
    
    
    
    
    # Drop-down list for "Kind of Book"
    st.session_state.kind_of_book = st.selectbox(
        "Kind of Book", ["Alien Invasion", "Others"], 
        index=0 if st.session_state.kind_of_book == "Alien Invasion" else 1
    )
    
            
        
                    
        
    # Check if the preferred  kind of book is 'Alien Invasion'
    if st.session_state.kind_of_book == "Alien Invasion":
        st.write("You selected: Alien Invasion! 👽")
    
    else:
        st.write("You selected: ", st.session_state.kind_of_book)
    
        

        
    #   CHECK IF THE SELECTED KIND OF BOOK IS 'ALIEN INVASION'
    search_result = qdrant.search(
        collection_name="my_books",
        query_vector=encoder.encode("Alien invasion").tolist(),
        limit=3 # Adjust the number of results to display
    )
    
    st.header("Search Results for 'Alien Invasion'")
    if search_result:
        for result in search_result:
            book_name = result.payload["Name"]
            book_author = result.payload["Author"]
            hit_score = result.score
            st.write(f"Name: {book_name}")
            st.write(f"Author: {book_author}")
            st.write(f"Match score: {(hit_score)*100} %")
            st.write("-------------")
    else:
        st.write("No books found for 'Alien Invasion'.")
    
    
    
    # BUTTON 2
    if st.button("Clear Input"):
        # Call the reset_input_fields function to clear the input fields
        reset_text_input_fields()
                
        
               

        
    st.header("Summary")
    if st.session_state.books:
        for i, book in enumerate(st.session_state.books):
            st.write(f"Book {i+1}:")
            st.write(f"Name: {book['Name']}")
            st.write(f"Author: {book['Author']}")
            st.write(f"Publication Year: {book['Publication Year']}")
            st.write(f"Short Description: {book['Short Description']}")
            st.write("-------------")
    else:
        st.write("No books added yet.")
        

    

if __name__ == "__main__":  
    
    #    CREATE COLLECTION
    # All data in Qdrant is organized by collections
    # In this case, we are storing books, so we are calling it my_books.
    # You can also use model.get_sentence_embedding_dimension() to get the 
    # dimensionality of the model you are using.
    vector_size = encoder.get_sentence_embedding_dimension()
    vectors_config = models.VectorParams(size=vector_size, distance=models.Distance.COSINE)
    qdrant.recreate_collection(collection_name="my_books", vectors_config=vectors_config)
    
    
    
    book_form()
    
    
    
# =============================================================================
#                   END
# =============================================================================



    
    
    
    
    
    
    
    
    
    
