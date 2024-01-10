import json
import os
import matplotlib.pyplot as plt

MOVIE_LENGTH_FLAG = 100
INPUT_FILE_NAME = 'movies.json'
OUTPUT_FILE_NAME = 'tree.json'
SPLIT = "=" * 75
MOVIES_IN_EACH_YEAR_OPTION = 1
MOVIES_WITH_EACH_LANGUAGE_OPTION = 2
MOVIES_LENGTH_OPTION = 3
RECOMMEND_MOVIE_OPTION = 4
EXIT_OPTION = 0


def build_tree(input_file_name: str, output_file_name: str):
    print(f"Start to build the tree file.")
    with open(input_file_name, "r") as f:
        cache = json.load(f)

    # 1. get how many different years
    year_list = []
    for movie in cache:
        year = movie["year"][:4]
        if year not in year_list:
            year_list.append(year)
    tree = {year: {} for year in year_list}

    # 2. get how many different languages in each year
    for movie in cache:
        languages = movie["language"].strip().split(",")
        year = movie["year"][:4]
        for language in languages:
            if language not in tree[year]:
                tree[year][language.strip()] = {f"{MOVIE_LENGTH_FLAG} more": [], f"{MOVIE_LENGTH_FLAG} less": []}

    # 3. store all movies:
    for movie in cache:
        try:
            languages = movie["language"].strip().split(",")
            year = movie["year"][:4]
            runtime = int(movie["runtime"].strip().split()[0])

            for language in languages:
                if runtime >= MOVIE_LENGTH_FLAG:
                    tree[year][language.strip()][f"{MOVIE_LENGTH_FLAG} more"].append(movie["title"])
                else:
                    tree[year][language.strip()][f"{MOVIE_LENGTH_FLAG} less"].append(movie["title"])
        except Exception as e:
            pass
    with open(output_file_name, "w") as f:
        json.dump(tree, f)
    print("Build the tree file succeed!")


def print_main_menu():
    print(SPLIT)
    # get the information of movies in each year
    print(f"{MOVIES_IN_EACH_YEAR_OPTION}: Get the statistical information of movies in each year.")
    # get the information of movies with different languages
    print(f"{MOVIES_WITH_EACH_LANGUAGE_OPTION}: Get the statistical information of movies with different languages. ")
    # get the information of movies with different length
    print(f"{MOVIES_LENGTH_OPTION}: Get the statistical information of the length of each movie.")
    # recommend movies to the user
    print(f"{RECOMMEND_MOVIE_OPTION}: Get movie recommendations.")
    # exit
    print(f"{EXIT_OPTION}: Exit.")
    print(SPLIT)

def movie_statistics_year(tree:dict):
    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    movie_year = {}
    for year in tree:
        movie_year[year] = []
        for language in tree[year]:
            for movie in tree[year][language][f"{MOVIE_LENGTH_FLAG} more"]:
                if movie not in movie_year[year]:
                    movie_year[year].append(movie)
            for movie in tree[year][language][f"{MOVIE_LENGTH_FLAG} less"]:
                if movie not in movie_year[year]:
                    movie_year[year].append(movie)
    movie_year = sorted(movie_year.items(), key=lambda x:x[0])

    year_list = []
    num_list = []
    for items in movie_year:
        year_list.append(items[0])
        num_list.append(len(items[1]))
    plt.bar(year_list, num_list)
    plt.title("Movie distribution in each year.")
    plt.ylabel("Number of movies")
    plt.xticks(year_list, rotation=45)
    plt.subplot(1, 2, 2)
    plt.pie(num_list, labels=year_list, autopct='%1.1f')
    plt.show()


