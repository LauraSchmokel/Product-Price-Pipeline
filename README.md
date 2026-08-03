# How to install dependencies and run the script
    1. Download the libraries used in this code
    2. Choose an option between ['laptops', 'tablets', 'phones']
    3. Run the code manually in the terminal, typing "python main.py --option {option you chose}". You can run automatic, because the default option is 'laptops'

# Technical decisions made and why
    There are a few things that I chose to use in this code, but there weren't any problems if I have chosen the another:

    ## Exit() vs raise()

        I could use both, but I choose to use exit() because it was more coherent in this case. I was thinkin if I was a client using this system or someone part of
        the internal team, the system would exit, just showing a message, and not showing the traceback for the user.

    ## csv library vs pandas library

        I also could use both, probably pandas would be more practical, but, for affinity, I chose csv library. 

    ## Terminal menu vs argparse library

        Both are useful, but argparse was a new library for me and it is more professional.
        
# What you'd do differently with more time.
    I checked if the website had pagination and it has no pagination element in the footer and returns the whole catalog in a single request. If it were paginated, 
    I would coded to paginate and take all products.