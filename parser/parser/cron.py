from api.parser import ImovirtualParser, IMOVIRTUAL_URL

def print_smth():
    print('5 minutes')

def launch_parser():
    try:
       parser = ImovirtualParser(IMOVIRTUAL_URL)
       parser.data_extraction()
    except Exception as e:
        print(e)

