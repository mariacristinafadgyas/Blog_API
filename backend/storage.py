import json


def read_data(file_path):
    """Reads the JSON file and returns the data. Handles errors if the file
     doesn't exist or contains invalid JSON."""
    try:
        with open(file_path, 'r') as fileobj:
            posts_data = json.load(fileobj)
            return posts_data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


def sync_data(file_path, posts_data):
    """Writes data to the JSON file. Handles errors that might occur during the write process."""
    updated_blog = json.dumps(posts_data)
    try:
        with open(file_path, 'w') as fileobj:
            fileobj.write(updated_blog)
    except IOError:
        print(f"Error: Unable to write to file {file_path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def update_post_in_json(file_path, updated_post):
    """Updates the post in the JSON file"""
    posts_data = read_data(file_path)
    post_found = False
    for post in posts_data:
        if post['id'] == updated_post['id']:
            post['title'] = updated_post['title']
            post['author'] = updated_post['author']
            post['content'] = updated_post['content']
            post['post_date'] = updated_post['post_date']
            post_found = True
            break

    if not post_found:
        print(f"Post with id {updated_post['id']} not found in JSON file.")

    sync_data(file_path, posts_data)


def main():
    blog_data = read_data('posts.json')
    new_data = {
        "author": "Jane Done",
        "title": "Third Post",
        "content": "This is the new post"
    }
    blog_data.append(new_data)
    sync_data('posts.json', blog_data)


if __name__ == "__main__":
    main()