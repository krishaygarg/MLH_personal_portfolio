#!/bin/bash

# Create a random post
echo "Adding a test post..."
RESPONSE=$(curl -X POST http://127.0.0.1:5000/api/timeline_post \
  -d "name=Test Student" \
  -d "email=student@example.com" \
  -d "content=Testing the API!")
echo "Response: $RESPONSE"

# Get the ID of the post we just made
POST_ID=$(echo "$RESPONSE" | grep -o '"id": *[0-9]*' | grep -o '[0-9]*')
echo "Created ID: $POST_ID"

# Get all posts and see if ours is there
echo "Checking if it is in the list..."
GET_RESP=$(curl http://127.0.0.1:5000/api/timeline_post)

if echo "$GET_RESP" | grep -q "\"id\": $POST_ID"; then
    echo "Found it!"
else
    echo "Could not find it!"
    exit 1
fi

# Delete it (bonus)
echo "Deleting the test post..."
curl -X DELETE http://127.0.0.1:5000/api/timeline_post -d "id=$POST_ID"

# Verify it's gone
echo "Making sure it is gone..."
VERIFY=$(curl http://127.0.0.1:5000/api/timeline_post)
if echo "$VERIFY" | grep -q "\"id\": $POST_ID"; then
    echo "Failed to delete"
    exit 1
else
    echo "Deleted successfully!"
fi
