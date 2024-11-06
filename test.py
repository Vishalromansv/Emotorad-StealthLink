import requests  # Library for making HTTP requests
import random  # Library for generating random numbers
import string  # Library for generating random strings
import json  # Library for handling JSON data

# Mock API URL (replace this with the actual URL of your API)
API_URL = "https://jsonplaceholder.typicode.com/posts"  # Placeholder API for testing

# Function to generate random test data for creating or updating a post
def generate_random_data():
    # Generate a random title with 10 characters (letters and digits)
    title = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    
    # Generate a random body with 50 characters (letters and digits)
    body = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    
    # Generate a random user ID between 1 and 100
    user_id = random.randint(1, 100)
    
    # Return the data as a dictionary
    return {
        "title": title,
        "body": body,
        "userId": user_id
    }

# Function to test a POST request
def test_post_request():
    # Generate random data for the POST request
    data = generate_random_data()
    
    # Send a POST request with the generated data
    response = requests.post(API_URL, json=data)
    
    # Print the POST request details and response
    print("POST Request:")
    print("Data Sent:", data)
    print("Response Status Code:", response.status_code)
    print("Response Data:", response.json())
    
    # Assert that the status code is 201, indicating successful creation
    assert response.status_code == 201, "POST request failed!"

# Function to test a GET request
def test_get_request():
    # Send a GET request to retrieve posts
    response = requests.get(API_URL)
    
    # Print the GET request details and sample response
    print("\nGET Request:")
    print("Response Status Code:", response.status_code)
    print("Sample Response Data:", response.json()[:5])  # Print first 5 items for brevity
    
    # Assert that the status code is 200, indicating successful retrieval
    assert response.status_code == 200, "GET request failed!"

# Function to test a PUT request
def test_put_request(post_id):
    # Generate random data to update an existing post
    data = generate_random_data()
    
    # Send a PUT request to update a specific post with the generated data
    response = requests.put(f"{API_URL}/{post_id}", json=data)
    
    # Print the PUT request details and response
    print("\nPUT Request:")
    print("Data Sent:", data)
    print("Response Status Code:", response.status_code)
    print("Response Data:", response.json())
    
    # Assert that the status code is 200, indicating successful update
    assert response.status_code == 200, "PUT request failed!"

# Function to test a DELETE request
def test_delete_request(post_id):
    # Send a DELETE request to delete a specific post
    response = requests.delete(f"{API_URL}/{post_id}")
    
    # Print the DELETE request details and response status
    print("\nDELETE Request:")
    print("Response Status Code:", response.status_code)
    
    # Assert that the status code is 200, indicating successful deletion
    assert response.status_code == 200, "DELETE request failed!"

# Run the test functions
if __name__ == "__main__":
    # Test the POST request
    test_post_request()
    
    # Test the GET request
    test_get_request()
    
    # Choose a random post ID for PUT and DELETE tests
    random_post_id = random.randint(1, 100)

    # Test the PUT request with a random post ID
    test_put_request(random_post_id)

    # Test the DELETE request with the same random post ID
    test_delete_request(random_post_id)
