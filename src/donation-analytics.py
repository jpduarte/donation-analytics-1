'''
Juan Pablo Duarte
Tasks:
1- take a file listing individual campaign contributions for multiple years
2- determine which ones came from repeat donors
3- calculate a few values and distill the results into a single output file
files:
./input/itcont.txt
./input/percentile.txt
./output/repeat_donors.txt
'''

import sys

class contributor():
    def __init__(self, CMTE_ID, NAME, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID):
        self.CMTE_ID = CMTE_ID
        self.NAME = NAME
        self.ZIP_CODE = ZIP_CODE
        self.TRANSACTION_DT = [TRANSACTION_DT]
        self.TRANSACTION_AMT = [int(TRANSACTION_AMT)]
        self.OTHER_ID = OTHER_ID
        self.total_donation = TRANSACTION_AMT
        self.percentile = 0
    '''CMTE_ID: identifies the flier, which for our purposes is the recipient of this contribution
    NAME: name of the donor
    ZIP_CODE: zip code of the contributor (we only want the first five digits/characters)
    TRANSACTION_DT: date of the transaction
    TRANSACTION_AMT: amount of the transaction
    OTHER_ID: a field that denotes whether contribution came from a person or an entity
    '''
    def get_CMTE_ID(self):
        return self.CMTE_ID
    def get_NAME(self):
        return self.NAME
    def get_ZIP_CODE(self):
        return self.ZIP_CODE[:4]
    def get_TRANSACTION_DT(self):
        return self.TRANSACTION_DT
    def get_TRANSACTION_AMT(self):
        return self.TRANSACTION_AMT
    def update(self,TRANSACTION_DT,TRANSACTION_AMT):
        self.TRANSACTION_DT.append(TRANSACTION_DT)
        self.TRANSACTION_AMT.append(int(TRANSACTION_AMT))
        self.total_donation = sum(self.TRANSACTION_AMT)
    def get_total_donation(self):
        return self.total_donation
    def get_percentile(self):
        return self.percentile

def main():
    contributor_list = []
    #obtaine name for files
    itcont_txt          = str(sys.argv[1])
    percentile_txt      = open(str(sys.argv[2]),'r')
    repeat_donors_txt   = str(sys.argv[3])
    #obtain percentile number
    percentile_value    = float(percentile_txt.readlines()[0])
    #read contributors file
    with open(itcont_txt, 'r') as file_in:
        for line_in in file_in:
            data_line = line_in.split('|')

            CMTE_ID         = data_line[0]
            NAME            = data_line[7]
            ZIP_CODE        = data_line[10]
            TRANSACTION_DT  = data_line[13]
            TRANSACTION_AMT = data_line[14]
            OTHER_ID        = data_line[15]

            #add first contributor to list
            if (len(contributor_list)==0):
                contributor_list.append(contributor( CMTE_ID, NAME, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID))
            else:
                #search for same contributor
                for individual_contributor in contributor_list:
                    find_contributor = 0
                    "you can assume two contributions are from the same donor if the names and zip codes are identical."
                    if ((NAME+ZIP_CODE[:4]) == (individual_contributor.get_NAME() + individual_contributor.get_ZIP_CODE())):
                        find_contributor = 1
                        individual_contributor.update(TRANSACTION_DT,TRANSACTION_AMT)
                #add new contributor if match is found
                if (find_contributor==0):
                    #print('Add contributor extra')
                    contributor_list.append(contributor( CMTE_ID, NAME, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID))


    with open(repeat_donors_txt, 'w') as outputFile:
        for donor in contributor_list:
            #str(individual_contributor.get_total_donation())
            CMTE_ID     = donor.get_CMTE_ID()
            zipcode     = donor.get_ZIP_CODE()
            year        = donor.get_TRANSACTION_DT()[0][-4:-1]
            percentile  = str(donor.get_percentile())
            donation    = str(donor.get_total_donation())
            total_transactions = (len(donor.get_TRANSACTION_AMT()))

            if (total_transactions>1):
                output_str =  CMTE_ID+ '|' + zipcode +  '|' + year  + '|' + percentile+'|'+ donation+'|'+str(total_transactions)
                outputFile.write(output_str+'\n')
    return

if __name__=="__main__":
    main()