def movie_statistics_language(tree:dict):
    # year
    # language
    # 135 more, 135 less
    # {2005:{"Chinese":{"100 more": [title1, title2, title3....], "100 less": []}, "English":{}}, 2006:{}.....}
    movie_language = {}
    for year in tree:
        for language in tree[year]:
            if language not in movie_language:
                movie_language[language] = []
            for movie in tree[year][language][f"{MOVIE_LENGTH_FLAG} more"]:
                if movie not in movie_language[language]:
                    movie_language[language].append(movie)
            for movie in tree[year][language][f"{MOVIE_LENGTH_FLAG} less"]:
                if movie not in movie_language[language]:
                    movie_language[language].append(movie)
    movie_language_top_10 = sorted(movie_language.items(), key=lambda x:len(x[1]), reverse=True)[:10]
    language_list = []
    num_list = []
    for items in movie_language_top_10:
        language_list.append(items[0])
        num_list.append(len(items[1]))

    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    plt.bar( language_list, num_list)
    plt.title("Movie distribution in each language.")
    plt.ylabel("Number of movies")
    plt.xticks(language_list, rotation=45)
    plt.subplot(1, 2, 2)
    plt.pie(num_list, labels=language_list, autopct='%1.1f')
    plt.show()


def movie_statistics_length(tree:dict):
    movie_length = {f"{MOVIE_LENGTH_FLAG} more":[], f"{MOVIE_LENGTH_FLAG} less":[]}
    for year in tree:
        for language in tree[year]:
            for movie in tree[year][language][f"{MOVIE_LENGTH_FLAG} more"]:
                if movie not in movie_length[f"{MOVIE_LENGTH_FLAG} more"]:
                    movie_length[f"{MOVIE_LENGTH_FLAG} more"].append(movie)

            for movie in tree[year][language][f"{MOVIE_LENGTH_FLAG} less"]:
                if movie not in movie_length[f"{MOVIE_LENGTH_FLAG} less"]:
                    movie_length[f"{MOVIE_LENGTH_FLAG} less"].append(movie)
    length_list = [f">{MOVIE_LENGTH_FLAG} min", f"<= {MOVIE_LENGTH_FLAG} min"]
    num_list = [len(movie_length[f"{MOVIE_LENGTH_FLAG} more"]), len(movie_length[f"{MOVIE_LENGTH_FLAG} less"])]

    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    plt.bar(length_list, num_list)
    plt.title("Movie distribution with different run time.")
    plt.ylabel("Number of movies")
    plt.xticks(length_list, rotation=45)
    plt.subplot(1, 2, 2)
    plt.pie(num_list, labels=length_list, autopct='%1.1f')
    plt.show()

def print_movies(movie_list:list):
    print("Title:")
    for movie in movie_list:
        print(movie)

def movie_recommendation(tree:dict):
    while True:
        year = input("Which year would you like to enter (2001 - 2020): ")
        if not year.isdigit() or int(year) < 2000 or int(year) > 2020:
            print("Invalid year! Please input again! ")
            continue
        language = input("Which language would you like to enter: ")
        length_flag = input(f"Longer than {MOVIE_LENGTH_FLAG} or less than {MOVIE_LENGTH_FLAG}? (y:longer, n:less): ")
        if length_flag != "y" and length_flag != "n":
            print("Invalid input! Please input again! ")
            continue
        movie_list = []
        if language.strip() not in tree[year]:
            print(f"No movie with {language.strip()} in year {year}.")
            continue

        if length_flag == "y":
            movie_list = tree[year][language.strip()][f"{MOVIE_LENGTH_FLAG} more"]
        elif length_flag == "n":
            movie_list = tree[year][language.strip()][f"{MOVIE_LENGTH_FLAG} less"]
        print(f"You can watch the following movies:")
        print_movies(movie_list)
        return


def main():
    if not os.path.exists(OUTPUT_FILE_NAME):
        build_tree(INPUT_FILE_NAME, OUTPUT_FILE_NAME)
    tree = json.load(open(OUTPUT_FILE_NAME, "r"))
    while True:
        print_main_menu()
        try:
            option = int(input("Enter your option: "))
            if option == EXIT_OPTION:
                print("Bye!")
                break
            elif option == MOVIES_IN_EACH_YEAR_OPTION:
                movie_statistics_year(tree)
            elif option == MOVIES_WITH_EACH_LANGUAGE_OPTION:
                movie_statistics_language(tree)
            elif option == MOVIES_LENGTH_OPTION:
                movie_statistics_length(tree)
            elif option == RECOMMEND_MOVIE_OPTION:
                movie_recommendation(tree)
            else:
                print("Invalid option! Please input again!")
        except Exception as e:
            print("Invalid option! Please input again!")


if __name__ == '__main__':
    main()

