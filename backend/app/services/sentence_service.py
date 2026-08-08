import re



# =====================================================
# Sentence splitting
# =====================================================


def split_sentences(
    text: str
):


    if not text:

        return []



    text = text.strip()



    # protect common abbreviations
    protected = {


        "Dr.":

            "Dr<dot>",


        "Prof.":

            "Prof<dot>",


        "z.B.":

            "z<dot>B<dot>",


        "u.a.":

            "u<dot>a<dot>",


        "d.h.":

            "d<dot>h<dot>",

    }



    for old,new in protected.items():

        text = text.replace(
            old,
            new
        )






    # protect dates
    #
    # 31. July
    # 01. August
    #

    text = re.sub(

        r"(\d{1,2})\.\s+([A-ZÄÖÜ][a-zäöü]+)",

        r"\1<date> \2",

        text

    )





    # protect decimal numbers
    #
    # 3.5
    #

    text = re.sub(

        r"(\d+)\.(\d+)",

        r"\1<decimal>\2",

        text

    )






    # split sentences
    #
    # . ! ?
    # followed by whitespace
    #

    sentences = re.split(

        r"(?<=[.!?])\s+(?=[A-ZÄÖÜ])",

        text

    )






    result=[]



    for sentence in sentences:


        sentence = sentence.strip()



        if not sentence:

            continue





        # restore protected symbols


        for old,new in protected.items():

            sentence = sentence.replace(
                new,
                old
            )



        sentence = sentence.replace(
            "<date>",
            "."
        )


        sentence = sentence.replace(
            "<decimal>",
            "."
        )



        result.append(
            sentence
        )




    return result