# Importing the Prisma class from prisma you installed using pip
from prisma import Prisma

# Creating a new instance of the Prisma class
prisma = Prisma()
# Mandatory prisma.connect() call
prisma.connect()
# comment out to not reset the database upon running
prisma.user.delete_many()
# prisma.post.delete_many() # Already set with onDelete: CASCADE
# Creating a new user
# we run prisma commands through the format of
# prisma.<model>.<action>

# The return type of the various types of operations are usually
# the model itself, or python List objects of the model

# In this case, we are creating a new user and including the posts
# that the user has authored by setting include={ 'posts': True }
user = prisma.user.create(
    data={
        'name': "Thom Yorke",
        # Running this on second time will throw an error because of unique constraint
        'email': "thomyorke@gmail.com"
    },
    include={
        'posts': True
    }
)
# This method may be deprecated for you, if so, use model_dump_json (I think)
# You should be able to get intellisense for the model by typing user. and triggering
# the intellisense by using Ctrl + Space
print("Created user: ")
print(user.json(indent=3))
print("")

# Creating a new post with the user we just created
post = prisma.post.create(
    data={
        'title': "My first post",
        'content': "Hello, world!",
        'author': {
            'connect': {
                'id': user.id
            }
        }
    },
    include={
        'author': True
    }
)
# print(post.json(indent=3))
# We can access certain fields of the post object using . notation
print("Created post details: ")
print(f"Post title: {post.title}")
print(f"Post content: {post.content}")
# Using include allows us to access the author object, otherwise it will be null and
# we will get an error, despite it being related to the post
print(f"Post author: {post.author.name}")
print("")

# Updating the post we just created
post = prisma.post.update(
    where={
        'id': post.id  # We can access the id of the post object using . notation
    },
    data={
        'title': "My first post (updated)"
    },
)

# We can access certain fields of the post object using . notation
print("Updated post details: ")
print(f"Newly updated post title: {post.title}")
print(f"Remaining Post content: {post.content}")
print("")

# Deleting the post we just created
deletedPost = prisma.post.delete(
    where={
        'id': prisma.post.find_first(
            where={
                'title': "My first post (updated)"
            }
        ).id
    }
)
print("Deleted post: ")
print(deletedPost.json(indent=3))
print("")

# Let's create two more posts and use find_many to get all posts
posts = prisma.post.create_many(
    data=[
        {
            'title': "My first post",
            'content': "Hello, world!",
            'authorId': user.id
        },
        {
            'title': "My second post",
            'content': "Second Post!",
            'authorId': user.id
        },
        {
            'title': "My third post",
            'content': "Third Post!",
            'authorId': user.id
        }
    ]
)

multiplePosts = prisma.post.find_many(
    where={
        'authorId': user.id
    },
)
# Find many retrieves a List[Post] object
# To access individual posts, we use iteration or other list access methods
for post in multiplePosts:
    print(post.title)
    print(post.content)
    try:
        print(post.author.name)
    except AttributeError:
        print("Author not found, did you put include={ 'author': True }?")
    print("")
