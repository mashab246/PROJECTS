from datetime import datetime
import random

# In-memory data structures
movies = {}
buyers = {}
sales = {}

# Function to add a movie
def add_movie(title, genre, release_date, actors, description, price):
    # Generate a unique random movie number
    while True:
        movie_number = (f"Movie number: {random.randint(1000, 9999)}")
        if movie_number not in movies:
            break

    movies[movie_number] = {
        'title': title,
        'genre': genre,
        'release_date': release_date,
        'actors': actors.split(", "),
        'description': description,
        'price': price
    }
    print(f'Movie "{title}" added successfully with Movie Number: {movie_number}!')

def search_and_display_movie(movie_number=None, title=None, actors=None, genre=None, release_date=None):
    # Search by movie number
    if movie_number:
        if movie_number in movies:
            print("\n--- Movie Found ---")
            print_movie_details(movie_number)
        else:
            print("Movie not found!")
        return

    # Search by other criteriaif
    found_movies = []
    for m_number, movie in movies.items():
        if (title and title.lower() in movie['title'].lower()) or \
           (actors and any(actor.lower() in [a.lower() for a in movie['actors']] for actor in actors.split(", "))) or \
           (genre and genre.lower() == movie['genre'].lower()) or \
           (release_date and release_date == movie['release_date']):
            found_movies.append(m_number)

    if found_movies:
        print("\n--- Movies Found ---")
        for m_number in found_movies:
            print_movie_details(m_number)
    else:
        print("No movies found matching the criteria.")
        
def print_movie_details(movie_number):
    """Helper function to print movie details."""
    movie = movies[movie_number]
    print(f"Movie Number: {movie_number}")
    print(f"Title: {movie['title']}")
    print(f"Genre: {movie['genre']}")
    print(f"Release Date: {movie['release_date']}")
    print(f"Actors: {', '.join(movie['actors'])}")
    print(f"Description: {movie['description']}")
    print(f"Price: ${movie['price']:.2f}")
    print("--------------------")

# Function to sell a movie
def buy_movie(movie_number, copies_sold, buyer_name, buyer_gender, buyer_contact):
    # Check if the movie exists
    if movie_number  in movies:
        print("Movie found!")
        return

    # Check if the buyer already exists, otherwise register them
    buyer_number = None
    for b_number, buyer in buyers.items():
        if buyer['name'] == buyer_name and buyer['contact'] == buyer_contact:
            buyer_number = b_number
            break

    if not buyer_number:
        # Generate a unique random buyer number
        while True:
            buyer_number = random.randint(1000, 9999)
            if buyer_number not in buyers:
                break

        buyers[buyer_number] = {
            'name': buyer_name,
            'gender': buyer_gender,
            'contact': buyer_contact
        }
        print(f'Buyer "{buyer_name}" registered successfully with Buyer Number: {buyer_number}!')

    # Generate a unique random receipt number
    while True:
        receipt_number = random.randint(1000, 9999)
        if receipt_number not in sales:
            break

    # Record the sale
    movie = movies[movie_number]
    total_price = movie['price'] * copies_sold
    sale_date = datetime.now().strftime('%Y-%m-%d')

    sales[receipt_number] = {
        'sale_date': sale_date,
        'movie_number': movie_number,
        'copies_sold': copies_sold,
        'total_price': total_price,
        'member_number': buyer_number
    }

    print(f'Sale recorded successfully! Receipt Number: {receipt_number}, Total Price: ${total_price:.2f}')

    # Generate and display the receipt immediately
    generate_receipt(receipt_number)

# Function to generate a receipt
def generate_receipt(receipt_number):
    if receipt_number not in sales:
        print("Receipt not found!")
        return

    sale = sales[receipt_number]
    movie = movies[sale['movie_number']]
    buyer = buyers[sale['member_number']]

    print("\n--- Receipt ---")
    print(f"Receipt Number: {receipt_number}")
    print(f"Sale Date: {sale['sale_date']}")
    print(f"Movie Title: {movie['title']}")
    print(f"Copies Sold: {sale['copies_sold']}")
    print(f"Total Price: ${sale['total_price']:.2f}")
    print(f"Buyer Name: {buyer['name']}")
    print("----------------\n")

# Main menu
def main_menu():
    while True:
        print("\n--- Movie Library System ---")
        print("1. Add Movie")
        print("2. Search Movie")
        print("3. Buy Movie")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            try:
                title = input("Enter Title: ")
                genre = input("Enter Genre: ")
                release_date = input("Enter Release Date (YYYY-MM-DD): ")
                actors = input("Enter Actors (comma separated): ")
                description = input("Enter Description: ")
                price = int(input("Enter Price: "))
                add_movie(title, genre, release_date, actors, description, price)
            except ValueError:
                print("Invalid input! Please try again.")
                
        elif choice == '2':
            print("\n--- Search Movie ---")
            search_type = input("Search by (1) Movie Number, (2) Title, (3) Actors, (4) Genre, (5) Release Date: ")
            if search_type == '1':
                movie_number = input("Enter Movie Number: ")
                search_and_display_movie(movie_number=movie_number)
            elif search_type == '2':
                title = input("Enter Title: ")
                search_and_display_movie(title=title)
            elif search_type == '3':
                actors = input("Enter Actors (comma separated): ")
                search_and_display_movie(actors=actors)
            elif search_type == '4':
                genre = input("Enter Genre: ")
                search_and_display_movie(genre=genre)
            elif search_type == '5':
                release_date = input("Enter Release Date (YYYY-MM-DD): ")
                search_and_display_movie(release_date=release_date)
            else:
                print("Invalid search option!")

        elif choice == '3':
            try:
                movie_number = int(input("Enter Movie Number: "))
                copies_bought = int(input("Enter Copies Sold: "))
                buyer_name = input("Enter Buyer Name: ")
                buyer_gender = input("Enter Buyer Gender: ")
                buyer_contact = input("Enter Buyer Contact: ")
                buy_movie(movie_number, copies_sold, buyer_name, buyer_gender, buyer_contact)
            except ValueError:
                print("Invalid input! Please try again.")

        elif choice == '4':
            confirm = input("Are you sure you want to exit? (yes/no): ").lower()
            if confirm == 'yes':
                print("THANK YOU FOR WORKING WITH US.")
                break

        else:
            print("Invalid option. Please try again.")

# Run the main menu
if __name__ == "__main__":
    main_menu()